"""檢測四：上線狀態。每個網站與每個縣市頁打不打得開、線上版本是否就是 repo 的最新版、憑證是否快到期。"""
import concurrent.futures, datetime, hashlib, os, socket, ssl, urllib.parse
from common import VIA_PROXY, finding, git_blob, http, repo_dir
import inventory


def cert_days(host):
    ctx = ssl.create_default_context()
    with socket.create_connection((host, 443), timeout=15) as s:
        with ctx.wrap_socket(s, server_hostname=host) as t:
            exp = t.getpeercert()["notAfter"]
    d = datetime.datetime.strptime(exp, "%b %d %H:%M:%S %Y %Z")
    return (d - datetime.datetime.utcnow()).days


def run(ctx):
    F, stats = [], {"pages": 0, "down": 0, "drift": 0, "sites": {}}
    if ctx.get("offline"):
        return F, stats
    jobs = []
    for s in inventory.SITES:
        jobs.append((s, "", s["url"], None))
        d = repo_dir(s["repo"])
        if d and os.path.exists(os.path.join(d, "CNAME")):
            want = open(os.path.join(d, "CNAME")).read().strip()
            if want != urllib.parse.urlsplit(s["url"]).netloc:
                F.append(finding("LIVE-DOWN", "medium", s["id"], "%s 的 CNAME（%s）與設定的網址不同" % (s["name"], want), "請確認 config/sites.json 或 repo 的 CNAME。", sub="cname"))
    for c in inventory.cities():
        jobs.append((c.site, c.slug, c.url, None))
        jobs.append((c.site, c.slug, c.url + "js/data.js", c.slug + "/js/data.js"))
        jobs.append((c.site, c.slug, c.url + "audio/cues.js", c.slug + "/audio/cues.js"))

    def work(j):
        s, slug, url, blob = j
        r = http(url, timeout=40, gap=0.3, max_bytes=20_000_000)
        if r["code"] != 200:  # 再試一次，避免偶發逾時誤報
            r = http(url, timeout=40, gap=2, max_bytes=20_000_000)
        return j, r

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for (s, slug, url, blob), r in ex.map(work, jobs):
            stats["pages"] += 1
            st = stats["sites"].setdefault(s["id"], {"ok": 0, "down": 0, "drift": 0})
            if r["code"] != 200:
                stats["down"] += 1
                st["down"] += 1
                F.append(finding("LIVE-DOWN", "high", s["id"], "網頁打不開：%s" % url, "HTTP %s %s" % (r["code"] or "連線失敗", r["err"]), slug, url=url, sub=url))
                continue
            st["ok"] += 1
            if blob:
                local = git_blob(repo_dir(s["repo"]), blob)
                if local is not None and hashlib.sha1(local).hexdigest() != hashlib.sha1(r["body"]).hexdigest():
                    stats["drift"] += 1
                    st["drift"] += 1
                    F.append(finding("LIVE-DRIFT", "medium", s["id"], "線上的 %s 不是 repo 的最新版" % blob,
                                     "GitHub Pages 可能部署失敗或還在部署。到該 repo 的 Actions 看「pages build and deployment」，失敗就按 Re-run all jobs。", slug, url=url, sub=blob))
    if not VIA_PROXY:
        warn = ctx["rules"]["live"]["cert_warn_days"]
        for s in inventory.SITES:
            host = urllib.parse.urlsplit(s["url"]).netloc
            try:
                n = cert_days(host)
                stats["sites"].setdefault(s["id"], {})["certDays"] = n
                if n < warn:
                    F.append(finding("LIVE-CERT", "high" if n < 7 else "medium", s["id"], "%s 的 HTTPS 憑證 %d 天後到期" % (host, n),
                                     "GitHub Pages 會自動續期；快到期還沒續，到 repo 的 Settings → Pages 取消再重新勾選 Enforce HTTPS，或重新儲存自訂網域。", sub="cert"))
            except Exception as e:
                F.append(finding("LIVE-CERT", "medium", s["id"], "%s 的 HTTPS 憑證檢查失敗" % host, str(e)[:200], sub="cert"))
    else:
        stats["certNote"] = "本次經由代理執行，略過憑證到期日檢查"
    return F, stats
