def doGet(request, session):
	html = u"""
	<!doctype html>
	<html>
	<head>
	  <meta charset="utf-8"/>
	  <title>Cross-Border Sections (RO / UA)</title>
	  <meta name="viewport" content="width=device-width, initial-scale=1"/>
	
	  <style>
	    /* GLOBAL – like Contragents / Market */
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
	      background:radial-gradient(circle at 0 0, #20365b 0, #050815 60%, #02040b 100%);
	    }
	
	    /* HEADER + TOOLBAR */
	    .header{
	      flex:0 0 auto;
	      font-size:22px;
	      font-weight:800;
	      padding:16px 20px 10px 20px;
	      color:#f0f4ff;
	    }
	    .toolbar{
	      flex:0 0 auto;
	      display:flex;
	      align-items:center;
	      gap:10px;
	      padding:0 20px 14px 20px;
	    }
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
	
	    /* New slot button */
	    .btn.newslot {
	      background:#22c55e;
	      color:#052e16;
	      box-shadow:0 0 4px rgba(34,197,94,0.6);
	      white-space:nowrap;
	      padding:0 18px;
	      height:30px;
	      font-weight:600;
	      border-color:#16a34a;
	    }
	    .btn.newslot:hover {
	      background:#16a34a;
	      box-shadow:0 0 8px rgba(34,197,94,0.85);
	      transform:translateY(-1px);
	    }
	
	    .btn.reloadlist {
	      background:#3c4858;
	      color:#ffffff;
	      box-shadow:0 0 4px rgba(15,23,42,0.45);
	      white-space:nowrap;
	      padding:0 18px;
	      height:30px;
	      font-weight:600;
	      border-color:#4b5563;
	    }
	    .btn.reloadlist:hover {
	      background:#465567;
	      box-shadow:0 0 8px rgba(15,23,42,0.7);
	      transform:translateY(-1px);
	    }
	
	    /* FILTER PANEL (top list filters) */
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
	    /* one row: filters + button, left aligned */
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
	
	    /* filter inputs in top panel */
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
	
	    /* GRID AREA (plain HTML table) */
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
	
	    /* gradient header */
	    .data-grid thead{
	      background: linear-gradient(to bottom, #233653, #1a2a40);
	      border-bottom:2px solid #284571;
	      position:sticky;
	      top:0;
	      z-index:2;
	    }
	    .data-grid thead th{
	      color:#e8f0ff;
	      font-weight:600;
	      padding:6px 8px;
	      text-shadow:0 1px 1px rgba(0,0,0,.4);
	    }
	
	    .data-grid th,
	    .data-grid td{
	      padding:4px 8px;
	      border-bottom:1px solid #1f2f46;
	      white-space:nowrap;
	      color:#e5ecf5;
	      text-align:center;
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
	
	    /* some widths */
	    .data-grid th:nth-child(1),
	    .data-grid td:nth-child(1){
	      width:40px;
	    }
	
	    /* collapsible rows */
	    .slot-parent { cursor:pointer; }
	    .slot-child  { background:#050b16; }
	    .slot-child-cell {
	      padding:0;
	      border-bottom:1px solid #1f2f46;
	    }
	
	    /* child inner grid */
	    .child-grid{
	      width:100%;
	      border-collapse:collapse;
	      font-size:12px;
	    }
	    .child-grid th,
	    .child-grid td{
	      padding:3px 6px;
	      border-bottom:1px solid #1f2f46;
	      text-align:center;
	    }
	    .child-grid thead,
	    .child-grid thead th{
	      background:linear-gradient(to bottom,#16537e,#16537e) !important;
	      border-bottom:2px solid #ffd966 !important;
	      color:#cfe2f3 !important;
	      font-weight:600;
	      padding:4px 6px;
	      text-shadow:none;
	    }
	
	    /* expander button */
	    .data-grid .expander{
	      display:inline-block;
	      width:18px;
	      height:18px;
	      line-height:18px;
	      border-radius:50%;
	      border:1px solid #9fc5e8;
	      background:#2c4a7a;
	      color:#9fc5e8;
	      font-size:11px;
	      font-weight:700;
	      text-align:center;
	      cursor:pointer;
	      user-select:none;
	    }
	    .data-grid .expander.open{
	      background:#22c55e;
	      color:#04130a;
	      border-color:#16a34a;
	    }
	
	    /* Export bar above grid */
	    .gridExportBar{
	      padding:0 26px 2px 0;
	      text-align:right;
	    }
	
	    /* Export + Apply – same base size */
	    .btn.export-btn,
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
	
	    .btn.export-btn{
	      display:inline-flex;
	      align-items:center;
	      justify-content:center;
	      gap:6px;
	    }
	    .export-icon{
	      font-size:14px;
	      color:#f1c232;
	      line-height:1;
	    }
	    .export-text{
	      font-size:13px;
	      font-weight:600;
	    }
	
	    .btn.export-btn:hover{
	      background:#22c55e;
	      color:#052e16;
	      border-color:#16a34a;
	      box-shadow:0 0 6px rgba(34,197,94,0.75);
	      transform:translateY(-1px);
	    }
	
	    .btn.filter-btn:hover{
	      background:#4b5563;
	      color:#ffffff;
	      border-color.#6b7280;
	      box-shadow:0 0 4px rgba(15,23,42,0.6);
	      transform:translateY(-1px);
	    }
	
	    /* ===== POPUP STYLES ===== */
	    .modal-backdrop{
	      position:fixed;
	      top:0; left:0; right:0; bottom:0;
	      background:rgba(0,0,0,.55);
	      display:none;
	      align-items:center;
	      justify-content:center;
	      z-index:999;
	    }
	
	    .modal{
	      background:#0f1b2a;
	      border-radius:12px;
	      border:1px solid rgba(204,220,255,.4);
	      width:96%;
	      max-width:1600px;
	      max-height:95vh;
	      display:flex;
	      flex-direction:column;
	    }
	
	    .modal-body{
	      padding:28px 30px;
	      overflow:auto;
	    }
	
	    .popup-form{
	      max-width:720px;
	      width:100%;
	      margin:0;
	    }
	
	    .popup-row{
	      display:grid;
	      grid-template-columns: repeat(2, minmax(0, 1fr));
	      column-gap:26px;
	      row-gap:14px;
	      margin-bottom:16px;
	    }
	    .popup-row > div{
	      width:100%;
	    }
	    .popup-row input[type="date"],
	    .popup-row select{
	      width:100% !important;
	      max-width:100% !important;
	      background:#071521;
	color:#e8f0ff;
	border:1px solid rgba(198,214,247,.40);
	padding:6px 9px;
	border-radius:8px;
	outline:none;
	      box-sizing:border-box;
	    }
	
	    /* HOURS TABLE */
	    .hours-table{
	      width:100%;
	      border-collapse:collapse;
	      font-size:12px;
	    }
	    .hours-table th,
	    .hours-table td{
	      border:1px solid rgba(198,214,247,.32);
	      padding:3px 4px;
	      text-align:center;
	      background:#102039;
	    }
	    .hours-table th:first-child,
	    .hours-table td:first-child{
	      text-align:center;
	      width:220px;
	      background:#0f1c31;
	    }
	    .hours-table input{
	      width:100%;
	      padding:2px 3px;
	      font-size:11px;
	      height:24px;
	      background:#071521;
	      border-radius:4px;
	      border:1px solid rgba(198,214,247,.40);
	      color:#e8f0ff;
	      text-align:center;
	      box-sizing:border-box;
	    }
	
	    .indicator-row{
	      display:flex;
	      justify-content:space-between;
	      align-items:center;
	      gap:6px;
	    }
	    .indicator-row span {
	      margin: 0 auto;
	      text-align: center;
	      flex: 1;
	    }
	    .row-clear-btn{
	      background:transparent;
	      border:1px solid rgba(230,239,255,.55);
	      border-radius:6px;
	      color:#e6efff;
	      font-size:12px;
	      padding:1px 7px;
	      cursor:pointer;
	    }
	    .row-clear-btn:hover{
	      background:#2a487e;
	    }
	
	    .price-input.zero-warning{
	      border-color:#ff5c5c !important;
	      background:#3b1111 !important;
	    }
	
	    .popup-btn-cancel {
	      background: #3c4858;
	      color: #ffffff;
	      border: none;
	      padding: 8px 20px;
	      border-radius: 6px;
	      cursor: pointer;
	      font-size: 13px;
	      transition: background 0.2s ease;
	    }
	    .popup-btn-cancel:hover {
	      background: #465567;
	    }
	
	    .popup-btn-save {
	      background: #22c55e;
	      color: #ffffff;
	      border: none;
	      padding: 8px 20px;
	      border-radius: 6px;
	      cursor: pointer;
	      font-size: 13px;
	      font-weight: 600;
	      transition: background 0.2s ease;
	    }
	    .popup-btn-save:hover {
	      background: #16a34a;
	    }
	  </style>
	</head>
	
	<body>
	  <div class="page">
	    <div class="header">Cross-Border Sections (RO / UA)</div>
	
	    <div class="toolbar">
	      <button class="btn newslot" onclick="startNewSlot()">+ New slot</button>
	    </div>
	
	    <div class="panel">
	      <div class="section-title">Active periods (list filter)</div>
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
	          <label>Country</label>
	          <select id="listArea">
	            <option value="">All countries</option>
	            <option value="RO">RO</option>
	            <option value="UA">UA</option>
	          </select>
	        </div>
	
	        <!-- Hour filter -->
	        <div>
	          <label>Hour</label>
	          <select id="listHour">
	            <option value="">All hours</option>
	            <option value="0">00</option>
	            <option value="1">01</option>
	            <option value="2">02</option>
	            <option value="3">03</option>
	            <option value="4">04</option>
	            <option value="5">05</option>
	            <option value="6">06</option>
	            <option value="7">07</option>
	            <option value="8">08</option>
	            <option value="9">09</option>
	            <option value="10">10</option>
	            <option value="11">11</option>
	            <option value="12">12</option>
	            <option value="13">13</option>
	            <option value="14">14</option>
	            <option value="15">15</option>
	            <option value="16">16</option>
	            <option value="17">17</option>
	            <option value="18">18</option>
	            <option value="19">19</option>
	            <option value="20">20</option>
	            <option value="21">21</option>
	            <option value="22">22</option>
	            <option value="23">23</option>
	            <option value="24">24</option>
	          </select>
	        </div>
	
	        <div class="filter-actions">
	          <button class="btn filter-btn" onclick="reloadSlots()">Apply filter</button>
	        </div>
	      </div>
	    </div>
	
	    <div id="debugInfo" style="padding:4px 20px; font-size:12px; opacity:.75;"></div>
	
	    <div class="gridExportBar">
	      <button class="btn export-btn" onclick="exportToExcel()">
	        <span class="export-icon">⬇</span>
	        <span class="export-text">Export Excel</span>
	      </button>
	    </div>
	
	    <div class="gridPanel">
	      <div class="gridWrap">
	        <table id="slotGrid" class="data-grid">
	          <thead>
	            <tr>
	              <th></th>
	              <th data-sort="slotIdx">Slot</th>
	              <th data-sort="area">Area</th>
	              <th data-sort="currencyid">Currency</th>
	              <th data-sort="date_from">Date from</th>
	              <th data-sort="date_to">Date to</th>
	              <th data-sort="forecast_price_section_import">Avg Price Import</th>
	              <th data-sort="forecast_price_section_export">Avg Price Export</th>
	            </tr>
	          </thead>
	          <tbody></tbody>
	        </table>
	      </div>
	    </div>
	  </div>
	
	  <div id="slotModalBackdrop" class="modal-backdrop" style="display:none;">
	    <div class="modal">
	      <div class="modal-body">
	        <div class="popup-form">
	          <div class="popup-row">
	            <div>
	              <label>Slot date from</label>
	              <input type="date" id="slotDateFrom"/>
	            </div>
	            <div>
	              <label>Slot date to</label>
	              <input type="date" id="slotDateTo"/>
	            </div>
	          </div>
	          <div class="popup-row">
	            <div>
	              <label>Area</label>
	              <select id="slotArea">
	                <option value="RO">RO</option>
	                <option value="UA">UA</option>
	              </select>
	            </div>
	            <div>
	              <label>Currency</label>
	              <select id="slotCurrency">
	                <option value="978">EUR</option>
	                <option value="946">RON</option>
	                <option value="980">UAH</option>
	                <option value="840">USD</option>
	                <option value="498">MDL</option>
	              </select>
	            </div>
	          </div>
	        </div>
	
	        <div style="overflow-x:auto; margin-top:14px;">
	          <table class="hours-table" id="hoursTable"></table>
	        </div>
	
	        <div style="text-align:right; margin-top:12px;">
	          <button class="popup-btn-cancel" onclick="closeSlotModal()">Cancel</button>
	          <button class="popup-btn-save" onclick="onSaveSlot()">Save</button>
	        </div>
	      </div>
	    </div>
	  </div>
	
	  <script>
	    var currentMode = "new";
	    var CCY_MAP = {"978":"EUR","840":"USD","946":"RON","980":"UAH","498":"MDL"};
	    var currentRows = [];
	    var currentGroups = [];
	    var sortState = {col:null,dir:1};
	    var NUM_FIELDS = {
	      "_idx":1,
	      "forecast_price_section_import":1,
	      "forecast_price_section_export":1
	    };
	    var lastTypedValue = null;
	
	    function pad2(n){ return (n<10?"0"+n:""+n); }
	    function toDateInputValue(d){
	      var yyyy=d.getFullYear(),mm=pad2(d.getMonth()+1),dd=pad2(d.getDate());
	      return yyyy+"-"+mm+"-"+dd;
	    }
	
	    function openSlotModal(){
	      document.getElementById("slotModalBackdrop").style.display="flex";
	      clearZeroHighlight();
	    }
	    function closeSlotModal(){
	      document.getElementById("slotModalBackdrop").style.display="none";
	    }
	
	    /* HOURS TABLE – 4 rows, clear & copy */
	    function buildHoursTable(){
	      lastTypedValue = null;
	
	      var table=document.getElementById("hoursTable");
	      table.innerHTML="";
	      var thead=document.createElement("thead");
	      var hr=document.createElement("tr");
	      var th0=document.createElement("th");
	      th0.textContent="Price per hour (MWh)";
	      hr.appendChild(th0);
	      for(var h=1;h<=24;h++){
	        var th=document.createElement("th");
	        th.textContent=pad2(h);
	        hr.appendChild(th);
	      }
	      thead.appendChild(hr);
	      table.appendChild(thead);
	      var tbody=document.createElement("tbody");
	      table.appendChild(tbody);
	
	      function createRow(label){
	        var tr=document.createElement("tr");
	        var tdLabel=document.createElement("td");
	        tdLabel.innerHTML =
	          '<div class="indicator-row">'+
	            '<span>'+label+'</span>'+
	            '<button type="button" class="row-clear-btn" title="Clear all" onclick="clearHourValues()">🧹</button>'+
	            '<button type="button" class="row-clear-btn" title="Copy last value to all" onclick="copyLastValueToAll()">📄</button>'+
	          '</div>';
	        tr.appendChild(tdLabel);
	        for(var h=1;h<=24;h++){
	          var td=document.createElement("td");
	          var inp=document.createElement("input");
	          inp.type="text";
	          inp.className="price-input";
	          inp.setAttribute("data-hour",h);
	          inp.value="0";
	          td.appendChild(inp);
	          tr.appendChild(td);
	        }
	        tbody.appendChild(tr);
	      }
	
	      createRow("Price Import");
	      createRow("Price Export");
	      createRow("Qty Import");
	      createRow("Qty Export");
	
	      setTimeout(function(){
	        document.querySelectorAll(".price-input").forEach(function(inp){
	          inp.addEventListener("input", function(){
	            var v=(this.value||"").trim();
	            if(v!==""){ lastTypedValue=v; }
	          });
	        });
	      },0);
	    }
	
	    function clearHourValues(){document.querySelectorAll(".price-input").forEach(function(inp){inp.value="";});}
	    function fillAllValuesWithZero(){document.querySelectorAll(".price-input").forEach(function(inp){inp.value="0";});}
	    function clearZeroHighlight(){document.querySelectorAll(".price-input").forEach(function(i){i.classList.remove("zero-warning");});}
	    function markZeroCellsAndCount(){
	      clearZeroHighlight();
	      var count=0;
	      document.querySelectorAll(".price-input").forEach(function(inp){
	        var v=(inp.value||"").trim().replace(",",".");
	        var num=parseFloat(v);
	        if(!isNaN(num)&&num===0){inp.classList.add("zero-warning");count++;}
	      });
	      return count;
	    }
	    function copyLastValueToAll(){
	      if(lastTypedValue===null){
	        alert("Firstly input a value in a cell.");
	        return;
	      }
	      document.querySelectorAll(".price-input").forEach(function(inp){
	        inp.value=lastTypedValue;
	      });
	    }
	
	    function collectSlotPayload(){
	      var prices={};
	      document.querySelectorAll(".price-input").forEach(function(inp){
	        prices[inp.getAttribute("data-hour")]=inp.value||null;
	      });
	      return {
	        mode:currentMode,
	        date_from:document.getElementById("slotDateFrom").value,
	        date_to:document.getElementById("slotDateTo").value,
	        area:document.getElementById("slotArea").value,
	        currencyid:document.getElementById("slotCurrency").value,
	        prices:prices
	      };
	    }
	
	    function startNewSlot(){
	      var today=new Date();
	      var ts=toDateInputValue(today);
	      document.getElementById("slotDateFrom").value=ts;
	      document.getElementById("slotDateTo").value=ts;
	      document.getElementById("slotArea").value="RO";
	      document.getElementById("slotCurrency").value="978";
	      fillAllValuesWithZero();
	      currentMode="new";
	      openSlotModal();
	    }
	
	    function onSaveSlot(){
	      var payload=collectSlotPayload();
	      if(!payload.date_from||!payload.date_to){
	        alert("Please fill Slot date from / to.");
	        return;
	      }
	      var zeroCount=markZeroCellsAndCount();
	      var msg=zeroCount>0
	        ?"You have "+zeroCount+" zero-valued hours. Continue?"
	        :(currentMode==="new"?"Create new slot?":"Update slot?");
	      if(!confirm(msg))return;
	      fetch("./saveSlot",{
	        method:"POST",
	        headers:{"Content-Type":"application/json"},
	        body:JSON.stringify(payload)
	      }).then(function(r){return r.json();}).then(function(json){
	        if(!json.ok){
	          alert("Save error: "+(json.error||"unknown"));
	          return;
	        }
	        closeSlotModal();
	        reloadSlots();
	      });
	    }
	
	    function buildSlotGroups(rows){
	      var map={};
	      rows.forEach(function(r){
	        var key=(r.area||"")+"|"+(r.currencyid||"")+"|"+(r.date_from||"")+"|"+(r.date_to||"");
	        if(!map[key]){
	          map[key]={
	            area:r.area||"",
	            currencyid:r.currencyid||"",
	            date_from:r.date_from||"",
	            date_to:r.date_to||"",
	            rows:[]
	          };
	        }
	        map[key].rows.push(r);
	      });
	      var groups=[];
	      var slotIdx=1;
	      for(var key in map){
	        if(!map.hasOwnProperty(key))continue;
	        var g=map[key];
	        var sumImp=0,sumExp=0,nImp=0,nExp=0;
	        g.rows.forEach(function(r){
	          var pI=Number(r.forecast_price_section_import);
	          var pE=Number(r.forecast_price_section_export);
	          if(!isNaN(pI)){sumImp+=pI;nImp++;}
	          if(!isNaN(pE)){sumExp+=pE;nExp++;}
	        });
	        groups.push({
	          slotIdx:slotIdx++,
	          area:g.area,
	          currencyid:g.currencyid,
	          date_from:g.date_from,
	          date_to:g.date_to,
	          avgImp:nImp?(sumImp/nImp):null,
	          avgExp:nExp?(sumExp/nExp):null,
	          rows:g.rows
	        });
	      }
	      return groups;
	    }
	
	    function renderSlotTableFromGroups(groups){
	      var tbody=document.querySelector("#slotGrid tbody");
	      if(!tbody)return;
	      tbody.innerHTML="";
	      groups.forEach(function(g,gi){
	        var trP=document.createElement("tr");
	        trP.className="slot-parent";
	        trP.setAttribute("data-group",gi);
	        function td(val,cls){
	          var cell=document.createElement("td");
	          if(cls)cell.className=cls;
	          if(val===null||val===undefined||val==="null"||val==="NULL")val="";
	          cell.textContent=val;
	          trP.appendChild(cell);
	        }
	        var tdExp=document.createElement("td");
	        var span=document.createElement("span");
	        span.className="expander";
	        span.setAttribute("data-group",gi);
	        span.textContent="+";
	        tdExp.appendChild(span);
	        trP.appendChild(tdExp);
	        var currency=CCY_MAP[String(g.currencyid)]||(g.currencyid||"");
	        td(g.slotIdx);
	        td(g.area||"");
	        td(currency);
	        td(g.date_from||"");
	        td(g.date_to||"");
	        td(g.avgImp!=null?g.avgImp.toFixed(0):"","col-right");
	        td(g.avgExp!=null?g.avgExp.toFixed(0):"","col-right");
	        tbody.appendChild(trP);
	
	        var trC=document.createElement("tr");
	        trC.className="slot-child";
	        trC.setAttribute("data-group",gi);
	        trC.style.display="none";
	        var tdChild=document.createElement("td");
	        tdChild.className="slot-child-cell";
	        tdChild.colSpan=8;
	        var inner=document.createElement("table");
	        inner.className="child-grid";
	        var thead=document.createElement("thead");
	        var hr=document.createElement("tr");
	        ["#","Hour","Price Import","Price Export","Qty Import","Qty Export"]
	          .forEach(function(h){
	            var th=document.createElement("th");
	            th.textContent=h;
	            hr.appendChild(th);
	          });
	        thead.appendChild(hr);
	        inner.appendChild(thead);
	        var tb=document.createElement("tbody");
	        g.rows.forEach(function(r,idx){
	          var tr=document.createElement("tr");
	          function td2(val,cls){
	            var cell=document.createElement("td");
	            if(cls)cell.className=cls;
	            if(val===null||val===undefined||val==="null"||val==="NULL")val="";
	            cell.textContent=val;
	            tr.appendChild(cell);
	          }
	          td2(idx+1);
	          td2(r.hour!=null?r.hour:"");
	          td2(r.forecast_price_section_import,"col-right");
	          td2(r.forecast_price_section_export,"col-right");
	          td2(r.forecast_quantity_section_import,"col-right");
	          td2(r.forecast_quantity_section_export,"col-right");
	          tb.appendChild(tr);
	        });
	        inner.appendChild(tb);
	        tdChild.appendChild(inner);
	        trC.appendChild(tdChild);
	        tbody.appendChild(trC);
	      });
	      document.querySelectorAll(".expander").forEach(function(el){
	        el.onclick=function(ev){
	          ev.stopPropagation();
	          var gid=this.getAttribute("data-group");
	          var childRow=document.querySelector('tr.slot-child[data-group="'+gid+'"]');
	          if(!childRow)return;
	          var isOpen=childRow.style.display!=="none";
	          childRow.style.display=isOpen?"none":"";
	          this.classList.toggle("open",!isOpen);
	          this.textContent=isOpen?"+":"−";
	        };
	      });
	    }
	
	    function sortBy(field){
	      if(!currentRows||!currentRows.length)return;
	      var realField=field;
	      if(field==="rownum")realField="_idx";
	      if(sortState.col===realField){
	        sortState.dir=-sortState.dir;
	      }else{
	        sortState.col=realField;
	        sortState.dir=1;
	      }
	      var dir=sortState.dir;
	      currentRows.sort(function(a,b){
	        var va=a[realField];
	        var vb=b[realField];
	        if(va==null&&vb==null)return 0;
	        if(va==null)return -1*dir;
	        if(vb==null)return 1*dir;
	        if(NUM_FIELDS[realField]){
	          va=Number(va);vb=Number(vb);
	          if(isNaN(va)&&isNaN(vb))return 0;
	          if(isNaN(va))return -1*dir;
	          if(isNaN(vb))return 1*dir;
	        }else{
	          va=String(va);vb=String(vb);
	        }
	        if(va<vb)return -1*dir;
	        if(va>vb)return 1*dir;
	        return 0;
	      });
	      currentGroups=buildSlotGroups(currentRows);
	      renderSlotTableFromGroups(currentGroups);
	    }
	
	    function reloadSlots(){
	      var from=document.getElementById("listFrom").value;
	      var to=document.getElementById("listTo").value;
	      var area=document.getElementById("listArea").value;
	      var hour=document.getElementById("listHour").value;
	
	      var url="./listSlots?from="+encodeURIComponent(from)+
	              "&to="+encodeURIComponent(to)+
	              "&area="+encodeURIComponent(area||"");
	              // hour is filtered client-side
	
	      var debugEl=document.getElementById("debugInfo");
	      if(debugEl)debugEl.textContent="Loading list from: "+url;
	      fetch(url)
	        .then(function(r){
	          if(!r.ok){
	            if(debugEl)debugEl.textContent="HTTP error "+r.status;
	            throw new Error("HTTP "+r.status);
	          }
	          return r.json();
	        })
	        .then(function(data){
	          var rows=[];
	          if(Array.isArray(data))rows=data;
	          else if(Array.isArray(data.json))rows=data.json;
	          else if(Array.isArray(data.rows))rows=data.rows;
	          rows.forEach(function(r,idx){r._idx=idx;});
	          currentRows=rows.slice();
	
	          // apply hour filter like in working UI
	          var filtered=currentRows;
	          if(hour !== ""){
	            var hNum=Number(hour);
	            filtered=currentRows.filter(function(r){
	              return Number(r.hour)===hNum;
	            });
	          }
	
	          sortState={col:null,dir:1};
	          if(debugEl)debugEl.textContent="Loaded "+filtered.length+" rows.";
	          currentGroups=buildSlotGroups(filtered);
	          renderSlotTableFromGroups(currentGroups);
	        })
	        .catch(function(err){
	          console.error("Error loading cross-border listSlots:",err);
	          if(debugEl)debugEl.textContent="Error loading list: "+err;
	          currentRows=[];
	          currentGroups=[];
	          renderSlotTableFromGroups([]);
	        });
	    }
	
	    function exportToExcel(){
	      var rows=currentRows||[];
	      if(!rows.length){
	        alert("No data to export.");
	        return;
	      }
	      var header=[
	        "#",
	        "Area",
	        "Currency",
	        "Hour",
	        "Date from",
	        "Date to",
	        "Price Import",
	        "Price Export",
	        "Qty Import",
	        "Qty Export"
	      ];
	      var lines=[];
	      lines.push(header.join(";"));
	      rows.forEach(function(r,idx){
	        var currency=CCY_MAP[String(r.currencyid)]||(r.currencyid||"");
	        var line=[
	          idx+1,
	          r.area||"",
	          currency,
	          (r.hour!=null?r.hour:""),
	          r.date_from||"",
	          r.date_to||"",
	          (r.forecast_price_section_import!=null?r.forecast_price_section_import:""),
	          (r.forecast_price_section_export!=null?r.forecast_price_section_export:""),
	          (r.forecast_quantity_section_import!=null?r.forecast_quantity_section_import:""),
	          (r.forecast_quantity_section_export!=null?r.forecast_quantity_section_export:"")
	        ].join(";");
	        lines.push(line);
	      });
	      var csv=lines.join("\\r\\n");
	      var blob=new Blob([csv],{type:"text/csv;charset=utf-8;"});
	      var url=URL.createObjectURL(blob);
	      var a=document.createElement("a");
	      a.href=url;
	      var from=document.getElementById("listFrom").value||"";
	      var to=document.getElementById("listTo").value||"";
	      var fname="cross_border_sections_"+(from||"from")+"_"+(to||"to")+".csv";
	      a.download=fname.replace(/[^a-zA-Z0-9_\\-\\.]/g,"_");
	      document.body.appendChild(a);
	      a.click();
	      document.body.removeChild(a);
	      URL.revokeObjectURL(url);
	    }
	
	    document.addEventListener("DOMContentLoaded",function(){
	      var modal=document.getElementById("slotModalBackdrop");
	      if(modal)modal.style.display="none";
	      buildHoursTable();
	      var today=new Date();
	      var listFrom=new Date(today.getTime()-24*3600*1000);
	      var listTo=new Date(today.getTime()+24*3600*1000);
	      document.getElementById("listFrom").value=toDateInputValue(listFrom);
	      document.getElementById("listTo").value=toDateInputValue(listTo);
	      document.querySelectorAll("#slotGrid thead th[data-sort]").forEach(function(th){
	        th.style.cursor="pointer";
	        th.addEventListener("click",function(){
	          var f=th.getAttribute("data-sort");
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