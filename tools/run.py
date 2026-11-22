#!/usr/bin/env python3
"""文資網站健檢：執行檢測並產生報告。

用法：
  python3 tools/run.py                    # 每週檢測（預設）
  python3 tools/run.py --level monthly    # 每月完整檢測：文資局圖片全部檢查、姊妹站所有資料檔的連結也檢查
  python3 tools/run.py --only official,integrity   # 只跑指定項目：official、integrity、live、links、news
  python3 tools/run.py --offline          # 不連網路（只跑不需要網路的部分，測試用）

需要其他網站的 repo 放在本 repo 旁邊（例如 /home/user/Cultural_Heritage），或用環境變數 REPOS_DIR 指定它們的上層資料夾。
產生：reports/latest.json、latest.md、latest.csv、history/；state/ 記錄跨次檢測的追蹤狀態。
只讀取其他 repo，不會修改它們。
"""
import argparse, datetime, os, sys, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import cfg, finding, log  # noqa: E402
import check_integrity, check_links, check_live, check_news, check_official, inventory, report  # noqa: E402

MODS = [("official", check_official), ("integrity", check_integrity), ("live", check_live), ("links", check_links), ("news", check_news)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--level", default="weekly", choices=["weekly", "monthly"])
    ap.add_argument("--only", default="")
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    rules = cfg("rules")
    lv = rules["levels"][a.level]
    want = [x for x in (a.only.split(",") if a.only else lv["checks"]) if x]
    started = datetime.datetime.now()
    if not inventory.cities():
        raise SystemExit("找不到 Cultural_Heritage／Cultural_Heritage2 的 clone。請放在本 repo 旁邊，或設定 REPOS_DIR。")
    ctx = {"rules": rules, "level": a.level, "level_cfg": lv, "offline": a.offline, "ran": [], "events": []}
    F, stats = [], {}
    for name, mod in MODS:
        if name not in want:
            continue
        if a.offline and name in ("official", "news", "live"):
            continue
        log("== 檢測：", name)
        try:
            f, st = mod.run(ctx)
            F += f
            stats[name] = st
            ctx["ran"].append(name)
            log("   %d 項發現" % len(f), st if name != "links" else "")
        except Exception as e:  # 單一項目失敗不影響其他項目，但要在報告裡看得到
            traceback.print_exc()
            F.append(finding("SYS-ERROR", "high", "", "檢測項目「%s」執行失敗" % name, "%s: %s" % (type(e).__name__, str(e)[:300]), sub=name))
    ctx["ran"].append("system")
    rep = report.build(ctx, F, stats, started)
    S = rep["summary"]
    print("健檢完成 %s：高 %d、中 %d、低 %d、參考 %d｜新發現 %d、已解決 %d、逾期 %d" % (rep["meta"]["date"], S["high"], S["medium"], S["low"], S["info"], S["new"], S["resolved"], S["overdue"]))


if __name__ == "__main__":
    main()
