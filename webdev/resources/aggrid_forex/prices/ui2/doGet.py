def doGet(request, session):
	html = u"""
	<!doctype html>
	<html>
	<head>
	  <meta charset="utf-8"/>
	  <title>Forex – Forecast FX</title>
	  <meta name="viewport" content="width=device-width, initial-scale=1"/>
	
	  <style>
	    /* GLOBAL */
	    html, body {
	      height:100%;
	      margin:0;
	      background:#071521;
	      color:#e5ecf5;
	      font:12px/1.4 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
	    }
	    .page{
	      height:100vh;
	      width:100vw;
	      display:flex;
	      flex-direction:column;
	      overflow:hidden;
	      background:#071521;
	    }
	
	    /* HEADER */
	    .header{
	      flex:0 0 auto;
	      font-size:28px;
	      font-weight:800;
	      padding:16px 20px 10px 20px;
	      color:#f0f4ff;
	    }
	
	    /* FILTER PANEL */
	    .panel{
	      margin:0 20px 8px 20px;
	      border:1px solid rgba(204,220,255,.32);
	      border-radius:12px;
	      padding:8px 6px 10px 14px;
	      background:#0f1b2a;
	      box-shadow:0 2px 10px rgba(0,0,0,.18);
	    }
	    .section-title{
	      font-size:13px;
	      font-weight:600;
	      opacity:.9;
	      margin-bottom:4px;
	    }
	    .row{
	      display:flex;
	      align-items:flex-end;
	      gap:30px;
	      margin-top:4px;
	      margin-bottom:4px;
	    }
	    .row > div:not(.filter-actions){
	      width:260px;
	    }
	    .filter-actions{
	      margin-left:auto;
	      display:flex;
	      justify-content:flex-end;
	      align-items:flex-end;
	    }
	
	    label{
	      display:block;
	      font-size:12px;
	      opacity:.9;
	      margin-bottom:4px;
	      color:#d6e3ff;
	    }
	
	    .panel input,
	    .panel select{
	      width:100%;
	      background:#1b2d4a;
	      color:#ebf2ff;
	      border:1px solid rgba(198,214,247,.45);
	      padding:5px 9px;
	      border-radius:8px;
	      outline:none;
	      font-size:13px;
	      box-sizing:border-box;
	    }
	    .panel input:focus,
	    .panel select:focus{
	      border-color:#6ea2ff;
	      box-shadow:0 0 0 2px rgba(110,162,255,.25);
	    }
	
	    /* BUTTON */
	    .btn{
	      padding:8px 14px;
	      cursor:pointer;
	      border-radius:10px;
	      border:1px solid rgba(204,220,255,.45);
	      background:#203a63;
	      color:#e9f2ff;
	      box-shadow:0 1px 0 rgba(0,0,0,.18) inset;
	      font-size:14px;
	      line-height:1.2;
	    }
	    .btn:hover{ background:#2a487e; }
	
	    .btn.filter-btn{
	      background:#3c4858;
	      color:#ffffff;
	      border-radius:10px;
	      border:1px solid #4b5563;
	      padding:0 18px;
	      height:30px;
	      font-size:14px;
	      font-weight:600;
	      cursor:pointer;
	      min-width:140px;
	      text-align:center;
	    }
	    .btn.filter-btn:hover{
	      background:#4b5563;
	      color:#ffffff;
	      border-color:#6b7280;
	      box-shadow:0 0 4px rgba(15,23,42,0.6);
	      transform:translateY(-1px);
	    }
	
	    /* GRID */
	    .gridPanel{
	      flex:1 1 auto;
	      display:flex;
	      flex-direction:column;
	      min-height:0;
	      margin:0 20px 18px 20px;
	    }
	    .gridWrap{
	      flex:1 1 auto;
	      min-height:0;
	      overflow:auto;
	      border-radius:10px;
	      border:1px solid rgba(204,220,255,.25);
	      background:#050b16;
	    }
	    .data-grid{
	      width:100%;
	      border-collapse:collapse;
	      font-size:13px;
	    }
	    .data-grid thead{
	      background:#13233a;
	      position:sticky;
	      top:0;
	      z-index:1;
	    }
	    .data-grid th,
	    .data-grid td{
	      padding:4px 8px;
	      border-bottom:1px solid #1f2f46;
	      white-space:nowrap;
	      color:#e5ecf5;
	      text-align:center;
	    }
	    .data-grid thead th{
	      color:#dbe7ff;
	      font-weight:500;
	    }
	    .data-grid tbody tr:nth-child(odd){
	      background:#0b1827;
	    }
	    .data-grid tbody tr:nth-child(even){
	      background:#091421;
	    }
	    .data-grid tbody tr:hover{
	      background:#163458;
	    }
	    .col-right{
	      text-align:right;
	    }
	
	    .data-grid th:nth-child(1),
	    .data-grid td:nth-child(1){
	      width:40px;          /* # */
	    }
	    .data-grid th:nth-child(2),
	    .data-grid td:nth-child(2){
	      width:110px;         /* day_date */
	    }
	    .data-grid th:nth-child(3),
	    .data-grid td:nth-child(3){
	      width:80px;          /* currency_id */
	    }
	    .data-grid th:nth-child(4),
	    .data-grid td:nth-child(4){
	      width:120px;         /* exchange_rate */
	    }
	    .data-grid th:nth-child(5),
	    .data-grid td:nth-child(5){
	      width:120px;         /* eq_value */
	    }
	  </style>
	</head>
	
	<body>
	  <div class="page">
	    <div class="header">Forex – Forecast FX</div>
	
	    <!-- FILTER PANEL -->
	    <div class="panel">
	      <div class="section-title">Filter by date and currency</div>
	      <div class="row">
	        <div>
	          <label>List from</label>
	          <input type="date" id="listFrom"/>
	        </div>
	        <div>
	          <label>List to</label>
	          <input type="date" id="listTo"/>
	        </div>
	        <div>
	          <label>Currency</label>
	          <select id="listCcy">
	            <option value="">All currencies</option>
            <option value="798">EUR</option>
            <option value="840">USD</option>
            <option value="946">RON</option>
            <option value="980">UAH</option>
            <option value="498">MDL</option>
	          </select>
	        </div>
	        <div class="filter-actions">
	          <button class="btn filter-btn" onclick="reloadSlots()">Apply filter</button>
	        </div>
	      </div>
	    </div>
	
	    <div id="debugInfo" style="padding:4px 20px; font-size:12px; opacity:.75;"></div>
	
	    <!-- GRID -->
	    <div class="gridPanel">
	      <div class="gridWrap">
	        <table id="slotGrid" class="data-grid">
	          <thead>
	            <tr>
	              <th data-sort="rownum">#</th>
	              <th data-sort="day_date">Day</th>
	              <th data-sort="currency_id">Currency</th>
	              <th data-sort="exchange_rate">Exchange rate</th>
	              <th data-sort="eq_value">Eq value</th>
	            </tr>
	          </thead>
	          <tbody></tbody>
	        </table>
	      </div>
	    </div>
	  </div>
	
	  <script>
	    var currentRows = [];
	    var sortState = { col:null, dir:1 };
	    var NUM_FIELDS = {
	      "_idx":1,
	      "exchange_rate":1,
	      "eq_value":1
	    };
	
	    function pad2(n){ return (n<10 ? "0"+n : ""+n); }
	    function toDateInputValue(d){
	      var yyyy = d.getFullYear(), mm = pad2(d.getMonth()+1), dd = pad2(d.getDate());
	      return yyyy + "-" + mm + "-" + dd;
	    }
	
	    /* RENDER TABLE */
	    function renderSlotTable(rows){
	      var tbody = document.querySelector("#slotGrid tbody");
	      if (!tbody) return;
	      tbody.innerHTML = "";
	
	      rows.forEach(function(r, idx){
	        var tr = document.createElement("tr");
	
	        function td(val, cls){
	          var cell = document.createElement("td");
	          if (cls) cell.className = cls;
	          if (val === null || val === undefined || val === "null" || val === "NULL"){
	            val = "";
	          }
	          cell.textContent = val;
	          tr.appendChild(cell);
	        }
	
	        td(idx + 1);
	        td(r.day_date || "");
	        td(r.currency_id || "");
	        td(r.exchange_rate != null ? r.exchange_rate : "", "col-right");
	        td(r.eq_value != null ? r.eq_value : "", "col-right");
	
	        tbody.appendChild(tr);
	      });
	    }
	
	    /* SORTING */
	    function sortBy(field){
	      if (!currentRows || !currentRows.length) return;
	
	      var realField = field;
	      if (field === "rownum"){
	        realField = "_idx";
	      }
	
	      if (sortState.col === realField){
	        sortState.dir = -sortState.dir;
	      } else {
	        sortState.col = realField;
	        sortState.dir = 1;
	      }
	      var dir = sortState.dir;
	
	      currentRows.sort(function(a,b){
	        var va = a[realField];
	        var vb = b[realField];
	
	        if (va == null && vb == null) return 0;
	        if (va == null) return -1*dir;
	        if (vb == null) return 1*dir;
	
	        if (NUM_FIELDS[realField]){
	          va = Number(va);
	          vb = Number(vb);
	          if (isNaN(va) && isNaN(vb)) return 0;
	          if (isNaN(va)) return -1*dir;
	          if (isNaN(vb)) return 1*dir;
	        } else {
	          va = String(va);
	          vb = String(vb);
	        }
	
	        if (va < vb) return -1*dir;
	        if (va > vb) return 1*dir;
	        return 0;
	      });
	
	      renderSlotTable(currentRows);
	    }
	
	    /* RELOAD SLOTS – calls Forex/ForeCastForex listSlots */
	    function reloadSlots(){
	      var from = document.getElementById("listFrom").value;
	      var to   = document.getElementById("listTo").value;
	      var ccy  = document.getElementById("listCcy").value;
	
	      var url = "./listSlots?from=" + encodeURIComponent(from) +
	                "&to="   + encodeURIComponent(to) +
	                "&ccy="  + encodeURIComponent(ccy || "");
	
	      var debugEl = document.getElementById("debugInfo");
	      if (debugEl){
	        debugEl.textContent = "Loading list from: " + url;
	      }
	
	      fetch(url)
	        .then(function(r){
	          if (!r.ok){
	            if (debugEl){
	              debugEl.textContent = "HTTP error " + r.status;
	            }
	            throw new Error("HTTP " + r.status);
	          }
	          return r.json();
	        })
	        .then(function(data){
	          console.log("forex data:", data);
	
	          var rows = [];
	          if (Array.isArray(data)){
	            rows = data;
	          } else if (Array.isArray(data.json)){
	            rows = data.json;
	          } else if (Array.isArray(data.rows)){
	            rows = data.rows;
	          }
	
	          rows.forEach(function(r, idx){ r._idx = idx; });
	
	          currentRows = rows.slice();
	          sortState = {col:null, dir:1};
	
	          if (debugEl){
	            debugEl.textContent = "Loaded " + rows.length + " rows.";
	          }
	          renderSlotTable(currentRows);
	        })
	        .catch(function(err){
	          console.error("Error loading forex listSlots:", err);
	          if (debugEl){
	            debugEl.textContent = "Error loading list: " + err;
	          }
	          currentRows = [];
	          renderSlotTable([]);
	        });
	    }
	
	    /* INIT */
	    document.addEventListener("DOMContentLoaded", function(){
	      var today  = new Date();
	      var listFrom = new Date(today.getTime() - 24*3600*1000);
	      var listTo   = new Date(today.getTime() + 24*3600*1000);
	
	      document.getElementById("listFrom").value = toDateInputValue(listFrom);
	      document.getElementById("listTo").value   = toDateInputValue(listTo);
	
	      document.querySelectorAll("#slotGrid thead th[data-sort]").forEach(function(th){
	        th.style.cursor = "pointer";
	        th.addEventListener("click", function(){
	          var f = th.getAttribute("data-sort");
	          sortBy(f);
	        });
	      });
	
	      reloadSlots();
	    });
	  </script>
	</body>
	</html>
	"""
	
	return {"html": html}