"""檢測三：內部一致性（不需要網路）。資料之間對不對得起來、該有的檔案在不在、姊妹站的資料是否過期。"""
import hashlib, os, re
from common import finding, git_date, load, repo_dir, repo_files
import inventory

PRIVATE = [(r"(?<![A-Za-z0-9])[A-Z][12]\d{8}(?!\d)", "疑似身分證字號"), (r"[\w.+-]+@[\w-]+\.[\w.]+", "疑似 Email"),
           (r"(?<![\d/.])09\d{2}-?\d{3}-?\d{3}(?!\d)", "疑似手機號碼")]


URLISH = re.compile(r"https?://\S+|[\w-]+\.(?:jpe?g|png|webp|gif|pdf)", re.I)


def _owned(x, own=""):
    """走訪資料裡的每個字串，並帶著它屬於哪一筆（最近一層有 id 的物件）。"""
    if isinstance(x, dict):
        o = x["id"] if isinstance(x.get("id"), str) else own
        for v in x.values():
            yield from _owned(v, o)
    elif isinstance(x, list):
        for v in x:
            yield from _owned(v, own)
    elif isinstance(x, str):
        yield own, x


def run(ctx):
    F, stats = [], {"cities": 0, "files": 0}
    cities = inventory.cities()
    for c in cities:
        stats["cities"] += 1
        sid = c.site["id"]
        files = repo_files(c.dir)
        off = {s["id"]: s for s in c.official}
        con = {s["id"] for s in c.content}
        f = lambda check, sev, title, detail="", item="", name="", sub="": F.append(finding(check, sev, sid, title, detail, c.slug, item, name, sub=sub or title))

        for i in sorted(set(off) - con):
            f("INT-CONTENT", "high", "「%s」有官方資料但沒有介紹內容" % off[i]["name"], "sites-official.json 有這筆，sites-content.json 沒有。", i, off[i]["name"])
        for i in sorted(con - set(off)):
            f("INT-CONTENT", "medium", "介紹內容「%s」對不到官方資料" % i, "sites-content.json 有這筆，sites-official.json 沒有（可能官方已移除或 id 改了）。", i)

        # 照片檔
        for k, lst in c.images.items():
            if k not in off and k not in {v["id"] for v in c.ich.get("venues", [])} and k not in {i["id"] for i in c.ich.get("items", [])}:
                f("INT-IMG", "low", "照片清單的「%s」對不到任何景點" % k, "images.json 的這個項目沒有對應的景點、展示點或無形文資。", k)
            for im in lst:
                for fld in ("local", "small"):
                    p = im.get(fld)
                    if p:
                        stats["files"] += 1
                        if (c.slug + "/" + p.lstrip("./")) not in files and p.lstrip("./") not in files:
                            f("INT-IMG", "medium", "照片檔不存在：%s" % p, "images.json 記了這個檔，repo 裡找不到。", k, off.get(k, {}).get("name", ""), sub=p)
                if not im.get("license") or not im.get("artist"):
                    f("INT-IMG", "medium", "「%s」有照片缺少作者或授權標示" % (off.get(k, {}).get("name") or k), "檔案：%s\n缺少：%s。照片都要標示作者與授權；查不到就換一張。" % (im.get("file") or im.get("page"), "、".join(n for n, v in (("作者", im.get("artist")), ("授權", im.get("license"))) if not v)), k, off.get(k, {}).get("name", ""), sub=str(im.get("file")))

        # 語音
        cues = inventory.audio_cues(c)
        if cues is None:
            f("INT-AUDIO", "medium", "讀不到語音字幕檔 audio/cues.js")
        else:
            for k in cues:
                stats["files"] += 1
                if "%s/audio/%s.mp3" % (c.slug, k) not in files:
                    f("INT-AUDIO", "medium", "語音檔不存在：audio/%s.mp3" % k, "cues.js 有這段字幕，mp3 檔不在 repo。請重跑 tools/gen_audio.py。", sub=k)
            for i in off:
                if "site-" + i not in cues:
                    f("INT-AUDIO", "low", "「%s」沒有語音導覽" % off[i]["name"], "cues.js 沒有 site-%s。新增或改過 id 的景點要重跑 tools/gen_audio.py。" % i, i, off[i]["name"])

        # 無形文資、展示點互相參照
        venues = {v["id"]: v for v in c.ich.get("venues", [])}
        items = {i["id"]: i for i in c.ich.get("items", [])}
        for it in items.values():
            if it.get("venueId") and it["venueId"] not in venues:
                f("INT-REF", "medium", "無形文資「%s」的展示點 %s 不存在" % (it["name"], it["venueId"]), "", it["id"], it["name"])
        for v in venues.values():
            if v.get("relatedSiteId") and v["relatedSiteId"] not in off:
                f("INT-REF", "medium", "展示點「%s」對應的景點 %s 不存在" % (v["name"], v["relatedSiteId"]), "", v["id"], v["name"])
            for i in v.get("ichIds") or []:
                if i not in items:
                    f("INT-REF", "medium", "展示點「%s」列的無形文資 %s 不存在" % (v["name"], i), "", v["id"], v["name"], sub=v["id"] + i)

        # 網頁實際載入的 data.js 是否與資料一致
        dj = inventory.data_js(c)
        if dj is None:
            f("INT-BUILD", "high", "讀不到 js/data.js", "縣市頁載入的資料檔不存在或格式錯誤，請重跑 tools/build_data.py。")
        else:
            built = {s.get("id"): s for s in dj.get("sites", [])} if isinstance(dj.get("sites"), list) else {}
            if built:
                miss, extra = set(off) - set(built), set(built) - set(off)
                ren = [i for i in set(off) & set(built) if built[i].get("name") != off[i]["name"] or built[i].get("category") != off[i].get("category")]
                if miss or extra or ren:
                    f("INT-BUILD", "high", "js/data.js 與資料檔不一致（少 %d 筆、多 %d 筆、名稱或類別不同 %d 筆）" % (len(miss), len(extra), len(ren)),
                      "data/*.json 改過之後沒有重新產生網頁資料。請在主網站執行 python3 tools/build_data.py。\n" + "、".join(sorted(miss | extra | set(ren))[:8]))

        # 個資樣式掃描（PIMS）
        for fn, d in c.json_files():
            if fn in ("images.json", "config.json"):
                continue
            for own, t in _owned(d):
                t = URLISH.sub(" ", t)
                for pat, label in PRIVATE:
                    for m in re.finditer(pat, t):
                        v = m.group(0)
                        if "@" in v and v.lower().endswith((".gov.tw", ".edu.tw", ".org.tw")):
                            continue  # 機關信箱
                        mask = v[:4] + "＊" * 4  # 報告是公開的，不把完整的號碼或信箱寫進去
                        ctxt = (t[max(0, m.start() - 18):m.start()] + mask + t[m.end():m.end() + 8]).replace("\n", " ")
                        nm = off.get(own, {}).get("name") or items.get(own, {}).get("name") or ""
                        f("INT-PII", "medium", "%s%s：%s" % ("「%s」的資料有" % nm if nm else "", label, mask),
                          "在 %s/data/%s。公開網站不應轉載個人聯絡資料；確認是機關公開電話才保留。\n前後文：…%s…" % (c.slug, fn, ctxt), own, nm, sub=fn + hashlib.sha1(v.encode()).hexdigest()[:8])

    # 入口頁縣市卡片上寫的數字
    d1 = repo_dir("Cultural_Heritage")
    if d1 and os.path.exists(os.path.join(d1, "assets/js/cities.js")):
        txt = open(os.path.join(d1, "assets/js/cities.js"), encoding="utf-8").read()
        for c in cities:
            m = re.search(r'slug:\s*"%s".*?desc:\s*"([^"]*)"' % re.escape(c.slug), txt, re.S)
            if not m:
                F.append(finding("INT-COUNT", "medium", "ch1", "cities.js 沒有 %s 的卡片說明" % c.name, "", c.slug, sub="nocard"))
                continue
            desc = m.group(1)
            for pat, real, label in ((r"(\d+)\s*處有形文化資產", len(c.official), "有形文化資產"), (r"(\d+)\s*項無形文化資產", len(c.ich.get("items", [])), "無形文化資產")):
                n = re.search(pat, desc)
                if n and int(n.group(1)) != real:
                    F.append(finding("INT-COUNT", "low", "ch1", "入口頁寫 %s 有 %s 項%s，實際是 %d" % (c.name, n.group(1), label, real),
                                     "請更新 assets/js/cities.js 的 desc（README 的數字也一併檢查）。", c.slug, sub=label))

    # 姊妹站：資料是否比主網站舊、筆數與 id 是否一致
    newest = max([d for d in (ctx.get("dataDate") or {c.slug: git_date(c.dir, c.slug + "/data") for c in cities}).values() if d] or [""])
    all_ids = {(c.slug, s["id"]) for c in cities for s in c.official}
    total = len(all_ids)
    n_ich = sum(len(c.ich.get("items", [])) for c in cities)
    stats["sisters"] = {}
    for s in inventory.SITES:
        if s["role"] != "sister":
            continue
        d = repo_dir(s["repo"])
        if not d:
            continue
        for rel in s.get("data", []):
            j = load(os.path.join(d, rel))
            if not j:
                continue
            meta = j.get("meta", {}) if isinstance(j, dict) else {}
            gen = meta.get("generated")
            stats["sisters"][s["id"]] = {"generated": gen, "mainDataDate": newest}
            if gen and newest and gen < newest:
                F.append(finding("INT-STALE", "medium", s["id"], "%s的資料比主網站舊" % s["name"],
                                 "%s 產生於 %s，主網站縣市資料最後更新是 %s。\n更新方法：在 %s 執行 %s，檢查後開 PR。" % (rel, gen, newest, s["repo"], s.get("rebuild", "")), sub=rel))
            for key, real, label in (("total", total, "有形文資"), ("sites", total, "有形文資"), ("sitesTotal", total, "有形文資"), ("totalIch", n_ich, "無形文資"), ("ich", n_ich, "無形文資")):
                if isinstance(meta.get(key), int) and meta[key] != real:
                    F.append(finding("INT-STALE", "medium", s["id"], "%s的%s筆數（%d）與主網站（%d）不同" % (s["name"], label, meta[key], real),
                                     "更新方法：在 %s 執行 %s。" % (s["repo"], s.get("rebuild", "")), sub=rel + key))
            break
    atlas = load(os.path.join(repo_dir("Cultural_Atlas") or "", "data/sites.json")) if repo_dir("Cultural_Atlas") else None
    if atlas and isinstance(atlas.get("sites"), list):
        slugs = [x["slug"] for x in atlas["counties"]]
        aid = {(slugs[r[0]], r[1]) for r in atlas["sites"]}
        gone, new = aid - all_ids, all_ids - aid
        if gone or new:
            F.append(finding("INT-STALE", "medium", "atlas", "地圖集的文資清單與主網站不同（主網站已沒有 %d 筆、地圖集缺 %d 筆）" % (len(gone), len(new)),
                             "例：" + "、".join("%s/%s" % x for x in sorted(gone | new)[:6]) + "\n地圖集是鄉鎮卡、鐵道版、海拔版的上游，請先重建地圖集再重建其他姊妹站。", sub="ids"))
    return F, stats
