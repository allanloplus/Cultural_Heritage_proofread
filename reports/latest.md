# 文資網站健檢報告　2026-11-22

- 檢測等級：每週｜執行項目：official、integrity、live、links、news、system｜耗時 259 秒
- 範圍：22 個縣市、3,032 處有形文化資產、624 項無形文化資產、559 件古物、11,315 個不重複網址
- 網頁版報告（可篩選）：`index.html`｜試算表：`reports/latest.csv`

## 摘要

| 優先度 | 件數 | 處理期限 |
|---|---|---|
| 高 | 2 | 7 天內 |
| 中 | 59 | 30 天內 |
| 低 | 30 | 90 天內 |
| 參考 | 32 | 看過即可 |

本次新發現 0 項｜已解決 0 項｜逾期 0 項｜列為例外 0 項

## 各網站

| 網站 | 狀態 | 高 | 中 | 低 | 參考 |
|---|---|---|---|---|---|
| [文資知識網站（第一網站）](https://cultural.123hi.org/) | 需處理 | 2 | 30 | 17 | 12 |
| [文資知識網站（第二網站）](https://cultural2.123hi.org/) | 留意 | 0 | 29 | 10 | 14 |
| [文資達人訪查](https://cultural-visit.123hi.org/) | 良好 | 0 | 0 | 0 | 0 |
| [文資地圖集](https://cultural-atlas.123hi.org/) | 良好 | 0 | 0 | 0 | 0 |
| [鄉鎮文資性格卡](https://cultural-town.123hi.org/) | 良好 | 0 | 0 | 0 | 0 |
| [鐵道文資](https://cultural-rail.123hi.org/) | 良好 | 0 | 0 | 0 | 0 |
| [從海口到山頂](https://cultural-ascent.123hi.org/) | 良好 | 0 | 0 | 0 | 3 |

## 官方資料比對（74）

與文化部文化資產局開放資料逐筆比對：有沒有新指定或登錄、廢止、升格、改名、新公告。

### 古物等級不同（1）

建議：以官方為準（一般古物、重要古物、國寶）。升級是值得在介紹裡提的事。

更新方法：

1. 修改 data/ich.json 該展示點 antiquities 裡這件古物的 level 與 registered。
2. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。
3. 重建文資達人訪查的資料（build_index.py）。
4. 各 repo 開 PR 合併到 main；第二網站的縣市先合併 Cultural_Heritage2，再合併 Cultural_Heritage。合併後確認 GitHub Pages 部署成功。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 高 | 高雄市 | 古物「台灣關地界碑」的等級與官方不同<br><sub>網站：重要古物<br>官方：一般古物（公告 2018-09-28）<br>展示點：高雄市立歷史博物館</sub> | 2026-11-22 | 2026-11-29 |

### 官方新增，網站未收錄（7）

建議：確認是否為新指定／登錄的文資。是的話新增到該縣市；若只是官方重新編案（網站已有同一處），加到例外清單。

更新方法：

1. 到國家文化資產網打開這筆，確認名稱、類別、地址、公告日期。
2. 在該縣市 data/sites-official.json 新增一筆（欄位照同檔其他筆；id 用「行政區拼音-名稱拼音」，定了就不要再改）。
3. 在 data/sites-content.json 寫介紹、雙人對話與測驗（規格見主網站 tools/newcity/SPEC.md，寫完用 tools/newcity/validate.py 檢查）。
4. 找授權清楚的照片：python3 tools/newcity/images.py <縣市> <資料夾>，再 python3 tools/fetch_images.py <資料夾>。
5. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。
6. 執行 python3 tools/gen_audio.py 產生新景點的語音。
7. 更新 assets/js/cities.js 與 README 裡的數量。
8. 依序重建姊妹站資料：文資達人訪查 build_index.py → 地圖集 build_sites.py → 鐵道版 build.py → 鄉鎮卡 build.py → 海拔版 build.py。
9. 各 repo 開 PR 合併到 main；第二網站的縣市先合併 Cultural_Heritage2，再合併 Cultural_Heritage。合併後確認 GitHub Pages 部署成功。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 高 | 澎湖縣 | [官方有「望安花宅」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/groupsOfBuildings/20061227000001)<br><sub>類別：聚落建築群｜登錄縣市：澎湖縣｜案號：20061227000001<br>公告：2018-06-11 變更/修正 府授文資字第10737016332號；2006-12-27 指定/登錄 府民禮字第09505007772號</sub> | 2026-11-22 | 2026-11-29 |
| 中 | 彰化縣 | [官方有「鹿港天后宮」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20191128000001)<br><sub>注意：網站已有同名的文資（案號不同），可能是同一處文資有兩種身分（例如古蹟＋文化景觀），或官方重新編案。<br>類別：縣(市)定古蹟｜登錄縣市：彰化縣｜案號：20191128000001<br>公告：2019-07-31 變更/修正 府授文資字第1080245853A號；1985-11-27 指定/登錄 臺內民字第357272號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 嘉義縣 | [官方有「阿里山林業暨鐵道文化景觀」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/culturalLandscape/20100505000001)<br><sub>注意：網站已有同名的文資（案號不同），可能是同一處文資有兩種身分（例如古蹟＋文化景觀），或官方重新編案。<br>類別：文化景觀｜登錄縣市：嘉義縣｜案號：20100505000001<br>公告：2010-04-27 指定/登錄 府文資字第0990072259號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 南投縣 | [官方有「Sbayan泰雅民族起源地」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/culturalLandscape/20160818000001)<br><sub>注意：網站已有同名的文資（案號不同），可能是同一處文資有兩種身分（例如古蹟＋文化景觀），或官方重新編案。<br>類別：文化景觀｜登錄縣市：南投縣｜案號：20160818000001<br>公告：2016-08-26 變更/修正 府授文資字第1050176493號；2016-08-18 指定/登錄 府授文資字第10501646381號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 新北市 | [官方有「新莊樂生療養院」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20090907000001)<br><sub>注意：網站已有同名的文資（案號不同），可能是同一處文資有兩種身分（例如古蹟＋文化景觀），或官方重新編案。<br>類別：歷史建築｜登錄縣市：新北市｜案號：20090907000001<br>公告：2010-03-26 變更/修正 北府文資字第0990003591號；2009-09-07 指定/登錄 北府文資字第09800123211號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺北市 | [官方有「建國啤酒廠」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20061123000003)<br><sub>注意：網站已有同名的文資（案號不同），可能是同一處文資有兩種身分（例如古蹟＋文化景觀），或官方重新編案。<br>類別：歷史建築｜登錄縣市：臺北市｜案號：20061123000003<br>公告：2021-11-04 變更/修正 北市文化文資字第11030409651號；2006-11-23 指定/登錄 府文化二字第09530338800號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 雲林縣 | [官方有「麥寮拱範宮」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20210625000013)<br><sub>注意：網站已有同名的文資（案號不同），可能是同一處文資有兩種身分（例如古蹟＋文化景觀），或官方重新編案。<br>類別：縣(市)定古蹟｜登錄縣市：雲林縣｜案號：20210625000013<br>公告：2012-07-18 指定/登錄 文資局蹟字第10130060062號；2006-12-22 指定/登錄 府文資字第0952401211；2006-06-20 指定/登錄 府文資字第0952400503號</sub> | 2026-11-22 | 2026-12-22 |

### 欄位與官方不同（34）

建議：名稱、類別、官方頁網址以官方為準；開放時間改了要同時看介紹裡的「開放資訊」；所有權由公有變私有時，確認詳情頁已隱藏門牌。

更新方法：

1. 直接修改該縣市 data/sites-official.json 對應欄位（name、category、address、lat、lng、open、officialImg、url、ownership）。
2. 開放時間：一併檢查 sites-content.json 的 openNote 是否矛盾。
3. 名稱或類別：檢查 sites-content.json 的介紹與對話是否沿用舊稱；類別改變時確認 config.json 的 categories 有這個類別。
4. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。
5. 名稱或類別有改時：依序重建姊妹站資料：文資達人訪查 build_index.py → 地圖集 build_sites.py → 鐵道版 build.py → 鄉鎮卡 build.py → 海拔版 build.py。
6. 各 repo 開 PR 合併到 main；第二網站的縣市先合併 Cultural_Heritage2，再合併 Cultural_Heritage。合併後確認 GitHub Pages 部署成功。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 中 | 彰化縣 | [「南瑤宮」的開放時間與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/19880425000001)<br><sub>網站：上午6時至下午9時30分<br>官方：南瑤宮廟區每日開放時間為上午6時至下午9時30分；南瑤宮媽祖文物館開放時間為上午 8時30分至 下午5時</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 彰化縣 | [「鹿港公會堂」的開放時間與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20000714000003)<br><sub>網站：週二至週日，上午10時至下午6時，週一及國定假日休館。<br>官方：週二至週五上午9時至下午5時；週六、週日上午10時至下午6時；週一及國定假日休館。</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 彰化縣 | [「鹿港敬義園紀念碑」的開放時間與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20070515000002)<br><sub>網站：全天候開放（鹿港公園內）。<br>官方：全天候開放（鹿港鎮立圖書館前公園內）。</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 嘉義市 | [「原南國運送店」的所有權與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20230509000004)<br><sub>網站：私有<br>官方：公有（影響私人宅第是否隱藏門牌）</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 嘉義縣 | [無形文資「鄒族戰祭（mayasvi）」的名稱與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20110825000008)<br><sub>網站：鄒族戰祭（mayasvi）<br>官方：鄒族mayasvi</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 新竹市 | [「新竹市消防博物館」的開放時間與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20181224000001)<br><sub>網站：工程施工中，暫休館至114年12月31日止<br>官方：113年起進行修復工程，自115年8月7日起恢復對外開放，目前開放1樓展示區參觀及防災設施體驗，2樓及鐘樓暫不開放，供民眾參觀消防歷史文物及體驗防災設施。</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 花蓮縣 | [「八通關古道」的所有權與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/19870417000001)<br><sub>網站：不明<br>官方：私有（影響私人宅第是否隱藏門牌）</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 花蓮縣 | [「檢察長宿舍」的開放時間與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20080723000002)<br><sub>網站：營業時間為12:00~21:00，每週四為公休日<br>官方：開放時間： 每週四至週二 10:00－18:00<br>休館日： 每週三<br>參觀方式： 外部空間開放民眾參觀，內部空間須事先預約。</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 花蓮縣 | [「美崙溪畔日式宿舍」的開放時間與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20050223000001)<br><sub>網站：目前修復工程進行中。<br>官方：委外營業中，營業時間：星期一~五：10：00~22：00</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 花蓮縣 | [「美崙溪畔日式宿舍」的開放時間與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20050329000003)<br><sub>網站：目前修復工程進行中。<br>官方：星期一~五：10：00~22：00</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 金門縣 | [「瓊林一門三節坊」的開放時間與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/19881111000004)<br><sub>網站：全天候<br>官方：（空）</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 南投縣 | [「八通關古道」的所有權與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/19870417000001)<br><sub>網站：不明<br>官方：私有（影響私人宅第是否隱藏門牌）</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺中市 | [「臺中市第四市場」的開放時間與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20140217000001)<br><sub>網站：1F咖啡館訂購餐點：0975-878061（週一到週二、週四到週日 10:00-18:00，週三店休）<br><br>2F辦公室電話： (04)2215-1977（週一至週五 09:30 ~ 18:00）<br>官方：1F咖啡館訂購餐點：0975-878061（週一到週二、週四到週日 10:00-18:00，週三店休）<br><br>2F辦公室電話： (04)2215-1977（週一至週五 09:30 ~ 18:00）<br><br>客服信箱：2021fourmarket@gmail.com</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺中市 | [「頭汴坑警察官吏派出所」的開放時間與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20200203000001)<br><sub>網站：尚未修復完成，暫不開放。<br>官方：週二至週日 9:00 ~12:00 & 13:00~17:00 (中午未開放)<br>星期一、國定假日固定休館</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺北市 | [無形文資「漆線」的名稱與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20130226000004)<br><sub>網站：漆線<br>官方：漆線-顏金益</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺東縣 | [無形文資「阿美族馬蘭複音歌謠（Macacadaay）」的名稱與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalPerformingart/20210419000001)<br><sub>網站：阿美族馬蘭複音歌謠（Macacadaay）<br>官方：阿美族馬蘭Macacadaay</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 雲林縣 | [無形文資「傳統建築彩繪」的名稱與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20180606000006)<br><sub>網站：傳統建築彩繪<br>官方：傳統彩繪</sub> | 2026-11-22 | 2026-12-22 |
| 低 | 新竹縣 | [「竹東長春醫院」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20240509000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2024-04-29/463395d4-26f4-4c68-b9f5-fcdd3acbe069/代表照片.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-17/ab350fa4-e1b7-4519-aed1-a14c2d2e7d7e/竹東長春醫院-正面-2.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 南投縣 | [「Sbayan泰雅民族起源地」的座標與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/culturalLandscape/20250725000003)<br><sub>網站：24.11649, 121.15587<br>官方：24.02864, 121.14441（相差約 9837 公尺）</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 新北市 | [「新莊樂生療養院」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/culturalLandscape/20090907000002)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2026-08-26/0b03215f-93e1-4f06-84e6-6b74bd66bd01/樂生療養院_全區空拍圖_01.jpg<br>官方：https://data.boch.gov.tw/old_upload/_upload/Assets_new/cultural_tourism/234/photo/新莊樂生療養院.JPG</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 臺中市 | [「頭汴坑警察官吏派出所」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20200203000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2020-02-03/085204a3-8589-4b95-b13f-0ad742b54cc2/IMG_3637.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-18/9651826e-f1c1-47fa-9371-9ec1b60d3770/20261013-07.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 臺南市 | [「烏山頭水庫暨嘉南大圳水利系統」的地址與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/culturalLandscape/20091005000001)<br><sub>網站：官田區烏山頭水庫位於台南市官田區及六甲區，灌溉設施的主要輸水幹線位於官田區、六甲區、柳營區、東山區、後壁區、白河區等地，灌溉範圍可達雲嘉南地區。<br>官方：烏山頭水庫位於台南市官田區及六甲區，灌溉設施的主要輸水幹線位於官田區、六甲區、柳營區、東山區、後壁區、白河區等地，灌溉範圍可達雲嘉南地區。</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「利澤簡永安宮」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20060921000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2021-07-29/feee2087-74a7-49fe-a917-cb1c7264bd88/永安宮代表圖.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-12/e93c34d1-9d18-4a2a-aa6c-6d38656eb4e8/利澤簡永安宮01.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「宜蘭國民小學科學教育中心」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20201020000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2021-11-11/293c924b-a0fb-4d93-8b2d-a905c9e4f53e/宜蘭國民小學科學教育中心_A990190.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-17/f22c1796-88f1-47ac-9622-021121840126/宜蘭國民小學科學教育中心03.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「宜蘭大學民權日式眷舍」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20071009000004)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2021-07-26/3bca6abc-6500-4e10-9979-b34f88b1fcbb/宜蘭大學民權日式眷舍2.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-13/7007a57d-647a-4062-9aea-aa6a313af4b7/宜蘭大學民權宿舍05.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「宜蘭測候所宜蘭飛行場出張所」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20020621000008)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2021-05-10/02812821-a525-4222-afd1-4f3201832c1f/H16宜蘭測候所宜蘭飛行場出張所02.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-12/6e3eed4b-388f-4be6-8b84-4720ca6d5a32/宜蘭測候所宜蘭飛行場出張所01.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「寒溪神社遺跡」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20120730000001)<br><sub>網站：https://data.boch.gov.tw/old_upload/_upload/Assets_new/building/37011/photo/24bc76a7-ce72-4ad0-86d4-1a198c9051f3.JPG<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-12/4db9e530-0dd0-48b5-b512-c643df13e8c7/寒溪神社遺跡02.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「礁溪協天廟老戲臺」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20260616000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2026-06-16/de1aac26-be27-415e-8285-8c53be574ebf/礁溪老戲臺-木棟架3.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-17/e99eb905-7585-463b-8072-465f834459f9/礁溪協天廟老戲臺02.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「第一商業銀行宜蘭分行」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20150302000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2021-11-03/433a1efc-e3b6-4d5c-8688-fcb0cc30fcb7/第一商業銀行宜蘭分行_A999398.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-12/b92b1a06-eb93-49cc-a02e-da794d497f02/第一商業銀行宜蘭分行01.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「羅東林區管理處處長宿舍」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20120207000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2024-05-24/218c148a-47c2-470e-93c8-50081898f11d/羅東林管處場長宿舍_A998261.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-17/ac625419-2a59-4a27-91c4-4d570c076726/羅東林區管理處處長宿舍01.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「蘇澳扇形鐵道暨轉車台」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20260605000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2026-06-05/1532b5a9-0584-4ec4-98d6-7f9d13b885ab/108蘇澳扇形鐵道暨轉車台.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-17/01ab30ed-9a56-48b9-bcab-a553a6d1b043/蘇澳扇形鐵道暨轉車台09.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「蘇澳砲台山及金刀比羅社遺蹟」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20201022000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2021-11-04/33214330-2a92-413b-8e22-c9cac92f4f90/蘇澳砲台山及金刀比羅社遺蹟_A998163.jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-12/419bf2d5-2443-4ce8-801a-3cd187039871/蘇澳砲台山及神社遺跡10.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「農糧署宜蘭市公糧倉庫群」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/historicalBuilding/20250829000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2025-11-07/f5782da3-702c-42f8-ab7a-7929bf41cc32/農糧署宜蘭市公糧倉庫群(4).jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-17/5730d932-293b-4f5c-829f-2cbee8031c53/農糧署宜蘭市公糧倉庫群10.jpg</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 宜蘭縣 | [「開蘭進士楊士芳旗杆座」的官方代表圖與官方資料不同](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/20071009000001)<br><sub>網站：https://data.boch.gov.tw/upload/representImageFile/2021-03-18/5db92bb1-1815-4ecd-a357-5cffd59aa4fa/開蘭進士楊士芳旗杆座(代表).jpg<br>官方：https://data.boch.gov.tw/upload/representImageFile/2026-11-12/d92ab24a-a33e-4b89-a24f-3a7443088844/開蘭進士楊士芳旗杆座08.jpg</sub> | 2026-11-22 | 2027-02-20 |

### 官方有的無形文資，網站未收錄（23）

建議：確認是否為新登錄項目。網站把同一項目的多位保存者合併成一筆時不用新增，加到例外清單即可。

更新方法：

1. 到國家文化資產網確認項目、保存者、登錄日期與是否仍有效（最後一筆公告是廢止的不用新增）。
2. 在該縣市 data/ich.json 的 items 新增一筆（規格見主網站 tools/newcity/SPEC.md），有固定地點就設 venueId 並在 venues 補展示點。
3. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。
4. 執行 python3 tools/gen_audio.py。
5. 更新 cities.js 與 README 的數量；重建文資達人訪查與鄉鎮卡的資料。
6. 各 repo 開 PR 合併到 main；第二網站的縣市先合併 Cultural_Heritage2，再合併 Cultural_Heritage。合併後確認 GitHub Pages 部署成功。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 中 | 新竹縣 | [官方有無形文資「新竹縣賽夏族矮靈祭（pasta'ay）」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20100108000001)<br><sub>類別：民俗｜主管機關：新竹縣政府｜案號：20100108000001<br>公告：2010-01-14 指定/登錄 府文獻字第0990103066號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 花蓮縣 | [官方有無形文資「噶瑪蘭香蕉絲編織工藝」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20151026000005)<br><sub>類別：傳統工藝｜主管機關：花蓮縣政府｜案號：20151026000005<br>公告：2015-10-26 指定/登錄 府文資字第1040206148A</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 花蓮縣 | [官方有無形文資「阿美族Fakong部落ilisin（豐年祭)」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20140428000004)<br><sub>類別：民俗｜主管機關：花蓮縣政府｜案號：20140428000004<br>公告：2014-05-28 指定/登錄 府文資字第1030096982A號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 高雄市 | [官方有無形文資「南管」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalPerformingart/20141217000001)<br><sub>類別：傳統表演藝術｜主管機關：高雄市政府｜案號：20141217000001<br>公告：2014-12-17 指定/登錄 高市府文博字第10370438200號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 高雄市 | [官方有無形文資「木雕」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20080516000004)<br><sub>類別：傳統工藝｜主管機關：高雄市政府｜案號：20080516000004<br>公告：2008-05-16 指定/登錄 高市府文中字第0970024887號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 金門縣 | [官方有無形文資「四月十二日迎城隍」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20111215000006)<br><sub>類別：民俗｜主管機關：金門縣政府｜案號：20111215000006<br>公告：2011-12-15 指定/登錄 府文資字第 1000092059號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 苗栗縣 | [官方有無形文資「賽夏族巴斯達隘（矮靈祭）」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20090109000003)<br><sub>類別：民俗｜主管機關：苗栗縣政府｜案號：20090109000003<br>公告：2009-01-09 指定/登錄 府文資字第0987500293號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 南投縣 | [官方有無形文資「布農族八部合音(pasibutbut祈禱小米豐收歌)」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalPerformingart/20090423000005)<br><sub>類別：傳統表演藝術｜主管機關：南投縣政府｜案號：20090423000005<br>公告：2017-12-06 變更/修正 府授文資字第10702661491號；2009-04-23 指定/登錄 府授文資字第09800916774號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 南投縣 | [官方有無形文資「邵族年祭」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20220623000001)<br><sub>類別：民俗｜主管機關：南投縣政府｜案號：20220623000001<br>公告：2018-12-06 指定/登錄 府授文資字第10702682761號；2009-04-23 指定/登錄 府授文資字第09800916773號函</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 新北市 | [官方有無形文資「傳統彩繪」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20210423000001)<br><sub>類別：傳統工藝｜主管機關：新北市政府｜案號：20210423000001<br>公告：2019-09-25 變更/修正 新北府文資字第10817548413號；2016-11-22 指定/登錄 新北府文資字第1052187094號；2013-09-26 指定/登錄 北府文資字第1022699875號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 新北市 | [官方有無形文資「製鼓工藝」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20100526000004)<br><sub>類別：傳統工藝｜主管機關：新北市政府｜案號：20100526000004<br>公告：2010-05-26 變更/修正 北府文資字第090006944號；2010-01-18 廢止/撤銷 北府文資字第0990000616號；2009-08-27 指定/登錄 北府文資字第0980011680號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺南市 | [官方有無形文資「保西代天府王醮暨遶境」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20190513000004)<br><sub>類別：民俗｜主管機關：臺南市政府｜案號：20190513000004<br>公告：2019-04-08 指定/登錄 府文資處字第1080390904B號  </sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺南市 | [官方有無形文資「木工藝」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20140630000004)<br><sub>類別：傳統工藝｜主管機關：臺南市政府｜案號：20140630000004<br>公告：2016-01-06 變更/修正 府文資處字第1041267356B號；2014-06-30 指定/登錄 府文資處字第1030570896C號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺南市 | [官方有無形文資「東山吉貝耍夜祭」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20080627000003)<br><sub>類別：民俗｜主管機關：臺南市政府｜案號：20080627000003<br>公告：2013-10-04 指定/登錄 文資局傳字第10220115721號；2008-06-27 指定/登錄 府文資字第0970141209號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺南市 | [官方有無形文資「歸仁仁壽宮王船醮典暨遶境」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20091008000001)<br><sub>類別：民俗｜主管機關：臺南市政府｜案號：20091008000001<br>公告：2009-10-08 指定/登錄 府文資字第0980242426號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺南市 | [官方有無形文資「結網」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20140630000005)<br><sub>類別：傳統工藝｜主管機關：臺南市政府｜案號：20140630000005<br>公告：2016-01-06 變更/修正 府文資處字第1041267356B號；2014-06-30 指定/登錄 府文資處字第1030570896D號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺南市 | [官方有無形文資「關廟山西宮遶境暨王醮祭典」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20090115000002)<br><sub>類別：民俗｜主管機關：臺南市政府｜案號：20090115000002<br>公告：2009-01-15 指定/登錄 府文資字第0980014134號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺東縣 | [官方有無形文資「卑南族傳統織布技藝(tenun)」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20240229000001)<br><sub>類別：傳統工藝｜主管機關：臺東縣政府｜案號：20240229000001<br>公告：2024-02-23 指定/登錄 府文資字第1130037126號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺東縣 | [官方有無形文資「卑南族建和部落(Kasavakan)木雕」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20240112000001)<br><sub>類別：傳統工藝｜主管機關：臺東縣政府｜案號：20240112000001<br>公告：2023-11-29 變更/修正 府文資字第1120256174號；2023-01-12 指定/登錄 府文資字第1200007677號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺東縣 | [官方有無形文資「排灣族(大王部落)傳統刺繡」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20190905000001)<br><sub>類別：傳統工藝｜主管機關：臺東縣政府｜案號：20190905000001<br>公告：2019-06-03 指定/登錄 府文資字第1080116019號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺東縣 | [官方有無形文資「阿美族樹皮布工藝」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20261028000001)<br><sub>類別：傳統工藝｜主管機關：臺東縣政府｜案號：20261028000001<br>公告：2026-11-03 指定/登錄 府文資字第1150244852號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 宜蘭縣 | [官方有無形文資「纏花工藝(春仔花)」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/traditionalCraft/20100526000005)<br><sub>類別：傳統工藝｜主管機關：宜蘭縣政府｜案號：20100526000005<br>公告：2019-01-10 變更/修正 府文資字第1080000292C號；2010-05-26 指定/登錄 府文資字第0990003680號</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 雲林縣 | [官方有無形文資「馬鳴山五年千歲五年大科」，網站還沒有收錄](https://nchdb.boch.gov.tw/assets/advanceSearch/folklore/20180606000001)<br><sub>類別：民俗｜主管機關：雲林縣政府｜案號：20180606000001<br>公告：2019-08-01 指定/登錄 文授資局傳字第10830078293號；2015-09-15 指定/登錄 府文資二字第1047408522B號</sub> | 2026-11-22 | 2026-12-22 |

### 官方新公告（1）

建議：看公告內容。常見的是範圍變更、名稱修正、類別變更、保存者異動；只影響地籍範圍的通常不用改網站。

更新方法：

1. 打開官方頁，看最新一筆公告的說明。
2. 需要改的欄位直接改該縣市 data/sites-official.json（名稱、類別、announced）或 ich.json（保存者、哪裡看得到）。
3. 介紹文字若提到舊資訊，一併改 sites-content.json；改到雙人對話就要重跑 python3 tools/gen_audio.py。
4. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。
5. 不需要改網站的，在本 repo 的 config/ignore.json 記一筆並寫原因。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 中 | 花蓮縣 | [「八通關古道」有新的官方公告（變更/修正）](https://nchdb.boch.gov.tw/assets/advanceSearch/monument/19870417000001)<br><sub>公告：2026-11-11 變更/修正 文授資局蹟字第11530109691號<br>請到國家文化資產網看公告內容（範圍變更、名稱修正、保存者異動、廢止等），再決定網站介紹是否要改。</sub> | 2026-11-22 | 2026-12-22 |

### 古物對不到官方紀錄（8）

建議：先用關鍵字到國家文化資產網搜尋。只是名稱寫法不同就改成官方名稱；確定已廢止才移除。

更新方法：

1. 修改 data/ich.json 該古物的 name（改成官方全名）或移除。
2. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。
3. 各 repo 開 PR 合併到 main；第二網站的縣市先合併 Cultural_Heritage2，再合併 Cultural_Heritage。合併後確認 GitHub Pages 部署成功。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 低 | 彰化縣 | 古物「彰化聖廟「與天地參」匾」在官方開放資料找不到同名紀錄<br><sub>展示點：彰化孔子廟。可能是網站用了簡稱、官方改名，或已廢止。請到國家文化資產網確認名稱與等級。</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 嘉義市 | 古物「臺灣野球史」在官方開放資料找不到同名紀錄<br><sub>展示點：嘉義市交趾陶館（嘉義市立博物館3樓）。可能是網站用了簡稱、官方改名，或已廢止。請到國家文化資產網確認名稱與等級。</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 苗栗縣 | 古物「嚴禁差役藉端擾累碑」在官方開放資料找不到同名紀錄<br><sub>展示點：中港慈裕宮。可能是網站用了簡稱、官方改名，或已廢止。請到國家文化資產網確認名稱與等級。</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 澎湖縣 | 古物「澎湖天后宮「帡幪臺廈」匾」在官方開放資料找不到同名紀錄<br><sub>展示點：澎湖天后宮。可能是網站用了簡稱、官方改名，或已廢止。請到國家文化資產網確認名稱與等級。</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 臺北市 | 古物「北魏曹天度造九層千佛石塔」在官方開放資料找不到同名紀錄<br><sub>展示點：國立歷史博物館。可能是網站用了簡稱、官方改名，或已廢止。請到國家文化資產網確認名稱與等級。</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 臺北市 | 古物「排灣族望嘉舊社佳邏夫岸頭目家雙面祖先像石雕柱」在官方開放資料找不到同名紀錄<br><sub>展示點：國立臺灣大學人類學博物館。可能是網站用了簡稱、官方改名，或已廢止。請到國家文化資產網確認名稱與等級。</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 臺北市 | 古物「黃土水《南國》（水牛群像）」在官方開放資料找不到同名紀錄<br><sub>展示點：臺北市中山堂。可能是網站用了簡稱、官方改名，或已廢止。請到國家文化資產網確認名稱與等級。</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 臺北市 | 古物「黃土水《釋迦出山》」在官方開放資料找不到同名紀錄<br><sub>展示點：臺北市立美術館。可能是網站用了簡稱、官方改名，或已廢止。請到國家文化資產網確認名稱與等級。</sub> | 2026-11-22 | 2027-02-20 |


## 連結（10）

網站裡每一個對外連結是否還打得開、有沒有搬家；照片在維基共享資源是否還在。

### 連結失效（1）

建議：找新網址取代；找不到就改連到該機關首頁、網站時光機（web.archive.org）的存檔，或拿掉連結並保留出處文字。

更新方法：

1. 用瀏覽器打開確認真的失效（有些網站只擋自動檢查）。
2. 搜尋頁面標題找新網址。
3. 修改「出現在」列出的檔案（多半是 data/eras.json 的 sources 或 config.json）。
4. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。
5. 確認沒問題但檢測一直誤報的，加到 config/ignore.json。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 中 | 彰化縣 | [維基百科條目「半線」不存在](https://zh.wikipedia.org/wiki/半線)<br><sub>條目可能已改名或刪除，請搜尋新條目名稱後更新連結。<br>出現在：changhua-county/data/eras.json：sources.url</sub> | 2026-11-22 | 2026-12-22 |

### 連結已搬家（2）

建議：目前還能自動轉到新網址，不急；下次更新該縣市時順手改成新網址，避免日後轉址取消。

更新方法：

1. 把「出現在」列出的檔案裡的舊網址換成新網址。
2. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 低 | 連江縣 | [連結已搬家：matsucc.gov.tw/?p=3240](https://matsucc.gov.tw/?p=3240)<br><sub>新網址：https://matsucc.gov.tw/museum/%e6%9e%97%e7%be%a9%e5%92%8c%e5%b7%a5%e5%9d%8a/<br>出現在：lienchiang-county/data/eras.json：sources.url</sub> | 2026-11-22 | 2027-02-20 |
| 低 | 雲林縣 | [連結已搬家：www.nownews.com/news/20180822/2804421/](https://www.nownews.com/news/20180822/2804421/)<br><sub>新網址：https://www.nownews.com/news/2804421<br>出現在：yunlin-county/data/eras.json：sources.url</sub> | 2026-11-22 | 2027-02-20 |

### 連結未能確認（7）

建議：先不用處理。連續多次連不上才會升級成「連結失效」。

更新方法：

1. 想立刻確認的話，用瀏覽器打開看看。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 參考 |  | [連結本次未能確認：gic.wra.gov.tw/gis/gic/API/Google/DownLoad.aspx?fname=BASIN&filetyp…](https://gic.wra.gov.tw/gis/gic/API/Google/DownLoad.aspx?fname=BASIN&filetype=SHP)<br><sub>RemoteDisconnected: Remote end closed connection without response。可能只是對方暫時忙碌或擋掉自動檢查；連續 3 次才會列為失效。<br>出現在：README.md</sub> | 2026-11-22 | — |
| 參考 |  | [連結本次未能確認：gic.wra.gov.tw/gis/gic/API/Google/DownLoad.aspx?fname=RIVERLIN&file…](https://gic.wra.gov.tw/gis/gic/API/Google/DownLoad.aspx?fname=RIVERLIN&filetype=SHP)<br><sub>URLError: <urlopen error [Errno 104] Connection reset by peer>。可能只是對方暫時忙碌或擋掉自動檢查；連續 3 次才會列為失效。<br>出現在：README.md</sub> | 2026-11-22 | — |
| 參考 |  | [連結本次未能確認：www.tgos.tw/MDE/VirtualDir_TC/Product/9981ede9-584a-4470-8c5c-dbe57…](https://www.tgos.tw/MDE/VirtualDir_TC/Product/9981ede9-584a-4470-8c5c-dbe579d4ecb4/)<br><sub>HTTP 403。可能只是對方暫時忙碌或擋掉自動檢查；連續 3 次才會列為失效。<br>出現在：README.md</sub> | 2026-11-22 | — |
| 參考 | 屏東縣 | [連結本次未能確認：www.cultural.pthg.gov.tw/vipzone/Default.aspx](https://www.cultural.pthg.gov.tw/vipzone/Default.aspx)<br><sub>URLError: <urlopen error [Errno 104] Connection reset by peer>。可能只是對方暫時忙碌或擋掉自動檢查；連續 3 次才會列為失效。<br>出現在：pingtung-county/data/sites-official.json：open</sub> | 2026-11-22 | — |
| 參考 | 桃園市 | [連結本次未能確認：scft.taoyuancf.org.tw/](https://scft.taoyuancf.org.tw/)<br><sub>URLError: <urlopen error Tunnel connection failed: 502 Bad Gateway>。可能只是對方暫時忙碌或擋掉自動檢查；連續 3 次才會列為失效。<br>出現在：taoyuan-city/data/sites-official.json：open</sub> | 2026-11-22 | — |
| 參考 | 宜蘭縣 | [連結本次未能確認：www.moc.gov.tw/en/information_108_75034.html](https://www.moc.gov.tw/en/information_108_75034.html)<br><sub>HTTP 403。可能只是對方暫時忙碌或擋掉自動檢查；連續 3 次才會列為失效。<br>出現在：yilan-county/data/eras.json：sources.url</sub> | 2026-11-22 | — |
| 參考 | 雲林縣 | [連結本次未能確認：news.ltn.com.tw/news/politics/breakingnews/5499641](https://news.ltn.com.tw/news/politics/breakingnews/5499641)<br><sub>HTTP 403。可能只是對方暫時忙碌或擋掉自動檢查；連續 3 次才會列為失效。<br>出現在：yunlin-county/data/eras.json：sources.url</sub> | 2026-11-22 | — |


## 內部一致性（11）

資料之間對不對得起來、照片與語音檔在不在、網頁資料是否重新產生、姊妹站資料是否過期、有沒有不該出現的個資。

### 照片檔或授權資訊有問題（6）

建議：缺檔會讓網頁出現破圖；缺作者或授權標示是著作權風險，要補齊或換照片。

更新方法：

1. 缺檔：python3 tools/fetch_images.py <資料夾> 重新下載。
2. 缺授權資訊：到 images.json 的 page 連結查作者與授權後補上；查不到就換一張。
3. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 中 | 彰化縣 | 「彰化孔子廟」有照片缺少作者或授權標示<br><sub>檔案：彰化孔廟.JPG<br>缺少：作者。照片都要標示作者與授權；查不到就換一張。</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 新北市 | 「新莊樂生療養院」有照片缺少作者或授權標示<br><sub>檔案：Losheng Sanatorium Dorm.JPG<br>缺少：作者。照片都要標示作者與授權；查不到就換一張。</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 屏東縣 | 「竹田車站」有照片缺少作者或授權標示<br><sub>檔案：Jhutian station.JPG<br>缺少：作者。照片都要標示作者與授權；查不到就換一張。</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺中市 | 「臺鐵舊山線-大安溪鐵橋」有照片缺少作者或授權標示<br><sub>檔案：Old Mountain Railway Taiwan-Ta-an river-bridge-P1020654.JPG<br>缺少：作者。照片都要標示作者與授權；查不到就換一張。</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺中市 | 「路思義教堂」有照片缺少作者或授權標示<br><sub>檔案：The Luce Chapel 1.jpg<br>缺少：作者。照片都要標示作者與授權；查不到就換一張。</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺北市 | 「艋舺龍山寺」有照片缺少作者或授權標示<br><sub>檔案：Lungshan temple taipei taiwan.jpg<br>缺少：作者。照片都要標示作者與授權；查不到就換一張。</sub> | 2026-11-22 | 2026-12-22 |

### 疑似個人資料（5）

建議：多半來自官方開放資料的「開放時間」欄（預約聯絡人手機）。公開網站轉載個人手機有個資風險；建議改寫成「需預約，聯絡方式見官方頁」。機關代表號與官方信箱可保留並加到例外清單。

更新方法：

1. 修改該縣市 data/sites-official.json 的 open（或其他出現的欄位），拿掉個人姓名與手機。
2. 同步檢查 sites-content.json 的 openNote。
3. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。
4. 確認可保留的，加到 config/ignore.json 並寫原因。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 中 | 新竹縣 | 「新埔張氏家廟」的資料有疑似手機號碼：0912＊＊＊＊<br><sub>在 hsinchu-county/data/sites-official.json。公開網站不應轉載個人聯絡資料；確認是機關公開電話才保留。<br>前後文：…預約參觀 （預約請洽 : 張紹瑚先生0912＊＊＊＊）…</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺中市 | 「林懋陽故居」的資料有疑似手機號碼：0903＊＊＊＊<br><sub>在 taichung-city/data/sites-official.json。公開網站不應轉載個人聯絡資料；確認是機關公開電話才保留。<br>前後文：…0800-528-777（免付費） 0903＊＊＊＊  除了本身有停…</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺中市 | 「清水大楊原美軍油庫設施」的資料有疑似手機號碼：0921＊＊＊＊<br><sub>在 taichung-city/data/sites-official.json。公開網站不應轉載個人聯絡資料；確認是機關公開電話才保留。<br>前後文：…會】協助開門進入參觀。  聯絡方式：0921＊＊＊＊ 曾先生 …</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺中市 | 「神岡呂家頂瓦厝」的資料有疑似手機號碼：0932＊＊＊＊<br><sub>在 taichung-city/data/sites-official.json。公開網站不應轉載個人聯絡資料；確認是機關公開電話才保留。<br>前後文：…欲參觀請於先預約。 敬請電洽呂主委：0932＊＊＊＊…</sub> | 2026-11-22 | 2026-12-22 |
| 中 | 臺中市 | 「臺中市第四市場」的資料有疑似手機號碼：0975＊＊＊＊<br><sub>在 taichung-city/data/sites-official.json。公開網站不應轉載個人聯絡資料；確認是機關公開電話才保留。<br>前後文：…1F咖啡館訂購餐點：0975＊＊＊＊（週一到週二、週…</sub> | 2026-11-22 | 2026-12-22 |


## 新聞線索（25）

近期新聞標題是否提到網站收錄的文資，或出現新的指定、登錄。只是線索，要看過內容才能判斷。

### 可能有新的指定或登錄（3）

建議：記下來即可。官方開放資料更新後，「官方新增，網站未收錄」會自動出現，那時再新增。

更新方法：

1. 想搶先新增的話，流程同「官方新增，網站未收錄」。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 參考 |  | [可能有新的指定或登錄：京町店屋群保存與都更拉鋸 北市博愛路93號登錄歷史建築](https://news.google.com/rss/articles/CBMiYEFVX3lxTFBTa3BteVJnblkxR216Q1IzclFvc1R4QVF3ajlXbGp1T0xmSHZreWwtTHduV3h4U05QQWIzNUFVa1BwNWJpMWJwTjNpdDY0eC1uTnZIbjFvVXNCZzlIMWhkNNIBZkFVX3lxTE5IRXlrSkd3SlBoNEo1RlRJbnppNUlPb0htQUpSbXE0WE42SERKQWRWdk5PeU40TFVBREpsQ2JOWDhZTWdsTXU5Y3JEOUw2M3BXclFJeC1NM25kbjlvOG9QcXFVekJUQQ?oc=5)<br><sub>自由藝文網・2026-10-19（關鍵字：登錄歷史建築）<br>官方開放資料通常晚幾週才更新；若確定是新指定／登錄，可先記下，等開放資料出現後一併新增。</sub> | 2026-11-22 | — |
| 參考 |  | [可能有新的指定或登錄：台北博愛路93號 再次登錄歷史建築](https://news.google.com/rss/articles/CBMiW0FVX3lxTE1CTFhkZjBKaVYtemdJQnpLU0dxTkx0RENYVUgwMjRqdWRVZDktMnNQYnlibFY4R24tRkNVRE1aQm5ZLWVDOFlXdTI1NDBWMFVlTHZNRGlFVVJiOVHSAWBBVV95cUxOUEhFdjlQSVlHSjYzN2Y4bkQ1bkFVRFo1NWxOUHBabGQ5d280UjVPcEYwelBzbVl2ZVJLU1dtVWdHMmlvZDVyajNRbGczN0JNMGNYY2VLSjAyNDdLNnh1OVQ?oc=5)<br><sub>自由時報・2026-10-20（關鍵字：登錄歷史建築）<br>官方開放資料通常晚幾週才更新；若確定是新指定／登錄，可先記下，等開放資料出現後一併新增。</sub> | 2026-11-22 | — |
| 參考 |  | [可能有新的指定或登錄：總統賴清德贈匾彰化南瑤宮 盼升格國定古蹟延續百年香火](https://news.google.com/rss/articles/CBMiV0FVX3lxTFBGUkZ2ZTU3b2M2ZEdteVVuTWl5a25nd1dyYnJDS1dQSy01UWV6M3JxVF9PdDVzWnJCOW5UNlhzRU11LU9WQmRiTFpsTnlfQzZvQXIwQkR5dw?oc=5)<br><sub>觀傳媒・2026-11-19（關鍵字：升格國定古蹟）<br>官方開放資料通常晚幾週才更新；若確定是新指定／登錄，可先記下，等開放資料出現後一併新增。</sub> | 2026-11-22 | — |

### 新聞提到網站收錄的文資（22）

建議：看新聞內容。火災、倒塌、拆除、修復完工、重新開放、升格都值得更新介紹或開放資訊；一般活動報導可略過。

更新方法：

1. 需要更新：修改該縣市 data/sites-content.json 的 intro、openNote 或 funFact；改到對話要重跑 gen_audio.py。
2. 在主網站執行 python3 tools/build_data.py（重新產生各縣市 js/data.js），再執行 python3 tools/build_search.py（全站搜尋索引）。
3. 不需要更新：不用做任何事，這則線索 45 天後自動消失。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 參考 | 彰化縣 | [新聞提到「鹿港文武廟」：再現古蹟風華 鹿港文武廟修復啟用](https://news.google.com/rss/articles/CBMingJBVV95cUxNWUx3UWE2d1gxX1V6TzVqd0p5Rk94MEJzaUNNd081VU1UdEptdk1nRWFiald6dF9mclAzZHNWd1doVnR2SzVPUjVrMjhqbzVzR3pnbDFKMzM2SjBkcTFvczN4VC1mSDVBZkFFeXg4SEJuQjNUT2tjd1JtZk5xRTBHSE9Ra29RMEtKV0tPWHpMb184VEVGSUVHd2thQmxmYnNYdnVVSy1INDhFa1VjOS1JbVRvdkZxWDhPR0d4VTRmTzlCSWp6endUSi03RGpRcVZJeVlwWWFqajE2aGx6elVYNmRxX1c3TFBJck9nWmg0b0ppU2F6Tk16Q0piT1dfNWhnV0lXdnlBMmhLT2Q4T2M4T1FzYmswOGFBZGY3ODNn?oc=5)<br><sub>新唐人亞太電視台・2026-11-07（關鍵字：歷史建築 修復 啟用）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 彰化縣 | [新聞提到「鹿港文武廟」：彰化縣定古蹟鹿港文武廟修復竣工- 社會新聞](https://news.google.com/rss/articles/CBMijAFBVV95cUxNNXVWam1YZkUtaXFURkZOMk5abHJKYjRqUGRpNTAzRFoxd2RBZTNxaGwxQ2RpRFlEREZORjlqX0pVWWIzZDVQN25RMEcxNlRWSDBCRkxocTdxbTdKSDNUM1lycTkzbzBNTE8wdnNPelE4aTFNYUN4VTFia1VOSnhNaFVfTXBra1BvVFFzMw?oc=5)<br><sub>PChome Online 新聞・2026-11-07（關鍵字：古蹟 火災）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 彰化縣 | [新聞提到「鹿港文武廟」：鹿港文武廟修復完成兩百年歷史古蹟重現昔日風采｜ 台灣好新聞](https://news.google.com/rss/articles/CBMiVkFVX3lxTFBtSnJJN25YbHFyXy1VdUVPaktMR0Z1ODdEbnBMVlpoRjBEa1R5WnVRVzNWRU91MjJLQlktRkJYZy1HVmRYcVU1VXJoMUdNcmNNZzhWQndB?oc=5)<br><sub>LINE TODAY・2026-11-06（關鍵字：古蹟 火災）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 彰化縣 | [新聞提到「鹿港街長宿舍」：「鹿港街長宿舍」修復完工重新啟用 成為鹿港深度文化走讀新地標](https://news.google.com/rss/articles/CBMiVEFVX3lxTE1YRXhDd1M1bEVnTzFRcWUzVm1lYXo4X1F6VVlnSEh0ZV8xdDdIS3RLNzhhcmkzOEo1OWFGdEZEWDN6VG9UWHZLa2RDbWJLR2xKZ3UxVw?oc=5)<br><sub>新頭條・2026-11-13（關鍵字：古蹟 修復 完工）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 彰化縣 | [新聞提到「鹿港街長宿舍」：風華再現！彰化歷史建築「鹿港街長宿舍」修復啟用- 生活新聞](https://news.google.com/rss/articles/CBMikwFBVV95cUxQdEFKOVhsMTFxZWJmeXp6UE53Ym43bHhPakctX0NDSE5YYXRQdDVhU0FUZ200WU9WRXJPa3c2ek95ZDdrQVpDbXpaY19EZU5kU1VPR1ZOeWpiSkZuQVNWcEljY1BSbktOX1hXVFR1WjdDT1ktVnN4UTdYUE1xekhHd1BmdlNoT2gxckxpem53WlJpMTQ?oc=5)<br><sub>PChome Online 新聞・2026-11-13（關鍵字：歷史建築 修復 啟用）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 嘉義市 | [新聞提到「舊嘉義市公所」：【建築】舊嘉義市公所——從歷史見證 到現代藝文空間的重生 ｜2026](https://news.google.com/rss/articles/CBMi1AJBVV95cUxObGlzc3FOODZxMlhqQVR5bUpZNTcxSkl6RmhsMUxPUkY4Y1Z6d0F6WlZxSXJyWHJncWQ2VlV2OTJ1QVhRUFVBeVRJWHo2SHJhUG5iWmVFLUx0OHptRm43Q284NEd2dGFfR0N2YURSZ04yVkloYlc5RERGbXp1NmtDRUdaeE5TT19sWVJxdUhlR2hjaExvaVZtYjNaZHpmc1A0Z3ZmT2pTdlk3d2ZuN2hDeWpUaUNJcHVhM01KdFY3WnllbGU2TW5PdmVlZks2UFYtTV9tdTl0R2pkUTMtNF95VjFnbFMwQ3NmMWp5WndpZzNUbXZRTVp1M3FEajhvUjBFVEp0MFJ4a1FHNXpCQXN1Uzc2WnI0bUpsYm05eF8weGVNT3dudmhUa3ZvZU02LVBfdTJESTFhRjIwT2R6eUU5ekRpMVB6VGdBZHF3ZXdMQnVMUnpl?oc=5)<br><sub>The Culturist・2026-11-13（關鍵字：登錄歷史建築）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 嘉義縣 | [新聞提到「新港台糖復興鐵橋(原臺糖嘉北線五分仔鐵道暨北港溪鐵橋)」：橫跨雲嘉 百年歷史建築「復興鐵橋」完工啟用](https://news.google.com/rss/articles/CBMiUkFVX3lxTE5NaS0tYk9yaFFZYWdFY0F6bGY2YV9mVTFhUTBYRklLVkJ5a3F1cE5QVHpBaDRFSkVPSmlxMnV0WDRuelNOcENqZE5fbGJ5ZWtDRnc?oc=5)<br><sub>蕃新聞・2026-11-12（關鍵字：歷史建築 修復 啟用）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 嘉義縣 | [新聞提到「新港台糖復興鐵橋(原臺糖嘉北線五分仔鐵道暨北港溪鐵橋)」：橫跨雲嘉歷史建築復興鐵橋啟用耗資2億餘元修復｜ 地方](https://news.google.com/rss/articles/CBMiX0FVX3lxTE5hTFNkTWliOWJwbExfc2VsTnJOWWFheE5yUGlQZTRfTjhoNDQtM1hmUTRZcnhSNnp0b3d4NlZQQmluTk13aXo1MU1HSjktM1R3eVhPNHFBVllzQTdFV3pr?oc=5)<br><sub>中央社 CNA・2026-11-11（關鍵字：歷史建築 修復 啟用）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 嘉義縣 | [新聞提到「新港台糖復興鐵橋(原臺糖嘉北線五分仔鐵道暨北港溪鐵橋)」：百年復興鐵橋修復啟用！678公尺鐵道景觀步道串聯雲嘉觀光- 社會新聞](https://news.google.com/rss/articles/CBMijAFBVV95cUxPNUhidVJBdExqZmhhdlRyZ0dZbUNFRk5GaVVyWTNabVBqaFVWSUNmamdFZGhMcDF0YjBRNlhoU3dYN0FVTk1qVlp1d2tUSFhRczJnejFsNmo1cDZHb2lYX0YtandwZFFXTUNtSlF5NXZQWGtlVTMzbEJZanJUZjNtSlFLcDIxQjV1SU1qTQ?oc=5)<br><sub>PChome Online 新聞・2026-11-12（關鍵字：歷史建築 修復 啟用）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 金門縣 | [新聞提到「永昌堂暨浯陽小學校」：百年古蹟永昌堂暨浯陽小學校修復上梁 融合中西建築特色再現僑鄉歷史風華](https://news.google.com/rss/articles/CBMif0FVX3lxTE5Lc2Ixb1pwX3hXdGNUTVFXZ3lTc0RoYnlOQkV0R0pZOXJnSVc0U2MtNUh0QnpHeFBMdUcwQkhpT0h0cEJ4Mm01U0ppZ1VpWnBJLWxMQ0c0bEszU0R0TEdFT3FKR3N2NHZVb2tEWmdOc3J4VGwyaTJCNG1YSDF5R0U?oc=5)<br><sub>金門GO資訊網・2026-11-10（關鍵字：古蹟 修復 完工）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 苗栗縣 | [新聞提到「南庄田美永和宮」：百年歷史建築南庄田美永和宮開工修復 總經費5550萬盼重現風華](https://news.google.com/rss/articles/CBMiZEFVX3lxTE9PSndfREk4NlVReWdpVUtTSDU0dDVoZkQ4RWVVSDR3dzJfS01wUUgya3dmdkdCdV90OXZ1a0FoS09CZTE1QUM4dWhWNmE5bktWVGVGSkNVRW1ISzQ5dnM1dm1ZT1_SAWpBVV95cUxObm81ZE41XzN1ZWw3QWctaS13QmJyZE1mUEwyUGxMUERvcjFZVGJwaDJOSEZsYkNEdTg4bWZDSGgxZXBGUmd3NC1wOTMyUzRYaUNudTNvRGdtY1ZZRjZzQXBPWEpIUm5MUXRB?oc=5)<br><sub>自由時報・2026-11-13（關鍵字：登錄歷史建築）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 苗栗縣 | [新聞提到「通霄神社」：秒到日本！通霄神社列古蹟保留石燈龍.拜殿格局- 地方](https://news.google.com/rss/articles/CBMibkFVX3lxTE8xZ3duYWFfQ2xfdmJfcnNERVotNzhkY1AwXzBoVk9EMmkwMUlLaE92MENtQkpmWUpIbHBzeXdxZmFiRXhMLTVzZlhZS1hmV1ljOFpEOS1HUzNCZG5CN3J3NzlUWFYyUmtIV3Bldl9B?oc=5)<br><sub>華視新聞網・2026-11-18（關鍵字：登錄歷史建築）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 苗栗縣 | [新聞提到「造橋車站暨附屬宿舍」：全面優化造橋車站周邊景觀 百年日式歷史建築群環境改造工程今動土](https://news.google.com/rss/articles/CBMiUEFVX3lxTE12WFlpUzdGUjU0TWJtNjBiUlk1c1dtbTJYc0xiNXl3NWtUdG1yU19Qd3lVUFBVT1lVTDZKMzVXTlIwN1dyS1l0a3h1alhsZ2dC0gFWQVVfeXFMT2tISXM1dTN0ZkpDTlBsRTc4UnBFSk5rRnI2eHhtc2FKTW1tdmcycmduNkc1MmZZeHU1TEJBOUpWZmVpQ0pKRXRQLTgzbkVtTWlmY1p1UWc?oc=5)<br><sub>UDN・2026-11-18（關鍵字：歷史建築 火警）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 苗栗縣 | [新聞提到「造橋車站暨附屬宿舍」：百年造橋車站迎新貌！串聯百年日式歷史建築群 打造157坪集會廣場](https://news.google.com/rss/articles/CBMiZEFVX3lxTE8za3Z0RFRHbDl4cjEtN1pXRk5aZXRsVlE4RXViWEpnQ1BFd1hNRXJTTHZhbWY4QklDbXk5MEs5Y2lnaURLUEZaNHlGQzBmMmdlOGdzM0lWY1BvZ3RFaFByX0owV27SAWpBVV95cUxQVkxRVXFRVmt4UzZJNjR2ZzVzejEtR3dnY2NHR1RfLWh1RlRLSWZKdHdPX3l6WFluX2ZiNHhWOU1BSmFmNnFjU2FweUYwd2N6YU9FV2tJTTd3SFZPQXNmc0xaT1djVTNYTW1R?oc=5)<br><sub>自由時報・2026-11-18（關鍵字：歷史建築 火警）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 屏東縣 | [新聞提到「屏東市勝利新村、崇仁新村（成功區）日治時期軍官眷舍」：屏東再獲4.76億打造「潮州、東港版」勝利星村 最後一塊拼圖曝光](https://news.google.com/rss/articles/CBMiX0FVX3lxTE1yeUFTVnc3M1FweExsZ1FaVkEtSERCMUVwSGFBTGRZbjZJMVJ3ZXVXQmZwOEI2TFBTR2t0cFdFNkg1NGNnRERWWHFvWGhqTFBhamtRekdvRVR2VEEtUm5Z?oc=5)<br><sub>中時新聞網・2026-10-22（關鍵字：登錄歷史建築）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 屏東縣 | [新聞提到「屏東憲光十村」：屏東獲再造歷史現場2.0補助4.76億 修復憲光十村潮州東港](https://news.google.com/rss/articles/CBMiUkFVX3lxTFB3TmVFbGRUUWdVa0tkbk9sSnBJeTZLVV9tU2hNNlB6RkZiMk1hTm5ucEh2YXdXQUV6dzAyNVc2TmhNQmtoUmlTU2ZYTEpSZncwVmc?oc=5)<br><sub>蕃新聞・2026-10-23（關鍵字：歷史建築 修復 啟用）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 臺中市 | [新聞提到「臺中州廳」：台中州廳修復完工！盧秀燕市政會議移師百年古蹟：修好了就要活用](https://news.google.com/rss/articles/CBMiZ0FVX3lxTE05OXZ4M0xqRXVjZGM3VHhWWDhhTktVenJzWVNGX2RGY2FjNU1GMkR3NHFnODlrUkFHbXFIM2xkQWdEY25qbHZGWC1ZUl83MGpyNWZtV0h6ZUZzWGFfVDVCOHlDdmh5dXM?oc=5)<br><sub>新華報導・2026-11-03（關鍵字：古蹟 修復 完工）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 臺中市 | [新聞提到「臺中州廳」：綠建築是現代發明？ 台中州廳早在百年前就做到了](https://news.google.com/rss/articles/CBMiUkFVX3lxTE5yZjZ5MnZWVEEtanpqRzFGMUkxMGx6S1hnT1RpZHBLVGVHbGEwbUl0Q3FicnowVWREandIMUdKWF9TM3B0XzFLTDZzYVptbnNhUnc?oc=5)<br><sub>蕃新聞・2026-11-12（關鍵字：文化資產審議 通過）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 臺中市 | [新聞提到「臺中州廳」：臺中州廳修復 融合現代永續設計 ｜ 青年日報](https://news.google.com/rss/articles/CBMiVkFVX3lxTE5adlM3clBMeXpseGNmUlBoTUo1Uml0YzBBVUZ2RWtNTG1KNzNTMExHem0xbWVHeGxJLV9EeURNcDhENHdBTkpxWERuejh6M3pqVFZldmpn?oc=5)<br><sub>LINE TODAY・2026-11-17（關鍵字：文化資產審議 通過）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 臺北市 | [新聞提到「西本願寺（鐘樓、樹心會館）」：萬華日式老屋回歸！西本願寺輪番所整修2年多　變身茶館重新營業](https://news.google.com/rss/articles/CBMia0FVX3lxTE9oYXZHZHMwT1JfazFRNmJmQW1Pc1VMYXRvMWhFWGpJeVVaZk54SmU5NURKQ1BsMDl3MFJQMTBrbGNHc0hva3BScUFYT2dFNkZGMGFqY05WbWI5cGNTWFBoTTVKMFozREYyYnRV0gFwQVVfeXFMUDU1Q01Wa1NldHZ5N1Y4QllwbEZIRGg0U2hrWkpEaE9HREpsR3lCSGk5VFkwQjJwdllyM2w5Tjhoa3RBVjVmcEc1SU1Ma0piVlIzRE0yNlZHaVZMdjhZWVlBcVBRbzZ0Q0xVWnRTYWNRWg?oc=5)<br><sub>好房網News・2026-10-21（關鍵字：登錄歷史建築）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 雲林縣 | [新聞提到「北港糖廠」：北港糖廠登錄歷史建築 倉庫群修復活化盼帶動觀光](https://news.google.com/rss/articles/CBMiT0FVX3lxTE94NnFUNGJSRERNY3hYRERsSFYtdElYbW54bUVURFlLaWJpenI3NVIwQ2RTemV2ZGxYbzZwTmx1bHgxMGtBdHh2cDl0SkY2TG8?oc=5)<br><sub>公視新聞・2026-10-27（關鍵字：登錄歷史建築）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |
| 參考 | 雲林縣 | [新聞提到「北港糖廠」：百年北港糖廠變身文化新地標！1911好庫開園 三大展覽一次看](https://news.google.com/rss/articles/CBMiTkFVX3lxTE81a0hTY0ViLUlXNU5DWTVIV0tCeThyZ1J3c1c2VWpnaHVSQlJENWJJS0tyZFh3ajlmUTdfeGxjaFRBbzlXMnlHRlNheXZwZw?oc=5)<br><sub>創新聞・2026-10-26（關鍵字：登錄無形文化資產）<br>請看內容是否影響網站介紹：災損、修復完工、重新開放、升格、範圍變更等。</sub> | 2026-11-22 | — |


## 檢測本身（3）

檢測過程遇到的問題，例如資料來源下載失敗。

### 資料來源暫時無法取得（3）

建議：通常下次檢測就會恢復。連續好幾次都失敗，再看是不是對方改了網址或格式。

更新方法：

1. 在 GitHub 的 Actions 手動重跑一次檢測（Run workflow）。
2. 連續失敗：檢查 tools/check_official.py 的下載網址是否仍正確。

| 優先度 | 縣市 | 內容 | 首次發現 | 期限 |
|---|---|---|---|---|
| 低 |  | 維基共享資源有 1791 個頁面本次未能確認<br><sub>commons.wikimedia.org 的 API 限流或沒有回應。這不代表連結失效，下次檢測會再查。</sub> | 2026-11-22 | 2027-02-20 |
| 低 |  | 維基百科有 1 個頁面本次未能確認<br><sub>en.wikipedia.org 的 API 限流或沒有回應。這不代表連結失效，下次檢測會再查。</sub> | 2026-11-22 | 2027-02-20 |
| 低 |  | 維基百科有 243 個頁面本次未能確認<br><sub>zh.wikipedia.org 的 API 限流或沒有回應。這不代表連結失效，下次檢測會再查。</sub> | 2026-11-22 | 2027-02-20 |

