"""檢測二：連結。把所有受檢網站資料與網頁裡的網址找出來，依網站種類用最省請求的方式確認。

  國家文化資產網 nchdb     是單頁應用，任何網址都回 200，所以用開放資料確認案號是否存在、網址是否與官方一致
  文資局圖片 data.boch     用 HEAD 確認；每次只查一部分（輪流），月檢查全部
  維基共享資源、維基百科    用官方 API 一次查一批（檔案被刪除多半是授權問題，網站上的本機副本也要下架）
  自己的網站 *.123hi.org    不發請求：直接用 repo 資料確認縣市在哪個網站、景點 id 是否存在
  其他網站                 逐一連線：404／410＝失效；403／429／逾時＝未能確認，連續多次才列為失效

每個網址的檢查結果記在 state/links.json，報告裡的「連續失敗次數」「首次失敗日」由此而來。
"""
import concurrent.futures, os, re, urllib.parse
from common import STATE, TODAY, cfg, days_between, dump, finding, get_json, http, load, log, repo_dir, repo_files
import inventory

LINKS = os.path.join(STATE, "links.json")
URL_RE = re.compile(r"https?://[!#-&(-;=?-\[\]_a-z~%]+", re.I)  # 夾在文字裡的網址：只取 ASCII，遇到中文就停
WHOLE_RE = re.compile(r"^https?://\S+$")  # 整個字串就是一個網址：原樣使用（維基條目名稱常含中文與括號）
URL_KEYS = {"url", "officialImg", "page", "thumb", "licenseUrl", "ubikeUrl", "original"}  # 這些欄位的值整個就是網址（文資局圖片檔名常含空白與中文）
TEXT_EXT = (".html", ".js", ".json", ".md", ".css", ".py")
SKIP_PATH = re.compile(r"(^|/)(data/raw/|t/|card/|og/|node_modules/|assets/search/|supabase/)|(^|/)js/data\.js$|cues(_all)?\.js$|(^|/)ubike\.json$")
OWN = re.compile(r"^https?://(cultural[\w-]*|www)\.123hi\.org", re.I)


def _clean(u):
    u = u.rstrip(".,;:!?]}*|")
    while u.endswith(")") and u.count("(") < u.count(")"):
        u = u[:-1].rstrip(".,;:!?]}*|")
    return u


def urls_in(text, key=""):
    t = text.strip()
    if t.startswith("http") and "\n" not in t and (key in URL_KEYS or WHOLE_RE.match(t)):
        return [t]
    return [_clean(u) for u in URL_RE.findall(text)]


def collect(sister):
    """回傳 {url: [出現位置…]}，位置是 dict：site、city、item、name、where。"""
    occ = {}

    def add(u, **w):
        if "{" in u or "$" in u or "…" in u or u.endswith("//") or len(u) < 12 or "<" in u:
            return
        occ.setdefault(u, []).append(w)

    for c in inventory.cities():
        names = {s["id"]: s["name"] for s in c.official}
        names.update({i["id"]: i["name"] for i in c.ich.get("items", [])})
        names.update({v["id"]: v["name"] for v in c.ich.get("venues", [])})

        def walk(x, fn, item, path):
            if isinstance(x, dict):
                it = x.get("id") if isinstance(x.get("id"), str) and x["id"] in names else item
                for k, v in x.items():
                    walk(v, fn, k if (fn == "images.json" and not path) else it, path + [k])
            elif isinstance(x, list):
                for v in x:
                    walk(v, fn, item, path)
            elif isinstance(x, str) and "http" in x:
                for u in urls_in(x, path[-1] if path else ""):
                    add(u, site=c.site["id"], city=c.slug, item=item or "", name=names.get(item, ""), where="%s/data/%s：%s" % (c.slug, fn, ".".join(path[-2:])))

        for fn, d in c.json_files():
            walk(d, fn, "", [])

    for s in inventory.SITES:
        d = repo_dir(s["repo"])
        if not d:
            continue
        core = s["role"] == "core"
        if not core and not sister:
            only = lambda p: "/" not in p or p.startswith("assets/js/") or p.startswith("assets/css/")
        else:
            only = lambda p: True
        city_dirs = {c.slug for c in inventory.cities() if c.repo == s["repo"]}
        for p in sorted(repo_files(d)):
            if not p.endswith(TEXT_EXT) or SKIP_PATH.search(p) or not only(p) or p.startswith(("tools/", ".github/", "docs/", "readme/")):
                continue
            top = p.split("/")[0]
            if core and top in city_dirs and "/data/" in p:
                continue  # 縣市資料已在上面逐筆處理
            fp = os.path.join(d, p)
            if not os.path.exists(fp) or os.path.getsize(fp) > 6_000_000:
                continue
            try:
                t = open(fp, encoding="utf-8").read()
            except Exception:
                continue
            for u in {_clean(u) for u in URL_RE.findall(t)}:
                add(u, site=s["id"], city=top if top in city_dirs else "", item="", name="", where=p)
    return occ


