#!/usr/bin/env python3
"""把 reports/latest.json 整理成短摘要（給 GitHub Actions 的執行摘要與 Issue 用）。
  python3 tools/summary.py            # 執行摘要
  python3 tools/summary.py --issue    # Issue 內文；沒有高優先度的新發現、逾期件數也沒有比上次多時，不輸出任何東西
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPORTS, load

SEV = {"high": "高", "medium": "中", "low": "低", "info": "參考"}


def esc(s):
    """報告裡有外部文字（新聞標題等），放進 Markdown 前把會變成連結、提及或格式的符號換掉。"""
    for a, b in (("|", "｜"), ("[", "〔"), ("]", "〕"), ("<", "＜"), (">", "＞"), ("@", "＠"), ("`", "'"), ("\n", " ")):
        s = s.replace(a, b)
    return s


def main():
    r = load(os.path.join(REPORTS, "latest.json"))
    S, M = r["summary"], r["meta"]
    issue = "--issue" in sys.argv
    new_high = [f for f in r["findings"] if f["sev"] == "high" and (f["isNew"] or S["firstRun"])]
    hot = new_high + [f for f in r["findings"] if f["overdue"] and f not in new_high]
    hist = load(os.path.join(REPORTS, "history", "index.json"), [])
    prev_over = hist[-2]["overdue"] if len(hist) > 1 else 0
    if issue and not new_high and S["overdue"] <= prev_over:
        return  # 沒有高優先度的新發現，逾期件數也沒有增加：不重複開 Issue
    L = ["## 文資網站健檢 %s" % M["date"], "",
         "| 高 | 中 | 低 | 參考 | 新發現 | 已解決 | 逾期 |", "|---|---|---|---|---|---|---|",
         "| %d | %d | %d | %d | %d | %d | %d |" % (S["high"], S["medium"], S["low"], S["info"], S["new"], S["resolved"], S["overdue"]), ""]
    if hot:
        L += ["### 需要優先處理（%d）" % len(hot), ""]
        for f in hot[:40]:
            city = S["byCity"].get(f["city"], {}).get("name", "")
            L.append("- **%s**｜%s%s%s　`%s`" % (SEV[f["sev"]], (city + "｜") if city else "", esc(f["title"]), "（逾期，首次發現 %s）" % f["first"] if f["overdue"] else "", f["key"]))
        if len(hot) > 40:
            L.append("- …另有 %d 項" % (len(hot) - 40))
        L.append("")
    L += ["完整報告：網頁版 `index.html`（GitHub Pages）、[reports/latest.md](../blob/HEAD/reports/latest.md)、[reports/latest.csv](../blob/HEAD/reports/latest.csv)",
          "更新方法：[docs/UPDATE-SOP.md](../blob/HEAD/docs/UPDATE-SOP.md)"]
    print("\n".join(L))


if __name__ == "__main__":
    main()
