"""把各項檢測的發現整理成報告：追蹤首次發現日、是否逾期、是否已解決，套用例外清單，產生 JSON／Markdown／CSV。"""
import collections, csv, datetime, io, os
from common import REPORTS, STATE, TODAY, cfg, days_between, dump, load
import inventory

FSTATE = os.path.join(STATE, "findings.json")
ESTATE = os.path.join(STATE, "events.json")
SEV_LABEL = {"high": "高", "medium": "中", "low": "低", "info": "參考"}
ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}


def _ignored(f, items):
    for it in items:
        m = it.get("match") or {}
        if not m:
            continue
        ok = all((f.get(k) == v) if k != "title_has" else (v in f["title"]) for k, v in m.items() if k != "note")
        if ok:
            until = it.get("until") or "9999-12-31"
            if until >= TODAY:
                return it
    return None


def keep_events(new, ctx):
    """事件型的發現（官方新公告、新增古物、新聞）只在發生那一次檢測得出來，所以存起來，直到處理完才拿掉：
    官方類：該縣市的資料在事件之後有更新（視為已處理），或列入例外清單；新聞類：超過保留天數。"""
    old = load(ESTATE, [])
    have = {e["key"] for e in old}
    for f in new:
        if f["key"] not in have:
            old.append(dict(f, detected=TODAY))
    keep = []
    dd = ctx.get("dataDate") or {}
    nk = ctx["rules"]["news"]["keep_days"]
    for e in old:
        if e["check"].startswith("NEWS"):
            if days_between(e.get("date") or e["detected"], TODAY) > nk:
                continue
        elif e.get("city") and dd.get(e["city"]) and dd[e["city"]] > e["detected"]:  # 同一天更新的不算（無法分辨先後），用例外清單處理
            continue
        keep.append(e)
    dump(keep, ESTATE, indent=0)
    return keep


