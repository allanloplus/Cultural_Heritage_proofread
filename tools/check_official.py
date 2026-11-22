"""檢測一：與文化部文化資產局開放資料比對（新指定／登錄、廢止、升格、名稱與地址異動、新公告）。

資料來源：https://data.boch.gov.tw/opendata/ （與主網站 tools/newcity/fetch_sources.py 相同）
  1.1 古蹟  1.2 歷史建築  1.3 聚落建築群  1.4 紀念建築  2.1 考古遺址  3.1 文化景觀
  4.1 傳統表演藝術  4.2 傳統工藝  5.1 民俗  5.2 口述傳統  5.3 傳統知識與實踐  6.1 古物
「保存技術及保存者」不在開放資料裡，這一類只統計、不比對。

基準檔 state/official-baseline.json 記下每一筆官方紀錄的公告摘要；下次檢測時，公告有增加或變動的就是「官方新公告」。
"""
import json, math, os, re, time
from common import CACHE, STATE, TODAY, dump, finding, git_date, http, load, log, norm_name, same_name
import inventory

TANGIBLE = [("1.1", "monument"), ("1.2", "building"), ("1.3", "cluster"), ("1.4", "memorial"), ("2.1", "archaeo"), ("3.1", "landscape")]
ICH = ["4.1", "4.2", "5.1", "5.2", "5.3"]
ALL = [c for c, _ in TANGIBLE] + ICH + ["6.1"]
BASELINE = os.path.join(STATE, "official-baseline.json")


def boch_url(c):
    return "https://data.boch.gov.tw/opendata/" + ("assetsCase/6.1.json" if c == "6.1" else "v2/assetsCase/%s.json" % c)


def fetch(max_age_h=20):
    """下載 12 類開放資料到 .cache/boch/。回傳 {類別: list}；下載失敗的類別不在裡面（該類別就不比對，並在報告註明）。"""
    out = {}
    for c in ALL:
        p = os.path.join(CACHE, "boch", c + ".json")
        fresh = os.path.exists(p) and time.time() - os.path.getmtime(p) < max_age_h * 3600
        if not fresh:
            for i in range(3):
                log("下載文資局開放資料", c)
                r = http(boch_url(c), timeout=1500, gap=2, max_bytes=80_000_000)
                try:
                    d = json.loads(r["body"])
                    assert isinstance(d, list) and d
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    open(p, "wb").write(r["body"])
                    break
                except Exception:
                    log("  失敗", r["code"], r["err"])
                    time.sleep(20 * (i + 1))
        d = load(p)
        if d:
            out[c] = d
    return out


def _variants(n):
    return {n, n.replace("臺", "台"), n.replace("台", "臺")}


def _cities_of(x):
    return [a.get("cityName") or "" for a in x.get("addresses") or [] if isinstance(a, dict)]


def _ann(x):
    return [(z.get("registerDate") or "")[:10] + " " + (z.get("classification") or "") + (" " + z["officialDocNo"] if z.get("officialDocNo") else "")
            for z in x.get("announcementList") or [] if isinstance(z, dict)]


def _category(kind, lvl, city_name):
    local = "市定古蹟" if city_name.endswith("市") else "縣定古蹟"
    return {"monument": "國定古蹟" if "國定" in lvl else local, "building": "歷史建築", "memorial": "紀念建築",
            "cluster": "聚落建築群", "archaeo": "考古遺址", "landscape": "文化景觀"}[kind]


def _dist_m(a, b, c, d):
    try:
        x = math.radians(float(d) - float(b)) * math.cos(math.radians((float(a) + float(c)) / 2))
        y = math.radians(float(c) - float(a))
        return math.hypot(x, y) * 6371000
    except Exception:
        return 0


def _clean(s):
    return re.sub(r"\s+", "", (s or "")).replace("台", "臺")


