def doGet(request, session):
	# --- keep query params (e.g., ?day=YYYY-MM-DD) ---
	qs = request.get("params") or {}
	qs_string = "?" + "&".join(["%s=%s" % (k, v) for k, v in qs.items()]) if qs else ""
	current_day = qs.get("day") or system.date.format(system.date.now(), "yyyy-MM-dd")
	
	base_local = "./v34"
	base_cdn   = "https://cdn.jsdelivr.net/npm/ag-grid-community@34.2.0/dist"
	
	html = u"""
	<!doctype html>
	<html>
	<head>
	  <meta charset="utf-8"/>
	  <title>24-hour Output Matrix</title>
	  <meta name="viewport" content="width=device-width, initial-scale=1"/>
	
	  <!-- AG Grid (local first, CDN fallback) -->
	  <link rel="stylesheet" href="%(css0)s">
	  <link rel="stylesheet" href="%(theme0)s">
	  <script src="%(js0)s"></script>
	
	  <link rel="stylesheet" href="%(css1)s">
	  <link rel="stylesheet" href="%(theme1)s">
	  <script src="%(js1)s"></script>
	
	  <style>
	    :root{
	      /* >>> Change these to recolor the lines <<< */
	      --divider-color: rgba(207,226,255,.28);    /* thick horizontal block dividers */
	      --col-divider-color: rgba(255,255,255,.10);/* thin vertical column lines     */
	    }
	
	    html, body { height:100%%; margin:0; background:#0b1220; }
	    body { color:#eaf2ff; font:14px/1.35 system-ui,-apple-system,Segoe UI,Roboto,Arial; }
	    .page { height:100vh; width:100vw; display:flex; flex-direction:column; }
	
	    .topbar{
	      position:sticky; top:0; z-index:5; background:#0d1628;
	      padding:10px 14px; border-bottom:3px solid rgba(207,226,255,.25);
	      display:flex; gap:12px; align-items:center;
	    }
	    .title{ font-weight:700; opacity:.92; color:#eaf2ff; }
	    .spacer{ flex:1 1 auto; }
	    .status{ font-size:12px; opacity:.75; background:#24324a; padding:2px 6px; border-radius:6px; }
	
	    .controls{ display:flex; gap:8px; align-items:center; }
	    .controls label{ font-size:12px; opacity:.8; }
	    .controls input[type="date"]{
	      background:#0f1a30; color:#eaf2ff; border:1px solid rgba(207,226,255,.25);
	      padding:6px 8px; border-radius:6px; outline:none;
	    }
	    .controls button{
	      background:#1e2a44; color:#eaf2ff; border:1px solid rgba(207,226,255,.35);
	      padding:6px 10px; border-radius:6px; cursor:pointer;
	    }
	    .controls button:hover{ background:#24324a; }
	
	    #grid { flex:1 1 auto; min-height:0; width:100%%; }
	
	    /* AG Alpine theming */
	    .ag-theme-alpine {
	      --ag-background-color: #101a30;
	      --ag-foreground-color: #eaf2ff;
	      --ag-header-foreground-color: #dbe7ff;
	      --ag-header-background-color: #0e172b;
	      --ag-row-border-color: rgba(255,255,255,.06);
	      --ag-border-color: rgba(255,255,255,.06);
	      --ag-header-column-separator-color: var(--col-divider-color);
	      --ag-header-column-separator-width: 1px;
	      --ag-font-size: 14px;
	    }
	    .ag-theme-alpine .ag-cell { color:#eaf2ff !important; }
	    .ag-theme-alpine .ag-header-cell-text { color:#dbe7ff !important; }
	    .ag-theme-alpine .ag-header { border-bottom:3px solid rgba(207,226,255,.25) !important; }
	
	    /* ========= VERTICAL COLUMN LINES =========
	       Header + body subtle right-side separators for each column. */
	    .ag-theme-alpine .ag-header-cell,
	    .ag-theme-alpine .ag-header-group-cell {
	      /*border-right: 1px solid var(--col-divider-color) !important*/;
	    }
	    .ag-theme-alpine .ag-center-cols-container .ag-cell {
	      border-right: 1px solid var(--col-divider-color) !important;
	      /* avoid bright white borders from default focus */
	      border-top-color: rgba(255,255,255,.06) !important;
	      border-bottom-color: rgba(255,255,255,.06) !important;
	      border-left-color: transparent !important;
	    }
	
	    /* KPI pinned divider (visible freeze border) */
	    .ag-theme-alpine .ag-pinned-left-header,
	    .ag-theme-alpine .ag-pinned-left-cols-container {
	      border-right: 1px solid rgba(98,149,199,.55) !important;
	      box-shadow: 1px 0 0 rgba(98,149,199,.25);
	    }
	
	    /* Gentle banding */
	    .ag-theme-alpine .ag-row:nth-child(odd) .ag-cell { background:#0f1a30; }
	    .ag-theme-alpine .ag-row:nth-child(even) .ag-cell { background:#102038; }
	    .ag-theme-alpine .ag-row-hover .ag-cell { background:#152848 !important; }
	
	    /* KPI column look */
	    .kpi { font-weight:600; background:#0e1a30 !important; }
	    .hcenter .ag-header-cell-label { justify-content:center; }
	    .right { text-align:right; }
	
	    .ag-header-cell-menu-button, .ag-header-icon { display:none !important; }
	    .ag-theme-alpine .ag-cell-focus,
	    .ag-theme-alpine .ag-cell-no-focus { border:1px solid transparent !important; }
	
	    /* ===== THICK HORIZONTAL BLOCK DIVIDER LINES =====
	       Apply on the row that STARTS a block (via getRowClass). */
	    .ag-theme-alpine .ag-row.dividerTop .ag-cell {
	      border-top: 2px solid var(--divider-color) !important;
	      box-shadow: inset 0 1px 0 var(--divider-color);
	    }
	  </style>
	</head>
	<body>
	  <div class="page">
	    <div class="topbar">
	      <span class="title">24-hour Output Matrix</span>
	      <div class="spacer"></div>
	      <div class="controls">
	        <label for="day">Date</label>
	        <input id="day" type="date" value="%(curday)s"/>
	        <button id="apply">Apply</button>
	      </div>
	      <span class="status" id="stat">loading…</span>
	    </div>
	    <div id="grid" class="ag-theme-alpine"></div>
	  </div>
	
	  <script>
	  (function(){
	    var STAT = document.getElementById("stat");
	    var DATA_URL = "data%(QS)s";
	    function setStat(s){ STAT.textContent = s; }
	
	    // Date control -> reload keeping other params
	    function updateQueryAndReload(newDay){
	      var url = new URL(window.location.href);
	      if(newDay){ url.searchParams.set("day", newDay); }
	      window.location.href = url.pathname + "?" + url.searchParams.toString();
	    }
	    document.getElementById("apply").addEventListener("click", function(){
	      var v = document.getElementById("day").value;
	      if(v){ updateQueryAndReload(v); }
	    });
	    document.getElementById("day").addEventListener("keypress", function(e){
	      if(e.key === "Enter"){ document.getElementById("apply").click(); }
	    });
	
	    function ready(cb){
	      var t=0;(function spin(){
	        if (window.agGrid && (agGrid.createGrid || agGrid.Grid)) return cb();
	        if (++t>120){ setStat("AG Grid not loaded"); return; }
	        setTimeout(spin,50);
	      })();
	    }
	
	    function num(v){
	      if (v == null || v === "") return 0;
	      if (typeof v === "number") return v;
	      var s = String(v).replace(/\\u00A0/g,"").replace(/\\s+/g,"").replace(",", ".");
	      var n = parseFloat(s);
	      return isNaN(n) ? 0 : n;
	    }
	    function fmt(p){ return num(p.value).toLocaleString(); }
	
	    function buildCols(cols){
	      return cols.map(function(c, idx){
	        var name = String(c);
	        if (idx === 0 || name.toUpperCase()==="KPI"){
	          return {
	            field:name, headerName:name, pinned:"left",
	            width: 340, minWidth:280, cellClass:"kpi",
	            suppressHeaderMenuButton:true, headerClass:"hcenter"
	          };
	        }
	        return {
	          field:name, headerName:name, width:94, minWidth:84,
	          valueFormatter: fmt, cellClass:"right",
	          suppressHeaderMenuButton:true, headerClass:"hcenter"
	        };
	      });
	    }
	
	    ready(function(){
	      setStat("fetching data…");
	      fetch(DATA_URL, {credentials:"same-origin"})
	        .then(function(r){ if(!r.ok) throw new Error("HTTP "+r.status); return r.json(); })
	        .then(function(payload){
	          var cols = (payload && payload.columns) || [];
	          var rows = (payload && payload.rows) || [];
	
	          // === Build the divider set (row-block separators) ===
	          // Draw a thick line AFTER these KPIs → i+1 row gets the top border.
	          var divideAfter = new Set([
	            "BESS Charge mFRR dw",
	            "BESS AN MFRR reservation dw",
	            "Band out GAS",
	            "EBand out GAS"
	          ]);
	
	          var dividerRowIdx = new Set();
	          for (var i=0;i<rows.length;i++){
	            var k = String(rows[i].KPI || rows[i].kpi || "").trim();
	            if (divideAfter.has(k)) dividerRowIdx.add(i+1);
	          }
	
	          var gridDiv = document.getElementById("grid");
	          var gridOptions = {
	            defaultColDef: { resizable:true, sortable:false, filter:false, suppressHeaderMenuButton:true },
	            columnDefs: buildCols(cols),
	            rowData: rows,
	            rowHeight: 38,
	            headerHeight: 42,
	            animateRows:true,
	            suppressCellFocus:true,
	            suppressMenuHide:true,
	
	            // add CSS class to the row that starts a block
	            getRowClass: function(params){
	              return dividerRowIdx.has(params.rowIndex) ? "dividerTop" : null;
	            }
	          };
	
	          var gridApi;
	          if (agGrid.createGrid){
	            gridApi = agGrid.createGrid(gridDiv, gridOptions);
	          } else {
	            new agGrid.Grid(gridDiv, gridOptions);
	            gridApi = gridOptions.api;
	          }
	          if (gridApi && gridApi.sizeColumnsToFit){
	            setTimeout(function(){ gridApi.sizeColumnsToFit(); }, 0);
	          }
	          setStat("ready");
	        })
	        .catch(function(err){
	          document.getElementById("grid").innerHTML =
	            '<div style="color:#ffb3b3;padding:12px;white-space:pre-wrap;">'+String(err)+'</div>';
	          setStat("error");
	        });
	    });
	  })();
	  </script>
	</body>
	</html>
	""" % {
	    "css0":   base_local + "/ag-grid.css",
	    "theme0": base_local + "/ag-theme-alpine.css",
	    "js0":    base_local + "/ag-grid-community.min.js",
	    "css1":   base_cdn   + "/styles/ag-grid.css",
	    "theme1": base_cdn   + "/styles/ag-theme-alpine.css",
	    "js1":    base_cdn   + "/ag-grid-community.min.js",
	    "QS":     qs_string,
	    "curday": current_day,
	}
	
	return {"html": html}