def build(ctx, F, stats, started):
    rules, checks = ctx["rules"], cfg("checks")
    ignore = (cfg("ignore") or {}).get("items", [])
    events = keep_events(ctx.get("events", []), ctx)
    allf = {f["key"]: f for f in F + events}  # 相同 key 只留一筆
    prev = load(FSTATE, {"open": {}, "resolved": []})
    first_ever = not prev["open"] and not prev["resolved"]
    ran = set(ctx["ran"])
    group_of = {k: v["group"] for k, v in checks["checks"].items()}
    # 這次沒有執行（或執行失敗）的檢測項目：上次的發現原樣帶過來並標示，不算已解決
    for k, v in prev["open"].items():
        if v.get("group") not in ran and k not in allf and v.get("detail") is not None:
            allf[k] = dict(v, carried=True)
    opens, accepted, now_open = [], [], {}
    for k, f in allf.items():
        f["group"] = group_of.get(f["check"], "system")
        f["label"] = checks["checks"].get(f["check"], {}).get("label", f["check"])
        ig = _ignored(f, ignore)
        p = prev["open"].get(k)
        f["first"] = p["first"] if p else (f.get("detected") or TODAY)
        f["age"] = days_between(f["first"], TODAY)
        f["isNew"] = not p and not first_ever
        f["carried"] = bool(f.get("carried"))
        sla = rules["sla_days"].get(f["sev"])
        f["due"] = (datetime.date.fromisoformat(f["first"]) + datetime.timedelta(days=sla)).isoformat() if sla else ""
        f["overdue"] = bool(sla and f["age"] > sla)
        if ig:
            f["accepted"] = {"reason": ig.get("reason", ""), "by": ig.get("by", ""), "until": ig.get("until", "")}
            accepted.append(f)
        else:
            opens.append(f)
        now_open[k] = {x: y for x, y in f.items() if x not in ("age", "isNew", "due", "overdue", "accepted", "carried", "label")}
    resolved = [dict(v, key=k, resolved=TODAY) for k, v in prev["open"].items() if k not in now_open]
    res_log = (resolved + prev["resolved"])[:300]
    dump({"open": now_open, "resolved": res_log}, FSTATE, indent=0)

    cities = {c.slug: c for c in inventory.cities()}
    opens.sort(key=lambda f: (ORDER[f["sev"]], f["group"], f["city"], f["title"]))
    cnt = collections.Counter(f["sev"] for f in opens)
    by_site = {}
    for s in inventory.SITES:
        fs = [f for f in opens if f["site"] == s["id"]]
        c = collections.Counter(f["sev"] for f in fs)
        by_site[s["id"]] = {"name": s["name"], "url": s["url"], "role": s["role"], "high": c["high"], "medium": c["medium"], "low": c["low"], "info": c["info"],
                            "status": "act" if c["high"] else ("watch" if c["medium"] else "good")}
    by_city = {}
    for c in cities.values():
        fs = [f for f in opens if f["city"] == c.slug]
        k = collections.Counter(f["sev"] for f in fs)
        by_city[c.slug] = {"name": c.name, "site": c.site["id"], "url": c.url, "sites": len(c.official), "ich": len(c.ich.get("items", [])),
                           "high": k["high"], "medium": k["medium"], "low": k["low"], "info": k["info"]}
    by_group = {g["id"]: dict(collections.Counter(f["sev"] for f in opens if f["group"] == g["id"])) for g in checks["groups"]}
    summary = {"total": len(opens), "high": cnt["high"], "medium": cnt["medium"], "low": cnt["low"], "info": cnt["info"],
               "new": sum(1 for f in opens if f["isNew"]), "resolved": len(resolved), "overdue": sum(1 for f in opens if f["overdue"]),
               "accepted": len(accepted), "firstRun": first_ever, "bySite": by_site, "byCity": by_city, "byGroup": by_group}
    meta = {"date": TODAY, "level": ctx["level"], "ran": ctx["ran"], "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "seconds": int((datetime.datetime.now() - started).total_seconds()), "sla": rules["sla_days"],
            "scope": {"cities": len(cities), "sites": sum(len(c.official) for c in cities.values()), "ich": sum(len(c.ich.get("items", [])) for c in cities.values()),
                      "antiquities": sum(len(v.get("antiquities", [])) for c in cities.values() for v in c.ich.get("venues", [])), "links": (stats.get("links") or {}).get("total")}}
    rep = {"meta": meta, "summary": summary, "stats": stats, "dialogue": dialogue(summary, stats, meta, opens), "catalog": checks,
           "findings": opens, "accepted": accepted, "resolved": resolved[:100]}
    dump(rep, os.path.join(REPORTS, "latest.json"), indent=0)
    # 歷次紀錄：一天一筆；同一天跑多次時保留「當天第一次」與「當天最後一次」，看得出修正前後的差別
    hdir = os.path.join(REPORTS, "history")
    hist = load(os.path.join(hdir, "index.json"), [])
    entry = {"date": TODAY, "level": ctx["level"], **{k: summary[k] for k in ("total", "high", "medium", "low", "info", "new", "resolved", "overdue")}}
    today = [h for h in hist if h["date"] == TODAY]
    if not today:
        hist.append(entry)
    else:
        first = next((h for h in today if h.get("run") == "first"), None)
        if not first:  # 第二次執行：原本那一筆變成「第一次」，它的完整報告另存
            first = today[0]
            first["run"] = "first"
            src = os.path.join(hdir, TODAY + ".json")
            if os.path.exists(src):
                os.replace(src, os.path.join(hdir, TODAY + "-first.json"))
        hist = [h for h in hist if h["date"] != TODAY] + [first, dict(entry, run="last")]
    dump(rep, os.path.join(hdir, TODAY + ".json"), indent=0)
    hist.sort(key=lambda h: (h["date"], h.get("run") == "last"))
    keep = {h["date"] for h in hist[-80:]}
    for fn in os.listdir(hdir):  # 完整報告留最近 80 筆，趨勢摘要全部保留
        if fn != "index.json" and fn.endswith(".json") and fn[:10] not in keep:
            os.remove(os.path.join(hdir, fn))
    dump(hist, os.path.join(REPORTS, "history", "index.json"))
    open(os.path.join(REPORTS, "latest.md"), "w", encoding="utf-8").write(markdown(rep))
    open(os.path.join(REPORTS, "latest.csv"), "w", encoding="utf-8-sig", newline="").write(to_csv(rep))
    return rep


