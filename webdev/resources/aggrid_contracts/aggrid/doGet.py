def doGet(request, session):

    html = u"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Contracts</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>

  <!-- AG Grid CDN -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ag-grid-community@34.2.0/styles/ag-grid.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ag-grid-community@34.2.0/styles/ag-theme-alpine.css">
  <script src="https://cdn.jsdelivr.net/npm/ag-grid-community@34.2.0/dist/ag-grid-community.min.js"></script>

  <style>
  /* --- SLATE (lighter dark) theme --------------------------------------- */
  html,body{
    height:100%; margin:0;
    background:#162235;
    color:#e6eeff;
    font:14px/1.4 system-ui,Segoe UI,Roboto,Arial;
  }

  .page{height:100vh;display:flex;flex-direction:column}

  .header{
    font-size:28px; font-weight:800;
    padding:16px 18px;
    color:#f0f4ff;
  }

  .toolbar{display:flex;gap:12px;padding:0 18px 12px 18px}
  .btn{
    padding:10px 14px; cursor:pointer;
    border-radius:10px;
    border:1px solid rgba(204,220,255,.45);
    background:#203a63;
    color:#e9f2ff;
    box-shadow:0 1px 0 rgba(0,0,0,.18) inset;
  }
  .btn:hover{ background:#2a487e; }
  .btn.primary{ background:#2751a0; border-color:#5c86db; }
  .btn.primary:hover{ background:#2e5fbb; }
  .btn.danger{ background:#63293a; border-color:#b86d7c; }
  .btn.danger:hover{ background:#7a3046; }

  .panel{
    margin:0 18px 16px 18px;
    border:1px solid rgba(204,220,255,.32);
    border-radius:12px;
    padding:14px;
    background:#1a2a45;
    box-shadow:0 2px 12px rgba(0,0,0,.15);
  }

  .row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:12px}
  label{display:block;font-size:12px;opacity:.86;margin-bottom:6px;color:#d6e3ff}

  input,select,textarea{
    width:100%;
    background:#1b2d4a;
    color:#ebf2ff;
    border:1px solid rgba(198,214,247,.45);
    padding:8px 10px;border-radius:8px;outline:none
  }
  input::placeholder, textarea::placeholder { color:#a9bde3; }
  input:focus,select:focus,textarea:focus{
    border-color:#6ea2ff; box-shadow:0 0 0 2px rgba(110,162,255,.25);
  }
  textarea{height:44px;resize:vertical}

  /* Fill the rest of the viewport */
  #grid{flex:1 1 auto;min-height:0;margin:0 18px 18px 18px}

  /* --- AG Grid Alpine theming (lighter) --------------------------------- */
  .ag-theme-alpine{
    --ag-background-color: #1b2c4b;
    --ag-foreground-color: #e8f0ff;
    --ag-header-background-color: #203456;
    --ag-header-foreground-color: #eaf2ff;
    --ag-row-border-color: rgba(255,255,255,.08);
    --ag-border-color: rgba(255,255,255,.10);
    --ag-header-column-separator-color: rgba(255,255,255,.18);
    --ag-header-column-separator-width: 1px;
    --ag-font-size: 14px;
  }

  /* Banding + hover */
  .ag-theme-alpine .ag-row:nth-child(odd) .ag-cell { background:#1a2946; }
  .ag-theme-alpine .ag-row:nth-child(even) .ag-cell { background:#1d2f52; }
  .ag-theme-alpine .ag-row-hover .ag-cell { background:#223a65 !important; }

  /* Vertical separators */
  .ag-theme-alpine .ag-header-cell,
  .ag-theme-alpine .ag-header-group-cell{
    border-right:1px solid rgba(255,255,255,.18) !important;
  }
  .ag-theme-alpine .ag-center-cols-container .ag-cell{
    border-right:1px solid rgba(255,255,255,.12) !important;
    border-top-color:rgba(255,255,255,.06) !important;
    border-bottom-color:rgba(255,255,255,.06) !important;
    border-left-color:transparent !important;
  }

  /* Hide menu icons */
  .ag-header-cell-menu-button,.ag-header-icon{display:none !important;}

  /* Pinned-left divider */
  .ag-theme-alpine .ag-pinned-left-header,
  .ag-theme-alpine .ag-pinned-left-cols-container{
    border-right:1px solid rgba(110,162,255,.55) !important;
    box-shadow:1px 0 0 rgba(110,162,255,.25);
  }

  /* Compact sizes */
  .ag-theme-alpine .ag-row{height:36px;}
  .ag-theme-alpine .ag-header{height:40px;}

  .right { text-align:right; }

  /* FORCE WHITE TEXT IN CELLS */
  .ag-theme-alpine .ag-cell,
  .ag-theme-alpine .ag-value-cell,
  .ag-theme-alpine .ag-cell-value { color:#e8f0ff !important; }

  .ag-theme-alpine .ag-header-cell-text,
  .ag-theme-alpine .ag-header-group-cell-label { color:#eaf2ff !important; }

  .ag-theme-alpine,
  .ag-theme-alpine .ag-root-wrapper,
  .ag-theme-alpine .ag-root-wrapper-body,
  .ag-theme-alpine .ag-center-cols-viewport,
  .ag-theme-alpine .ag-center-cols-container,
  .ag-theme-alpine .ag-header,
  .ag-theme-alpine .ag-floating-top,
  .ag-theme-alpine .ag-floating-bottom { background:#1b2c4b !important; }

  .ag-theme-alpine .ag-pinned-left-header,
  .ag-theme-alpine .ag-pinned-left-cols-container,
  .ag-theme-alpine .ag-pinned-right-header,
  .ag-theme-alpine .ag-pinned-right-cols-container { background:#1b2c4b !important; }

  .page{height:100vh;display:flex;flex-direction:column;}
  #grid{flex:1 1 auto;min-height:0;}

  /* Cell borders (body) */
  .ag-theme-alpine .ag-center-cols-container .ag-row .ag-cell {
    border-right: 1px solid rgba(255,255,255,.18) !important;
    border-bottom: 1px solid rgba(255,255,255,.12) !important;
  }
  .ag-theme-alpine .ag-center-cols-container .ag-row .ag-cell:last-child {
    border-right: 1px solid rgba(255,255,255,.18) !important;
  }

  /* Header borders */
  .ag-theme-alpine .ag-header {
    border-bottom: 1px solid rgba(255,255,255,.24) !important;
  }
  .ag-theme-alpine .ag-header-cell,
  .ag-theme-alpine .ag-header-group-cell {
    border-right: 1px solid rgba(255,255,255,.18) !important;
  }
  .ag-theme-alpine .ag-header-cell:last-child,
  .ag-theme-alpine .ag-header-group-cell:last-child {
    border-right: 1px solid rgba(255,255,255,.18) !important;
  }

  .ag-theme-alpine .ag-root-wrapper {
    border: 1px solid rgba(255,255,255,.22) !important;
    border-radius: 8px;
  }
  .ag-theme-alpine .ag-pinned-left-header,
  .ag-theme-alpine .ag-pinned-left-cols-container {
    border-right: 2px solid rgba(255,255,255,.24) !important;
  }

  /* EXCLUDE LAST-ROW BOTTOM BORDER (scoped) */
  .contracts-grid .ag-center-cols-container .ag-row-last .ag-cell,
  .contracts-grid .ag-center-cols-container .ag-row:last-child .ag-cell,
  .contracts-grid .ag-pinned-left-cols-container .ag-row-last .ag-cell,
  .contracts-grid .ag-pinned-right-cols-container .ag-row-last .ag-cell {
    border-bottom: none !important;
  }
  </style>
</head>
<body>
  <div class="page">
    <div class="header">Contracts</div>

    <div class="toolbar">
      <button class="btn"          id="btnNew">New</button>
      <button class="btn primary" id="btnSave">Save</button>
      <button class="btn danger"  id="btnDelete">Delete</button>
      <button class="btn"         id="btnReload">Reload</button>
      <div style="margin-left:auto;opacity:.7;font-size:12px" id="stat">loading…</div>
    </div>

    <div class="panel">
      <div class="row">
        <div>
          <label>Counterparty (contragentid)</label>
          <select id="f_contragentid">
            <option value="">-- Select counterparty --</option>
          </select>
        </div>
        <div>
          <label>Contract Code (dealno)</label>
          <input id="f_dealno" placeholder="ACME-2026-BASE"/>
        </div>
        <div>
          <label>Product / Type (contract_typeid)</label>
          <select id="f_contract_typeid">
            <option value="">-- Select type --</option>
          </select>
        </div>
      </div>

      <div class="row">
        <div>
          <label>Currency (contract_currencyid)</label>
          <select id="f_contract_currencyid">
            <option value="">-- Select currency --</option>
          </select>
        </div>
        <div>
          <label>Country (contragent_countryid)</label>
          <select id="f_contragent_countryid">
            <option value="">-- Select country --</option>
          </select>
        </div>
        <div>
          <label>Border cost CCY (x_border_cost_ccyid)</label>
          <select id="f_x_border_cost_ccyid">
            <option value="">-- Select CCY --</option>
          </select>
        </div>
      </div>

      <div class="row">
        <div>
          <label>Start Date (date_from)</label>
          <input id="f_date_from" type="date"/>
        </div>
        <div>
          <label>End Date (date_to)</label>
          <input id="f_date_to" type="date"/>
        </div>
        <div>
          <label>Signed (sign_date)</label>
          <input id="f_sign_date" type="date"/>
        </div>
      </div>

      <div class="row">
        <div>
          <label>Price MWh</label>
          <input id="f_price_mwh" inputmode="decimal" placeholder="3000"/>
        </div>
        <div>
          <label>Price eq MDL</label>
          <input id="f_price_eq_mdl" inputmode="decimal" placeholder="3000"/>
        </div>
        <div>
          <label>Quantity kWh</label>
          <input id="f_quantity_kwh" inputmode="decimal" placeholder="223000"/>
        </div>
      </div>

      <div class="row">
        <div>
          <label>Border costs</label>
          <input id="f_x_border_costs" inputmode="decimal" placeholder="0"/>
        </div>
        <div>
          <label>Internal datetime</label>
          <input id="f_datetime" type="datetime-local"/>
        </div>
        <div>
          <label>Notes (optional)</label>
          <input id="f_notes" placeholder="optional"/>
        </div>
      </div>
      <input type="hidden" id="f_contract_id"/>
    </div>

    <!-- Grid -->
    <div id="grid" class="ag-theme-alpine contracts-grid"></div>
  </div>

  <script>
    const $ = id => document.getElementById(id);
    const STAT = $("stat");
    const setStat = s => STAT.textContent = s;

    function pad2(n){ return (n < 10 ? "0" + n : "" + n); }

    function num(v){
      if(v==null||v==="") return null;
      var n=parseFloat(String(v).replace(/\\s+/g,"").replace(",", "."));
      return isNaN(n)?null:n;
    }
    function fmtNum(p){
      const n = num(p.value);
      return n==null? "" : n.toLocaleString();
    }

    function parseDate(v){ return v || null; }
    function fmtDate(p){
      if(!p.value) return "";
      const s = String(p.value);
      if (/^\\d{4}-\\d{2}-\\d{2}/.test(s)) return s.slice(0,10);
      const d = new Date(s);
      return isNaN(d) ? s.slice(0,10) : d.toISOString().slice(0,10);
    }

    // --- Dropdown data caches ---
    let COUNTERPARTIES = [];
    let CURRENCIES     = [];
    let COUNTRIES      = [];
    let CONTRACT_TYPES = [];

    function loadCounterparties(){
      return fetch("counterparties",{credentials:"same-origin"})
        .then(r=>r.json())
        .then(payload=>{
          COUNTERPARTIES = payload.rows || [];
          const sel = $("f_contragentid");
          sel.innerHTML = "<option value=''>-- Select counterparty --</option>";
          COUNTERPARTIES.forEach(row=>{
            const opt = document.createElement("option");
            opt.value = row.id;     // contragentid
            opt.textContent = row.name; // client_name
            sel.appendChild(opt);
          });
        })
        .catch(e=>console.error("counterparties error",e));
    }

    function loadCurrencies(){
      return fetch("currencies",{credentials:"same-origin"})
        .then(r=>r.json())
        .then(payload=>{
          CURRENCIES = payload.rows || [];
          const selMain = $("f_contract_currencyid");
          const selBCost = $("f_x_border_cost_ccyid");
          selMain.innerHTML  = "<option value=''>-- Select currency --</option>";
          selBCost.innerHTML = "<option value=''>-- Select CCY --</option>";
          CURRENCIES.forEach(row=>{
            const label = row.code + " - " + row.name; // EUR - Euro
            const opt1 = document.createElement("option");
            opt1.value = row.id;
            opt1.textContent = label;
            selMain.appendChild(opt1);

            const opt2 = document.createElement("option");
            opt2.value = row.id;
            opt2.textContent = label;
            selBCost.appendChild(opt2);
          });
        })
        .catch(e=>console.error("currencies error",e));
    }

    function loadCountries(){
      return fetch("countries",{credentials:"same-origin"})
        .then(r=>r.json())
        .then(payload=>{
          COUNTRIES = payload.rows || [];
          const sel = $("f_contragent_countryid");
          sel.innerHTML = "<option value=''>-- Select country --</option>";
          COUNTRIES.forEach(row=>{
            const opt = document.createElement("option");
            opt.value = row.code; // MDA, ROU, ...
            opt.textContent = row.code + " - " + row.name;
            sel.appendChild(opt);
          });
        })
        .catch(e=>console.error("countries error",e));
    }

    function loadContractTypes(){
      return fetch("contract_types",{credentials:"same-origin"})
        .then(r=>r.json())
        .then(payload=>{
          CONTRACT_TYPES = payload.rows || [];
          const sel = $("f_contract_typeid");
          sel.innerHTML = "<option value=''>-- Select type --</option>";
          CONTRACT_TYPES.forEach(row=>{
            const opt = document.createElement("option");
            opt.value = row.id;    // contract_typeid
            opt.textContent = row.name;
            sel.appendChild(opt);
          });
        })
        .catch(e=>console.error("contract_types error",e));
    }

    // --- Form helpers ---
    function setForm(row){
      $("f_contract_id").value          = row.contract_id || "";
      $("f_contragentid").value         = row.contragentid || "";
      $("f_dealno").value               = row.dealno || "";
      $("f_contract_typeid").value      = row.contract_typeid || "";
      $("f_contract_currencyid").value  = row.contract_currencyid || "";
      $("f_contragent_countryid").value = row.contragent_countryid || "";
      $("f_x_border_cost_ccyid").value  = row.x_border_cost_ccyid || "";
      $("f_date_from").value            = row.date_from ? String(row.date_from).slice(0,10) : "";
      $("f_date_to").value              = row.date_to   ? String(row.date_to).slice(0,10)   : "";
      $("f_sign_date").value            = row.sign_date ? String(row.sign_date).slice(0,10) : "";
      $("f_price_mwh").value            = row.price_mwh || "";
      $("f_price_eq_mdl").value         = row.price_eq_mdl || "";
      $("f_quantity_kwh").value         = row.quantity_kwh || "";
      $("f_x_border_costs").value       = row.x_border_costs || "";
      $("f_datetime").value             = row.datetime ? String(row.datetime).replace(" ","T").slice(0,16) : "";
      $("f_notes").value                = row.notes || "";

      const isExisting = !!row.contract_id;
      $("f_contragentid").disabled         = isExisting;
      $("f_contract_typeid").disabled      = isExisting;
      $("f_contract_currencyid").disabled  = isExisting;
      $("f_contragent_countryid").disabled = isExisting;
      $("f_x_border_cost_ccyid").disabled  = isExisting;
    }

    function clearForm(){
      setForm({}); // contract_id falsy -> dropdowns enabled
    }

    function readForm(){
      return {
        contract_id: $("f_contract_id").value || null,
        contragentid: $("f_contragentid").value || null,
        dealno: $("f_dealno").value || null,
        contract_typeid: $("f_contract_typeid").value || null,
        contract_currencyid: $("f_contract_currencyid").value || null,
        contragent_countryid: $("f_contragent_countryid").value || null,
        x_border_cost_ccyid: $("f_x_border_cost_ccyid").value || null,
        date_from: parseDate($("f_date_from").value),
        date_to:   parseDate($("f_date_to").value),
        sign_date: parseDate($("f_sign_date").value),
        price_mwh: num($("f_price_mwh").value),
        price_eq_mdl: num($("f_price_eq_mdl").value),
        quantity_kwh: num($("f_quantity_kwh").value),
        x_border_costs: num($("f_x_border_costs").value),
        datetime: (function(v){ return v? v.replace("T"," ") + ":00" : null; })($("f_datetime").value),
        notes: $("f_notes").value || null
      };
    }

    // --- Grid ---
    let gridApi;

    function buildColumns(){
      const defs = [];
      function add(field, header, w, fmt){
        const c = {field, headerName: header||field, minWidth: (w||120), headerClass:"hcenter"};
        if (fmt==="num")   c.valueFormatter = fmtNum,  c.cellClass="right";
        if (fmt==="date")  c.valueFormatter = fmtDate;
        c.suppressHeaderMenuButton = true;
        defs.push(c);
      }
      add("contract_id","ID",90);
      add("dealno","Code",180);
      add("contragentid","Counterparty",140);
      add("contract_typeid","Type",110);
      add("contract_currencyid","Cur",90);
      add("price_mwh","Price MWh",130,"num");
      add("price_eq_mdl","Price eq MDL",140,"num");
      add("quantity_kwh","Quantity kWh",150,"num");
      add("x_border_costs","Border costs",130,"num");
      add("x_border_cost_ccyid","BCost CCY",110);
      add("contragent_countryid","Country",90);
      add("date_from","Start",120,"date");
      add("date_to","End",120,"date");
      add("sign_date","Signed",120,"date");
      add("notes","Notes",220);
      add("datetime","Datetime",170);
      return defs;
    }

    function loadGrid(){
      setStat("fetching…");
      fetch("data",{credentials:"same-origin"})
        .then(r=>r.json())
        .then(payload=>{
          const rows = payload.rows || [];
          const cols = buildColumns();
          const gridDiv = document.getElementById("grid");
          const opts = {
            columnDefs: cols,
            rowData: rows,
            defaultColDef: {resizable:true, sortable:true, filter:true, suppressHeaderMenuButton:true},
            animateRows:true,
            rowHeight:36,
            headerHeight:40,
            onRowClicked: p => setForm(p.data),
          };
          if (gridApi && gridApi.destroy) gridApi.destroy();
          if (agGrid.createGrid) gridApi = agGrid.createGrid(gridDiv, opts);
          else { new agGrid.Grid(gridDiv, opts); gridApi = opts.api; }
          if (gridApi && gridApi.sizeColumnsToFit) setTimeout(()=>gridApi.sizeColumnsToFit(),50);
          setStat("ready • "+rows.length+" rows");
        })
        .catch(e=>{
          document.getElementById("grid").innerHTML =
            "<pre style='color:#ffb3b3;padding:12px'>"+String(e)+"</pre>";
          setStat("error");
        });
    }

    // --- Buttons ---
    $("btnNew").onclick = ()=> clearForm();
    $("btnReload").onclick = ()=> loadGrid();

    $("btnSave").onclick = () => {
      const data = readForm();

      // if internal datetime is empty -> set to NOW (local time)
      if (!data.datetime) {
        const now = new Date();
        const yyyy = now.getFullYear();
        const mm   = pad2(now.getMonth() + 1);
        const dd   = pad2(now.getDate());
        const hh   = pad2(now.getHours());
        const mi   = pad2(now.getMinutes());
        const ss   = pad2(now.getSeconds());

        // value for DB: "YYYY-MM-DD HH:MM:SS"
        data.datetime = yyyy + "-" + mm + "-" + dd + " " + hh + ":" + mi + ":" + ss;

        // value for input control: "YYYY-MM-DDTHH:MM"
        $("f_datetime").value = yyyy + "-" + mm + "-" + dd + "T" + hh + ":" + mi;
      }

      setStat("saving…");
      fetch("save",{
        method:"POST",
        credentials:"same-origin",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(data)
      })
      .then(r=>r.json())
      .then(res=>{
        if(!res.ok){ throw new Error(res.error||"save failed"); }
        setStat("saved • id="+res.contract_id);
        loadGrid();
        setForm(Object.assign({}, data, {contract_id: res.contract_id}));
      })
      .catch(e=>{
        alert("Save error: "+e);
        setStat("error");
      });
    };

    $("btnDelete").onclick = ()=>{
      const id = $("f_contract_id").value;
      if(!id){ alert("Select a row first."); return; }
      if(!confirm("Delete contract "+id+"?")) return;
      setStat("deleting…");
      fetch("delete",{
        method:"POST",
        credentials:"same-origin",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({contract_id:id})
      })
      .then(r=>r.json())
      .then(res=>{
        if(!res.ok){ throw new Error(res.error||"delete failed"); }
        setStat("deleted");
        clearForm();
        loadGrid();
      })
      .catch(e=>{
        alert("Delete error: "+e);
        setStat("error");
      });
    };

    // Load lists first, then grid
    document.addEventListener("DOMContentLoaded", ()=>{
      Promise.all([
        loadCounterparties(),
        loadCurrencies(),
        loadCountries(),
        loadContractTypes()
      ]).then(loadGrid);
    });
  </script>
</body>
</html>
"""
    return {"html": html}