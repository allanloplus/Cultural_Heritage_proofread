# 文資網站健檢室

「[Allan Lo 和你逛文化](https://cultural.123hi.org/)」文資系列網站的**內容與連結檢測系統**。Allan 和阿拉蕾每週替全系列網站做一次健檢，把需要更新的地方列成清單，並附上建議與更新方法。

- 規劃設計：Allan Lo，https://www.123hi.org，2026 年 11 月
- 報告網頁：本 repo 的 `index.html`（開啟 GitHub Pages 後即可瀏覽，見〈第一次設定〉）
- 管理機制：[`docs/MECHANISM.md`](docs/MECHANISM.md)｜更新方法：[`docs/UPDATE-SOP.md`](docs/UPDATE-SOP.md)｜請 Claude 協助：[`docs/AI-REVIEW.md`](docs/AI-REVIEW.md)

## 檢測什麼

重點是兩個文資知識網站（[Cultural_Heritage](https://github.com/allanloplus/Cultural_Heritage)、[Cultural_Heritage2](https://github.com/allanloplus/Cultural_Heritage2)，22 個縣市、3,032 處有形文化資產、624 項無形文化資產、559 件古物），五個姊妹站一併檢查上線狀態與資料是否同步。

| 類別 | 找什麼 | 怎麼確認 |
|---|---|---|
| 📜 官方資料比對 | 官方新指定或登錄而網站未收錄、已廢止、升格、改名、開放時間異動、新公告 | 文化部文化資產局開放資料 12 類，逐筆比對 |
| 🔗 連結 | 失效、搬家；照片在維基共享資源被刪除（授權風險） | 全系列約 18,000 個不重複網址，依網站種類用開放資料、官方 API 或實際連線確認 |
| 🧩 內部一致性 | 資料對不起來、缺照片或語音檔、缺授權標示、網頁資料沒重新產生、姊妹站資料過期、疑似個資 | 讀各 repo 的資料檔 |
| 🌐 上線狀態 | 網頁打不開、GitHub Pages 部署失敗停在舊版、憑證快到期 | 連線到正式網站，與 repo 比對 |
| 📰 新聞線索 | 近期新聞提到網站收錄的文資（災損、修復完工、重新開放）、新的指定或登錄 | 關鍵字查新聞標題，比對文資名稱 |

每一筆發現有優先度（高 7 天、中 30 天、低 90 天、參考）、首次發現日與處理期限；解決後自動記入「已解決」。

## 怎麼用

1. **看報告**：打開報告網頁。Allan 和阿拉蕾會先播報這次的結果，下面是可篩選的待辦清單。
2. **判斷**：每一筆點開有說明、建議、更新方法。
   - 要更新 → 按「複製給 Claude 的修正指示」貼到 Claude 的工作階段，或照步驟自己改。
   - 不需處理 → 按「複製例外清單格式」，貼進 `config/ignore.json` 的 `items`，填上原因與到期日。
3. **更新**：修改主網站資料、重新產生網頁、開 PR 合併（步驟見 [`docs/UPDATE-SOP.md`](docs/UPDATE-SOP.md)）。
4. **確認**：下次健檢該筆自動消失。想立刻確認：GitHub → Actions →「文資網站健檢」→ Run workflow。

也可以直接讀 [`reports/latest.md`](reports/latest.md)，或用 Excel 開 [`reports/latest.csv`](reports/latest.csv)。

## 排程

`.github/workflows/check.yml`：

| 檢測 | 時間（臺灣時間） | 差別 |
|---|---|---|
| 每週 | 每週一 03:17 | 文資局圖片輪流查 300 張 |
| 每月完整 | 每月 1 日 04:47 | 文資局圖片全部查；姊妹站所有資料檔的連結也查 |
| 手動 | 隨時 | Actions 頁面按 Run workflow，可選等級 |

檢測完自動把報告寫回本 repo。有**高優先度的新發現**，或**逾期件數比上次多**時，自動開一個 Issue（GitHub 會寄信通知）。排程只取出各 repo 的文字檔，不下載語音與照片。不需要任何密碼或金鑰。

## 第一次設定

1. **預設分支**：把本 repo 的預設分支設為 `main`（排程與 GitHub Pages 都看預設分支）。
2. **GitHub Pages**：Settings → Pages → Source 選 **Deploy from a branch**，Branch 選 `main`、資料夾 `/ (root)`。報告網頁網址會是 `https://allanloplus.github.io/Cultural_Heritage_proofread/`；要用自訂網域（例如 `cultural-check.123hi.org`）的話，在 DNS 加 CNAME 後於同一頁設定。
3. **Actions 權限**：Settings → Actions → General → Workflow permissions 選 **Read and write permissions**（讓排程能寫回報告）。
4. **試跑**：Actions →「文資網站健檢」→ Run workflow。

報告網頁設了 `noindex`，不會被搜尋引擎收錄；repo 是公開的，報告本身任何人都看得到，所以報告不會寫出完整的個人資料。

## 在本機或 Claude 工作階段執行

把其他 repo 放在本 repo 旁邊（或用環境變數 `REPOS_DIR` 指定它們的上層資料夾），只需要 Python 3.9 以上，不用安裝任何套件：

```bash
python3 tools/run.py                              # 每週檢測
python3 tools/run.py --level monthly              # 每月完整檢測
python3 tools/run.py --only official,integrity    # 只跑指定項目：official、integrity、live、links、news
python3 -m http.server 8000                       # 本機看報告網頁：http://localhost:8000/
```

第一次下載文資局開放資料約需 1～10 分鐘（古蹟、歷史建築、古物三個檔各 6～12 MB，伺服器較慢），存在 `.cache/`（不進版控）。

## 檔案

| 檔案 | 內容 |
|---|---|
| `index.html`、`assets/` | 報告網頁（Allan 與阿拉蕾播報、待辦清單、各縣市、檢測項目、管理機制） |
| `tools/run.py` | 主程式：依等級執行各項檢測並產生報告 |
| `tools/check_official.py` | 官方資料比對 |
| `tools/check_links.py` | 連結 |
| `tools/check_integrity.py` | 內部一致性 |
| `tools/check_live.py` | 上線狀態 |
| `tools/check_news.py` | 新聞線索 |
| `tools/report.py` | 追蹤首次發現日、逾期、已解決，套用例外清單，產生 JSON／Markdown／CSV 與角色播報 |
| `tools/summary.py` | Actions 執行摘要與 Issue 內文 |
| `tools/gen_docs.py` | 由 `config/checks.json` 產生 `docs/UPDATE-SOP.md` |
| `config/sites.json` | 受檢網站清單 |
| `config/rules.json` | 規則：處理期限、各等級的檢測範圍、略過的網域、新聞關鍵字 |
| `config/checks.json` | 檢測項目目錄：每個項目的名稱、建議、更新步驟（報告網頁與手冊共用） |
| `config/ignore.json` | 例外清單（不需處理的發現，含原因與到期日） |
| `reports/` | 最新報告（`latest.*`）與歷次報告（`history/`） |
| `state/` | 跨次檢測的追蹤狀態（首次發現日、官方公告基準、連結連續失敗次數、事件） |
| `docs/` | 管理機制、更新方法手冊、請 Claude 協助的提示詞 |

## 常見調整

| 想做的事 | 改哪裡 |
|---|---|
| 新增一個姊妹站 | `config/sites.json` 加一筆；`.github/workflows/check.yml` 的 repo 清單加上名稱 |
| 某個網站老是擋自動檢查 | `config/rules.json` 的 `links.manual_hosts`（只統計、不檢查）或 `skip_hosts`（完全略過） |
| 調整處理期限 | `config/rules.json` 的 `sla_days` |
| 增減新聞關鍵字、關閉新聞線索 | `config/rules.json` 的 `news.queries`、`news.enabled` |
| 修改某類問題的建議或更新步驟 | `config/checks.json`，再執行 `python3 tools/gen_docs.py` |
| 某一筆確定不用處理 | `config/ignore.json` |

## 網路禮儀

- 所有請求使用固定的 User-Agent（只含本專案網址，不含個人資訊）。
- 同一網站的請求之間固定間隔；回應 429 或 403 時不重複衝撞，列為「未能確認」等下次。
- 新聞線索只取標題、來源、日期與連結，不抓取、不轉載內文；每次檢測每組關鍵字只查一次。

---

Copyright © 2026 Allan Lo. 角色圖檔與程式碼版權所有；檢測引用的第三方資料依各自授權。