def dialogue(S, stats, meta, opens):
    """Allan 與阿拉蕾的檢測播報（依本次結果組出來）。"""
    sc = meta["scope"]
    D = []
    say = lambda who, mood, text: D.append({"who": who, "mood": mood, "text": text})
    say("R", "fight", "Allan，%d 月 %d 日的健檢做完了！這次檢查了 %d 個縣市、%s 處有形文資、%d 項無形文資。" % (int(meta["date"][5:7]), int(meta["date"][8:10]), sc["cities"], format(sc["sites"], ","), sc["ich"]))
    if sc.get("links"):
        say("A", "smile", "辛苦了。連結呢？全系列一共 %s 個不重複的網址，都看過了嗎？" % format(sc["links"], ","))
    if S["high"] == 0 and S["medium"] == 0:
        say("R", "thumb", "都看過了，沒有需要馬上處理的問題！只有 %d 個小提醒。" % (S["low"] + S["info"]))
        say("A", "laugh", "太好了，今天可以安心出門逛古蹟。")
    else:
        say("R", "explain", "看過了。要處理的有 %d 項：優先度高的 %d 項、中的 %d 項、低的 %d 項，另外有 %d 則參考線索。" % (S["high"] + S["medium"] + S["low"], S["high"], S["medium"], S["low"], S["info"]))
        if S["high"]:
            pick = ["OFF-GONE", "ICH-GONE", "LNK-COMMONS", "LIVE-DOWN", "OFF-NEW", "ANT-LEVEL", "OFF-FIELD", "INT-BUILD", "INT-CONTENT"]
            hi = [f for f in opens if f["sev"] == "high"]
            top = min(hi, key=lambda f: pick.index(f["check"]) if f["check"] in pick else 99) if hi else None
            say("A", "surprised", "高的有 %d 項？先說最要緊的。" % S["high"])
            if top:
                say("R", "think", "例如這一筆：%s。這類問題建議 %d 天內處理。" % (top["title"] if len(top["title"]) < 60 else top["label"], meta["sla"]["high"]))
        else:
            say("A", "wink", "沒有高優先度的，很好。中的那幾項我們排進這個月處理。")
    off = stats.get("official") or {}
    if off:
        n_new = sum(1 for f in opens if f["check"] in ("OFF-NEW", "ICH-NEW"))
        n_ann = sum(1 for f in opens if f["check"] == "OFF-ANN")
        if n_new or n_ann:
            say("R", "surprised", "和文資局的官方資料比對後，有 %d 筆官方有、我們還沒收錄，另外有 %d 則新公告要看。" % (n_new, n_ann))
            say("A", "point", "文化資產會新增、升格，也會廢止。重點是定期對一次，不要讓網站停在過去。")
        else:
            say("R", "thumb", "和文資局的官方資料逐筆比對，沒有新增、也沒有廢止，網站和官方同步。")
    n_news = sum(1 for f in opens if f["group"] == "news")
    if n_news:
        say("R", "explain", "還有 %d 則新聞提到我們收錄的文資，像修復完工、重新開放這類消息。" % n_news)
        say("A", "think", "新聞只是線索，要讀過內容才知道介紹要不要改。有空一則一則看。")
    if S["overdue"]:
        say("A", "scratch", "不好意思，有 %d 項已經超過處理期限了，這幾項我會優先處理。" % S["overdue"])
    if S["resolved"]:
        say("R", "laugh", "好消息！上次的問題有 %d 項已經解決了。" % S["resolved"])
    if S["firstRun"]:
        say("A", "smile", "這是第一次健檢，結果就是我們的起點。之後每週自動檢查一次，新的問題會標出來。")
    say("R", "fight", "下面的清單每一筆都有建議和更新方法，照著做就可以。走吧，開始整理！")
    return D