def _host(u):
    return urllib.parse.urlsplit(u).netloc.lower()


def classify(u, rules):
    h = _host(u)
    L = rules["links"]
    if h.split(":")[0] in L["skip_hosts"] or any(h.endswith(x) for x in L["skip_host_suffix"]) or h.startswith(("localhost", "127.")):
        return "skip"
    if OWN.match(u) or h.endswith("github.io"):
        return "own"
    if h in L["manual_hosts"]:
        return "manual"
    if h == "nchdb.boch.gov.tw":
        return "nchdb"
    if h == "data.boch.gov.tw":
        return "bochimg"
    if h in ("commons.wikimedia.org", "upload.wikimedia.org", "thumb.wikimedia.org"):
        return "commons"
    if h.endswith(".wikipedia.org"):
        return "wiki"
    if h in ("creativecommons.org", "github.com", "www.123hi.org"):
        return "skip" if h != "creativecommons.org" else "other"
    return "other"


def commons_title(u):
    p = urllib.parse.unquote(urllib.parse.urlsplit(u).path)
    m = re.match(r"/wiki/(File:.+)$", p) or re.match(r"/wiki/(Category:.+)$", p)
    if m:
        return m.group(1).replace("_", " ")
    m = re.match(r"/wikipedia/commons/(?:thumb/)?[0-9a-f]/[0-9a-f]{2}/([^/]+)", p)
    if m:
        return "File:" + m.group(1).replace("_", " ")
    return None


def wiki_title(u):
    sp = urllib.parse.urlsplit(u)
    m = re.match(r"/(?:wiki|zh-tw|zh-hant|zh-hk|zh-cn|zh)/(.+)$", sp.path)
    if not m:
        return None
    return urllib.parse.unquote(m.group(1)).replace("_", " ")


def api_exists(host, titles):
    """用 MediaWiki API 查一批標題是否存在。回傳 {title: True/False}；查不到（被限流）的標題不在結果裡。"""
    out, titles, miss = {}, sorted(set(titles)), 0
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        q = urllib.parse.urlencode({"action": "query", "format": "json", "formatversion": "2", "redirects": "1", "converttitles": "1", "titles": "|".join(chunk)})  # converttitles：中文維基的繁簡、臺／台標題視為同一條目
        d = get_json("https://%s/w/api.php?%s" % (host, q), gap=1.5, tries=2)
        if not d or "query" not in d:
            log("  %s API 沒有回應（可能被限流），這一批 %d 個標題未確認" % (host, len(chunk)))
            miss += 1
            if i == 0 or miss >= 2:
                return out  # 一開始就被擋，或連續兩批失敗：其餘放棄，不再衝撞（列為未能確認，下次再查）
            continue
        miss = 0
        qd = d["query"]
        alias = {}
        for k in ("normalized", "converted", "redirects"):
            for m in qd.get(k) or []:
                alias[m["from"]] = m["to"]
        pages = {p["title"]: not (p.get("missing") or p.get("invalid")) for p in qd.get("pages") or []}
        for t in chunk:
            x = t
            for _ in range(6):
                if x in alias:
                    x = alias[x]
            if x in pages:
                out[t] = pages[x]
    return out


