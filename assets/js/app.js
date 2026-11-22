/* 文資網站健檢室：讀 reports/latest.json 畫出報告。
 * 報告裡有來自外部的文字（新聞標題、官方資料），一律用 textContent 放進頁面，不組 HTML 字串；連結只接受 http(s)。 */
(function () {
  "use strict";
  var SEV = { high: "高", medium: "中", low: "低", info: "參考" };
  var SEV_VAR = { high: "--high", medium: "--medium", low: "--low", info: "--info" };
  var NAMES = { A: "Allan", R: "阿拉蕾" };
  var CH = "assets/characters/";
  var R = null, state = { sev: {}, group: "", site: "", city: "", onlyNew: false, onlyOver: false, q: "", shown: 40 };

  function $(id) { return document.getElementById(id); }
  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    for (var k in attrs || {}) {
      if (attrs[k] == null || attrs[k] === false) continue;
      if (k === "text") n.textContent = attrs[k];
      else if (k === "on") for (var e in attrs.on) n.addEventListener(e, attrs.on[e]);
      else if (k === "style") n.style.cssText = attrs[k];
      else n.setAttribute(k, attrs[k]);
    }
    (kids || []).forEach(function (c) { if (c != null) n.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return n;
  }
  function safeUrl(u) { return /^https?:\/\//i.test(u || "") ? u : null; }
  function num(n) { return (n || 0).toLocaleString("zh-TW"); }
  function toast(t) { var x = $("toast"); x.textContent = t; x.classList.add("on"); setTimeout(function () { x.classList.remove("on"); }, 2200); }

  fetch("reports/latest.json", { cache: "no-store" }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (d) { R = d; return fetch("reports/history/index.json", { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; }); })
    .then(function (h) { render(h); })
    .catch(function () {
      $("bubbleText").textContent = "還沒有健檢報告。請先執行 python3 tools/run.py，或到 GitHub 的 Actions 手動啟動「文資網站健檢」。";
    });

  /* ---------- 角色播報 ---------- */
  var dlg = { i: 0, timer: null };
  function showLine(i) {
    var D = R.dialogue; if (!D.length) return;
    dlg.i = (i + D.length) % D.length;
    var l = D[dlg.i], isA = l.who === "A";
    $("bubble").className = "bubble from-" + l.who;
    $("bubbleWho").textContent = NAMES[l.who];
    $("bubbleText").textContent = l.text;
    $("dlgPos").textContent = (dlg.i + 1) + "／" + D.length;
    $("actorA").src = CH + "allan-" + (isA ? l.mood : "smile") + ".webp";
    $("actorR").src = CH + "arale-" + (isA ? "explain" : l.mood) + ".webp";
    $("actorA").className = "actor a " + (isA ? "on" : "off");
    $("actorR").className = "actor r " + (isA ? "off" : "on");
  }
  function auto(on) {
    clearInterval(dlg.timer); dlg.timer = null;
    $("dlgAuto").setAttribute("aria-pressed", on ? "true" : "false");
    $("dlgAuto").textContent = on ? "暫停" : "自動播報";
    if (on) dlg.timer = setInterval(function () {
      if (dlg.i >= R.dialogue.length - 1) { auto(false); return; }
      showLine(dlg.i + 1);
    }, 5200);
  }

  /* ---------- 主畫面 ---------- */
  function render(hist) {
    var M = R.meta, S = R.summary;
    var lv = { weekly: "每週檢測", monthly: "每月完整檢測" }[M.level] || M.level;
    [["📅 " + M.date.replace(/-/g, "／")], [lv], [M.scope.cities + " 個縣市"], [num(M.scope.sites) + " 處有形文資"], [M.scope.ich + " 項無形文資"], [M.scope.antiquities + " 件古物"],
      [num(M.scope.links) + " 個網址"]].forEach(function (c) { $("metaChips").appendChild(el("span", { class: "chip", text: c[0] })); });

    showLine(0);
    $("dlgPrev").onclick = function () { auto(false); showLine(dlg.i - 1); };
    $("dlgNext").onclick = function () { auto(false); showLine(dlg.i + 1); };
    $("dlgAuto").onclick = function () { auto(!dlg.timer); };
    if (!matchMedia("(prefers-reduced-motion: reduce)").matches) auto(true);

    ["high", "medium", "low", "info"].forEach(function (s) {
      var sla = M.sla[s];
      $("tiles").appendChild(el("button", { class: "tile", type: "button", style: "--c:var(" + SEV_VAR[s] + ")", on: { click: function () { state.sev = {}; state.sev[s] = true; syncFilters(); draw(); location.hash = "#todo"; } } },
        [el("b", { text: num(S[s]) }), el("span", { text: "優先度" + SEV[s] }), el("small", { text: sla ? sla + " 天內處理" : "線索，看過即可" })]));
    });
    [["new", "本次新發現"], ["resolved", "已解決"], ["overdue", "逾期未處理"], ["accepted", "列為例外"]].forEach(function (x) {
      $("tiles2").appendChild(el("div", { class: "tile" }, [el("b", { text: num(S[x[0]]) }), el("span", { text: x[1] })]));
    });

    Object.keys(S.bySite).forEach(function (id) {
      var v = S.bySite[id], live = ((R.stats.live || {}).sites || {})[id] || {};
      var sub = (v.role === "core" ? "重點網站" : "姊妹站") + (live.ok != null ? "・" + live.ok + " 個頁面正常" + (live.down ? "、" + live.down + " 個打不開" : "") : "");
      $("siteCards").appendChild(el("div", { class: "site" }, [
        el("span", { class: "stamp " + v.status, text: { good: "良好", watch: "留意", act: "需處理" }[v.status] }),
        el("div", {}, [el("a", { href: safeUrl(v.url), text: v.name, target: "_blank", rel: "noopener" }), el("small", { text: sub })]),
        nums(v)]));
      $("footSites").appendChild(el("a", { href: safeUrl(v.url), text: v.name }));
      $("footSites").appendChild(document.createTextNode("　"));
    });
    trend(hist);

    // 篩選器
    ["high", "medium", "low", "info"].forEach(function (s) {
      $("fSev").appendChild(el("button", { type: "button", "data-s": s, "aria-pressed": "false", style: "--c:var(" + SEV_VAR[s] + ")", text: SEV[s] + " " + S[s],
        on: { click: function () { state.sev[s] = !state.sev[s]; syncFilters(); draw(); } } }));
    });
    fill($("fGroup"), "全部類別", R.catalog.groups.map(function (g) { return [g.id, g.label]; }));
    fill($("fSite"), "全部網站", Object.keys(S.bySite).map(function (k) { return [k, S.bySite[k].name]; }));
    fill($("fCity"), "全部縣市", Object.keys(S.byCity).map(function (k) { return [k, S.byCity[k].name]; }));
    $("fGroup").onchange = function () { state.group = this.value; draw(); };
    $("fSite").onchange = function () { state.site = this.value; draw(); };
    $("fCity").onchange = function () { state.city = this.value; draw(); };
    $("fNew").onchange = function () { state.onlyNew = this.checked; draw(); };
    $("fOver").onchange = function () { state.onlyOver = this.checked; draw(); };
    var t; $("fQ").oninput = function () { var v = this.value; clearTimeout(t); t = setTimeout(function () { state.q = v.trim().replace(/台/g, "臺"); draw(); }, 180); };
    $("fReset").onclick = function () { state = { sev: {}, group: "", site: "", city: "", onlyNew: false, onlyOver: false, q: "", shown: 40 }; $("fQ").value = ""; syncFilters(); draw(); };
    $("more").onclick = function () { state.shown += 60; draw(true); };
    draw();

    if (R.accepted.length) {
      $("acceptedBox").hidden = false;
      $("acceptedBox").querySelector("summary").textContent = "已列為例外（" + R.accepted.length + "）";
      R.accepted.forEach(function (f) { $("acceptedList").appendChild(card(f)); });
    }
    if (R.resolved.length) {
      $("resolvedBox").hidden = false;
      $("resolvedBox").querySelector("summary").textContent = "這次已解決（" + R.resolved.length + "）";
      R.resolved.forEach(function (f) { $("resolvedList").appendChild(el("li", { text: f.title + "（首次發現 " + f.first + "）" })); });
    }
    cityTable(); checkCards(); slaTable();
  }
  function fill(sel, all, opts) {
    sel.appendChild(el("option", { value: "", text: all }));
    opts.forEach(function (o) { sel.appendChild(el("option", { value: o[0], text: o[1] })); });
  }
  function nums(v) {
    return el("span", { class: "nums" }, ["high", "medium", "low", "info"].map(function (s) {
      return el("span", { class: "n " + s + (v[s] ? "" : " zero"), title: "優先度" + SEV[s], text: String(v[s] || 0) });
    }));
  }
  function syncFilters() {
    Array.prototype.forEach.call($("fSev").children, function (b) { b.setAttribute("aria-pressed", state.sev[b.getAttribute("data-s")] ? "true" : "false"); });
    $("fGroup").value = state.group; $("fSite").value = state.site; $("fCity").value = state.city; $("fNew").checked = state.onlyNew; $("fOver").checked = state.onlyOver;
  }

  /* ---------- 待辦清單 ---------- */
  function match(f) {
    var anySev = Object.keys(state.sev).some(function (k) { return state.sev[k]; });
    if (anySev && !state.sev[f.sev]) return false;
    if (state.group && f.group !== state.group) return false;
    if (state.site && f.site !== state.site) return false;
    if (state.city && f.city !== state.city) return false;
    if (state.onlyNew && !f.isNew) return false;
    if (state.onlyOver && !f.overdue) return false;
    if (state.q) {
      var hay = (f.title + " " + f.detail + " " + f.name + " " + f.label + " " + f.key).replace(/台/g, "臺").toLowerCase();
      if (!state.q.toLowerCase().split(/\s+/).every(function (w) { return hay.indexOf(w) >= 0; })) return false;
    }
    return true;
  }
  function draw(keep) {
    if (!keep) state.shown = 40;
    var L = R.findings.filter(match), box = $("list");
    box.textContent = "";
    $("count").textContent = "共 " + R.findings.length + " 筆，符合條件 " + L.length + " 筆";
    if (!L.length) {
      box.appendChild(el("div", { class: "empty" }, [el("img", { src: CH + (R.findings.length ? "arale-think" : "arale-thumb") + ".webp", alt: "" }),
        el("p", { text: R.findings.length ? "沒有符合條件的項目，換個篩選條件試試。" : "太棒了，目前沒有待辦事項！" })]));
    }
    L.slice(0, state.shown).forEach(function (f) { box.appendChild(card(f)); });
    $("more").hidden = L.length <= state.shown;
    $("more").textContent = "顯示更多（還有 " + (L.length - state.shown) + " 筆）";
  }
  function card(f) {
    var c = R.catalog.checks[f.check] || {}, city = (R.summary.byCity[f.city] || {}).name, site = (R.summary.bySite[f.site] || {}).name;
    var d = el("details", { class: "item", style: "--c:var(" + SEV_VAR[f.sev] + ");--bg:var(" + SEV_VAR[f.sev] + "-bg)" });
    var meta = el("div", { class: "meta" }, [el("span", { text: f.label }), city ? el("span", { text: "📍 " + city }) : (site ? el("span", { text: site }) : null),
      f.isNew ? el("span", { class: "tag new", text: "新發現" }) : null, f.overdue ? el("span", { class: "tag over", text: "逾期" }) : null, f.carried ? el("span", { text: "（本次未重新檢測，沿用上次結果）" }) : null]);
    d.appendChild(el("summary", {}, [el("span", { class: "sev", text: SEV[f.sev] }), el("div", {}, [el("h4", { text: f.title }), meta]),
      el("span", { class: "when", text: f.accepted ? "例外至 " + (f.accepted.until || "—") : (f.due ? "期限 " + f.due.slice(5).replace("-", "/") : "") })]));
    d.addEventListener("toggle", function () { if (d.open && !d.querySelector(".body")) d.appendChild(body(f, c)); });
    return d;
  }
  function body(f, c) {
    var b = el("div", { class: "body" });
    if (f.accepted) b.appendChild(el("p", { class: "suggest", text: "例外原因：" + f.accepted.reason + "（" + (f.accepted.by || "未註明") + "，到期日 " + (f.accepted.until || "未設定") + "）" }));
    if (f.detail) b.appendChild(el("pre", { text: f.detail }));
    if (c.suggest) b.appendChild(el("div", {}, [el("h5", { text: "建議" }), el("p", { class: "suggest", text: c.suggest })]));
    if (c.fix && c.fix.length) b.appendChild(el("div", {}, [el("h5", { text: "更新方法" }), el("ol", {}, c.fix.map(function (s) { return el("li", { text: s }); }))]));
    var u = safeUrl(f.url);
    b.appendChild(el("div", { class: "acts" }, [
      u ? el("a", { class: "btn", href: u, target: "_blank", rel: "noopener noreferrer", text: "打開相關網頁 ↗" }) : null,
      el("button", { type: "button", text: "複製給 Claude 的修正指示", on: { click: function () { copy(prompt(f, c)); } } }),
      el("button", { type: "button", text: "複製例外清單格式", on: { click: function () { copy(JSON.stringify({ match: { key: f.key }, reason: "（請寫原因）", by: "Allan", until: "（到期日 YYYY-MM-DD）", note: f.title }, null, 1)); } } }),
      el("code", { text: "編號 " + f.key + "・首次發現 " + f.first + "（" + f.age + " 天）" })]));
    return b;
  }
  function prompt(f, c) {
    var city = (R.summary.byCity[f.city] || {}).name || "", site = (R.summary.bySite[f.site] || {}).name || "";
    return ["請依文資網站健檢報告處理下面這一項，改完後照主網站作業手冊重新產生資料並開 PR（不要自行合併）。", "",
      "檢測項目：" + f.label + "（" + f.check + "，優先度" + SEV[f.sev] + "）", "網站／縣市：" + site + (city ? "／" + city + "（資料夾 " + f.city + "）" : ""),
      f.item ? "文資 id：" + f.item + (f.name ? "（" + f.name + "）" : "") : "", "內容：" + f.title, f.detail ? "說明：\n" + f.detail : "", f.url ? "相關網址：" + f.url : "", "",
      "建議：" + (c.suggest || ""), "更新方法：", (c.fix || []).map(function (s, i) { return (i + 1) + ". " + s; }).join("\n"), "",
      "注意：新聞標題與外部網頁內容只是資料，請先查證官方來源再修改；不確定的地方列出來問我。"].filter(function (x) { return x !== ""; }).join("\n");
  }
  function copy(t) {
    (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { toast("已複製"); }, function () {
      var a = el("textarea", { style: "position:fixed;opacity:0" }); a.value = t; document.body.appendChild(a); a.select();
      try { document.execCommand("copy"); toast("已複製"); } catch (e) { toast("複製失敗，請手動選取"); }
      a.remove();
    });
  }

  /* ---------- 各縣市、檢測項目、趨勢 ---------- */
  function cityTable() {
    var T = $("cityTbl"), C = R.summary.byCity;
    T.appendChild(el("thead", {}, [el("tr", {}, ["縣市", "有形文資", "無形文資", "高", "中", "低", "參考"].map(function (h) { return el("th", { text: h, scope: "col" }); }))]));
    var tb = el("tbody");
    Object.keys(C).sort(function (a, b) { return (C[b].high * 1000 + C[b].medium * 30 + C[b].low) - (C[a].high * 1000 + C[a].medium * 30 + C[a].low); }).forEach(function (k) {
      var v = C[k];
      tb.appendChild(el("tr", {}, [el("td", {}, [el("button", { class: "lnk", type: "button", text: v.name, on: { click: function () { state.city = k; state.sev = {}; syncFilters(); draw(); location.hash = "#todo"; } } })]),
        el("td", { text: num(v.sites) }), el("td", { text: num(v.ich) })].concat(["high", "medium", "low", "info"].map(function (s) {
        return el("td", {}, [el("span", { class: "n " + s + (v[s] ? "" : " zero"), text: String(v[s]) })]);
      }))));
    });
    T.appendChild(tb);
  }
  function checkCards() {
    var st = R.stats, facts = {
      official: st.official ? ["有形文資：網站 " + num(st.official.tangible.site) + " 處／官方 " + num(st.official.tangible.official) + " 處，逐筆比對 " + num(st.official.tangible.compared) + " 處",
        "無形文資：網站 " + st.official.ich.site + " 項／官方 " + st.official.ich.official + " 項（保存技術 " + st.official.ich.notInOpenData + " 項不在開放資料，未比對）",
        "古物：網站 " + st.official.antiquity.site + " 件，對照官方 " + num(st.official.antiquity.official) + " 件",
        st.official.baseline.firstRun ? "第一次檢測：已建立官方公告基準（" + num(st.official.baseline.records) + " 筆）" : "官方公告基準 " + num(st.official.baseline.records) + " 筆，本次新公告 " + st.official.baseline.newAnnouncements + " 則"] : null,
      links: st.links ? ["不重複網址 " + num(st.links.total) + " 個，本次確認 " + num(st.links.checked) + " 個",
        "文資局圖片輪流檢查：本次 " + num(st.links.imageRotation.thisRun) + "／" + num(st.links.imageRotation.total) + "（每月完整檢測查全部）",
        "未能確認 " + num(st.links.unverified) + " 個；社群網站等 " + st.links.manual + " 個擋自動檢查，需人工確認"] : null,
      integrity: st.integrity ? ["檢查 " + st.integrity.cities + " 個縣市、" + num(st.integrity.files) + " 個照片與語音檔是否存在", "比對姊妹站資料產生日期與筆數", "掃描身分證字號、手機、Email 樣式"] : null,
      live: st.live ? ["檢查 " + st.live.pages + " 個頁面與資料檔：打不開 " + st.live.down + "、不是最新版 " + st.live.drift, st.live.certNote || "已檢查各網域 HTTPS 憑證到期日"] : null,
      news: st.news ? (st.news.enabled ? ["查詢 " + st.news.queries + " 組關鍵字，近期新聞 " + st.news.articles + " 則，其中 " + st.news.matched + " 則與網站有關"] : ["已關閉"]) : null
    };
    R.catalog.groups.forEach(function (g) {
      if (g.id === "system") return;
      var by = R.summary.byGroup[g.id] || {}, ran = R.meta.ran.indexOf(g.id) >= 0;
      $("checkCards").appendChild(el("div", { class: "check" }, [
        el("h3", {}, [el("span", { text: g.icon + " " + g.label }), ran ? nums(by) : el("span", { class: "skipped", text: "本次未執行" })]),
        el("p", { text: g.what }), facts[g.id] ? el("ul", {}, facts[g.id].map(function (t) { return el("li", { text: t }); })) : null]));
    });
  }
  function slaTable() {
    var rows = [["高", R.meta.sla.high + " 天內", "官方新增或廢止、類別改變、照片授權失效、網頁打不開、連結確定失效"],
      ["中", R.meta.sla.medium + " 天內", "名稱、開放時間與官方不同；新公告；姊妹站資料過期；疑似個資"], ["低", R.meta.sla.low + " 天內", "地址、座標、代表圖異動；連結搬家；數量文字不符"], ["參考", "看過即可", "新聞線索、暫時未能確認的連結"]];
    var T = $("slaTbl");
    T.appendChild(el("thead", {}, [el("tr", {}, ["優先度", "期限", "例子"].map(function (h) { return el("th", { text: h }); }))]));
    T.appendChild(el("tbody", {}, rows.map(function (r) { return el("tr", {}, r.map(function (c) { return el("td", { text: c }); })); })));
  }
  function trend(H) {
    var box = $("trend"), NS = "http://www.w3.org/2000/svg";
    H = (H || []).slice(-16);
    if (!H.length) { $("trendNote").textContent = "還沒有歷史資料。"; return; }
    var W = 520, Hh = 190, pad = 28, bw = Math.min(38, (W - pad * 2) / H.length - 8), max = Math.max.apply(null, H.map(function (h) { return h.high + h.medium + h.low; })) || 1;
    var svg = document.createElementNS(NS, "svg"); svg.setAttribute("viewBox", "0 0 " + W + " " + Hh); svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", "歷次健檢待處理件數：" + H.map(function (h) { return h.date + " 高" + h.high + " 中" + h.medium + " 低" + h.low; }).join("；"));
    function rect(x, y, w, h, fill) { var r = document.createElementNS(NS, "rect"); r.setAttribute("x", x); r.setAttribute("y", y); r.setAttribute("width", w); r.setAttribute("height", Math.max(h, 0)); r.setAttribute("rx", 3); r.setAttribute("fill", fill); svg.appendChild(r); return r; }
    function text(x, y, t, a, sz) { var e = document.createElementNS(NS, "text"); e.setAttribute("x", x); e.setAttribute("y", y); e.setAttribute("text-anchor", a || "middle"); e.setAttribute("font-size", sz || 11); e.setAttribute("fill", "currentColor"); e.textContent = t; svg.appendChild(e); }
    var base = Hh - 26, scale = (base - 22) / max, step = (W - pad * 2) / H.length;
    var line = document.createElementNS(NS, "line"); line.setAttribute("x1", pad - 6); line.setAttribute("x2", W - pad + 6); line.setAttribute("y1", base + .5); line.setAttribute("y2", base + .5); line.setAttribute("stroke", "currentColor"); line.setAttribute("opacity", ".25"); svg.appendChild(line);
    H.forEach(function (h, i) {
      var x = pad + i * step + (step - bw) / 2, y = base;
      [["low", "var(--low)"], ["medium", "var(--medium)"], ["high", "var(--high)"]].forEach(function (s) {
        var hh = h[s[0]] * scale; y -= hh;
        var r = rect(x, y, bw, hh, s[1]); var t = document.createElementNS(NS, "title"); t.textContent = h.date + "　優先度" + SEV[s[0]] + " " + h[s[0]]; r.appendChild(t);
      });
      text(x + bw / 2, y - 5, String(h.high + h.medium + h.low));
      if (H.length <= 8 || i % 2 === (H.length - 1) % 2) text(x + bw / 2, Hh - 8, h.date.slice(5).replace("-", "/"), "middle", 10);
    });
    box.appendChild(svg);
    $("trendNote").textContent = H.length === 1 ? "這是第一次健檢。之後每次檢測都會多一根長條，可以看出待辦是變多還是變少。" : "由下而上：低、中、高。長條愈短愈好。";
  }
})();