def markdown(rep):
    M, S, C = rep["meta"], rep["summary"], rep["catalog"]
    L = ["# 文資網站健檢報告　%s" % M["date"], "",
         "- 檢測等級：%s｜執行項目：%s｜耗時 %d 秒" % ({"weekly": "每週", "monthly": "每月（完整）"}.get(M["level"], M["level"]), "、".join(M["ran"]), M["seconds"]),
         "- 範圍：%d 個縣市、%s 處有形文化資產、%d 項無形文化資產、%d 件古物、%s 個不重複網址" % (M["scope"]["cities"], format(M["scope"]["sites"], ","), M["scope"]["ich"], M["scope"]["antiquities"], format(M["scope"]["links"] or 0, ",")),
         "- 網頁版報告（可篩選）：`index.html`｜試算表：`reports/latest.csv`", "",
         "## 摘要", "", "| 優先度 | 件數 | 處理期限 |", "|---|---|---|"]
    for s in ("high", "medium", "low", "info"):
        L.append("| %s | %d | %s |" % (SEV_LABEL[s], S[s], ("%d 天內" % M["sla"][s]) if s in M["sla"] else "看過即可"))
    L += ["", "本次新發現 %d 項｜已解決 %d 項｜逾期 %d 項｜列為例外 %d 項" % (S["new"], S["resolved"], S["overdue"], S["accepted"]), "",
          "## 各網站", "", "| 網站 | 狀態 | 高 | 中 | 低 | 參考 |", "|---|---|---|---|---|---|"]
    for v in S["bySite"].values():
        L.append("| [%s](%s) | %s | %d | %d | %d | %d |" % (v["name"], v["url"], {"act": "需處理", "watch": "留意", "good": "良好"}[v["status"]], v["high"], v["medium"], v["low"], v["info"]))
    for g in C["groups"]:
        fs = [f for f in rep["findings"] if f["group"] == g["id"]]
        if not fs:
            continue
        L += ["", "## %s（%d）" % (g["label"], len(fs)), "", g["what"], ""]
        by = collections.OrderedDict()
        for f in fs:
            by.setdefault(f["check"], []).append(f)
        for chk, lst in by.items():
            c = C["checks"].get(chk, {})
            L += ["### %s（%d）" % (c.get("label", chk), len(lst)), "", "建議：" + c.get("suggest", ""), "", "更新方法：", ""]
            L += ["%d. %s" % (i + 1, x) for i, x in enumerate(c.get("fix", []))]
            L += ["", "| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |", "|---|---|---|---|---|"]
            for f in lst[:200]:
                t = f["title"].replace("|", "｜")
                if f["url"]:
                    t = "[%s](%s)" % (t.replace("[", "〔").replace("]", "〕"), f["url"].replace(" ", "%20").replace(")", "%29"))
                d = f["detail"].replace("|", "｜").replace("\n", "<br>")
                L.append("| %s%s | %s | %s<br><sub>%s</sub> | %s | %s |" % (SEV_LABEL[f["sev"]], "・新" if f["isNew"] else "", S["byCity"].get(f["city"], {}).get("name", ""), t, d, f["first"], (f["due"] + ("（逾期）" if f["overdue"] else "")) or "—"))
            L.append("")
    if rep["resolved"]:
        L += ["## 已解決（%d）" % len(rep["resolved"]), ""] + ["- %s" % r["title"] for r in rep["resolved"]]
    return "\n".join(L) + "\n"


def to_csv(rep):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["編號", "優先度", "檢測類別", "檢測項目", "網站", "縣市", "文資", "內容", "說明", "網址", "首次發現", "處理期限", "逾期", "本次新發現", "建議"])
    C = rep["catalog"]
    gl = {g["id"]: g["label"] for g in C["groups"]}
    for f in rep["findings"]:
        w.writerow([f["key"], SEV_LABEL[f["sev"]], gl.get(f["group"], ""), f["label"], rep["summary"]["bySite"].get(f["site"], {}).get("name", ""),
                    rep["summary"]["byCity"].get(f["city"], {}).get("name", ""), f["name"], f["title"], f["detail"], f["url"], f["first"], f["due"],
                    "是" if f["overdue"] else "", "是" if f["isNew"] else "", C["checks"].get(f["check"], {}).get("suggest", "")])
    return out.getvalue()
