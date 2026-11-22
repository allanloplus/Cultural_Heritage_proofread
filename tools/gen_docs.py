#!/usr/bin/env python3
"""由 config/checks.json 產生 docs/UPDATE-SOP.md（更新方法手冊）。改了 checks.json 之後執行一次。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, cfg

SEV_NOTE = {"OFF-NEW": "高", "OFF-GONE": "高", "OFF-ANN": "中（廢止為高）", "OFF-FIELD": "類別＝高；名稱、開放時間、所有權、官方頁網址＝中；地址、座標、代表圖＝低",
            "ICH-NEW": "中", "ICH-GONE": "高", "ANT-LEVEL": "高", "ANT-GONE": "低", "ANT-NEW": "低", "LNK-BROKEN": "重點網站＝高；其他＝中", "LNK-REDIRECT": "低（官方頁網址不同＝中）",
            "LNK-COMMONS": "高", "LNK-OFFIMG": "低", "LNK-UNSURE": "參考", "INT-CONTENT": "高", "INT-IMG": "中", "INT-AUDIO": "中（缺單一景點語音＝低）", "INT-REF": "中", "INT-BUILD": "高", "INT-COUNT": "低",
            "INT-DEEPLINK": "中", "INT-STALE": "中", "INT-PII": "中", "LIVE-DOWN": "高", "LIVE-DRIFT": "中", "LIVE-CERT": "中（7 天內到期＝高）", "NEWS-SITE": "參考", "NEWS-NEW": "參考",
            "SYS-SOURCE": "低～中", "SYS-ERROR": "高"}


def main():
    C = cfg("checks")
    L = ["# 更新方法手冊", "",
         "> 本檔由 `tools/gen_docs.py` 依 `config/checks.json` 產生，請改 `checks.json` 後重新產生，不要直接改這裡。", "",
         "健檢報告的每一筆發現都屬於下面某一個檢測項目。這裡列出每個項目的意思、建議與更新步驟。",
         "步驟裡的指令都在**主網站 `Cultural_Heritage`** 執行（第二網站的縣市資料夾在 `Cultural_Heritage2`，工具會自動寫到那裡）；完整規則見主網站的作業手冊 `tools/newcity/README.md`。", "",
         "## 共通原則", "",
         "1. **先查證再改**：以國家文化資產網與主管機關公告為準。新聞與維基百科只當線索。",
         "2. **只改資料檔**：改 `<縣市>/data/*.json`，不要手動改 `index.html`、`js/data.js`、`audio/cues.js`（它們由工具產生）。",
         "3. **id 不要改**：景點 id 一旦上線就固定，姊妹站與訪查紀錄都用它對應。",
         "4. **改完要重新產生**：`python3 tools/build_data.py` → 有改對話就 `python3 tools/gen_audio.py` → `python3 tools/build_search.py`。",
         "5. **姊妹站跟著更新**：新增、移除、改名、改類別之後，依序重建文資達人訪查、地圖集、鐵道版、鄉鎮卡、海拔版。",
         "6. **用 PR 留紀錄**：每次更新開 PR，內文貼上對應的健檢編號。第二網站的縣市先合併 `Cultural_Heritage2`，再合併 `Cultural_Heritage`。",
         "7. **不需處理的要留下理由**：記在本 repo 的 `config/ignore.json`（原因、決定的人、到期日）。", ""]
    for g in C["groups"]:
        L += ["## %s %s" % (g["icon"], g["label"]), "", g["what"], ""]
        for code, c in C["checks"].items():
            if c["group"] != g["id"]:
                continue
            L += ["### %s　`%s`" % (c["label"], code), "", "- 優先度：%s" % SEV_NOTE.get(code, ""), "- 建議：%s" % c["suggest"], "", "更新步驟：", ""]
            L += ["%d. %s" % (i + 1, s) for i, s in enumerate(c["fix"])]
            L.append("")
    open(os.path.join(ROOT, "docs", "UPDATE-SOP.md"), "w", encoding="utf-8").write("\n".join(L))
    print("wrote docs/UPDATE-SOP.md")


if __name__ == "__main__":
    main()