def run(ctx):
    F, stats = [], {}
    boch = fetch()
    missing = [c for c in ALL if c not in boch]
    if missing:
        F.append(finding("SYS-SOURCE", "medium", "", "文資局開放資料有 %d 類下載失敗，這幾類本次沒有比對" % len(missing),
                         "類別：" + "、".join(missing) + "。通常是文資局伺服器忙碌，下次檢測會再試。", sub="boch"))
    cities = inventory.cities()
    by_name = {}
    for c in cities:
        for v in _variants(c.name):
            by_name[v] = c
    base = load(BASELINE, {})
    first_run = not base
    new_base = dict(base)
    data_date = {c.slug: git_date(c.dir, c.slug + "/data") for c in cities}

    # ---- 有形文化資產 ----
    T = {}
    for code, kind in TANGIBLE:
        for x in boch.get(code, []):
            T[x["caseId"]] = (kind, x)
    t_ok = all(c in boch for c, _ in TANGIBLE)
    site_ids = {}
    for c in cities:
        for s in c.official:
            site_ids.setdefault(s.get("caseId"), []).append((c, s))
    n_cmp = n_diff = n_dup = 0
    for cid, lst in site_ids.items():
        for c, s in lst:
            if cid not in T:
                if t_ok:
                    F.append(finding("OFF-GONE", "high", c.site["id"], "官方開放資料已經沒有「%s」" % s["name"],
                                     "文資局開放資料找不到案號 %s。可能已廢止、撤銷，或併入其他案件。請到國家文化資產網確認後，決定是否下架或加註。" % cid,
                                     c.slug, s["id"], s["name"], s.get("url")))
                continue
            kind, x = T[cid]
            n_cmp += 1
            diffs = []
            oname = x["caseName"].replace("國定古蹟-", "").replace("國定古蹟", "").strip()
            if not same_name(oname, s["name"]):
                diffs.append(("名稱", s["name"], oname, "medium"))
            lvl = (x.get("assetsClassifyName") or "").strip()
            # 跨縣市的文資（登錄在鄰縣）類別以網站所在縣市判斷市定／縣定，官方登錄縣市不同時不比
            reg_here = any(v in _variants(c.name) for v in _cities_of(x))
            ocat = _category(kind, lvl, c.name)
            if ocat != s.get("category") and (reg_here or ocat not in ("市定古蹟", "縣定古蹟")):
                diffs.append(("類別", s.get("category"), ocat, "high"))
            if reg_here:
                a0 = next((a for a in x.get("addresses") or [] if isinstance(a, dict) and (a.get("cityName") or "") in _variants(c.name)), {})
                oaddr = (a0.get("distName") or "") + (a0.get("address") or "")
                if _clean(oaddr) != _clean(s.get("address")) and not (_clean(a0.get("address")) and _clean(s.get("address")).endswith(_clean(a0.get("address")))):
                    diffs.append(("地址", s.get("address"), oaddr, "low"))
                la, ln = x.get("latitude"), x.get("longitude")
                if la and float(la) > 100:
                    la, ln = ln, la
                if la and s.get("lat") and _dist_m(la, ln, s["lat"], s["lng"]) > 150:
                    diffs.append(("座標", "%.5f, %.5f" % (s["lat"], s["lng"]), "%.5f, %.5f（相差約 %d 公尺）" % (float(la), float(ln), _dist_m(la, ln, s["lat"], s["lng"])), "low"))
            if _clean(x.get("openUpTime")) != _clean(s.get("open")):
                diffs.append(("開放時間", s.get("open") or "（空）", x.get("openUpTime") or "（空）", "medium"))
            oimg = (x.get("representImage") or {}).get("original")
            if (oimg or None) != (s.get("officialImg") or None):
                diffs.append(("官方代表圖", s.get("officialImg") or "（無）", oimg or "（無）", "low"))
            ourl = (x.get("caseUrl") or "").replace("http://", "https://")
            if ourl and ourl != s.get("url"):
                diffs.append(("官方頁網址", s.get("url"), ourl, "medium"))
            from_own = _ownership(x)
            if s.get("ownership") and from_own != s["ownership"]:
                diffs.append(("所有權", s["ownership"], from_own + "（影響私人宅第是否隱藏門牌）", "medium"))
            for fld, old, new, sev in diffs:
                n_diff += 1
                F.append(finding("OFF-FIELD", sev, c.site["id"], "「%s」的%s與官方資料不同" % (s["name"], fld),
                                 "網站：%s\n官方：%s" % (old, new), c.slug, s["id"], s["name"], s.get("url"), sub=fld,
                                 extra={"field": fld}))
    if t_ok:
        for cid, (kind, x) in T.items():
            if cid in site_ids:
                continue
            reg = [by_name[v] for v in _cities_of(x) if v in by_name]
            c = reg[0] if reg else None
            ann = _ann(x)
            # 同一處文資常有兩筆官方紀錄（縣市登錄＋國家指定，或改類別後新編案號）。同縣市已有同名的就不算缺。
            regs = set(_cities_of(x))
            if any(same_name(s2["name"], x["caseName"], loose=True) for cc in cities if regs & _variants(cc.name) for s2 in cc.official):
                n_dup += 1
                continue
            same = [s2["name"] for cc in cities for s2 in cc.official if norm_name(s2["name"]) == norm_name(x["caseName"])]
            F.append(finding("OFF-NEW", "medium" if same else "high", c.site["id"] if c else "", "官方有「%s」，網站還沒有收錄" % x["caseName"],
                             ("注意：網站已有同名的文資（案號不同），可能是同一處文資有兩種身分（例如古蹟＋文化景觀），或官方重新編案。\n" if same else "") + "類別：%s｜登錄縣市：%s｜案號：%s\n公告：%s" % (x.get("assetsClassifyName") or {"monument": "古蹟", "building": "歷史建築", "cluster": "聚落建築群", "memorial": "紀念建築", "archaeo": "考古遺址", "landscape": "文化景觀"}[kind], "、".join(sorted(set(_cities_of(x)))) or "不明",
                                                                 cid, "；".join(ann[-3:]) or "（無）"),
                             c.slug if c else "", cid, x["caseName"], (x.get("caseUrl") or "").replace("http://", "https://"), sub=cid))
    stats["tangible"] = {"site": sum(len(c.official) for c in cities), "official": len(T), "compared": n_cmp, "fieldDiffs": n_diff, "duplicateRecords": n_dup}

    # ---- 無形文化資產 ----
    I = {}
    for code in ICH:
        for x in boch.get(code, []):
            I[x["caseId"]] = x
    i_ok = all(c in boch for c in ICH)
    site_ich, ptp, names_by_city = {}, 0, {}
    for c in cities:
        for it in c.ich.get("items", []):
            names_by_city.setdefault(c.slug, []).append((it["name"], _holders(it.get("holder")), it.get("type")))
            m = re.search(r"/([A-Za-z]+)/(\d{14})", it.get("url") or "")
            if not m:
                continue
            if m.group(1) == "ptp":
                ptp += 1
                continue
            site_ich.setdefault(m.group(2), []).append((c, it))
    for cid, lst in site_ich.items():
        for c, it in lst:
            if cid not in I:
                if i_ok:
                    F.append(finding("ICH-GONE", "high", c.site["id"], "官方開放資料已經沒有無形文資「%s」" % it["name"],
                                     "案號 %s。可能已廢止登錄（例如保存者辭世），或官方重新編案。請確認後更新「哪裡看得到」與保存者說明。" % cid,
                                     c.slug, it["id"], it["name"], it.get("url")))
                continue
            x = I[cid]
            if not same_name(x["caseName"], it["name"], loose=True):
                F.append(finding("OFF-FIELD", "medium", c.site["id"], "無形文資「%s」的名稱與官方資料不同" % it["name"],
                                 "網站：%s\n官方：%s" % (it["name"], x["caseName"]), c.slug, it["id"], it["name"], it.get("url"), sub="名稱", extra={"field": "名稱"}))
    n_ich_new = n_ich_dup = 0
    if i_ok:
        for cid, x in I.items():
            if cid in site_ich:
                continue
            reg = [by_name[v] for v in _cities_of(x) if v in by_name]
            if not reg:
                g = (x.get("govInstitutionName") or "")[:3]
                reg = [by_name[g]] if g in by_name else []
            c = reg[0] if reg else None
            # 同縣市已有同名項目（網站把同一項目的多位保存者合併成一筆）就不算缺
            # 網站依規格把同一項目的縣市登錄與國家指定合併成一筆，也把多位保存者合併：同縣市同名，或保存者相同且類別相同（或名稱有共同用字），就視為已收錄
            oh = _holders(x.get("recorder"))
            ot = (x.get("assetsClassifyName") or "").strip()
            if c and any(same_name(x["caseName"], n, loose=True)
                         or (_holder_match(oh, h) and (t == ot or len(set(norm_name(n)) & set(norm_name(x["caseName"]))) >= 2))
                         for n, h, t in names_by_city.get(c.slug, ())):
                n_ich_dup += 1
                continue
            n_ich_new += 1
            F.append(finding("ICH-NEW", "medium", c.site["id"] if c else "", "官方有無形文資「%s」，網站還沒有收錄" % x["caseName"],
                             "類別：%s｜主管機關：%s｜案號：%s\n公告：%s" % (x.get("assetsClassifyName"), x.get("govInstitutionName"), cid, "；".join(_ann(x)[-3:]) or "（無）"),
                             c.slug if c else "", cid, x["caseName"], (x.get("caseUrl") or "").replace("http://", "https://"), sub=cid))
    stats["ich"] = {"site": sum(len(c.ich.get("items", [])) for c in cities), "official": len(I), "notInOpenData": ptp, "missing": n_ich_new, "duplicateRecords": n_ich_dup}

    # ---- 古物 ----
    A = boch.get("6.1", [])
    a_by_county, a_all = {}, {}
    for x in A:
        a_all.setdefault(norm_name(x["caseName"]), []).append(x)
        for c in cities:
            if any((x.get("belongCity") or "").startswith(v) for v in _variants(c.name)):
                a_by_county.setdefault(c.slug, {}).setdefault(norm_name(x["caseName"]), []).append(x)
    n_ant = n_ant_miss = 0
    for c in cities:
        for v in c.ich.get("venues", []):
            for a in v.get("antiquities", []):
                n_ant += 1
                if not A:
                    continue
                k = norm_name(a["name"])
                xs = a_by_county.get(c.slug, {}).get(k) or a_all.get(k)
                if not xs:  # 名稱不完全相同：官方名稱常多加年代、族語或用不同標點
                    cand = [ys for ys in a_by_county.get(c.slug, {}).values() if same_name(a["name"], ys[0]["caseName"], loose=True)]
                    xs = cand[0] if len(cand) == 1 else None
                x = None
                if xs:  # 同一件古物有多筆官方紀錄時，等級相符的優先
                    x = next((y for y in xs if (y.get("assetsClassifyName") or "").strip() == a.get("level")), xs[0])
                if not x:
                    n_ant_miss += 1
                    F.append(finding("ANT-GONE", "low", c.site["id"], "古物「%s」在官方開放資料找不到同名紀錄" % a["name"],
                                     "展示點：%s。可能是網站用了簡稱、官方改名，或已廢止。請到國家文化資產網確認名稱與等級。" % v["name"],
                                     c.slug, v["id"], a["name"], sub=a["name"]))
                    continue
                lv = (x.get("assetsClassifyName") or "").strip()
                if lv and a.get("level") and lv != a["level"]:
                    F.append(finding("ANT-LEVEL", "high", c.site["id"], "古物「%s」的等級與官方不同" % a["name"],
                                     "網站：%s\n官方：%s（公告 %s）\n展示點：%s" % (a["level"], lv, x.get("registerDate"), v["name"]),
                                     c.slug, v["id"], a["name"], sub=a["name"]))
    stats["antiquity"] = {"site": n_ant, "official": len(A), "unmatched": n_ant_miss}

    # ---- 官方新公告（與上次檢測的基準比較）----
    events = []
    for cid, (kind, x) in T.items():
        sig = _ann(x)
        new_base[cid] = sig
        _ann_diff(events, base, first_run, cid, sig, x["caseName"], site_ids.get(cid), data_date, x)
    for cid, x in I.items():
        sig = _ann(x)
        new_base[cid] = sig
        _ann_diff(events, base, first_run, cid, sig, x["caseName"], site_ich.get(cid), data_date, x)
    for x in A:
        cid = "A" + x["caseId"]
        sig = [(x.get("registerDate") or "") + " " + (x.get("assetsClassifyName") or "")]
        new_base[cid] = sig
        if not first_run and cid not in base:
            c = next((c for c in cities if any((x.get("belongCity") or "").startswith(v) for v in _variants(c.name))), None)
            events.append(finding("ANT-NEW", "low", c.site["id"] if c else "", "官方新增古物「%s」" % x["caseName"],
                                  "等級：%s｜所在：%s｜公告：%s\n網站的古物是依展示點收錄；若這件古物有公開展示，可考慮加入。" % (x.get("assetsClassifyName"), x.get("belongCity"), x.get("registerDate")),
                                  c.slug if c else "", cid, x["caseName"], sub=cid))
    if boch:
        dump(new_base, BASELINE, indent=0)
    stats["baseline"] = {"firstRun": first_run, "records": len(new_base), "newAnnouncements": len(events)}
    ctx["events"] = ctx.get("events", []) + events
    ctx["boch"] = {"T": T, "I": I}
    ctx["dataDate"] = data_date
    return F, stats