def _is_home(u):
    p = urllib.parse.urlsplit(u)
    return p.path in ("", "/") and not p.query


def _same(a, b):
    f = lambda u: re.sub(r"^https?://(www\.)?", "", urllib.parse.unquote(u)).rstrip("/").lower()
    return f(a) == f(b)


def check_http(u, method, timeout):
    gap = 0.4 if method == "HEAD" else 1.2  # HEAD 只用在文資局圖片：數量多、負擔輕，間隔短一點
    r = http(u, method=method, timeout=timeout, gap=gap)
    if method == "HEAD" and r["code"] in (0, 400, 403, 405, 501):
        r = http(u, method="GET", timeout=timeout, gap=gap, max_bytes=2048)
    code = r["code"]
    if code == 200:
        body = r["body"][:20000].decode("utf-8", "replace")
        t = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
        title = (t.group(1).strip() if t else "")[:80]
        if r["hops"] and _is_home(r["final"]) and not _is_home(u):
            return "moved", code, r["final"], "被轉到網站首頁，原本的頁面可能已經移除"
        if re.search(r"\b404\b|找不到(網頁|頁面|此頁)|頁面不存在|page not found|無此頁面|查無資料", title, re.I):
            return "broken", code, r["final"], "網頁標題顯示找不到頁面：" + title
        if r["hops"] and r["perm"] and not _same(u, r["final"]):
            return "redirect", code, r["final"], "永久轉址到新網址"
        return "ok", code, r["final"], ""
    if code in (404, 410):
        return "broken", code, r["final"], "HTTP %d" % code
    return "unsure", code, r["final"], ("HTTP %d" % code) if code else r["err"]


