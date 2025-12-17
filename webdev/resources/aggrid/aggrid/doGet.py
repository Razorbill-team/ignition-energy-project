def doGet(request, session):
	# Web Dev → aggrid/aggrid (Script) → doGet
	qs = request.get("params") or {}
	qs_string = "?" + "&".join(["{}={}".format(k, v) for k, v in qs.items()]) if qs else ""
	
	html = """
	<!doctype html>
	<html>
	<head>
	  <meta charset="utf-8"/>
	  <title>AG Grid</title>
	  <meta name="viewport" content="width=device-width, initial-scale=1"/>
	
	  <!-- Local AG Grid assets -->
	  <link rel="stylesheet" href="./v34/css/ag-grid.css">
	  <link rel="stylesheet" href="./v34/css/ag-theme-alpine.css">
	  <script src="./v34/ag-grid-enterprise.min.js"></script>
	
	  <style>
	    /* ====== page layout: top bar + grid ====== */
	    html, body { height:100%; margin:0; background:#0a0f1a; }
	    .page { height:100vh; width:100vw; display:flex; flex-direction:column; overflow:hidden; }
	
	    /* Top bar ABOVE table (outside it) */
	    .topbar{
	      position:sticky; top:0; z-index:99;
	      display:flex; align-items:center; gap:12px;
	      padding:10px 12px;
	      background:#182d47;
	      border-bottom:2px solid rgba(255,255,255,0.15);
	      color:#eaf2ff; font:600 12px/1 system-ui;
	    }
	    .tb-title{ opacity:.9; }
	
	    /* Push the button to the far right */
	    .apply-btn { margin-right:auto; }
	
	    /* Grid takes remaining space */
	    #grid { flex:1 1 auto; min-height:0; height:auto; width:100%; }
	
	    /* Base button + badge */
	    .btn {
	      padding:8px 5px; border-radius:3px; border:1px solid #445;
	      background:#1b2a45; color:#fff; cursor:pointer;
	    }
	    .badge {
	      display:inline-flex; min-width:1em; height:1em; padding:0 .35em;
	      border-radius:500px; align-items:center; justify-content:center;
	      background:#2f7; color:#000; font:700 11px/1 system-ui;
	    }
	
	    /* --- HERO button --- */
	    .btn-hero{
	      display:inline-flex; align-items:center; justify-content:center;
	      height:35px;
	      min-width:100px;
	      padding:0 22px;
	      border-radius:10px;
	      border:2px solid rgba(255,255,255,0.25);
	      background:#0c0c0f;
	      color:#fff;
	      font:600 15px/1.1 system-ui;
	      letter-spacing:.2px;
	      box-shadow: inset 0 0 0 1px rgba(0,0,0,0.35);
	      transition: transform .06s ease, box-shadow .12s ease, border-color .12s ease;
	    }
	    .btn-hero:hover{
	      border-color:rgba(124,192,255,0.55);
	      box-shadow: 0 0 0 2px rgba(124,192,255,0.15), inset 0 0 0 1px rgba(0,0,0,0.35);
	    }
	    .btn-hero:active{ transform: translateY(1px); }
	    .btn-hero .badge{
	      margin-left:5px; height:24px; min-width:24px; padding:0 6px; font-size:12px;
	      background:#2f7; color:#000;
	    }
	    .btn-hero.disabled { opacity:.6; cursor:default; }
	
	    /* ---------- Editing visuals ---------- */
	    .ag-theme-alpine .ag-cell-inline-editing { background: transparent !important; padding:0 !important; }
	    .ag-theme-alpine .ag-cell-inline-editing input,
	    .ag-theme-alpine .ag-cell-inline-editing textarea,
	    .ag-theme-alpine .ag-cell-inline-editing .ag-input-field-input,
	    .ag-theme-alpine .ag-cell-inline-editing .ag-text-field-input{
	      background: rgba(0,0,0,0.15) !important; color:#e9f4ff !important;
	      border:2px solid rgba(255,255,255,0.35) !important; border-radius:4px !important;
	      height:100% !important; width:100% !important; box-sizing:border-box !important; padding:0 6px !important;
	    }
	    .ag-theme-alpine .ag-cell-inline-editing input:focus,
	    .ag-theme-alpine .ag-cell-inline-editing textarea:focus,
	    .ag-theme-alpine .ag-cell-inline-editing .ag-input-field-input:focus,
	    .ag-theme-alpine .ag-cell-inline-editing .ag-text-field-input:focus{
	      border-color:#7cc0ff !important; box-shadow:0 0 0 2px rgba(124,192,255,0.25) !important;
	    }
	    .can-edit { text-decoration: underline dotted; text-underline-offset:3px; }
	
	    /* ===== NEW: highlight cells with unsent edits ===== */
	    .edited-cell{
	      background: rgba(124,192,255,.12) !important;
	      box-shadow: inset 0 0 0 2px rgba(124,192,255,.45);
	    }
	
	    /* ---------- Borders & layout ---------- */
	    .ag-cell, .ag-header-cell, .ag-header-group-cell { box-sizing:border-box; }
	    .ag-cell { border-right:1px solid rgba(255,255,255,0.28) !important; }
	    .ag-header-cell, .ag-header-group-cell { border-right:2px solid rgba(255,255,255,0.55) !important; }
	    .ag-center-cols-clipper .ag-row .ag-cell:last-child,
	    .ag-header-row .ag-header-cell:last-child { border-right:2px solid rgba(255,255,255,0.55) !important; }
	
	    .split-left { border-left:2px solid rgba(255,255,255,0.55) !important; }
	    .sep-left   { border-left:2px solid rgba(255,255,255,0.85) !important; }
	
	    .ag-header-viewport .ag-header-row.ag-header-group-row{ border-bottom:2px solid rgba(255,255,255,0.55) !important; }
	    .ag-header-viewport .ag-header-row:not(.ag-header-group-row){ border-bottom:2px solid rgba(255,255,255,0.55) !important; }
	    .ag-pinned-left-header .ag-header-row { border-bottom:2px solid rgba(255,255,255,0.55) !important; }
	
	    /* PINNED-LEFT: remove row separators */
	    .ag-theme-alpine .ag-pinned-left-cols-container .ag-row { border-bottom: none !important; }
	    .ag-theme-alpine .ag-pinned-left-cols-container .ag-row .ag-cell { border-bottom: none !important; }
	    .ag-theme-alpine .ag-pinned-left-cols-container .ag-row.row-final { border-bottom: 2px solid rgba(255,255,255,0.55) !important; }
	    .ag-theme-alpine .ag-pinned-left-cols-container .ag-row.row-final .ag-cell { border-bottom: none !important; }
	    
	    /* Remove row separators (all viewports) */
	    .ag-theme-alpine .ag-center-cols-container .ag-row,
	    .ag-theme-alpine .ag-center-cols-container .ag-row .ag-cell,
	    .ag-theme-alpine .ag-pinned-left-cols-container .ag-row,
	    .ag-theme-alpine .ag-pinned-left-cols-container .ag-row .ag-cell,
	    .ag-theme-alpine .ag-pinned-right-cols-container .ag-row,
	    .ag-theme-alpine .ag-pinned-right-cols-container .ag-row .ag-cell {
	      border-bottom: none !important;
	    }
	
	     /* Keep the strong separator only on the "final" rows */
	    .ag-theme-alpine .ag-center-cols-container .ag-row.row-final .ag-cell,
	    .ag-theme-alpine .ag-pinned-left-cols-container .ag-row.row-final .ag-cell,
	    .ag-theme-alpine .ag-pinned-right-cols-container .ag-row.row-final .ag-cell {
	     border-bottom: 2px solid rgba(255,255,255,0.55) !important;
	    }
	    
	    
	    .ag-header-viewport { border-bottom: 2px solid rgba(255,255,255,0.55) !important; }
	
	    .val-cell { padding:0 8px; }
	    .right { text-align:right; }
	
	    .ag-header { background:#0a1324; }
	    .ag-header-cell-label, .ag-header-group-cell-label { color:#cfe2ff; font-weight:600; }
	    .time-header { background:#0b162b; color:#cfe2ff; }
	    .center-header .ag-header-cell-label { justify-content:center; }
	    .hour-group .ag-header-group-cell-label{
	      display:flex!important; width:100%!important;
	      justify-content:center!important; align-items:center!important; padding-left:0!important; padding-right:0!important;
	      }
	    .hour-group .ag-header-group-text{ margin:0 auto!important; }
	
	    /* Row color coding */
	    .row-source-1 .ag-cell { background:#142233; color:#e8f0ff; }
	    .row-source-2 .ag-cell { background:#16283e; color:#e8f0ff; }
	    .row-source-3 .ag-cell { background:#1a304a; color:#e8f0ff; }
	    .row-avg    .ag-cell { background:#1e3a56; color:#e9f4ff; font-style:italic; }
	    .row-auto   .ag-cell { background:#203e5e; color:#e9f4ff; }
	    .row-manual .ag-cell { background:#234567; color:#e9f4ff; }
	    .row-final  .ag-cell { background:#2b4f7a; color:#fff; font-weight:700; border-bottom: 2px solid rgba(255,255,255,0.55) !important}
	    .row-total  .ag-cell { background:#0f172a; color:#fff; font-weight:700; }
	
	    /* farm bands (pinned-left only) */
	    .farm-a .ag-pinned-left-cols-container .ag-cell { background:#10243e; }
	    .farm-b .ag-pinned-left-cols-container .ag-cell { background:#0d1c33; }
	
	    .col-selected .ag-cell-wrapper { justify-content:center; }
	
	    /* Fill the blank area below the last row (all viewports) */
	    .ag-theme-alpine .ag-center-cols-viewport,
	    .ag-theme-alpine .ag-pinned-left-cols-viewport,
	    .ag-theme-alpine .ag-pinned-right-cols-viewport,
	    .ag-theme-alpine .ag-root-wrapper,
	    .ag-theme-alpine .ag-root-wrapper-body {
	      background-color: #142233 !important;
	    }
	
	    /* ===== Overlay colors ===== */
	    :root { --overlay-bg:#142233; --overlay-fg:#eaf2ff; }
	    .ag-theme-alpine .ag-overlay-wrapper { background-color: var(--overlay-bg) !important; }
	    .ag-theme-alpine .ag-overlay-no-rows-center,
	    .ag-theme-alpine .ag-overlay-loading-center {
	      background: transparent !important;
	      color: var(--overlay-fg) !important;
	      border: none !important;
	      box-shadow: none !important;
	      font-weight: 600;
	    }
	    .ag-theme-alpine .ag-center-cols-viewport,
	    .ag-theme-alpine .ag-pinned-left-cols-viewport,
	    .ag-theme-alpine .ag-pinned-right-cols-viewport {
	      background-color: var(--overlay-bg) !important;
	    }
	
	    /* ===== modal (loading & result) ===== */
	    .modal {
	      position: fixed; inset: 0;
	      background: rgba(0,0,0,.45);
	      display: none;
	      align-items: center; justify-content: center;
	      z-index: 9999;
	    }
	    .modal.show { display: flex; }
	
	    .modal-box {
	      min-width: 360px; max-width: 640px;
	      padding: 18px 20px;
	      border-radius: 10px;
	      background: #0c0c0f;
	      color: #eaf2ff;
	      border: 1px solid rgba(124,192,255,.35);
	      box-shadow: 0 10px 40px rgba(0,0,0,.45);
	      font: 14px/1.4 system-ui,-apple-system,Segoe UI,Roboto,Arial;
	    }
	    .modal-title { font-weight: 700; margin-bottom: 8px; }
	    .modal-body  { white-space: pre-wrap; margin: 8px 0 14px; }
	    .modal-actions { display:flex; justify-content:flex-end; gap:8px; }
	    .modal-btn {
	      padding: 8px 12px; border-radius: 8px;
	      border: 1px solid rgba(255,255,255,.25);
	      background:#1b2a45; color:#fff; cursor:pointer;
	    }
	    .modal-btn[disabled] { opacity:.6; cursor:default; }
	
	    .spinner {
	      width: 28px; height: 28px; border-radius: 50%;
	      border: 3px solid rgba(124,192,255,.35);
	      border-top-color: #7cc0ff;
	      animation: spin .8s linear infinite;
	      margin-right: 8px;
	    }
	    @keyframes spin { to { transform: rotate(360deg); } }
	    .modal-row { display:flex; align-items:center; gap:10px; }
	  </style>
	</head>
	<body>
	  <div class="page">
	    <header class="topbar">
	      <button id="btnApply" class="btn btn-hero apply-btn">
	        Apply now <span id="badge" class="badge">0</span>
	      </button>
	      <div id="qs" style="margin-left:auto;opacity:.7"></div>
	    </header>
	
	    <div id="grid" class="ag-theme-alpine"></div>
	  </div>
	
	  <!-- Modal -->
	  <div id="modal" class="modal" aria-hidden="true">
	    <div class="modal-box">
	      <div class="modal-title" id="modalTitle">Saving...</div>
	      <div class="modal-body"  id="modalBody">
	        <div class="modal-row"><div class="spinner"></div><div>Sending data to database…</div></div>
	      </div>
	      <div class="modal-actions">
	        <button id="modalClose" class="modal-btn" style="display:none;">Close</button>
	      </div>
	    </div>
	  </div>
	
	  <script>
	  (function(){
	    /* --------- URLs --------- */
	    var DATA_URL = "data{QS}";
	    var _m = (location.pathname.match(/\\/system\\/webdev\\/([^\\/]+)/) || []);
	    var PROJECT   = _m[1] || "the_project_1";
	    var APPLY_URL = "/system/webdev/" + PROJECT + "/api/forecast/applyCells";
	
	    /* ===== modal helpers ===== */
	    function showLoading(message){
	      var m  = document.getElementById("modal");
	      var t  = document.getElementById("modalTitle");
	      var b  = document.getElementById("modalBody");
	      var cl = document.getElementById("modalClose");
	      t.textContent = "Saving...";
	      b.innerHTML = '<div class="modal-row"><div class="spinner"></div><div>' +
	                    (message || 'Sending data to database...') + '</div></div>';
	      cl.style.display = "none";
	      m.classList.add("show");
	    }
	    function showResult(title, text){
	      var m  = document.getElementById("modal");
	      var t  = document.getElementById("modalTitle");
	      var b  = document.getElementById("modalBody");
	      var cl = document.getElementById("modalClose");
	      t.textContent = title || "Done";
	      b.textContent = text || "";
	      cl.style.display = "inline-block";
	      cl.onclick = function(){ m.classList.remove("show"); };
	    }
	    function hideModal(){ document.getElementById("modal").classList.remove("show"); }
	
	    /* --------- NEW: read sources from querystring (CSV / JSON / Python style) --------- */
	    var sp = new URLSearchParams(location.search);
	
	    function parseSources(raw){
	      if (!raw) return [];
	      raw = decodeURIComponent(String(raw)).trim();
	
	      // "<ArrayWrapper>: [u'source_3', u'avg_sources', ...]"
	      if (raw.indexOf("[") !== -1 && raw.indexOf("]") !== -1 && /[uU]?'[^']+'/.test(raw)) {
	        var inside = raw.slice(raw.indexOf("["), raw.lastIndexOf("]") + 1);
	        var out = [], re = /['"]([^'"]+)['"]/g, m;
	        while ((m = re.exec(inside))) out.push(m[1]);
	        return out;
	      }
	      // JSON array
	      if (raw.charAt(0) === "[" && raw.charAt(raw.length - 1) === "]") {
	        try { var a = JSON.parse(raw); if (Array.isArray(a)) return a; } catch(e){}
	      }
	      // CSV
	      return raw.split(",").map(function(s){return (s||"").trim();}).filter(function(s){return !!s;});
	    }
	
	    var rawSources = (sp.get("sources") || sp.get("forecast_source_filter") || "");
	    var sourcesArr = parseSources(rawSources);
	    var selectedSet = new Set(sourcesArr.map(function(s){ return String(s).toLowerCase(); }));
	    var hasExternalSelection = selectedSet.size > 0;
	
	    var qsEl = document.getElementById("qs");
	    var DEBUG = (sp.get("debug") === "1");
	    if (qsEl) {
	      if (DEBUG && sourcesArr.length) {
	        qsEl.textContent = "sources=" + sourcesArr.join(",");
	        qsEl.style.display = "block";
	      } else {
	        qsEl.style.display = "none";
	      }
	    }
	
	    /* --------- helpers --------- */
	    function minuteLabel(hhmm){ var m=(hhmm||"").split(":")[1]||""; return m ? (m + "'") : hhmm; }
	    function hourGroup(hhmm){ var h=(hhmm||"").split(":")[0]||""; return h ? String(parseInt(h,10)) : hhmm; }
	    function num(v){
	      if (v == null) return 0;
	      if (typeof v === "number") return v;
	      var s = String(v).replace(/\\u00A0/g,"").replace(/\\s+/g,"");
	      var n = parseFloat(s.replace(/[^0-9.\\-]/g,""));
	      return isNaN(n) ? 0 : n;
	    }
	    function normalizeRows(payload){
	      if (payload && Array.isArray(payload.columns) && Array.isArray(payload.rows)){
	        var cols = payload.columns;
	        return payload.rows.map(function(r){ var o={}; for (var i=0;i<cols.length;i++) o[cols[i]] = r[i]; return o; });
	      }
	      if (payload && Array.isArray(payload.records)) return payload.records;
	      if (payload && Array.isArray(payload.json))    return payload.json;
	      if (Array.isArray(payload)) return payload;
	      return [];
	    }
	    function groupKey(d){ return [d.date, d.farm_name, d.status_name].join("|"); }
	
	    /* farm class alternation for left band */
	    var farmPalette=["farm-a","farm-b"], farmClassMap={};
	    function getFarmClass(name){
	      if(!name) return "";
	      if(!farmClassMap.hasOwnProperty(name)){
	        var idx = Object.keys(farmClassMap).length % farmPalette.length;
	        farmClassMap[name] = farmPalette[idx];
	      }
	      return farmClassMap[name];
	    }
	
	    /* --------- pending edits (dedup by site|farm|date|field) --------- */
	    var PENDING_MAP = new Map();
	    function pendingKey(row, field){
	      var m = String(row.date||"").match(/^(\\d{2})-(\\d{2})-(\\d{4})$/);
	      var iso = m ? (m[3]+"-"+m[2]+"-"+m[1]) : "";
	      return [Number(row.siteid)||0, Number(row.farmid)||0, iso, field].join("|");
	    }
	    function badge(n){ var el=document.getElementById("badge"); if(el){ el.textContent=String(n||0); } }
	
	    /* --------- ag-Grid setup --------- */
	    var knownTimeCols=[];
	    var gridOptions = {
	      defaultColDef: { sortable:true, filter:true, resizable:true, suppressSizeToFit:true, editable:false },
	      singleClickEdit:true,
	      stopEditingWhenCellsLoseFocus:true,
	      rowSelection:"multiple",
	      animateRows:true,
	      pagination:true,
	      paginationPageSize:50,
	      suppressColumnMoveAnimation:true,
	      suppressAggFuncInHeader:true,
	      suppressCellFocus:true,
	
	      rowClassRules:{
	        'row-source-1': function(p){ return p.data && String(p.data.Source_name||'').toLowerCase()==='source_1'; },
	        'row-source-2': function(p){ return p.data && String(p.data.Source_name||'').toLowerCase()==='source_2'; },
	        'row-source-3': function(p){ return p.data && String(p.data.Source_name||'').toLowerCase()==='source_3'; },
	        'row-avg':      function(p){ return p.data && String(p.data.Source_name||'').toLowerCase()==='avg_sources'; },
	        'row-auto':     function(p){ return p.data && String(p.data.Source_name||'').toLowerCase()==='auto_correction'; },
	        'row-manual':   function(p){ return p.data && String(p.data.Source_name||'').toLowerCase()==='manual_correction'; },
	        'row-final':    function(p){ return p.data && String(p.data.Source_name||'').toLowerCase()==='final_forecast'; },
	        'row-total':    function(p){ return p.data && String(p.data.Source_name||'').toLowerCase()==='total_general'; },
	        'farm-a':       function(p){ return p.data && getFarmClass(p.data.farm_name)==='farm-a'; },
	        'farm-b':       function(p){ return p.data && getFarmClass(p.data.farm_name)==='farm-b'; }
	      },
	
	      /* ====== UPDATED: collect edits + toggle highlight ====== */
	      onCellValueChanged: function(p){
	        var f = p.colDef && p.colDef.field;
	        var isTime = /^\\d{2}:\\d{2}$/.test(f||"");
	        var row = p.data || {};
	        var source = String(row.Source_name||"").toLowerCase();
	        if (!isTime || source !== "manual_correction") return;
	
	        var raw = p.newValue;
	        var key = pendingKey(row, f);
	
	        // If value cleared -> drop pending + refresh highlight
	        if (raw == null || String(raw).trim()===""){
	          if (PENDING_MAP.has(key)) {
	            PENDING_MAP.delete(key);
	            badge(PENDING_MAP.size);
	            if (p.api && p.node) p.api.refreshCells({rowNodes:[p.node], columns:[f], force:true});
	          }
	          var gk = groupKey(row);
	          setTimeout(function(){ recomputeForKey(gk); recomputeTotals(); },0);
	          return;
	        }
	
	        var v = Number(String(raw).replace(/\\s+/g,"").replace(",", "."));
	        if (!isFinite(v)) return;
	
	        // Store/overwrite pending edit
	        var m = String(row.date||"").match(/^(\\d{2})-(\\d{2})-(\\d{4})$/);
	        var iso = m ? (m[3]+"-"+m[2]+"-"+m[1]) : "";
	
	        PENDING_MAP.set(key, {
	          siteid: Number(row.siteid)||0,
	          farmid: Number(row.farmid)||0,
	          date:   iso,     // yyyy-MM-dd
	          field:  f,       // HH:mm
	          value:  v
	        });
	        badge(PENDING_MAP.size);
	
	        // Refresh just this cell so the class flips instantly
	        if (p.api && p.node) p.api.refreshCells({rowNodes:[p.node], columns:[f], force:true});
	
	        var gk = groupKey(row);
	        setTimeout(function(){ recomputeForKey(gk); recomputeTotals(); },0);
	      }
	    };
	
	    var gridDiv=document.getElementById("grid");
	    var gridApi, columnApi;
	    if (agGrid.createGrid){
	      gridApi = agGrid.createGrid(gridDiv, gridOptions);
	      columnApi = (gridApi.getColumnApi && gridApi.getColumnApi()) || gridApi.columnApi || null;
	    } else {
	      new agGrid.Grid(gridDiv, gridOptions);
	      gridApi = gridOptions.api; columnApi = gridOptions.columnApi;
	    }
	
	    function setColumnDefs(colDefs){
	      if (gridApi && gridApi.setGridOption) gridApi.setGridOption("columnDefs", colDefs);
	      else if (gridOptions.api) gridOptions.api.setColumnDefs(colDefs);
	    }
	    function setRowData(rows){
	      if (gridApi && gridApi.setGridOption) gridApi.setGridOption("rowData", rows);
	      else if (gridOptions.api) gridOptions.api.setRowData(rows);
	    }
	    function setPinnedTopRowData(rows){
	      if (gridApi && gridApi.setGridOption) gridApi.setGridOption('pinnedTopRowData', rows);
	      else if (gridOptions.api) gridOptions.api.setPinnedTopRowData(rows);
	    }
	
	    /* --- recompute logic --- */
	    var groupMap={}, totalNode=null;
	
	    function forEachPinnedTop(cb){
	      if (!gridApi || !gridApi.getPinnedTopRowCount) return;
	      var n = gridApi.getPinnedTopRowCount();
	      for (var i=0;i<n;i++){ var rn = gridApi.getPinnedTopRow(i); if (rn) cb(rn); }
	    }
	
	    function rebuildMaps(){
	      groupMap={}; totalNode=null;
	
	      gridApi.forEachNode(function(node){
	        var r=node.data||{}, s=String(r.Source_name||"").toLowerCase();
	        if (s==="total_general"){ totalNode=node; return; }
	        var key=groupKey(r);
	        var g=groupMap[key]||(groupMap[key]={sources:{},avg:null,auto:null,manual:null,final:null});
	        if (s==="source_1") g.sources[1]=node;
	        else if (s==="source_2") g.sources[2]=node;
	        else if (s==="source_3") g.sources[3]=node;
	        else if (s==="avg_sources") g.avg=node;
	        else if (s==="auto_correction") g.auto=node;
	        else if (s==="manual_correction") g.manual=node;
	        else if (s==="final_forecast") g.final=node;
	      });
	
	      forEachPinnedTop(function(node){
	        var r=node.data||{}, s=String(r.Source_name||"").toLowerCase();
	        if (s==="total_general"){ totalNode=node; return; }
	        var key=groupKey(r);
	        var g=groupMap[key]||(groupMap[key]={sources:{},avg:null,auto:null,manual:null,final:null});
	        if (s==="source_1") g.sources[1]=node;
	        else if (s==="source_2") g.sources[2]=node;
	        else if (s==="source_3") g.sources[3]=node;
	        else if (s==="avg_sources") g.avg=node;
	        else if (s==="auto_correction") g.auto=node;
	        else if (s==="manual_correction") g.manual=node;
	        else if (s==="final_forecast") g.final=node;
	      });
	    }
	
	    function recomputeForKey(key){
	      var g=groupMap[key]; if(!g) return;
	
	      if (g.avg && g.avg.data){
	        var avgRow=g.avg.data;
	        var srcNodes=[g.sources[1],g.sources[2],g.sources[3]].filter(function(n){return n && n.data && n.data.selected;});
	        knownTimeCols.forEach(function(col){
	          var vals=srcNodes.map(function(n){return num(n.data[col]);});
	          var mean=vals.length ? vals.reduce(function(a,b){return a+b;},0)/vals.length : 0;
	          avgRow[col]=Math.round(mean);
	        });
	        gridApi.refreshCells({rowNodes:[g.avg], columns:knownTimeCols, force:true});
	      }
	
	      if (g.final && g.final.data){
	        var finalRow=g.final.data;
	        knownTimeCols.forEach(function(col){
	          var sum=0;
	          if (g.avg    && g.avg.data.selected)    sum+=num(g.avg.data[col]);
	          if (g.auto   && g.auto.data.selected)   sum+=num(g.auto.data[col]);
	          if (g.manual && g.manual.data.selected) sum+=num(g.manual.data[col]);
	          finalRow[col]=Math.round(sum);
	        });
	        gridApi.refreshCells({rowNodes:[g.final], columns:knownTimeCols, force:true});
	      }
	    }
	
	    function recomputeTotals(){
	      if(!totalNode) return;
	      var totals={}; knownTimeCols.forEach(function(c){ totals[c]=0; });
	
	      gridApi.forEachNode(function(node){
	        var r=node.data||{};
	        if (String(r.Source_name||"").toLowerCase()==="final_forecast"){
	          knownTimeCols.forEach(function(c){ totals[c]+=num(r[c]); });
	        }
	      });
	      forEachPinnedTop(function(node){
	        var r=node.data||{};
	        if (String(r.Source_name||"").toLowerCase()==="final_forecast"){
	          knownTimeCols.forEach(function(c){ totals[c]+=num(r[c]); });
	        }
	      });
	
	      knownTimeCols.forEach(function(c){ totalNode.data[c]=Math.round(totals[c]); });
	      gridApi.refreshCells({rowNodes:[totalNode], columns:knownTimeCols, force:true});
	    }
	
	    function recomputeAll(){ rebuildMaps(); for (var k in groupMap){ if (groupMap.hasOwnProperty(k)) recomputeForKey(k); } recomputeTotals(); }
	
	    function buildColumnDefs(rows,payload){
	      var cols = (payload && Array.isArray(payload.columns) && Array.isArray(payload.rows) && payload.columns.length)
	        ? payload.columns.slice(0)
	        : (rows[0] ? Object.keys(rows[0]) : []);
	      knownTimeCols = cols.filter(function(c){return /^\\d{2}:\\d{2}$/.test(c);}).sort();
	      var firstTimeCol = knownTimeCols[0]||null;
	
	      var pinnedChildren = [
	        { field:"site_name", headerName:"Site", pinned:"left", hide:true, width:110, minWidth:110 },
	        { field:"farm_name", headerName:"Farm", pinned:"left", width:140, minWidth:140 },
	        { field:"status_name", headerName:"Status", pinned:"left", width:110, minWidth:100 },
	        {
	          colId:"selected", headerName:"", pinned:"left",
	          width:49, minWidth:49, maxWidth:49, suppressMenu:true, sortable:false, filter:false,
	          headerClass:"col-selected center-header", cellClass:"col-selected",
	          valueGetter:function(p){
	            var s=String(p.data && p.data.Source_name || "").toLowerCase();
	            if (s==="final_forecast" || s==="total_general") return null;
	            return !!(p.data && p.data.selected);
	          },
	          cellRenderer:function(params){
	            var s=String(params.data && params.data.Source_name || "").toLowerCase();
	            if (s==="final_forecast" || s==="total_general") return document.createElement("span");
	            var el=document.createElement("input");
	            el.type="checkbox"; el.checked=!!params.value;
	            el.addEventListener("click",function(e){
	              e.stopPropagation();
	              var v=el.checked;
	              if (params.node && params.node.data) params.node.data.selected=v;
	              if (params.node && params.node.setDataValue) params.node.setDataValue("selected", v);
	              var key=[params.data.date, params.data.farm_name, params.data.status_name].join("|");
	              setTimeout(function(){ recomputeForKey(key); recomputeTotals(); },0);
	            });
	            return el;
	          }
	        },
	        { field:"Source_name", headerName:"Source_name", pinned:"left", width:150, minWidth:150 }
	      ];
	      var pinnedGroup = { headerName:"", marryChildren:true, children:pinnedChildren };
	
	      var maybeIds=[]; ["siteid","farmid"].forEach(function(f){ if (cols.indexOf(f)>=0) maybeIds.push({field:f, hide:true}); });
	
	      var groupsMap={}; knownTimeCols.forEach(function(f){ var g=hourGroup(f); (groupsMap[g]=groupsMap[g]||[]).push(f); });
	      var hourKeys=Object.keys(groupsMap).sort(function(a,b){return parseInt(a,10)-parseInt(b,10);});
	
	      var grouped = hourKeys.map(function (g, groupIdx) {
	        var children = groupsMap[g].sort().map(function (field, childIdx) {
	          var isFirstMinuteOfThisHour = (childIdx === 0);
	          var addHourSeparator       = isFirstMinuteOfThisHour && groupIdx > 0;
	          var isFirstTimeColOverall  = (field === firstTimeCol);
	          var extraCls = (isFirstTimeColOverall ? " split-left" : "") + (addHourSeparator ? " sep-left" : "");
	
	          function isManualRow(row){
	            return String((row && row.Source_name) || "").toLowerCase() === "manual_correction";
	          }
	          return {
	            field: field,
	            headerName: minuteLabel(field),
	            headerClass: "time-header center-header" + extraCls,
	
	            /* ====== UPDATED: inject edited-cell when pending ====== */
	            cellClass: function (p) {
	              var base = "val-cell right" + extraCls;
	              var isManual = isManualRow(p.data);
	              if (!isManual) return base;
	              var edited = false;
	              try {
	                var k = pendingKey(p.data, field);
	                edited = PENDING_MAP && PENDING_MAP.has && PENDING_MAP.has(k);
	              } catch(_) {}
	              return base + " can-edit" + (edited ? " edited-cell" : "");
	            },
	
	            filter: "agNumberColumnFilter",
	            width: 100, minWidth: 110,
	            editable: function (p) {
	              var isManual = String((p.data && p.data.Source_name) || "").toLowerCase() === "manual_correction";
	              return isManual && !(p && p.node && p.node.rowPinned);
	            },
	            valueParser: function (p) {
	              var s = String(p.newValue == null ? "" : p.newValue)
	                        .replace(/\\u00A0/g, "")
	                        .replace(/\\s+/g, "")
	                        .replace(",", ".");
	              var n = parseFloat(s);
	              return isNaN(n) ? null : n;
	            },
	            valueFormatter: function (p) { return num(p.value).toLocaleString(); }
	          };
	        });
	
	        return {
	          headerName: g,
	          headerClass: "center-group time-header hour-group",
	          marryChildren: true,
	          children: children
	        };
	      });
	
	      return [pinnedGroup].concat(maybeIds).concat(grouped);
	    }
	
	    /* --------- snapshot of computed rows to send --------- */
	    function snapshotComputedRows(){
	      var wanted = new Set(["avg_sources","auto_correction","final_forecast"]);
	      var rows = [];
	
	      function toISO(d){
	        if (!d || d.length!==10) return d||"";
	        if (d[4]==="-" && d[7]==="-") return d;
	        if (d[2]==="-" && d[5]==="-"){ var dd=d.slice(0,2), mm=d.slice(3,5), yy=d.slice(6,10); return yy+"-"+mm+"-"+dd; }
	        return d;
	      }
	
	      function grab(node){
	        if(!node || !node.data) return;
	        var src = String(node.data.Source_name||"").toLowerCase();
	        if(!wanted.has(src)) return;
	        if (src !== "final_forecast" && !node.data.selected) return; // obey checkboxes
	
	        var r = {
	          id: node.data.id,
	          date: toISO(node.data.date),
	          siteid: node.data.siteid,
	          farmid: node.data.farmid,
	          Source_name: node.data.Source_name
	        };
	        for (var i=0;i<knownTimeCols.length;i++){
	          var c = knownTimeCols[i];
	          var v = node.data[c];
	          if (v == null || v === "") continue;
	          r[c] = (typeof v === "number") ? v : Number(String(v).replace(/\\s+/g,"").replace(",", "."));
	        }
	        rows.push(r);
	      }
	
	      gridApi.forEachNode(grab);
	      if (gridApi.getPinnedTopRowCount){
	        for (var i=0; i<gridApi.getPinnedTopRowCount(); i++){
	          grab(gridApi.getPinnedTopRow(i));
	        }
	      }
	      return rows;
	    }
	
	    /* --------- Apply ALL: manual edits + computed rows --------- */
	    function applyAll(){
	      gridApi.stopEditing();
	
	      var btn = document.getElementById("btnApply");
	      if (btn){ btn.disabled = true; btn.classList.add("disabled"); }
	
	      try{
	        gridApi.setGridOption && gridApi.setGridOption('suppressAnimationFrame', true);
	        gridApi.setGridOption && gridApi.setGridOption('suppressRowTransform',  true);
	      }catch(_){}
	
	      var edits = Array.from((PENDING_MAP && PENDING_MAP.values()) || []);
	      var rows  = snapshotComputedRows();
	
	      if (!edits.length && !rows.length){
	        showResult("Nothing to save","There are no manual edits or computed rows to send.");
	        document.getElementById("modal").classList.add("show");
	        try{
	          gridApi.setGridOption && gridApi.setGridOption('suppressAnimationFrame', false);
	          gridApi.setGridOption && gridApi.setGridOption('suppressRowTransform',  false);
	        }catch(_){}
	        if (btn){ btn.disabled = false; btn.classList.remove("disabled"); }
	        return;
	      }
	
	      var payload = { edits: edits, rows: rows, timeCols: knownTimeCols.slice() };
	
	      // show loading modal
	      showLoading("Sending edits and computed rows");
	
	      fetch(APPLY_URL, {
	        method: "POST",
	        headers: { "Content-Type": "application/json" },
	        body: JSON.stringify(payload),
	        credentials: "same-origin"
	      })
	      .then(function(r){
	        return r.json();
	      })
	      .then(function(res){
	        var msg = [
	          "Manual saved " + (res.saved_manual||0) + ", skipped " + (res.skipped_manual||0),
	          "Computed saved " + (res.saved_calc||0)   + ", skipped " + (res.skipped_calc||0)
	        ].join("\\n");
	
	        // Clear pending + badge + remove highlights
	        PENDING_MAP.clear();
	        badge(0);
	        if (gridApi && gridApi.refreshCells) { gridApi.refreshCells({force:true}); }
	
	        showResult("Save complete", msg);
	      })
	      .catch(function(err){
	        console.error("Apply ALL error:", err);
	        showResult("Error", "Apply failed:\\n" + (err && err.message ? err.message : String(err)));
	      })
	      .finally(function(){
	        try{
	          gridApi.setGridOption && gridApi.setGridOption('suppressAnimationFrame', false);
	          gridApi.setGridOption && gridApi.setGridOption('suppressRowTransform',  false);
	        }catch(_){}
	        if (btn){ btn.disabled = false; btn.classList.remove("disabled"); }
	      });
	    }
	    document.getElementById("btnApply").addEventListener("click", applyAll);
	
	    /* --------- load & render --------- */
	    fetch(DATA_URL, {credentials:"same-origin"})
	      .then(function(r){ if(!r.ok) throw new Error("HTTP "+r.status); return r.json(); })
	      .then(function(payload){
	        var rows = normalizeRows(payload);
	
	        rows.forEach(function(r){ getFarmClass(r.farm_name); });
	
	        /* --------- preselect using querystring 'sources' --------- */
	        rows.forEach(function(r){
	          var src = String(r.Source_name||"").toLowerCase();
	          var defaultSelected = (src!=="final_forecast" && src!=="total_general");
	          r.selected = hasExternalSelection ? selectedSet.has(src) : defaultSelected;
	          if (src==="final_forecast" || src==="total_general") r.selected = false;
	        });
	
	        var colDefs = buildColumnDefs(rows, payload||{});
	        setColumnDefs(colDefs);
	
	        var pinned = rows.length ? [rows[0]] : [];
	        var body   = rows.length ? rows.slice(1) : [];
	        setPinnedTopRowData(pinned);
	        setRowData(body);
	
	        setTimeout(function(){ recomputeAll(); if (gridApi.redrawRows) gridApi.redrawRows(); },0);
	      })
	      .catch(function(err){
	        document.getElementById("grid").innerHTML =
	          '<pre style="padding:8px;color:#c00">Load error: ' + String(err) + '</pre>';
	        console.error(err);
	      });
	  })();
	  </script>
	</body>
	</html>
	""".replace("{QS}", qs_string)
	
	return {"html": html}