def _ann_diff(events, base, first_run, cid, sig, name, on_site, data_date, x):
    """公告有新增或異動 → 事件。第一次檢測沒有基準：只看公告日期晚於網站該縣市資料最後更新日的。"""
    if not on_site:
        return  # 網站沒收錄的由 OFF-NEW／ICH-NEW 處理
    c, s = on_site[0]
    if first_run:
        since = data_date.get(c.slug)
        new = [a for a in sig if since and a[:10] > since]
    else:
        old = set(base.get(cid) or [])
        new = [a for a in sig if a not in old] if cid in base else []
    for a in new:
        kind = "廢止" if "廢止" in a or "撤銷" in a else ("變更" if "變更" in a or "修正" in a else "指定登錄")
        sev = {"廢止": "high", "變更": "medium", "指定登錄": "medium"}[kind]
        events.append(finding("OFF-ANN", sev, c.site["id"], "「%s」有新的官方公告（%s）" % (s["name"], a[11:].split(" ")[0] or kind),
                              "公告：%s\n請到國家文化資產網看公告內容（範圍變更、名稱修正、保存者異動、廢止等），再決定網站介紹是否要改。" % a,
                              c.slug, s["id"], s["name"], s.get("url"), sub=a))


def _holders(s):
    """保存者字串拆成名字集合：去掉括號說明、（歿）等註記，異體字統一。"""
    s = re.sub(r"[（(](歿|已故|已歿|故)[)）]", "", s or "")
    s = re.sub(r"[（()）]", "、", s)  # 括號裡常是本名或族名，也算一個名字
    return {norm_name(t) for t in re.split(r"[、,，;；\s]+", s) if len(norm_name(t)) >= 2}


def _holder_match(a, b):
    """兩邊的保存者是否有同一個人或團體（「關廟山西宮」與「關廟山西宮管理委員會」算同一個）。"""
    return any(x == y or (min(len(x), len(y)) >= 3 and (x in y or y in x)) for x in a for y in b)


def _ownership(rec):
    b = {i.get("buildingownership") for i in rec.get("buildingSiteList") or [] if isinstance(i, dict) and i.get("buildingownership")}
    land = {i.get("landownership") for i in rec.get("landlotList") or [] if isinstance(i, dict) and i.get("landownership")}
    vals = b or land
    if not vals:
        return "不明"
    return "公有" if vals == {"公有"} else "私有"
