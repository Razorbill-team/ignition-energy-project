def doGet(request, session):
	html = u"""
	<!doctype html>
	<html>
	<head>
	<meta charset="utf-8"/>
	<title>Market prices (OPCOM / RDN / OPEM)</title>
	<meta name="viewport" content="width=device-width, initial-scale=1"/>
	
	<style>
	/* GLOBAL – like Contragents */
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
	
	/* MAIN TOP BUTTONS */
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
	/* .btn.reloadlist removed */
	
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
	flex-wrap:wrap;
	align-items:flex-end;
	gap:18px;
	margin-top:4px;
	margin-bottom:4px;
	}
	.row > div:not(.filter-actions){
	width:200px;              /* List from, List to, Market, Currency, Hour */
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
    overflow-y:auto;        /* still scrollable vertically */
    overflow-x:hidden;      /* no horizontal scroll */
    border-radius:10px;
    border:1px solid rgba(204,220,255,.25);
    background:#050b16;

    /* Hide scrollbars everywhere */
    scrollbar-width: none;  /* Firefox */
}
	.data-grid{
	width:100%;
	border-collapse:collapse;
	font-size:13px;
	}
	/* PARENT TABLE HEADER */
	.data-grid thead {
	    background: linear-gradient(to bottom, #233653, #1a2a40);
	    border-bottom: 2px solid #284571;
	    position: sticky;
	    top: 0;
	    z-index: 2;
	}
	
	.data-grid thead th {
	    color: #e8f0ff;
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
	    text-align:center;     /* all centered */
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
	
	/* --- collapsible rows --- */
	.slot-parent { cursor:pointer; }
	.slot-child  { background:#050b16; }
	
	.slot-child-cell {
	    padding:0;
	    border-bottom:1px solid #1f2f46;
	}
	
	/* child inner grid */
	.child-grid {
	    width:100%;
	    border-collapse:collapse;
	    font-size:12px;
	}
	
	.child-grid th,
	.child-grid td {
	    padding:3px 6px;
	    border-bottom:1px solid #1f2f46;
	    text-align:center;
	}
	
	/* CHILD TABLE HEADER (expanded detail, yellow test) */
	.child-grid thead,
	.child-grid thead th {
	    background: linear-gradient(to bottom, #16537e, #16537e) !important;
	    border-bottom: 2px solid #16537e !important;
	    color: #cfe2f3 !important;      /* dark text for contrast */
	    font-weight: 600;
	    padding: 4px 6px;
	    text-shadow: none;
	}
	/* FIX: Restore expander button styling */
		.data-grid .expander {
		    display:inline-block !important;
		    width:18px !important;
		    height:18px !important;
		    line-height:18px !important;
		    border-radius:50% !important;
		    border:1px solid #9fc5e8 !important;
		    background:#2c4a7a !important;
		    color:#9fc5e8 !important;
		    font-size:11px !important;
		    font-weight:700;
		    text-align:center;
		    cursor:pointer;
		    user-select:none;
		    box-shadow:0 0 6px rgba(255,215,0,0.6) inset;   /* glow INSIDE the block */
		}
		
	
	/* When expanded (open state) */
	.data-grid .expander.open {
	    background:#22c55e !important;
	    color:#04130a !important;
	    border-color:#16a34a !important;
	}
	/* ---- SORTING ARROWS ---- */
	th.sortable {
	    position: relative;
	    padding-right: 4px;   /* minimal spacing */
	    user-select: none;
	}
	
	th.sortable .sort-arrow {
	    display: inline-block;
	    margin-left: 6px;       /* small space after text */
	    vertical-align: middle;
	    opacity: 0.35;
	    width: 0;
	    height: 0;
	    border-left: 4px solid transparent;
	    border-right: 4px solid transparent;
	    border-top: 6px solid #7fa6ff;  /* neutral arrow */
	}
	
	/* ascending */
	th.sortable.asc .sort-arrow {
	    border-top: none;
	    border-bottom: 6px solid #22c55e; /* green up */
	    opacity: 1;
	}
	
	/* descending */
	th.sortable.desc .sort-arrow {
	    border-top: 6px solid #eab308;   /* yellow down */
	    border-bottom: none;
	    opacity: 1;
	}
	
	/* ================================
   PARENT GRID COLUMN WIDTHS ONLY
   ================================ */
		
		/* 1) Expander */
		.data-grid th:nth-child(1),
		.data-grid td:nth-child(1){
		    width:40px;
		}
		
		/* 2) Slot */
		.data-grid th:nth-child(2),
		.data-grid td:nth-child(2){
		    width:55px;
		}
		
		/* 3) Created At */
		.data-grid th:nth-child(3),
		.data-grid td:nth-child(3){
		    width:130px;
		}
		
		/* 4) Date From */
		.data-grid th:nth-child(4),
		.data-grid td:nth-child(4){
		    width:130px;
		}
		
		/* 5) Date To */
		.data-grid th:nth-child(5),
		.data-grid td:nth-child(5){
		    width:130px;
		}
		
		/* 6) Market */
		.data-grid th:nth-child(6),
		.data-grid td:nth-child(6){
		    width:150px;
		}
		
		/* 7) Currency */
		.data-grid th:nth-child(7),
		.data-grid td:nth-child(7){
		    width:110px;
		}
		
		/* 8–10 metric columns */
		.data-grid th:nth-child(8),
		.data-grid td:nth-child(8),
		.data-grid th:nth-child(9),
		.data-grid td:nth-child(9),
		.data-grid th:nth-child(10),
		.data-grid td:nth-child(10){
		    width:180px;
		}
		
		/* 11) Actions */
		.data-grid th:nth-child(11),
		.data-grid td:nth-child(11){
		    width:320px;
		    text-align:center;
		}

	/* Export bar above grid */
	.gridExportBar{
	padding:0 26px 2px 14px;
	text-align:right;
	}
	
	/* Export + Apply – same base size */
	.btn.export-btn,
	.btn.filter-btn{
	background:#3c4858;
	color:#ffffff;
	border-radius:10px;
	border:1px solid #4b5563;
	padding:0 10px;
	height:30px;
	font-size:14px;
	font-weight:600;
	cursor:pointer;
	min-width:140px;        /* same width for both */
	text-align:center;
	}
	/* icon + label inside Export button */
	.btn.export-btn{
	display:inline-flex;
	align-items:center;
	justify-content:center;
	gap:6px;
	}
	
	.export-icon{
	font-size:14px;
	color:#f1c232;
	}
	
	.export-text{
	font-size:13px;
	font-weight:600;
	}
	
	/* hover green ONLY for Export */
	.btn.export-btn:hover{
	background:#22c55e;
	color:#052e16;
	border-color:#16a34a;
	box-shadow:0 0 6px rgba(34,197,94,0.75);
	transform:translateY(-1px);
	}
	
	/* hover grey for Apply filter */
	.btn.filter-btn:hover{
	background:#4b5563;
	color:#ffffff;
	border-color:#6b7280;
	box-shadow:0 0 4px rgba(15,23,42,0.6);
	transform:translateY(-1px);
	}
	
	/* POPUP BACKDROP */
	.modal-backdrop{
	position:fixed;
	top:0; left:0; right:0; bottom:0;
	background:rgba(0,0,0,.55);
	display:none;
	align-items:center;
	justify-content:center;
	z-index:999;
	}
	
	/* POPUP CONTAINER */
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
	
	/* POPUP FORM – LEFT aligned, 2 rows, fixed widths */
	.popup-form{
	max-width:720px;
	width:100%;
	margin:0;
	}
	.popup-row{
	display:flex;
	flex-wrap:nowrap;
	gap:18px;            /* symmetric gaps between columns */
	margin-bottom:14px;  /* gap between rows */
	}
	.popup-row > div{
	width:310px;         /* fixed width for each field */
	}
	
	/* popup inputs & selects – dark, no white */
	.popup-row input,
	.popup-row select{
	width:100%;
	background:#071521;
	color:#e8f0ff;
	border:1px solid rgba(198,214,247,.40);
	padding:6px 9px;
	border-radius:8px;
	outline:none;
	font-size:13px;
	box-sizing:border-box;
	}
	.popup-row input:focus,
	.popup-row select:focus{
	border-color:#6ea2ff;
	box-shadow:0 0 0 2px rgba(110,162,255,.25);
	}
	
	/* HOURS TABLE IN POPUP */
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
    border:none;                 /* ← No border */
    border-radius:6px;
    color:#e6efff;
    font-size:12px;
    padding:1px 7px;
    cursor:pointer;
	}
	.row-clear-btn:hover{
	    background:#2a487e;
	}

	.row-copy-btn{
    background:transparent;
    border:none;                 /* ← No border */
    border-radius:6px;
    color:#e6efff;
    font-size:12px;
    padding:1px 7px;
    cursor:pointer;
	}
	.row-copy-btn:hover{
	    background:#2a487e;
	}
	.price-input.zero-warning{
	border-color:#ff5c5c !important;
	background:#3b1111 !important;
	}
	
	/* POPUP BUTTONS */
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
	
	/* HIDE APPLY FILTER BUTTON */
	  /*  .filter-actions {*/
	  /*      display: none !important;*/
	  /*  }*/
		/* === CHROME / EDGE / SAFARI (WebKit) === */
		.gridWrap::-webkit-scrollbar {
		    width: 10px !important;
		}
		
		.gridWrap::-webkit-scrollbar-track {
		    background: #1a2334 !important;
		    border-radius: 8px;
		}
		
		.gridWrap::-webkit-scrollbar-thumb {
		    background: #555c66 !important;
		    border-radius: 8px;
		}
		
		.gridWrap::-webkit-scrollbar-thumb:hover {
		    background: #79808a !important;
		}
		
		/* === FIREFOX === */
		.gridWrap {
		    scrollbar-width: thin !important;
		    scrollbar-color: #555c66 #1a2334 !important;  /* thumb / track */
		}
	/* Base styling (same for Edit + Delete) */
	.action-btn{
	    padding:4px 12px;
	    font-size:12px;
	    border-radius:6px;
	    border:1px solid rgba(15,23,42,.9);
	    background:#1f2937;
	    color:#f9fafb;
	    cursor:pointer;
	    white-space:nowrap;
	    box-shadow:0 1px 0 rgba(0,0,0,.28) inset;
	    transition:all .15s ease;
	
	    width: 70px;          /* << EXACT same width */
	    text-align: center;
	    display: inline-block;
	}

	/* EDIT BUTTON  (your color #416b95) */
	.action-btn.edit{
	    background:#416b95;     /* EXACT color you provided */
	    border-color:#1e40af;   /* same border tone as in your snippet */
	}
	.action-btn.edit:hover:not(:disabled){
	    background:#1d4ed8;     /* EXACT hover you provided */
	}
	
	/* DELETE BUTTON (your color #b91c1c) */
	.action-btn.delete{
	    background:#b91c1c;     /* EXACT color from your snippet */
	    color:#f9fafb;          /* you provided this explicitly */
	    border-color:#7f1d1d;   /* matching Contragents border tone */
	}
	.action-btn.delete:hover:not(:disabled){
	    background:#dc2626;     /* EXACT hover from your snippet */
	}
	
	</style>
	</head>
	
	<body>
	<div class="page">
	<div class="header">Market prices (OPCOM / RDN / OPEM)</div>
	
	<div class="toolbar">
	<button class="btn newslot" onclick="startNewSlot()">+ New slot</button>
	<!-- Reload list button removed -->
	</div>
	
	<!-- FILTER PANEL (TOP LIST FILTERS) -->
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
	    <label>Market</label>
	    <select id="listMarket">
	      <option value="">All markets</option>
	      <option value="OPCOM">OPCOM</option>
	      <option value="RDN">RDN</option>
	      <option value="OPEM">OPEM</option>
	    </select>
	  </div>
	  <div>
	    <label>Currency</label>
	    <select id="listCurrency">
	      <option value="">All currencies</option>
	      <option value="978">EUR</option>
	      <option value="946">RON</option>
	      <option value="980">UAH</option>
	      <option value="840">USD</option>
	      <option value="498">MDL</option>
	    </select>
	  </div>
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
	
	<!-- Export button above grid -->
	<div class="gridExportBar">
	  <button class="btn export-btn" onclick="exportToExcel()">
	    <span class="export-icon">⬇</span>
	    <span class="export-text">Download Excel</span>
	  </button>
	</div>
	
	<!-- GRID (plain table) -->
	<div class="gridPanel">
	<div class="gridWrap">
	  <table id="slotGrid" class="data-grid">
	    <thead>
		  <tr>
		    <th></th> <!-- expander -->
		
		    <th data-sort="slotIdx" class="sortable">
		      Slot <span class="sort-arrow"></span>
		    </th>
			<!-- NEW: Created At -->
		    <th data-sort="created_at" class="sortable">
		      Created At <span class="sort-arrow"></span>
		    </th>
		    
		
		    <!-- NEW: Date From -->
		    <th data-sort="date_from" class="sortable">
		      Date From <span class="sort-arrow"></span>
		    </th>
		
		    <!-- NEW: Date To -->
		    <th data-sort="date_to" class="sortable">
		      Date To <span class="sort-arrow"></span>
		    </th>
		
		    <th data-sort="market" class="sortable">
		      Market <span class="sort-arrow"></span>
		    </th>
		
		    <th data-sort="currencyid" class="sortable">
		      Currency <span class="sort-arrow"></span>
		    </th>
		
		    <th data-sort="forecast_price_closed" class="sortable">
		      Avg price <span class="sort-arrow"></span>
		    </th>
		
		    <th data-sort="CURRENCY_FX_EQ_MDL" class="sortable">
		      Avg FX <span class="sort-arrow"></span>
		    </th>
		
		    <th data-sort="forecast_price_closed_eq" class="sortable">
		      Avg price eq MDL <span class="sort-arrow"></span>
		    </th>
		
		    <th>Actions</th>
		  </tr>
		</thead>
	    <tbody></tbody>
	  </table>
	</div>
	</div>
	</div>
	
	<!-- POPUP (HIDDEN BY DEFAULT) -->
	<div id="slotModalBackdrop" class="modal-backdrop" style="display:none;">
	<div class="modal">
	<div class="modal-body">
	  <div class="popup-form">
	    <!-- row 1: dates -->
	    <div class="popup-row" id="rowSlotDates">
	      <div>
	        <label>Slot date from</label>
	        <input type="date" id="slotDateFrom"/>
	      </div>
	      <div>
	        <label>Slot date to</label>
	        <input type="date" id="slotDateTo"/>
	      </div>
	    </div>
	    <!-- row 2: market + currency -->
	    <div class="popup-row">
	      <div>
	        <label>Market</label>
	        <select id="slotMarket">
	          <option value="OPCOM">OPCOM</option>
	          <option value="RDN">RDN</option>
	          <option value="OPEM">OPEM</option>
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
	var currentEditKey = null;
	var lastTypedValue = null;
	
	
	/* currency code -> name */
	var CCY_MAP = {
	"978":"EUR",
	"840":"USD",
	"946":"RON",
	"980":"UAH",
	"498":"MDL"
	};
	
	/* for sorting/export */
	var currentRows = [];
	var sortState = { col:null, dir:1 };
	var NUM_FIELDS = {
	"hour_slot":1,
	"CURRENCY_FX_EQ_MDL":1,
	"forecast_price_closed":1,
	"forecast_price_closed_eq":1,
	"_idx":1
	};
	var CHILD_NUM_FIELDS = {
    hour_slot: 1,
    forecast_price_closed: 1,
    CURRENCY_FX_EQ_MDL: 1,
    forecast_price_closed_eq: 1
};
	function pad2(n){ return (n<10 ? "0"+n : ""+n); }
	function toDateInputValue(d){
	var yyyy = d.getFullYear(), mm = pad2(d.getMonth()+1), dd = pad2(d.getDate());
	return yyyy + "-" + mm + "-" + dd;
	}
	function formatNumberSpace(x, decimals){
    if (x === null || x === undefined || x === "") return "";
    x = String(x).replace(",", ".");  // normalize , -> .
    var num = Number(x);
    if (isNaN(num)) return x;

    var opts = {};
    if (typeof decimals === "number") {
        opts.minimumFractionDigits = decimals;
        opts.maximumFractionDigits = decimals;
    }

    // format with space as thousand separator
    return num.toLocaleString("fr-FR", opts).replace(/\u00A0/g, " ");
}
	/* MODAL OPEN/CLOSE */
	function openSlotModal(){
	document.getElementById("slotModalBackdrop").style.display = "flex";
	clearZeroHighlight();
	}
	function closeSlotModal(){
	document.getElementById("slotModalBackdrop").style.display = "none";
	}
	
	/* HOURS TABLE */
	function buildHoursTable(){
    lastTypedValue = null; // reset whenever table is built

    var table = document.getElementById("hoursTable");
    table.innerHTML = "";
    
    var thead = document.createElement("thead");
    var hr = document.createElement("tr");
    var th0 = document.createElement("th");
    th0.textContent = "Price per hour (MWh)";
    hr.appendChild(th0);
    
    for (var h=1; h<=24; h++){
        var th = document.createElement("th");
        th.textContent = pad2(h);
        hr.appendChild(th);
    }
    thead.appendChild(hr);
    table.appendChild(thead);
    
    var tbody = document.createElement("tbody");
    table.appendChild(tbody);
    
    var tr = document.createElement("tr");
    var tdLabel = document.createElement("td");
    tdLabel.innerHTML =
      '<div class="indicator-row">' +
        '<span>Price</span>' +
        '<button type="button" class="row-clear-btn" onclick="fillAllValuesWithZero()">🧹</button>' +
        '<button type="button" class="row-copy-btn" onclick="copyLastValueToAll()">📄</button>' +
      '</div>';
    tr.appendChild(tdLabel);
    
    // create inputs
    for (var h=1; h<=24; h++){
        var td = document.createElement("td");
        var input = document.createElement("input");
        input.type = "text";
        input.className = "price-input";
        input.setAttribute("data-hour", h);
        td.appendChild(input);
        tr.appendChild(td);
    }
    tbody.appendChild(tr);

    // 🔥 ATTACH LAST-TYPED LISTENERS
    setTimeout(function(){
        document.querySelectorAll(".price-input").forEach(function(inp){
            inp.addEventListener("input", function(){
                var v = (this.value || "").trim();
                if (v !== "") {
                    lastTypedValue = v;  // store the last edited value
                }
            });
        });
    }, 0);
	}
	
	function clearHourValues(){
	document.querySelectorAll(".price-input").forEach(function(inp){ inp.value=""; });
	}
	function fillAllValuesWithZero(){
	document.querySelectorAll(".price-input").forEach(function(inp){ inp.value="0"; });
	}
	function clearZeroHighlight(){
	document.querySelectorAll(".price-input").forEach(function(i){ i.classList.remove("zero-warning"); });
	}
	function markZeroCellsAndCount(){
	clearZeroHighlight();
	var count = 0;
	document.querySelectorAll(".price-input").forEach(function(inp){
	var v = (inp.value || "").trim().replace(",", ".");
	var num = parseFloat(v);
	if (!isNaN(num) && num === 0){
	  inp.classList.add("zero-warning");
	  count++;
	}
	});
	return count;
	}
	/*COPY LAST VALUE in VALUE CELL in PRICE POP UP NEW SLOT*/
	function copyLastValueToAll(){
    if (lastTypedValue === null){
        alert("Firstly input a value in a cell.");
        return;
    }

    document.querySelectorAll(".price-input").forEach(function(inp){
        inp.value = lastTypedValue;
    });
}
	/* PAYLOAD */
	function collectSlotPayload(){
	var prices = {};
	document.querySelectorAll(".price-input").forEach(function(inp){
	prices[inp.getAttribute("data-hour")] = inp.value || null;
	});
	return {
	mode: currentMode,
	date_from: document.getElementById("slotDateFrom").value,
	date_to:   document.getElementById("slotDateTo").value,
	market:    document.getElementById("slotMarket").value,
	currencyid:document.getElementById("slotCurrency").value,
	prices: prices
	};
	}
	
	function applySlotData(slot){
	document.getElementById("slotDateFrom").value = slot.date_from || "";
	document.getElementById("slotDateTo").value   = slot.date_to   || "";
	document.getElementById("slotMarket").value   = slot.market;
	document.getElementById("slotCurrency").value = slot.currencyid;
	
	clearHourValues();
	var prices = slot.prices || {};
	document.querySelectorAll(".price-input").forEach(function(inp){
	var h = inp.getAttribute("data-hour");
	inp.value = prices[h] != null ? prices[h] : "0";
	});
	}
	
	/* RENDER LIST TABLE */
	var currentGroups = [];
	
	/* group flat rows into slots: (date + market + currency) */
	function buildSlotGroups(rows){
	    var map = {};
	    rows.forEach(function(r){
	        var key = (r.data || "") + "|" + (r.market || "") + "|" + (r.currencyid || "");
	        if (!map[key]){
	            map[key] = {
	                data: r.data || "",
	                market: r.market || "",
	                currencyid: r.currencyid || "",
	                rows: []
	            };
	        }
	        map[key].rows.push(r);
	    });
	
	    var groups = [];
	    var slotIdx = 1;
	    for (var key in map){
	        if (!map.hasOwnProperty(key)) continue;
	        var g = map[key];
	
	        var sumPrice = 0, sumFx = 0, sumEq = 0, nPrice = 0, nFx = 0, nEq = 0;
	
	        g.rows.forEach(function(r){
	            var p  = Number(String(r.forecast_price_closed || "").replace(",", "."));
	            var fx = Number(String(r.CURRENCY_FX_EQ_MDL || "").replace(",", "."));
	            var eq = Number(String(r.forecast_price_closed_eq || "").replace(",", "."));
	
	            if (!isNaN(p)){ sumPrice += p; nPrice++; }
	            if (!isNaN(fx)){ sumFx += fx; nFx++; }
	            if (!isNaN(eq)){ sumEq += eq; nEq++; }
	        });
	
	        var firstRow = g.rows[0] || {};

		groups.push({
		    slotIdx: slotIdx++,
		    data: g.data,
		    market: g.market,
		    currencyid: g.currencyid,
		
		    // NEW ADDED FIELDS
		    created_at: firstRow.created_at || "",
		    date_from:  firstRow.date_from  || "",
		    date_to:    firstRow.date_to    || "",
		
		    avgPrice: nPrice ? (sumPrice / nPrice) : null,
		    avgFx:    nFx    ? (sumFx    / nFx)    : null,
		    avgEq:    nEq    ? (sumEq    / nEq)    : null,
		
		    rows: g.rows
		});
	    }
	
	    return groups;
	}
	function openEditSlot(groupIndex){
    var g = currentGroups[groupIndex];
    if (!g) return;

    // prevent editing old slots
    var todayStr = toDateInputValue(new Date());
    if (g.data < todayStr){
        alert("You can edit only slots with date >= today.");
        return;
    }

	    currentMode = "edit";
	    currentEditKey = {
	        data: g.data,
	        market: g.market,
	        currencyid: g.currencyid
	    };
	
	    // hide date selectors during edit
	    var datesRow = document.getElementById("rowSlotDates");
	    if (datesRow) datesRow.style.display = "none";
	
	    // create a fake slot object for applySlotData()
	    var slot = {
	        date_from: g.data,
	        date_to:   g.data,
	        market:    g.market,
	        currencyid: g.currencyid,
	        prices: {}
	    };
	
	    g.rows.forEach(function(r){
	        slot.prices[r.hour_slot] = r.forecast_price_closed;
	    });
	
	    applySlotData(slot);
	    openSlotModal();
	}
	/* DELETE THE PARENT ROW */
	function onDeleteSlot(groupIndex){
	    var g = currentGroups[groupIndex];
	    if (!g) return;
	
	    // 🔒 prevent deleting old slots
	    var todayStr = toDateInputValue(new Date());  // YYYY-MM-DD
	    if (g.data < todayStr){
	        alert("You can delete only slots with date >= today.");
	        return;
	    }
	
	    if (!confirm("Are you sure you want to delete this slot?")) return;
	
	    var payload = {
	        mode:"delete",
	        date_from: g.data,
	        date_to:   g.data,
	        market:    g.market,
	        currencyid:g.currencyid
	    };
	
	    fetch("./saveSlot", {
	        method:"POST",
	        headers:{ "Content-Type":"application/json" },
	        body:JSON.stringify(payload)
	    })
	    .then(r => r.json())
	    .then(json => {
	        if (!json.ok){
	            alert("Delete failed: " + (json.error || "unknown"));
	            return;
	        }
	        reloadSlots();
	    })
	    .catch(err => alert("Error: "+err));
	}
function renderSlotTableFromGroups(groups){
    var tbody = document.querySelector("#slotGrid tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    groups.forEach(function(g, gi){
        /* PARENT ROW (slot summary) */
        var trP = document.createElement("tr");
        trP.className = "slot-parent";
        trP.setAttribute("data-group", gi);

        // cell helper
        function td(val, cls){
            var cell = document.createElement("td");
            if (cls) cell.className = cls;
            if (val === null || val === undefined || val === "null" || val === "NULL") val = "";
            cell.textContent = val;
            trP.appendChild(cell);
        }

        // expander cell
        var tdExp = document.createElement("td");
        tdExp.className = "expander-cell";
        var span = document.createElement("span");
        span.className = "expander";
        span.setAttribute("data-group", gi);
        span.textContent = "+";
        tdExp.appendChild(span);
        trP.appendChild(tdExp);

        var currencyName = CCY_MAP[String(g.currencyid)] || (g.currencyid || "");

        td(g.slotIdx);                           // Slot
			td(g.created_at || "");                  // Created At
			td(g.date_from || "");                   // Date From
			td(g.date_to || "");                     // Date To
			td(g.market || "");                      // Market
			td(currencyName);                        // Currency
			td(formatNumberSpace(g.avgPrice, 1), "col-right");
			td(formatNumberSpace(g.avgFx, 2), "col-right");
			td(formatNumberSpace(g.avgEq, 1), "col-right");

        // --- NEW: single "Actions" column with both buttons ---
        var tdActions = document.createElement("td");
        tdActions.className = "actions-cell";

        var btnEdit = document.createElement("button");
        btnEdit.className = "action-btn edit";
        btnEdit.textContent = "Edit";
        btnEdit.onclick = function(ev){
            ev.stopPropagation();
            openEditSlot(gi);
        };
        tdActions.appendChild(btnEdit);

        var btnDel = document.createElement("button");
        btnDel.className = "action-btn delete";
        btnDel.textContent = "Delete";
        btnDel.style.marginLeft = "6px";
        btnDel.onclick = function(ev){
            ev.stopPropagation();
            onDeleteSlot(gi);
        };
        tdActions.appendChild(btnDel);

        trP.appendChild(tdActions);
        tbody.appendChild(trP);

        /* CHILD ROW (full present table for that slot) */
        var trC = document.createElement("tr");
        trC.className = "slot-child";
        trC.setAttribute("data-group", gi);
        trC.style.display = "none";

        var tdChild = document.createElement("td");
        tdChild.className = "slot-child-cell";
        tdChild.colSpan = 11;   // expander + 7 data cols + Actions = 9

        var inner = document.createElement("table");
        inner.className = "child-grid";

        var thead = document.createElement("thead");
        var hr = document.createElement("tr");

        // headers + fields for child sorting
        var childHeaders = [
            { label: "#",            field: null },
            { label: "Date",         field: "data" },
            { label: "Hour",         field: "hour_slot" },
            { label: "Market",       field: "market" },
            { label: "Currency",     field: "currencyid" },
            { label: "Price",        field: "forecast_price_closed" },
            { label: "FX",           field: "CURRENCY_FX_EQ_MDL" },
            { label: "Price eq MDL", field: "forecast_price_closed_eq" }
        ];

        // per-group sort state for the child grid
        if (!g.childSort){
            g.childSort = { col: null, dir: 1 };
        }

        childHeaders.forEach(function(col){
            var th = document.createElement("th");
            th.textContent = col.label;

            if (col.field){
                th.classList.add("sortable");
                th.setAttribute("data-sort-child", col.field);

                var arrow = document.createElement("span");
                arrow.className = "sort-arrow";
                th.appendChild(arrow);

                th.addEventListener("click", function(ev){
                    ev.stopPropagation();
                    var field = col.field;
                    var sortState = g.childSort;

                    // flip / set direction
                    if (sortState.col === field){
                        sortState.dir = -sortState.dir;
                    } else {
                        sortState.col = field;
                        sortState.dir = 1;
                    }
                    var dir = sortState.dir;

                    // clear arrow classes only in THIS child header row
                    hr.querySelectorAll("th.sortable").forEach(function(th2){
                        th2.classList.remove("asc", "desc");
                    });
                    th.classList.add(dir === 1 ? "asc" : "desc");

                    // sort underlying rows for THIS group
                    g.rows.sort(function(a, b){
                        var va = a[field];
                        var vb = b[field];

                        if (va == null && vb == null) return 0;
                        if (va == null) return -1 * dir;
                        if (vb == null) return 1 * dir;

                        if (CHILD_NUM_FIELDS[field]){
                            va = Number(va);
                            vb = Number(vb);
                            if (isNaN(va) && isNaN(vb)) return 0;
                            if (isNaN(va)) return -1 * dir;
                            if (isNaN(vb)) return 1 * dir;
                        } else {
                            va = String(va);
                            vb = String(vb);
                        }

                        if (va < vb) return -1 * dir;
                        if (va > vb) return 1 * dir;
                        return 0;
                    });

                    // re-render only this child body
                    renderChildBody(gi);
                });
            }

            hr.appendChild(th);
        });

        thead.appendChild(hr);
        inner.appendChild(thead);

        var tb = document.createElement("tbody");
        tb.id = "child-body-" + gi;
        inner.appendChild(tb);

        // helper that draws the rows for this child table
        function renderChildBody(groupIndex){
            var body = document.getElementById("child-body-" + groupIndex);
            if (!body) return;
            body.innerHTML = "";

            var gg = currentGroups[groupIndex];

            gg.rows.forEach(function(r, idx){
                var tr = document.createElement("tr");

                function td2(val, cls){
                    var cell = document.createElement("td");
                    if (cls) cell.className = cls;
                    if (val === null || val === undefined || val === "null" || val === "NULL") val = "";
                    cell.textContent = val;
                    tr.appendChild(cell);
                }

                var currencyNameRow = CCY_MAP[String(r.currencyid)] || (r.currencyid || "");

                td2(idx + 1);                                                // #
                td2(r.data || "");                                          // Date
                td2(r.hour_slot != null ? r.hour_slot : "");                // Hour
                td2(r.market || "");                                        // Market
                td2(currencyNameRow);                                       // Currency
                td2(formatNumberSpace(r.forecast_price_closed, 1), "col-right");
                td2(formatNumberSpace(r.CURRENCY_FX_EQ_MDL, 2), "col-right");
                td2(formatNumberSpace(r.forecast_price_closed_eq, 2), "col-right");

                body.appendChild(tr);
            });
        }

        tdChild.appendChild(inner);
        trC.appendChild(tdChild);
        tbody.appendChild(trC);

        // first render AFTER adding to DOM
        renderChildBody(gi);
    });

    // bind expand/collapse
    document.querySelectorAll(".expander").forEach(function(el){
        el.onclick = function(ev){
            ev.stopPropagation();
            var gid = this.getAttribute("data-group");
            var childRow = document.querySelector('tr.slot-child[data-group="' + gid + '"]');
            if (!childRow) return;
            var isOpen = childRow.style.display !== "none";
            childRow.style.display = isOpen ? "none" : "";
            this.classList.toggle("open", !isOpen);
            this.textContent = isOpen ? "+" : "−";
        };
    });
}
	
	/* SORTING */
	// which group fields are numeric
var GROUP_NUM_FIELDS = {
    slotIdx: 1,
    avgPrice: 1,
    avgFx: 1,
    avgEq: 1
};

function sortBy(field){
    if (!currentGroups || !currentGroups.length) return;

    // flip / set direction
    if (sortState.col === field){
        sortState.dir = -sortState.dir;
    } else {
        sortState.col = field;
        sortState.dir = 1;
    }
    var dir = sortState.dir;

    // 🔽 clear previous arrows
    document.querySelectorAll("#slotGrid thead th.sortable")
        .forEach(function(th){
            th.classList.remove("asc", "desc");
        });

    // 🔼 mark active header
    var activeTh = document.querySelector(
        '#slotGrid thead th[data-sort="' + field + '"]'
    );
    if (activeTh){
        activeTh.classList.add(dir === 1 ? "asc" : "desc");
    }

    // sort the *groups*
    currentGroups.sort(function(a, b){
        var va = a[field];
        var vb = b[field];

        if (va == null && vb == null) return 0;
        if (va == null) return -1 * dir;
        if (vb == null) return 1 * dir;

        if (GROUP_NUM_FIELDS[field]) {
            va = Number(va);
            vb = Number(vb);
            if (isNaN(va) && isNaN(vb)) return 0;
            if (isNaN(va)) return -1 * dir;
            if (isNaN(vb)) return 1 * dir;
        } else {
            va = String(va);
            vb = String(vb);
        }

        if (va < vb) return -1 * dir;
        if (va > vb) return 1 * dir;
        return 0;
    });

    // re-render grouped table
    renderSlotTableFromGroups(currentGroups);
}
	
	/* RELOAD SLOTS – uses listSlots WebDev */
	function reloadSlots(){
	var from     = document.getElementById("listFrom").value;
	var to       = document.getElementById("listTo").value;
	var market   = document.getElementById("listMarket").value;
	var currency = document.getElementById("listCurrency").value;
	var hour     = document.getElementById("listHour").value;
	
	var url = "./listSlots?from=" + encodeURIComponent(from) +
	        "&to=" + encodeURIComponent(to) +
	        "&market=" + encodeURIComponent(market || "") +
	        "&currency=" + encodeURIComponent(currency || "") +
	        "&hour=" + encodeURIComponent(hour || "");
	
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
	  console.log("slots data:", data);
	  var rows = Array.isArray(data) ? data : (data.rows || []);
	
	  rows.forEach(function(r, idx){ r._idx = idx; });
	
	  currentRows = rows.slice();
	  sortState = {col:null, dir:1};
	
	  if (debugEl){
	    debugEl.textContent = "Loaded " + rows.length + " rows.";
	  }
	  currentGroups = buildSlotGroups(currentRows);
	  renderSlotTableFromGroups(currentGroups);
	})
	.catch(function(err){
	  console.error("Error loading slots:", err);
	  if (debugEl){
	    debugEl.textContent = "Error loading slots: " + err;
	  }
	  currentRows = [];
	  currentGroups = [];
	  renderSlotTableFromGroups(currentGroups);
	});
	}
	
	/* EXPORT TO "EXCEL" (CSV) */
	function exportToExcel(){
	var rows = currentRows || [];
	if (!rows.length){
	alert("No data to export.");
	return;
	}
	
	var header = ["#","Date","Hour","Market","Price","Currency","FX rate","Price eq MDL"];
	var lines = [];
	lines.push(header.join(";"));
	
	rows.forEach(function(r, idx){
	var currency = CCY_MAP[String(r.currencyid)] || (r.currencyid || "");
	var fx = (r.CURRENCY_FX_EQ_MDL != null ? r.CURRENCY_FX_EQ_MDL : "");
	var price = (r.forecast_price_closed != null ? r.forecast_price_closed : "");
	var priceEq = (r.forecast_price_closed_eq != null ? r.forecast_price_closed_eq : "");
	
	var line = [
	  idx + 1,
	  r.data || "",
	  (r.hour_slot != null ? r.hour_slot : ""),
	  r.market || "",
	  price,
	  currency,
	  fx,
	  priceEq
	].join(";");
	lines.push(line);
	});
	
	var csv = lines.join("\\r\\n");
	var blob = new Blob([csv], {type:"text/csv;charset=utf-8;"});
	var url = URL.createObjectURL(blob);
	var a = document.createElement("a");
	a.href = url;
	var from = document.getElementById("listFrom").value || "";
	var to   = document.getElementById("listTo").value || "";
	var fname = "market_prices_" + (from || "from") + "_" + (to || "to") + ".csv";
	a.download = fname.replace(/[^a-zA-Z0-9_\\-\\.]/g,"_");
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	URL.revokeObjectURL(url);
	}
	
	/* NEW + SAVE */
	function startNewSlot(){
    currentMode = "new";
    currentEditKey = null;

    // show date row when creating new slot
    var rowDates = document.getElementById("rowSlotDates");
    if (rowDates) rowDates.style.display = "flex";

    var today = new Date();
    var ts = toDateInputValue(today);

    document.getElementById("slotDateFrom").value = ts;
    document.getElementById("slotDateTo").value   = ts;
    document.getElementById("slotMarket").value   = "OPCOM";
    document.getElementById("slotCurrency").value = "978";

    fillAllValuesWithZero();
    openSlotModal();
}
	
	function onSaveSlot(){
    var payload = collectSlotPayload();
    
    console.log("DEBUG payload object:", payload);
    console.log("DEBUG JSON string:", JSON.stringify(payload));
    
    if (!payload.date_from || !payload.date_to){
        alert("Please fill Slot date from / to.");
        return;
    }
    
    // ----- zero-warning + confirmation text -----
	var zeroCount = markZeroCellsAndCount(); 
	var msg;
	
	if (currentMode === "new") {
	    if (zeroCount > 0) {
	        msg = "You have " + zeroCount + " zero-valued hours. Create new slot anyway?";
	    } else {
	        msg = "Create new slot?";
	    }
	} else {
	    if (zeroCount > 0) {
	        msg = "You have " + zeroCount + " zero-valued hours. Override existing values anyway?";
	    } else {
	        msg = "Are you sure you want to override existing values?";
	    }
	}
	
	if (!confirm(msg)) return;
	// -------------------------------------------
	
    fetch("./saveSlot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(function(r){ return r.json(); })
    .then(function(json){
        console.log("DEBUG server reply:", json);
        if (!json.ok){
            alert("Save error: " + (json.error || "unknown"));
            return;
        }
        closeSlotModal();
        reloadSlots();
    })
    .catch(function(err){
        console.error("Fetch error:", err);
        alert("Fetch failed: " + err);
    });
}
	
	/* INIT */
	document.addEventListener("DOMContentLoaded", function(){
	var modal = document.getElementById("slotModalBackdrop");
	if (modal) modal.style.display = "none";
	
	buildHoursTable();
	
	var fromInput    = document.getElementById("listFrom");
	var toInput      = document.getElementById("listTo");
	var marketInput  = document.getElementById("listMarket");
	var ccyInput     = document.getElementById("listCurrency");
	var hourInput    = document.getElementById("listHour");
	
	// 1) read from URL if present (?from=...&to=...&market=...&currency=...&hour=...)
	var params        = new URLSearchParams(window.location.search);
	var fromParam     = params.get("from");
	var toParam       = params.get("to");
	var marketParam   = params.get("market");
	var currencyParam = params.get("currency");
	var hourParam     = params.get("hour");
	
	var today = new Date();
	
	if (fromParam){
	fromInput.value = fromParam;
	} else {
	var listFrom = new Date(today.getTime() - 24*3600*1000);
	fromInput.value = toDateInputValue(listFrom);
	}
	
	if (toParam){
	toInput.value = toParam;
	} else {
	var listTo = new Date(today.getTime() + 24*3600*1000);
	toInput.value = toDateInputValue(listTo);
	}
	
	if (marketParam){
	marketInput.value = marketParam;
	} else {
	marketInput.value = "";
	}
	
	if (currencyParam){
	ccyInput.value = currencyParam;
	} else {
	ccyInput.value = "";
	}
	
	if (hourParam){
	hourInput.value = hourParam;
	} else {
	hourInput.value = "";
	}
	
	// clickable headers for sorting
	document.querySelectorAll("#slotGrid thead th[data-sort]").forEach(function(th){
	th.style.cursor = "pointer";
	th.addEventListener("click", function(){
	  var f = th.getAttribute("data-sort");
	  sortBy(f);
	});
	});
	    // Auto-apply filters when user changes Market / Currency / Hour
    document.getElementById("listFrom").addEventListener("change", reloadSlots);
	 document.getElementById("listTo").addEventListener("change", reloadSlots);
    document.getElementById("listMarket").addEventListener("change", reloadSlots);
    document.getElementById("listCurrency").addEventListener("change", reloadSlots);
    document.getElementById("listHour").addEventListener("change", reloadSlots);
	// initial load uses filters from URL or default sysdate-1/+1
	reloadSlots();
	});
	</script>
	</body>
	</html>
	"""
	
	return {"html": html}