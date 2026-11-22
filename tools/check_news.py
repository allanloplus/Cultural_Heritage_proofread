"""檢測五：新聞監看。用關鍵字查近期新聞標題，比對標題裡是否提到網站收錄的文資，或出現「指定古蹟」「登錄歷史建築」等字眼。

只取標題、來源、日期與連結，不抓內文；結果只是線索（info），要人或 AI 看過才知道需不需要更新網站。
來源是 Google 新聞的 RSS 搜尋，每個關鍵字一個請求、每次檢測只查一輪。可在 config/rules.json 把 news.enabled 設為 false 關閉。
"""
import email.utils, re, urllib.parse, xml.etree.ElementTree as ET
from common import TODAY, days_between, finding, http, log, norm_name
import inventory


def fetch(q, days):
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": "%s when:%dd" % (q, days), "hl": "zh-TW", "gl": "TW", "ceid": "TW:zh-Hant"})
    r = http(url, timeout=30, gap=3, max_bytes=3_000_000)
    if r["code"] != 200:
        return None
    out = []
    try:
        for it in ET.fromstring(r["body"]).iter("item"):
            t = (it.findtext("title") or "").strip()
            src = (it.findtext("source") or "").strip()
            if src and t.endswith(" - " + src):
                t = t[:-len(src) - 3]
            try:
                date = email.utils.parsedate_to_datetime(it.findtext("pubDate")).date().isoformat()
            except Exception:
                date = ""
            out.append({"title": t, "source": src, "date": date, "link": (it.findtext("link") or "").strip()})
    except Exception:
        return None
    return out


def run(ctx):
    N = ctx["rules"]["news"]
    stats = {"enabled": N["enabled"], "queries": 0, "articles": 0, "matched": 0}
    if not N["enabled"] or ctx.get("offline"):
        return [], stats
    names = {}
    stop = {norm_name(x) for x in N["stop_names"]}
    for c in inventory.cities():
        short = {s["id"]: s.get("short") for s in c.content}
        for s in c.official:
            for n in {s["name"], short.get(s["id"]) or ""}:
                k = norm_name(n)
                if len(k) >= N["name_min_len"] and k not in stop:
                    names.setdefault(k, (c, s["id"], s["name"]))
        for it in c.ich.get("items", []):
            k = norm_name(it["name"])
            if len(k) >= N["name_min_len"] + 1:
                names.setdefault(k, (c, it["id"], it["name"]))
    arts, fail = {}, 0
    for q in N["queries"]:
        r = fetch(q, N["days"])
        stats["queries"] += 1
        if r is None:
            fail += 1
            continue
        for a in r:
            if a["date"] and days_between(a["date"], TODAY) <= N["days"]:
                arts.setdefault(a["title"], dict(a, q=q))
    stats["articles"] = len(arts)
    E = []
    if fail:
        log("新聞查詢失敗 %d／%d" % (fail, stats["queries"]))
    keys = sorted(names, key=len, reverse=True)
    per, seen = {}, set()
    for t, a in sorted(arts.items(), key=lambda x: x[1]["date"], reverse=True):
        nt = norm_name(t)
        core = re.sub(r"^.{0,8}[|｜]", "", nt)[:24]  # 同一則新聞被不同媒體轉載、標題前後加字：只留一則
        if core in seen:
            continue
        seen.add(core)
        hit = next((k for k in keys if k in nt), None)
        where = "%s・%s" % (a["source"], a["date"])
        if hit:
            c, iid, nm = names[hit]
            per[iid] = per.get(iid, 0) + 1
            if per[iid] > 3:
                continue
            E.append(finding("NEWS-SITE", "info", c.site["id"], "新聞提到「%s」：%s" % (nm, t), "%s（關鍵字：%s）\n請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。" % (where, a["q"]),
                             c.slug, iid, nm, a["link"], sub=t, extra={"date": a["date"]}))
        elif any(w in t for w in N["new_designation_words"]):
            E.append(finding("NEWS-NEW", "info", "", "可能有新的指定或登錄：%s" % t, "%s（關鍵字：%s）\n官方開放資料通常晚幾週才更新；若確定是新指定／登錄，可先記下，等開放資料出現後一併新增。" % (where, a["q"]),
                             url=a["link"], sub=t, extra={"date": a["date"]}))
    E = E[:N["max_findings"]]
    stats["matched"] = len(E)
    ctx["events"] = ctx.get("events", []) + E
    return [], stats