def run(ctx):
    rules = ctx["rules"]
    L = rules["links"]
    lv = ctx["level_cfg"]
    occ = collect(lv.get("sister_links", False))
    state = load(LINKS, {})
    kinds = {}
    for u in occ:
        kinds.setdefault(classify(u, rules), []).append(u)
    stats = {"total": len(occ), "byKind": {k: len(v) for k, v in sorted(kinds.items())}, "checked": 0, "unverified": 0}
    F = []
    cities = {c.slug: c for c in inventory.cities()}
    core_of = lambda u: next((o for o in occ[u] if o["site"] in ("ch1", "ch2")), occ[u][0])

    def emit(check, sev, u, title, detail, sub=""):
        o = core_of(u)
        where = sorted({x["where"] for x in occ[u]})
        more = "" if len(where) <= 3 else "…等 %d 處" % len(where)
        F.append(finding(check, sev, o["site"], title, (detail + "\n" if detail else "") + "出現在：" + "；".join(where[:3]) + more,
                         o["city"], o["item"], o["name"], u, sub=u + sub))

    # ---- 自己的網站：用 repo 資料確認 ----
    site_of_slug = {c.slug: c.site for c in cities.values()}
    ids = {c.slug: {s["id"] for s in c.official} | {v["id"] for v in c.ich.get("venues", [])} | {i["id"] for i in c.ich.get("items", [])} for c in cities.values()}
    for u in kinds.get("own", []):
        m = re.match(r"^https?://(cultural2?)\.123hi\.org/([a-z-]+)/?(?:index\.html)?(?:\?[^#]*)?(?:#(\w+)(?:/([^/?#]+))?)?", u)
        if not m:
            continue
        host, slug, page, iid = m.groups()
        if slug not in site_of_slug:
            if slug in ("assets", "guide", "tools", "audio"):
                continue
            emit("INT-DEEPLINK", "medium", u, "連結指向不存在的縣市資料夾「%s」" % slug, "")
            continue
        want = urllib.parse.urlsplit(site_of_slug[slug]["url"]).netloc.split(".")[0]
        if host != want:
            emit("INT-DEEPLINK", "medium", u, "連結的網域錯了：%s 放在 %s.123hi.org" % (cities[slug].name, want), "")
        elif page == "map" and iid and urllib.parse.unquote(iid) not in ids[slug]:
            emit("INT-DEEPLINK", "medium", u, "連結指向 %s 不存在的景點「%s」" % (cities[slug].name, iid), "主網站可能改過 id 或移除了這筆；姊妹站要重新產生資料。")
    stats["checked"] += len(kinds.get("own", []))

    # ---- 國家文化資產網：用開放資料確認 ----
    boch = ctx.get("boch")
    n_spa = 0
    for u in kinds.get("nchdb", []):
        m = re.search(r"/assets/(?:advanceSearch|overview)/([A-Za-z]+)/(\d{14})", u)
        if not m or not boch:
            n_spa += 1
            continue
        typ, cid = m.groups()
        rec = boch["T"].get(cid, (None, None))[1] or boch["I"].get(cid)
        if rec is None:
            if typ in ("ptp", "antiquity", "antiquities"):
                n_spa += 1
                continue
            emit("LNK-BROKEN", "high", u, "官方頁連結的案號在開放資料裡找不到", "案號 %s。國家文化資產網是單頁應用，連結打開不會顯示錯誤，但內容會是空的。" % cid)
        else:
            good = (rec.get("caseUrl") or "").replace("http://", "https://")
            if good and good != u.replace("http://", "https://").replace("/overview/", "/advanceSearch/"):
                emit("LNK-REDIRECT", "medium", u, "官方頁連結與開放資料提供的網址不同", "官方網址：" + good)
        stats["checked"] += 1
    stats["nchdbUnverifiable"] = n_spa

    # ---- 維基共享資源、維基百科：API 批次 ----
    for kind, label in (("commons", "維基共享資源"), ("wiki", "維基百科")):
        groups = {}
        for u in kinds.get(kind, []):
            t = commons_title(u) if kind == "commons" else wiki_title(u)
            if t and not t.startswith("Category:"):
                groups.setdefault("commons.wikimedia.org" if kind == "commons" else _host(u), {}).setdefault(t.split("#")[0], []).append(u)
        for host, tmap in groups.items():
            log("%s：用 API 確認 %d 個頁面" % (host, len(tmap)))
            res = {} if ctx.get("offline") else api_exists(host, list(tmap))
            un = [t for t in tmap if t not in res]
            stats["unverified"] += sum(len(tmap[t]) for t in un)
            stats["checked"] += sum(len(tmap[t]) for t in res)
            if un and not ctx.get("offline"):
                F.append(finding("SYS-SOURCE", "low", "", "%s有 %d 個頁面本次未能確認" % (label, len(un)),
                                 "%s 的 API 限流或沒有回應。這不代表連結失效，下次檢測會再查。" % host, sub=host))
            for t, ok in res.items():
                if ok:
                    continue
                u = sorted(tmap[t], key=lambda x: "/wiki/" not in x)[0]
                if kind == "commons":
                    emit("LNK-COMMONS", "high", u, "照片「%s」已從維基共享資源刪除" % t[5:],
                         "共享資源刪除檔案多半是授權有問題。網站上這張照片的本機副本應一併下架，換一張授權清楚的照片。")
                else:
                    emit("LNK-BROKEN", "medium", u, "維基百科條目「%s」不存在" % t, "條目可能已改名或刪除，請搜尋新條目名稱後更新連結。")

    # ---- 需要實際連線的：文資局圖片（輪流）＋其他網站 ----
    todo = []
    imgs = sorted(kinds.get("bochimg", []), key=lambda u: (state.get(u, {}).get("t", ""), u))
    todo += [(u, "HEAD") for u in imgs[:lv.get("official_image_budget", 300)]]
    for u in kinds.get("other", []):
        st = state.get(u, {})
        if st.get("s") == "ok" and days_between(st.get("t", "2000-01-01"), TODAY) < L["recheck_ok_days"]:
            continue
        todo.append((u, "GET"))
    stats["manual"] = len(kinds.get("manual", []))
    if ctx.get("offline"):
        todo = []
    log("連線檢查 %d 個網址（文資局圖片 %d／%d）" % (len(todo), min(len(imgs), lv.get("official_image_budget", 300)), len(imgs)))

    def work(a):
        u, m = a
        try:
            return u, check_http(u, m, L["timeout"])
        except Exception as e:
            return u, ("unsure", 0, u, "檢查程式錯誤：%s" % e)

    done = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for u, (s, code, final, note) in ex.map(work, todo):
            done += 1
            if done % 100 == 0:
                log("  已檢查 %d／%d" % (done, len(todo)))
            st = state.setdefault(u, {})
            bad = s in ("broken", "moved", "unsure")
            if not bad:
                st["f"] = 0
            elif st.get("t") != TODAY or not st.get("f"):  # 連續失敗以「天」計：同一天重跑幾次都只算一次
                st["f"] = st.get("f", 0) + 1
            if bad and not st.get("ff"):
                st["ff"] = TODAY
            if not bad:
                st.pop("ff", None)
            st.update({"s": s, "c": code, "t": TODAY, "n": note, "final": final if final != u else ""})
            stats["checked"] += 1

    # 依記錄產生發現（本次沒重查的網址沿用上次結果）
    cur_img = {(x.get("representImage") or {}).get("original") for _, x in (boch or {"T": {}})["T"].values()}
    dead = {}
    for u in kinds.get("bochimg", []):
        st = state.get(u)
        if st and st["s"] in ("broken", "moved"):
            o = core_of(u)
            dead.setdefault((o["site"], o["city"]), []).append((o["name"] or o["item"] or _short(u), u in cur_img))
    for (sid, slug), lst in sorted(dead.items()):
        same = sum(1 for _, x in lst if x)
        F.append(finding("LNK-OFFIMG", "low", sid, "%s有 %d 處的「官方代表圖」連結打不開" % (cities[slug].name if slug in cities else slug, len(lst)),
                         "景點詳情頁的「官方代表圖（連結）」點下去是 404。其中 %d 處是官方開放資料目前提供的網址本身就失效（多半是缺副檔名的舊資料），%d 處是官方已換新圖。\n" % (same, len(lst) - same)
                         + "、".join(n for n, _ in sorted(lst)), slug, sub="offimg"))
    for u in kinds.get("other", []):
        st = state.get(u)
        if not st:
            continue
        core = any(o["site"] in ("ch1", "ch2") for o in occ[u])
        since = "（自 %s 起連續 %d 次）" % (st.get("ff", TODAY), st.get("f", 1)) if st.get("f", 0) > 1 else ""
        if st["s"] == "broken":
            emit("LNK-BROKEN", "high" if core else "medium", u, "連結失效：" + _short(u), st.get("n", "") + since)
        elif st["s"] == "moved":
            emit("LNK-BROKEN", "medium", u, "連結被轉到首頁：" + _short(u), st.get("n", "") + since)
        elif st["s"] == "redirect":
            emit("LNK-REDIRECT", "low", u, "連結已搬家：" + _short(u), "新網址：" + st.get("final", ""))
        elif st["s"] == "unsure":
            if st.get("f", 0) >= L["fails_before_broken"] + 1:
                emit("LNK-BROKEN", "medium", u, "連結連續 %d 次連不上：%s" % (st["f"], _short(u)), "最近一次：%s。可能是對方擋掉自動檢查，請用瀏覽器打開確認。" % st.get("n", ""))
            else:
                stats["unverified"] += 1
                emit("LNK-UNSURE", "info", u, "連結本次未能確認：" + _short(u), "%s。可能只是對方暫時忙碌或擋掉自動檢查；連續 %d 次才會列為失效。" % (st.get("n", ""), L["fails_before_broken"] + 1))
    # 清掉已不在網站上的網址
    for u in [u for u in state if u not in occ]:
        del state[u]
    if not ctx.get("offline"):
        dump(state, LINKS, indent=0)
    stats["imageRotation"] = {"total": len(imgs), "thisRun": min(len(imgs), lv.get("official_image_budget", 300))}
    return F, stats


def _short(u):
    u = urllib.parse.unquote(re.sub(r"^https?://", "", u))
    return u if len(u) <= 70 else u[:67] + "…"
