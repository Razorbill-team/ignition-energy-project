def doGet(request, session):
	html = """
	<!doctype html>
	<html>
	<head>
	<meta charset="utf-8"/>
	<title>Contragents View</title>
	<meta name="viewport" content="width=device-width, initial-scale=1"/>
	
	<style>
	/* GLOBAL */
	html, body {
	  height:100%;
	  margin:0;
	  background:#071521;
	  color:#e5ecf5;
	  font: 14px/1.4 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
	}
	.page {
	  height:100vh;
	  width:100vw;
	  display:flex;
	  flex-direction:column;
	  overflow:hidden;
	  background:#071521;
	}
	
	/* TOP BAR */
	.topbar {
	  flex:0 0 auto;
	  display:flex;
	  align-items:center;
	  padding:8px 20px;
	  background:radial-gradient(circle at 0 0, #20365b 0, #050815 60%, #02040b 100%);
	  border-bottom:1px solid #1f2f46;
	  box-shadow:0 2px 8px rgba(0,0,0,0.6);
	  gap:16px;
	}
	.top-title {
	  font-size:22px;
	  font-weight:800;
	  margin-right:auto;
	  color:#f7fafc;
	}
	.top-info {
	  font-size:12px;
	  color:#9fb0c7;
	}
	
	/* MAIN CONTENT */
	.content {
	  flex:1 1 auto;
	  min-height:0;
	}
	.hidden { display:none !important; }
	
	/* LIST PANEL */
	.listPanel {
	  height:100%;
	  display:flex;
	  flex-direction:column;
	  padding:10px 20px 16px;
	  background:#071521;
	}
	
	/* TOOLBAR */
	.grid-toolbar {
	  display:flex;
	  align-items:flex-end;
	  gap:12px;
	  margin-bottom:8px;
	}
	.grid-toolbar .field {
	  max-width:260px;
	}
	.field {
	  display:flex;
	  flex-direction:column;
	  flex:1 1 0;
	  min-width:0;
	}
	.field.small { flex:0 0 160px; }
	.field label {
	  font-size:12px;
	  color:#9fb0c7;
	  margin-bottom:2px;
	  white-space:nowrap;
	}
	.field input,
	.field select {
	  height:30px;
	  border-radius:4px;
	  border:1px solid #243b5a;
	  background:#091421;
	  color:#e5ecf5;
	  padding:4px 8px;
	  box-sizing:border-box;
	  font-size:13px;
	}
	.field input::placeholder {
	  color:#60708a;
	}
	.field input:focus,
	.field select:focus {
	  outline:none;
	  border-color:#2e6af5;
	  box-shadow:0 0 0 1px rgba(46,106,245,0.65);
	}
	/* FILTER PANEL (like Market prices top list filters) */
.panel{
  margin:10px 0px 8px 0px;
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
  flex-wrap:wrap;
  align-items:flex-end;
  gap:18px;
  margin-top:4px;
  margin-bottom:4px;
}
/* make the filter row fill the whole panel width */
.panel .row{
  width:100%;
}

/* adds empty flexible space to the right (panel grows, fields stay fixed) */
.panel .row::after{
  content:"";
  flex: 1 1 auto;
}
/* same sizing idea as Market UI */
.row > div:not(.filter-actions){
  width:240px;
}
.filter-actions{
  margin-left:auto;
  display:flex;
  justify-content:flex-end;
  align-items:flex-end;
}

/* panel inputs */
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
  height:30px;
}
.panel input:focus,
.panel select:focus{
  border-color:#6ea2ff;
  box-shadow:0 0 0 2px rgba(110,162,255,.25);
}

/* Apply filter button */
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
  min-width:140px;
}
.btn.filter-btn:hover{
  background:#4b5563;
  border-color:#6b7280;
  box-shadow:0 0 4px rgba(15,23,42,0.6);
  transform:translateY(-1px);
}
	/* RED BORDER FOR INVALID MANDATORY FIELDS */
	.input-error {
	  border-color:#e11d48 !important;
	  box-shadow:0 0 4px rgba(225,29,72,0.6);
	}
	
	/* search + new button row */
	.search-row {
	  display:flex;
	  align-items:flex-end;
	  gap:8px;
	}
	.search-row input {
	  flex:1 1 auto;
	}
	
	/* GRID PANEL & TABLE */
	.gridPanel {
	  flex:1 1 auto;
	  display:flex;
	  flex-direction:column;
	  min-width:0;
	  background:#071521;
	}
	.gridWrap {
	  flex:1 1 auto;
	  min-height:0;
	  overflow:auto;
	  background: radial-gradient(circle at 0 0, #20365b 0%, #050815 60%, #02040b 100%);
  border-radius:8px;
	}
	.data-grid {
	  width:100%;
	  border-collapse: separate;
	  border-spacing: 0;
	  font-size:13px;
	  border-radius: 8px 8px 0 0;
	  overflow: hidden;
	   background: transparent; 
	}
	.data-grid thead {
	  background:#122946;
	  position:sticky;
	  top:0;
	  z-index:1;
	}
	.data-grid thead th:first-child {
	  border-top-left-radius: 8px;
	}
	.data-grid thead th:last-child {
	  border-top-right-radius: 8px;
	}
	
	/* ---- SORTING ARROWS ---- */
	th.sortable {
	    position: relative;
	    padding-right: 4px;
	    user-select: none;
	    cursor: pointer;
	}
	th.sortable .sort-arrow {
	    display: inline-block;
	    margin-left: 6px;
	    vertical-align: middle;
	    opacity: 0.35;
	    width: 0;
	    height: 0;
	    border-left: 4px solid transparent;
	    border-right: 4px solid transparent;
	    border-top: 6px solid #7fa6ff;
	}
	th.sortable.asc .sort-arrow {
	    border-top: none;
	    border-bottom: 6px solid #22c55e;
	    opacity: 1;
	}
	th.sortable.desc .sort-arrow {
	    border-bottom: none;
	    border-top: 6px solid #eab308;
	    opacity: 1;
	}
	
	.data-grid th {
	  padding:5px 8px;
	  border-bottom:1px solid #1f2f46;
	  text-align:left;
	  white-space:nowrap;
	  color:#dbe7ff;
	  font-weight:500;
	}
	.data-grid td {
	  padding:4px 8px;
	  border-bottom:1px solid #1f2f46;
	  text-align:left;
	  white-space:nowrap;
	  color:#e5ecf5;
	}
	.data-grid tbody tr:nth-child(odd){
	  background:#0b1827;
	}
	.data-grid tbody tr:nth-child(even){
	  background:#091421;
	}
	.data-grid tbody tr:hover {
	  background:#163458;
	}
	.col-actions {
	  text-align:center;
	  width:140px;
	}
	.data-grid thead th.col-actions {
	  text-align:center;
	}
	.col-actions .row-actions {
	  display:flex;
	  align-items:center !important;
	  justify-content:center;
	}
	
	/* ACTION BUTTONS IN ROW (Edit / Del / Details) */
	.row-actions {
	  display:flex;
	  justify-content:center;
	  gap:6px;
	}
	.row-action-btn {
	  height:28px;
	  min-width:40px;
	  border-radius:4px;
	  display:inline-flex;
	  align-items:center;
	  justify-content:center;
	  border:none;
	  cursor:pointer;
	  font-size:12px;
	  font-weight:600;
	  padding:0 10px;
	  transition:0.16s ease-in-out;
	}
	.row-action-btn.edit {
	  background:#416b95;
	  color:#e5ecf5;
	}
	.row-action-btn.edit:hover {
	  background:#1d4ed8;
	}
	.row-action-btn.del {
	  background:#b91c1c;
	  color:#f9fafb;
	}
	.row-action-btn.del:hover {
	  background:#7f1d1d;
	}
	
	/* Blue round info icon */
	.row-action-btn.info {
	  width:22px;
	  height:22px;
	  min-width:22px !important;
	  min-height:22px !important;
	
	  border-radius:50%;
	  border:1px solid #3b6ebf;
	
	  background: radial-gradient(circle at 30% 30%, #6fa8ff 0%, #3b79d9 70%);
	  color:#ffffff;
	  font-weight:700;
	  font-size:12px;
	  line-height:1;
	
	  display:flex;
	  align-items:center;
	  justify-content:center;
	
	  cursor:pointer;
	  padding:0;
	  margin:0;
	
	  box-shadow:0 1px 3px rgba(0,0,0,0.4);
	  transition:0.15s ease-in-out;
	}
	.row-action-btn.info:hover {
	  background: radial-gradient(circle at 30% 30%, #8fc0ff 0%, #5089ff 70%);
	  box-shadow:0 0 6px rgba(80,137,255,0.7);
	  transform:translateY(-1px);
	}
	
	/* MODALS */
	.modal-backdrop {
	  position:fixed;
	  inset:0;
	  background:rgba(0,0,0,0.55);
	  z-index:40;
	}
	.modal {
	  position:fixed;
	  inset:0;
	  display:flex;
	  align-items:center;
	  justify-content:center;
	  z-index:50;
	}
	.modal-card {
	  background:#0f1b2d;
	  border-radius:10px;
	  border:1px solid #22324a;
	  box-shadow:0 10px 30px rgba(0,0,0,0.8);
	  width:820px;
	  max-width:95vw;
	  padding:20px 22px 20px;
	}
	.modal-header {
	  display:flex;
	  align-items:center;
	  justify-content:space-between;
	  margin-bottom:12px;
	}
	.modal-title {
	  font-size:16px;
	  font-weight:600;
	  color:#e5e7eb;
	}
	.modal-close {
	  border:none;
	  background:transparent;
	  color:#9fb0c7;
	  font-size:20px;
	  cursor:pointer;
	}
	#modalDetails .modal-body {
	  margin-top: 2px;
	  padding-top: 0px;
	}
	.modal-footer {
	  display:flex;
	  justify-content:flex-end;
	  gap:8px;
	  margin-top:10px;
	}
	
	/* Confirm update popup highlight */
	#modalConfirmUpdate .modal-card {
	  border: 2px solid #999999;
	  box-shadow: 0 0 12px rgba(34,197,94,0.6);
	}
	
	/* Delete popup highlight */
	#modalDelete .modal-card {
	  border: 2px solid #dc2626;
	  box-shadow: 0 0 12px rgba(220, 38, 38, 0.6);
	}
	
	/* BUTTONS (SAVE / CANCEL / DELETE / NEW) */
	.btn {
	  display:inline-flex;
	  align-items:center;
	  justify-content:center;
	  padding:6px 18px;
	  font-size:13px;
	  font-weight:600;
	  border-radius:6px;
	  border:none;
	  cursor:pointer;
	  transition:0.18s ease-in-out;
	  color:#fff;
	}
	.btn.save {
	  background:#4ade80;
	  box-shadow:0 0 4px rgba(74,222,128,0.35);
	}
	.btn.save:hover {
	  background:#22c55e;
	  box-shadow:0 0 8px rgba(34,197,94,0.65);
	  transform:translateY(-1px);
	}
	.btn.cancel {
	  background:#4b5563;
	}
	.btn.cancel:hover {
	  background:#374151;
	}
	.btn.delete {
	  background:#b91c1c;
	  box-shadow:0 0 4px rgba(185,28,28,0.55);
	}
	.btn.delete:hover {
	  background:#7f1d1d;
	  box-shadow:0 0 8px rgba(185,28,28,0.85);
	  transform:translateY(-1px);
	}
	.btn.newclient {
	  background:#22c55e;
	  color:#052e16;
	  box-shadow:0 0 4px rgba(34,197,94,0.6);
	  white-space:nowrap;
	  padding:0 18px;
	  height:30px;
	}
	.btn.newclient:hover {
	  background:#16a34a;
	  box-shadow:0 0 8px rgba(34,197,94,0.85);
	  transform:translateY(-1px);
	}
	.btn:disabled {
	  opacity:0.6;
	  cursor:not-allowed;
	  transform:none;
	  box-shadow:none;
	}
	
	/* ⭐ YOUR NEW YELLOW BUTTON STYLE */
	.btn.add-contact {
	  background:#eab308;            /* amber yellow */
	  color:#051014;
	  box-shadow:0 0 4px rgba(234,179,8,0.5);
	}
	.btn.add-contact:hover {
	  background:#ca8a04;
	  box-shadow:0 0 8px rgba(234,179,8,0.8);
	  transform:translateY(-1px);
	}
	
	/* Modal form rows */
	.modal-row {
	  display:flex;
	  gap:10px;
	  margin-bottom:8px;
	}
	.modal-row .field {
	  flex:1 1 0;
	}
	
	/* Contact blocks */
	.contact-block {
	  border:1px dashed #1f2f46;
	  border-radius:6px;
	  padding:8px;
	  margin-bottom:8px;
	}
	.contact-block-title {
	  font-size:12px;
	  color:#9fb0c7;
	  margin-bottom:4px;
	}
	/* NEW: header for title + remove button */
.contact-block-header {
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:4px;
}

.contact-remove {
  background:transparent;
  border:none;
  color:#9ca3af;
  font-size:12px;
  cursor:pointer;
  padding:0 4px;
}

.contact-remove:hover {
  color:#f97316;   /* orange highlight */
}
	
	/* DETAILS TABLE INSIDE DETAILS MODAL */
	.details-table {
	  width:100%;
	  border-collapse:collapse;
	  font-size:13px;
	}
	.details-table th,
	.details-table td {
	  border-bottom:1px solid #1f2f46;
	  padding:4px 6px;
	}
	.details-table th {
	  text-align:left;
	  color:#9fb0c7;
	  width:210px;
	  white-space:nowrap;
	}
	.details-table td {
	  color:#e5ecf5;
	}
	
	/* DETAILS MODAL – gradient title bar */
	#modalDetails .modal-header {
	  background: radial-gradient(circle at 0 0, #20365b 0, #050815 60%, #02040b 100%);
	  padding: 14px 18px;
	  margin-bottom: 4px;
	  border-radius: 8px 8px 0 0;
	  border-bottom: 1px solid #1f2f46;
	}
	#modalDetails .modal-title {
	  color: #f7fafc;
	}
	</style>
	</head>
	<body>
	<div class="page">
	
	<header class="topbar">
	  <div class="top-title">Contragents</div>
	  <div class="top-info" id="selInfo">Clients loaded: 0</div>
	</header>
	
	<div class="content">
	
	  <!-- SINGLE VIEW: CLIENTS TABLE -->
	  <section id="viewClients" class="listPanel">
	    <!-- FILTER PANEL (TOP LIST FILTERS) -->
<div class="panel">
  <div class="section-title">Active clients (list filter)</div>
		<div class="row">
	    <div>
	      <label>Status</label>
	      <select id="statusFilter">
	        <option value="all">All contragents</option>
	        <option value="active">Active only</option>
	        <option value="closed">Closed only</option>
	      </select>
	    </div>
	
	    <div>
	      <label>Search by client name</label>
	      <input id="searchName" placeholder="Type client name..." />
	    </div>
	
	    <!--
		<div class="filter-actions">
		  <button id="btnApplyClientFilter" class="btn filter-btn" type="button">
		    Apply filter
		  </button>
		</div>
		-->
	  </div>
	</div>
	
	<!-- NEW CLIENT button row -->
	<div style="padding:0 20px 8px 20px; display:flex; justify-content:flex-end;">
	  <button id="btnNewClient" class="btn newclient">+ New client</button>
	</div>
	
	    <div class="gridPanel">
	      <div class="gridWrap">
	        <table id="gridClients" class="data-grid">
	          <thead>
	            <tr>
	              <th class="sortable" data-col="contragentid">
	                ID <span class="sort-arrow"></span>
	              </th>
	              <th class="sortable" data-col="client_name">
	                Client name <span class="sort-arrow"></span>
	              </th>
	              <th class="sortable" data-col="idno">
	                IDNO <span class="sort-arrow"></span>
	              </th>
	              <th class="sortable" data-col="country">
	                Country <span class="sort-arrow"></span>
	              </th>
	              <th>Open date</th>
	              <th>Close date</th>
	              <th>Phone</th>
	              <th>Email</th>
	              <th>Admin</th>
	              <th>Active</th>
	              <th>Address</th>
	              <th class="col-actions">Actions</th>
	            </tr>
	          </thead>
	          <tbody></tbody>
	        </table>
	      </div>
	    </div>
	  </section>
	
	</div> <!-- .content -->
	
	<!-- MODAL BACKDROP -->
	<div id="modalBackdrop" class="modal-backdrop hidden"></div>
	
	<!-- MODAL: NEW CLIENT -->
	<div id="modalNew" class="modal hidden">
	  <div class="modal-card">
	    <div class="modal-header">
	      <div class="modal-title">New client</div>
	      <button class="modal-close" id="closeNewX">&times;</button>
	    </div>
	    <div class="modal-body">
	      <div class="modal-row">
	        <div class="field">
	          <label>Client name *</label>
	          <input id="new_client_name" />
	        </div>
	      </div>
	      <div class="modal-row">
	        <div class="field">
	          <label>IDNO *</label>
	          <input id="new_idno" />
	        </div>
	        <div class="field">
	          <label>Country *</label>
	          <select id="new_country">
	            <option value="">Select country...</option>
	          </select>
	        </div>
	      </div>
	      <div class="modal-row">
	        <div class="field">
	          <label>Open date *</label>
	          <input id="new_open_date" type="date" />
	        </div>
	      </div>
	      <div class="modal-row">
	        <div class="field">
	          <label>Phone (admin)</label>
	          <input id="new_phone" />
	        </div>
	        <div class="field">
	          <label>Email (admin)</label>
	          <input id="new_email" />
	        </div>
	      </div>
	      <div class="modal-row">
	        <div class="field">
	          <label>Address</label>
	          <input id="new_address" />
	        </div>
	      </div>
	      <div class="modal-row">
	        <div class="field">
	          <label>Admin name</label>
	          <input id="new_admin_name" />
	        </div>
	      </div>
	
	      <!-- Contacts section -->
			<div class="modal-row">
			  <div class="field">
			    <label>Contacts</label>
			    <button id="btnNewAddContact"
			            type="button"
			            class="btn add-contact"
			            style="padding:4px 12px; height:26px; font-size:12px;">
			      + Add contact
			    </button>
			  </div>
			</div>
	
	      <!-- Contact 1 -->
	      <div id="new_contact_block_1" class="contact-block hidden">
	        <div class="contact-block-title">Contact 1</div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Role</label>
	            <select id="new_contact1_role">
	              <option value="">Select role...</option>
	            </select>
	          </div>
	          <div class="field">
	            <label>Name</label>
	            <input id="new_contact1_name" />
	          </div>
	        </div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Phone</label>
	            <input id="new_contact1_phone" />
	          </div>
	          <div class="field">
	            <label>Email</label>
	            <input id="new_contact1_email" />
	          </div>
	        </div>
	      </div>
	
	      <!-- Contact 2 -->
	      <div id="new_contact_block_2" class="contact-block hidden">
	        <div class="contact-block-title">Contact 2</div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Role</label>
	            <select id="new_contact2_role">
	              <option value="">Select role...</option>
	            </select>
	          </div>
	          <div class="field">
	            <label>Name</label>
	            <input id="new_contact2_name" />
	          </div>
	        </div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Phone</label>
	            <input id="new_contact2_phone" />
	          </div>
	          <div class="field">
	            <label>Email</label>
	            <input id="new_contact2_email" />
	          </div>
	        </div>
	      </div>
	
	      <!-- Contact 3 -->
	      <div id="new_contact_block_3" class="contact-block hidden">
	        <div class="contact-block-title">Contact 3</div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Role</label>
	            <select id="new_contact3_role">
	              <option value="">Select role...</option>
	            </select>
	          </div>
	          <div class="field">
	            <label>Name</label>
	            <input id="new_contact3_name" />
	          </div>
	        </div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Phone</label>
	            <input id="new_contact3_phone" />
	          </div>
	          <div class="field">
	            <label>Email</label>
	            <input id="new_contact3_email" />
	          </div>
	        </div>
	      </div>
	
	    </div>
	    <div class="modal-footer">
	      <button id="btnNewCancel" class="btn cancel">Cancel</button>
	      <button id="btnNewSave" class="btn save">Save</button>
	    </div>
	  </div>
	</div>
	
	<!-- MODAL: EDIT CLIENT -->
	<div id="modalEdit" class="modal hidden">
	  <div class="modal-card">
	    <div class="modal-header">
	      <div class="modal-title">Edit client</div>
	      <button class="modal-close" id="closeEditX">&times;</button>
	    </div>
	    <div class="modal-body">
	      <div class="modal-row">
	        <div class="field">
	          <label>Client name *</label>
	          <input id="edit_client_name" />
	        </div>
	      </div>
	      <div class="modal-row">
	        <div class="field">
	          <label>IDNO *</label>
	          <input id="edit_idno" />
	        </div>
	        <div class="field">
	          <label>Country *</label>
	          <select id="edit_country">
	            <option value="">Select country...</option>
	          </select>
	        </div>
	      </div>
	      <div class="modal-row">
	        <div class="field">
	          <label>Open date *</label>
	          <input id="edit_open_date" type="date" />
	        </div>
	        <div class="field">
	          <label>Close date</label>
	          <input id="edit_close_date" type="date" />
	        </div>
	      </div>
	      <div class="modal-row">
	        <div class="field">
	          <label>Phone (admin)</label>
	          <input id="edit_phone" />
	        </div>
	        <div class="field">
	          <label>Email (admin)</label>
	          <input id="edit_email" />
	        </div>
	      </div>
	      <div class="modal-row">
	        <div class="field">
	          <label>Address</label>
	          <input id="edit_address" />
	        </div>
	      </div>
	      <div class="modal-row">
	        <div class="field">
	          <label>Admin name</label>
	          <input id="edit_admin_name" />
	        </div>
	      </div>
	
	      <!-- Contacts section -->
	      <div class="modal-row">
	        <div class="field">
	          <label>Contacts</label>
	          <button id="btnEditAddContact" type="button" class="btn add-contact" style="padding:4px 12px; height:26px; font-size:12px;">
	            + Add contact
	          </button>
	        </div>
	      </div>
	
	      <!-- Contact 1 -->
	      <div id="edit_contact_block_1" class="contact-block hidden">
	        <div class="contact-block-title">Contact 1</div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Role</label>
	            <select id="edit_contact1_role">
	              <option value="">Select role...</option>
	            </select>
	          </div>
	          <div class="field">
	            <label>Name</label>
	            <input id="edit_contact1_name" />
	          </div>
	        </div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Phone</label>
	            <input id="edit_contact1_phone" />
	          </div>
	          <div class="field">
	            <label>Email</label>
	            <input id="edit_contact1_email" />
	          </div>
	        </div>
	      </div>
	
	      <!-- Contact 2 -->
	      <div id="edit_contact_block_2" class="contact-block hidden">
	        <div class="contact-block-title">Contact 2</div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Role</label>
	            <select id="edit_contact2_role">
	              <option value="">Select role...</option>
	            </select>
	          </div>
	          <div class="field">
	            <label>Name</label>
	            <input id="edit_contact2_name" />
	          </div>
	        </div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Phone</label>
	            <input id="edit_contact2_phone" />
	          </div>
	          <div class="field">
	            <label>Email</label>
	            <input id="edit_contact2_email" />
	          </div>
	        </div>
	      </div>
	
	      <!-- Contact 3 -->
	      <div id="edit_contact_block_3" class="contact-block hidden">
	        <div class="contact-block-title">Contact 3</div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Role</label>
	            <select id="edit_contact3_role">
	              <option value="">Select role...</option>
	            </select>
	          </div>
	          <div class="field">
	            <label>Name</label>
	            <input id="edit_contact3_name" />
	          </div>
	        </div>
	        <div class="modal-row">
	          <div class="field">
	            <label>Phone</label>
	            <input id="edit_contact3_phone" />
	          </div>
	          <div class="field">
	            <label>Email</label>
	            <input id="edit_contact3_email" />
	          </div>
	        </div>
	      </div>
	
	    </div>
	    <div class="modal-footer">
	      <button id="btnEditCancel" class="btn cancel">Cancel</button>
	      <button id="btnEditSave" class="btn save">Save</button>
	    </div>
	  </div>
	</div>
	
	<!-- MODAL: DELETE CLIENT -->
	<div id="modalDelete" class="modal hidden">
	  <div class="modal-card">
	    <div class="modal-header">
	      <div class="modal-title">Delete client</div>
	      <button class="modal-close" id="closeDeleteX">&times;</button>
	    </div>
	
	    <div class="modal-body">
	      <p style="color:#fca5a5; font-size:14px; margin-bottom:10px;">
	        Are you sure you want to delete this client?<br>
	        <strong>This action cannot be undone.</strong>
	      </p>
	
	      <div class="modal-row">
	        <div class="field">
	          <label>Client name</label>
	          <input id="del_client_name" disabled />
	        </div>
	      </div>
	
	      <div class="modal-row">
	        <div class="field">
	          <label>IDNO</label>
	          <input id="del_idno" disabled />
	        </div>
	        <div class="field">
	          <label>Country</label>
	          <input id="del_country" disabled />
	        </div>
	      </div>
	    </div>
	
	    <div class="modal-footer">
	      <button id="btnDeleteCancel" class="btn cancel">Cancel</button>
	      <button id="btnDeleteConfirm" class="btn delete">Delete</button>
	    </div>
	  </div>
	</div>
	
	<!-- MODAL: DETAILS (READ-ONLY) -->
	<div id="modalDetails" class="modal hidden">
	  <div class="modal-card">
	    <div class="modal-header">
	      <div class="modal-title">Client details</div>
	      <button class="modal-close" id="closeDetailsX">&times;</button>
	    </div>
	    <div class="modal-body">
	      <div id="detailsTable"></div>
	    </div>
	    <div class="modal-footer">
	      <button id="btnDetailsClose" class="btn cancel">Close</button>
	    </div>
	  </div>
	</div>
	
	<!-- MODAL: CONFIRM UPDATE -->
	<div id="modalConfirmUpdate" class="modal hidden">
	  <div class="modal-card">
	    <div class="modal-header">
	      <div class="modal-title">Confirm update</div>
	      <button class="modal-close" id="closeConfirmUpdateX">&times;</button>
	    </div>
	    <div class="modal-body">
	      <p style="color:#d1d5db; font-size:14px; margin-bottom:8px;">
	        Are you sure you want to save the changes to this client?
	      </p>
	    </div>
	    <div class="modal-footer">
	      <button id="btnConfirmUpdateCancel" class="btn cancel">Cancel</button>
	      <button id="btnConfirmUpdateOk" class="btn save">Yes, save</button>
	    </div>
	  </div>
	</div>
	
	</div> <!-- .page -->
	
	<script>
	(function(){
	
	  const BASE = "/system/webdev/the_project_1_2025-12-04_2202/aggrid_contragents_modif/contragents/";
	
	  const LIST_URL     = BASE + "list";
	  const CREATE_URL   = BASE + "create";
	  const UPDATE_URL   = BASE + "update";
	  const DELETE_URL   = BASE + "delete";
	  const COUNTRY_URL  = BASE + "country";
	  const ROLETYPE_URL = BASE + "roletypes";
	
	  const $ = id => document.getElementById(id);
	
	  const selInfo       = $("selInfo");
	  const statusFilter  = $("statusFilter");
	  const searchName    = $("searchName");
	  const gridClients   = $("gridClients");
	  const thead         = gridClients.querySelector("thead");
	
	  const btnNewClient  = $("btnNewClient");
	  const btnApplyClientFilter = $("btnApplyClientFilter");
		
		if (btnApplyClientFilter){
		  btnApplyClientFilter.addEventListener("click", function(){
		    applyFilters();
		  });
		}
		
	  const modalBackdrop      = $("modalBackdrop");
	  const modalNew           = $("modalNew");
	  const modalEdit          = $("modalEdit");
	  const modalDelete        = $("modalDelete");
	  const modalConfirmUpdate = $("modalConfirmUpdate");
	  const modalDetails       = $("modalDetails");
	  const detailsTable       = $("detailsTable");
	  const closeDetailsX      = $("closeDetailsX");
	  const btnDetailsClose    = $("btnDetailsClose");
	
	  // New modal
	  const btnNewSave    = $("btnNewSave");
	  const btnNewCancel  = $("btnNewCancel");
	  const closeNewX     = $("closeNewX");
	  const btnNewAddContact = $("btnNewAddContact");
	
	  const newContactBlocks = [
	    $("new_contact_block_1"),
	    $("new_contact_block_2"),
	    $("new_contact_block_3")
	  ];
	
	  const newInputs = {
	    client_name: $("new_client_name"),
	    idno:        $("new_idno"),
	    country:     $("new_country"),
	    open_date:   $("new_open_date"),
	    phone:       $("new_phone"),
	    email:       $("new_email"),
	    address:     $("new_address"),
	    admin_name:  $("new_admin_name"),
	
	    contact_person_1_role_id: $("new_contact1_role"),
	    contact_person_1_name:    $("new_contact1_name"),
	    contact_person_1_phone:   $("new_contact1_phone"),
	    contact_person_1_email:   $("new_contact1_email"),
	
	    contact_person_2_role_id: $("new_contact2_role"),
	    contact_person_2_name:    $("new_contact2_name"),
	    contact_person_2_phone:   $("new_contact2_phone"),
	    contact_person_2_email:   $("new_contact2_email"),
	
	    contact_person_3_role_id: $("new_contact3_role"),
	    contact_person_3_name:    $("new_contact3_name"),
	    contact_person_3_phone:   $("new_contact3_phone"),
	    contact_person_3_email:   $("new_contact3_email")
	  };
	
	  // Edit modal
	  const btnEditSave    = $("btnEditSave");
	  const btnEditCancel  = $("btnEditCancel");
	  const closeEditX     = $("closeEditX");
	  const btnEditAddContact = $("btnEditAddContact");
	
	  const editContactBlocks = [
	    $("edit_contact_block_1"),
	    $("edit_contact_block_2"),
	    $("edit_contact_block_3")
	  ];
	
	  const editInputs = {
	    client_name: $("edit_client_name"),
	    idno:        $("edit_idno"),
	    country:     $("edit_country"),
	    open_date:   $("edit_open_date"),
	    close_date:  $("edit_close_date"),
	    phone:       $("edit_phone"),
	    email:       $("edit_email"),
	    address:     $("edit_address"),
	    admin_name:  $("edit_admin_name"),
	
	    contact_person_1_role_id: $("edit_contact1_role"),
	    contact_person_1_name:    $("edit_contact1_name"),
	    contact_person_1_phone:   $("edit_contact1_phone"),
	    contact_person_1_email:   $("edit_contact1_email"),
	
	    contact_person_2_role_id: $("edit_contact2_role"),
	    contact_person_2_name:    $("edit_contact2_name"),
	    contact_person_2_phone:   $("edit_contact2_phone"),
	    contact_person_2_email:   $("edit_contact2_email"),
	
	    contact_person_3_role_id: $("edit_contact3_role"),
	    contact_person_3_name:    $("edit_contact3_name"),
	    contact_person_3_phone:   $("edit_contact3_phone"),
	    contact_person_3_email:   $("edit_contact3_email")
	  };
	
	  // Delete modal
	  const btnDeleteConfirm   = $("btnDeleteConfirm");
	  const btnDeleteCancel    = $("btnDeleteCancel");
	  const closeDeleteX       = $("closeDeleteX");
	  const delFields = {
	    client_name: $("del_client_name"),
	    idno:        $("del_idno"),
	    country:     $("del_country")
	  };
	
	  // Confirm-update modal
	  const closeConfirmUpdateX    = $("closeConfirmUpdateX");
	  const btnConfirmUpdateCancel = $("btnConfirmUpdateCancel");
	  const btnConfirmUpdateOk     = $("btnConfirmUpdateOk");
	
	  const roleSelects = [
	    newInputs.contact_person_1_role_id,
	    newInputs.contact_person_2_role_id,
	    newInputs.contact_person_3_role_id,
	    editInputs.contact_person_1_role_id,
	    editInputs.contact_person_2_role_id,
	    editInputs.contact_person_3_role_id
	  ];
	
	  let allRows = [];
	  let currentEditId   = null;
	  let currentDeleteId = null;
	
	  let sortCol = null;
	  let sortDir = "asc";
	
	  thead.addEventListener("click", function(ev){
	    const th = ev.target.closest("th.sortable");
	    if (!th) return;
	
	    const col = th.dataset.col;
	    if (!col) return;
	
	    if (sortCol === col) {
	        sortDir = (sortDir === "asc" ? "desc" : "asc");
	    } else {
	        sortCol = col;
	        sortDir = "asc";
	    }
	
	    thead.querySelectorAll("th.sortable").forEach(h => {
	        h.classList.remove("asc", "desc");
	    });
	
	    th.classList.add(sortDir === "asc" ? "asc" : "desc");
	
	    applyFilters();
	  });
	
	  function formatTodayIso(){
	    const d = new Date();
	    const dd = String(d.getDate()).padStart(2,"0");
	    const mm = String(d.getMonth() + 1).padStart(2,"0");
	    const yyyy = d.getFullYear();
	    return yyyy + "-" + mm + "-" + dd;
	  }
	
	  function openModal(modal){
	    modalBackdrop.classList.remove("hidden");
	    modal.classList.remove("hidden");
	  }
	
	  function closeModal(modal){
	    modal.classList.add("hidden");
	    modalBackdrop.classList.add("hidden");
	  }
	
	  function markInvalid(input, isInvalid) {
	    if (!input) return;
	    if (isInvalid) {
	      input.classList.add("input-error");
	    } else {
	      input.classList.remove("input-error");
	    }
	  }
	
	  function hideContactBlocks(blocks, button){
	    blocks.forEach(b => b.classList.add("hidden"));
	    if (button) button.disabled = false;
	  }
	
	  function showNextContactBlock(blocks, button){
	    for (var i=0; i<blocks.length; i++){
	      if (blocks[i].classList.contains("hidden")){
	        blocks[i].classList.remove("hidden");
	        if (i === blocks.length - 1 && button){
	          button.disabled = true;
	        }
	        return;
	      }
	    }
	    if (button) button.disabled = true;
	  }
	
	  function clearNewForm(){
	    Object.values(newInputs).forEach(inp => inp.value = "");
	    newInputs.open_date.value = formatTodayIso();
	    markInvalid(newInputs.client_name, false);
	    markInvalid(newInputs.idno,        false);
	    markInvalid(newInputs.open_date,   false);
	    markInvalid(newInputs.country,     false);
	    hideContactBlocks(newContactBlocks, btnNewAddContact);
	  }
	
	  function clearEditForm(){
	    Object.values(editInputs).forEach(inp => inp.value = "");
	    markInvalid(editInputs.client_name, false);
	    markInvalid(editInputs.idno,        false);
	    markInvalid(editInputs.open_date,   false);
	    markInvalid(editInputs.country,     false);
	    hideContactBlocks(editContactBlocks, btnEditAddContact);
	  }
	
	  function clearDeleteForm(){
	    Object.values(delFields).forEach(inp => inp.value = "");
	  }
	
	  function setSelectValue(sel, value){
	    const v = (value == null ? "" : String(value));
	    if (!v){
	      sel.value = "";
	      return;
	    }
	    let opt = Array.prototype.find.call(sel.options, o => o.value === v);
	    if (!opt){
	      opt = document.createElement("option");
	      opt.value = v;
	      opt.textContent = v;
	      sel.appendChild(opt);
	    }
	    sel.value = v;
	  }
	
	  const columnsOrder = [
	    "contragentid","client_name","idno","country","open_date","close_date",
	    "phone","email","admin_name","is_active","address"
	  ];
	
	  function renderTable(rows){
	    const tbody = gridClients.querySelector("tbody");
	    tbody.innerHTML = "";
	
	    rows.forEach(row => {
	      const tr = document.createElement("tr");
	      tr.dataset.id = row.contragentid;
	
	      columnsOrder.forEach(col => {
	        const td = document.createElement("td");
	        let v = row[col];
	        if (v === null || v === undefined || v === "null" || v === "NULL"){
	          v = "";
	        }
	        td.textContent = v != null ? v : "";
	        tr.appendChild(td);
	      });
	
	      const tdActions = document.createElement("td");
	      tdActions.className = "col-actions";
	      const wrap = document.createElement("div");
	      wrap.className = "row-actions";
	
	      const btnInfo = document.createElement("button");
	      btnInfo.className = "row-action-btn info";
	      btnInfo.dataset.action = "details";
	      btnInfo.title = "Details";
	      btnInfo.textContent = "i";
	
	      const btnE = document.createElement("button");
	      btnE.className = "row-action-btn edit";
	      btnE.dataset.action = "edit";
	      btnE.title = "Edit client";
	      btnE.textContent = "Edit";
	
	      const btnD = document.createElement("button");
	      btnD.className = "row-action-btn del";
	      btnD.dataset.action = "delete";
	      btnD.title = "Delete client";
	      btnD.textContent = "Del";
	
	      wrap.appendChild(btnInfo);
	      wrap.appendChild(btnE);
	      wrap.appendChild(btnD);
	      tdActions.appendChild(wrap);
	      tr.appendChild(tdActions);
	
	      // double-click row -> open details
	      tr.ondblclick = function(){
	        openDetailsForRow(row);
	      };
	
	      tbody.appendChild(tr);
	    });
	
	    selInfo.textContent = "Clients loaded: " + rows.length;
	
	    tbody.onclick = function(ev){
	      const btn = ev.target.closest("button[data-action]");
	      if (!btn) return;
	      const tr = btn.closest("tr");
	      if (!tr) return;
	      const id = tr.dataset.id;
	      const row = allRows.find(r => String(r.contragentid) === String(id));
	      if (!row) return;
	
	      if (btn.dataset.action === "details"){
	        openDetailsForRow(row);
	      } else if (btn.dataset.action === "edit"){
	        openEditForRow(row);
	      } else if (btn.dataset.action === "delete"){
	        openDeleteForRow(row);
	      }
	    };
	  }
	
	  function applyFilters(){
	    const status = statusFilter.value;
	    const search = (searchName.value || "").trim().toLowerCase();
	
	    let filtered = (allRows || []).filter(r => {
	      if (status === "active" && !r.is_active) return false;
	      if (status === "closed" &&  r.is_active) return false;
	
	      if (search){
	        const name = (r.client_name || "").toLowerCase();
	        if (!name.includes(search)) return false;
	      }
	      return true;
	    });
	
	    if (sortCol){
	      filtered = filtered.slice().sort(function(a, b){
	        let va = a[sortCol];
	        let vb = b[sortCol];
	
	        if (sortCol === "contragentid") {
	          va = Number(va) || 0;
	          vb = Number(vb) || 0;
	        } else {
	          va = (va == null ? "" : String(va).toLowerCase());
	          vb = (vb == null ? "" : String(vb).toLowerCase());
	        }
	
	        if (va < vb) return (sortDir === "asc" ? -1 : 1);
	        if (va > vb) return (sortDir === "asc" ?  1 : -1);
	        return 0;
	      });
	    }
	
	    renderTable(filtered);
	  }
	
	  statusFilter.addEventListener("change", applyFilters);
	  searchName.addEventListener("input", applyFilters);
	
	  function loadClients(){
	    fetch(LIST_URL, {credentials:"same-origin"})
	      .then(r => r.json())
	      .then(data => {
	        if (Array.isArray(data)){
	          allRows = data;
	        } else if (Array.isArray(data.rows)){
	          allRows = data.rows;
	        } else if (data && data.json && Array.isArray(data.json.rows)){
	          allRows = data.json.rows;
	        } else {
	          allRows = [];
	        }
	        applyFilters();
	      })
	      .catch(err => console.error("Load error", err));
	  }
	
	  function loadCountries(){
	    fetch(COUNTRY_URL, {credentials:"same-origin"})
	      .then(r => r.json())
	      .then(rows => {
	        const selects = [newInputs.country, editInputs.country];
	        selects.forEach(sel => {
	          sel.innerHTML = '<option value="">Select country...</option>';
	        });
	
	        rows.forEach(row => {
	          const code = row.country_code3;
	          const name = row.country_name;
	          if (code && name){
	            selects.forEach(sel => {
	              const opt = document.createElement("option");
	              opt.value = code;
	              opt.textContent = name;
	              sel.appendChild(opt);
	            });
	          }
	        });
	      })
	      .catch(err => console.error("Country load error", err));
	  }
	
	  function loadRoleTypes(){
  fetch(ROLETYPE_URL, { credentials: "same-origin" })
    .then(r => r.json())
    .then(data => {
      console.log("Roletypes raw:", data);

      // 1) Normalize to an array `rows`
      let rows;
      if (Array.isArray(data)) {
        rows = data;
      } else if (data && Array.isArray(data.rows)) {
        rows = data.rows;
      } else if (data && data.json && Array.isArray(data.json.rows)) {
        rows = data.json.rows;
      } else {
        console.warn("Roletypes: no rows array found");
        return;
      }

      // 2) Clear all selects safely
      roleSelects.forEach(sel => {
        if (!sel) return;   // avoid errors if any is null
        sel.innerHTML = '<option value="">Select role...</option>';
      });

      // 3) Add options using your real field names
      rows.forEach(row => {
        const id   = row.contragent_user_role_id;
        const name = row.contragent_user_role_name;
        if (id == null || !name) return;

        roleSelects.forEach(sel => {
          if (!sel) return;
          const opt = document.createElement("option");
          opt.value = id;
          opt.textContent = name;
          sel.appendChild(opt);
        });
      });
    })
    .catch(err => {
      console.error("Roletypes load error", err);
    });
}
	
	  // New client
	  function openNewModal(){
	    clearNewForm();
	    openModal(modalNew);
	  }
	
	  btnNewClient.addEventListener("click", openNewModal);
	
	  btnNewCancel.addEventListener("click", function(){
	    closeModal(modalNew);
	  });
	  closeNewX.addEventListener("click", function(){
	    closeModal(modalNew);
	  });
	
	  btnNewAddContact.addEventListener("click", function(){
	    showNextContactBlock(newContactBlocks, btnNewAddContact);
	  });
	
	  btnNewSave.addEventListener("click", function(){
	    const nameEmpty    = !newInputs.client_name.value.trim();
	    const idnoEmpty    = !newInputs.idno.value.trim();
	    const dateEmpty    = !newInputs.open_date.value.trim();
	    const countryEmpty = !newInputs.country.value.trim();
	
	    markInvalid(newInputs.client_name, nameEmpty);
	    markInvalid(newInputs.idno,        idnoEmpty);
	    markInvalid(newInputs.open_date,   dateEmpty);
	    markInvalid(newInputs.country,     countryEmpty);
	
	    if (nameEmpty || idnoEmpty || dateEmpty || countryEmpty){
	      return;
	    }
	
	    const payload = {
	      client_name: newInputs.client_name.value,
	      idno:        newInputs.idno.value,
	      country:     newInputs.country.value,
	      open_date:   newInputs.open_date.value,
	      admin_phone: newInputs.phone.value,
	      admin_email: newInputs.email.value,
	      address:     newInputs.address.value,
	      admin_name:  newInputs.admin_name.value,
	
	      contact_person_1_role_id: newInputs.contact_person_1_role_id.value || null,
	      contact_person_1_name:    newInputs.contact_person_1_name.value,
	      contact_person_1_phone:   newInputs.contact_person_1_phone.value,
	      contact_person_1_email:   newInputs.contact_person_1_email.value,
	
	      contact_person_2_role_id: newInputs.contact_person_2_role_id.value || null,
	      contact_person_2_name:    newInputs.contact_person_2_name.value,
	      contact_person_2_phone:   newInputs.contact_person_2_phone.value,
	      contact_person_2_email:   newInputs.contact_person_2_email.value,
	
	      contact_person_3_role_id: newInputs.contact_person_3_role_id.value || null,
	      contact_person_3_name:    newInputs.contact_person_3_name.value,
	      contact_person_3_phone:   newInputs.contact_person_3_phone.value,
	      contact_person_3_email:   newInputs.contact_person_3_email.value
	    };
	
	    fetch(CREATE_URL, {
	      method:"POST",
	      credentials:"same-origin",
	      headers: {"Content-Type":"application/json"},
	      body: JSON.stringify(payload)
	    })
	    .then(r => {
	      if (!r.ok) throw new Error("Create failed (" + r.status + ")");
	      return r.json();
	    })
	    .then(data => {
	      console.log("Create response:", data);
	      closeModal(modalNew);
	      loadClients();
	      alert("Client was created successfully.");
	    })
	    .catch(err => {
	      console.error("Create error", err);
	      alert("Error creating client: " + err.message);
	    });
	  });
	
	  // Edit client
	  function openEditForRow(row){
	    currentEditId = row.contragentid;
	
	    editInputs.client_name.value = row.client_name || "";
	    editInputs.idno.value        = row.idno || "";
	    setSelectValue(editInputs.country, row.country || "");
	    editInputs.open_date.value   = row.open_date || "";
	    editInputs.close_date.value  = (row.close_date && row.close_date !== "1970-01-01") ? row.close_date : "";
	    editInputs.phone.value       = row.phone || "";
	    editInputs.email.value       = row.email || "";
	    editInputs.address.value     = row.address || "";
	    editInputs.admin_name.value  = row.admin_name || "";
	
	    // reset contact blocks
	    hideContactBlocks(editContactBlocks, btnEditAddContact);
	
	    // contact 1
	    setSelectValue(editInputs.contact_person_1_role_id, row.contact_person_1_role_id);
	    editInputs.contact_person_1_name.value  = row.contact_person_1_name  || "";
	    editInputs.contact_person_1_phone.value = row.contact_person_1_phone || "";
	    editInputs.contact_person_1_email.value = row.contact_person_1_email || "";
	
	    // contact 2
	    setSelectValue(editInputs.contact_person_2_role_id, row.contact_person_2_role_id);
	    editInputs.contact_person_2_name.value  = row.contact_person_2_name  || "";
	    editInputs.contact_person_2_phone.value = row.contact_person_2_phone || "";
	    editInputs.contact_person_2_email.value = row.contact_person_2_email || "";
	
	    // contact 3
	    setSelectValue(editInputs.contact_person_3_role_id, row.contact_person_3_role_id);
	    editInputs.contact_person_3_name.value  = row.contact_person_3_name  || "";
	    editInputs.contact_person_3_phone.value = row.contact_person_3_phone || "";
	    editInputs.contact_person_3_email.value = row.contact_person_3_email || "";
	
	    // show blocks that have data
	    var anyShown = false;
	    [1,2,3].forEach(function(idx){
	      var name  = row["contact_person_" + idx + "_name"];
	      var phone = row["contact_person_" + idx + "_phone"];
	      var email = row["contact_person_" + idx + "_email"];
	      var role  = row["contact_person_" + idx + "_role_id"];
	      var hasData = (name || phone || email || role);
	      if (hasData){
	        editContactBlocks[idx-1].classList.remove("hidden");
	        anyShown = true;
	      }
	    });
	    if (!anyShown){
	      // all hidden; allow adding from scratch
	      btnEditAddContact.disabled = false;
	    } else {
	      // disable if all 3 visible
	      var visibleCount = editContactBlocks.filter(b => !b.classList.contains("hidden")).length;
	      btnEditAddContact.disabled = (visibleCount >= editContactBlocks.length);
	    }
	
	    markInvalid(editInputs.client_name, false);
	    markInvalid(editInputs.idno,        false);
	    markInvalid(editInputs.open_date,   false);
	    markInvalid(editInputs.country,     false);
	
	    openModal(modalEdit);
	  }
	
	  btnEditCancel.addEventListener("click", function(){
	    closeModal(modalEdit);
	    clearEditForm();
	    currentEditId = null;
	  });
	  closeEditX.addEventListener("click", function(){
	    closeModal(modalEdit);
	    clearEditForm();
	    currentEditId = null;
	  });
	
	  btnEditAddContact.addEventListener("click", function(){
	    showNextContactBlock(editContactBlocks, btnEditAddContact);
	  });
	
	  btnEditSave.addEventListener("click", function(){
	    if (!currentEditId){
	      alert("No client selected to update.");
	      return;
	    }
	
	    const nameEmpty    = !editInputs.client_name.value.trim();
	    const idnoEmpty    = !editInputs.idno.value.trim();
	    const dateEmpty    = !editInputs.open_date.value.trim();
	    const countryEmpty = !editInputs.country.value.trim();
	
	    markInvalid(editInputs.client_name, nameEmpty);
	    markInvalid(editInputs.idno,        idnoEmpty);
	    markInvalid(editInputs.open_date,   dateEmpty);
	    markInvalid(editInputs.country,     countryEmpty);
	
	    if (nameEmpty || idnoEmpty || dateEmpty || countryEmpty){
	      return;
	    }
	
	    openModal(modalConfirmUpdate);
	  });
	
	  btnConfirmUpdateCancel.addEventListener("click", function(){
	    closeModal(modalConfirmUpdate);
	  });
	  closeConfirmUpdateX.addEventListener("click", function(){
	    closeModal(modalConfirmUpdate);
	  });
	
	  btnConfirmUpdateOk.addEventListener("click", function(){
	    if (!currentEditId){
	      alert("No client selected to update.");
	      closeModal(modalConfirmUpdate);
	      return;
	    }
	
	    const payload = {
	      contragentid: currentEditId,
	      client_name:  editInputs.client_name.value,
	      idno:         editInputs.idno.value,
	      country:      editInputs.country.value,
	      open_date:    editInputs.open_date.value,
	      close_date:   editInputs.close_date.value,
	      admin_phone:  editInputs.phone.value,
	      admin_email:  editInputs.email.value,
	      address:      editInputs.address.value,
	      admin_name:   editInputs.admin_name.value,
	
	      contact_person_1_role_id: editInputs.contact_person_1_role_id.value || null,
	      contact_person_1_name:    editInputs.contact_person_1_name.value,
	      contact_person_1_phone:   editInputs.contact_person_1_phone.value,
	      contact_person_1_email:   editInputs.contact_person_1_email.value,
	
	      contact_person_2_role_id: editInputs.contact_person_2_role_id.value || null,
	      contact_person_2_name:    editInputs.contact_person_2_name.value,
	      contact_person_2_phone:   editInputs.contact_person_2_phone.value,
	      contact_person_2_email:   editInputs.contact_person_2_email.value,
	
	      contact_person_3_role_id: editInputs.contact_person_3_role_id.value || null,
	      contact_person_3_name:    editInputs.contact_person_3_name.value,
	      contact_person_3_phone:   editInputs.contact_person_3_phone.value,
	      contact_person_3_email:   editInputs.contact_person_3_email.value
	    };
	
	    fetch(UPDATE_URL, {
	      method:"POST",
	      credentials:"same-origin",
	      headers: {"Content-Type":"application/json"},
	      body: JSON.stringify(payload)
	    })
	    .then(r => {
	      if (!r.ok) throw new Error("Update failed (" + r.status + ")");
	      return r.json();
	    })
	    .then(data => {
	      console.log("Update response:", data);
	      closeModal(modalConfirmUpdate);
	      closeModal(modalEdit);
	      clearEditForm();
	      currentEditId = null;
	      loadClients();
	      alert("Client was updated successfully.");
	    })
	    .catch(err => {
	      console.error("Update error", err);
	      alert("Error updating client: " + err.message);
	    });
	  });
	
	  // Delete client
	  function openDeleteForRow(row){
	    currentDeleteId = row.contragentid;
	    delFields.client_name.value = row.client_name || "";
	    delFields.idno.value        = row.idno || "";
	    delFields.country.value     = row.country || "";
	    openModal(modalDelete);
	  }
	
	  btnDeleteCancel.addEventListener("click", function(){
	    closeModal(modalDelete);
	    clearDeleteForm();
	    currentDeleteId = null;
	  });
	
	  closeDeleteX.addEventListener("click", function(){
	    closeModal(modalDelete);
	    clearDeleteForm();
	    currentDeleteId = null;
	  });
	
	  btnDeleteConfirm.addEventListener("click", function(){
	    if (!currentDeleteId){
	      alert("No client selected to delete.");
	      return;
	    }
	
	    var sure = window.confirm(
	      "Are you sure you want to DELETE this client?\\n\\n" +
	      "This action cannot be undone."
	    );
	    if (!sure){
	      return;
	    }
	
	    const payload = { contragentid: currentDeleteId };
	
	    fetch(DELETE_URL, {
	      method:"POST",
	      credentials:"same-origin",
	      headers: {"Content-Type":"application/json"},
	      body: JSON.stringify(payload)
	    })
	    .then(r => {
	      if (!r.ok) throw new Error("Delete failed (" + r.status + ")");
	      return r.json();
	    })
	    .then(data => {
	      console.log("Delete response:", data);
	      closeModal(modalDelete);
	      clearDeleteForm();
	      currentDeleteId = null;
	      loadClients();
	      alert("Client was deleted successfully.");
	    })
	    .catch(err => {
	      console.error("Delete error", err);
	      alert("Error deleting client: " + err.message);
	    });
	  });
	
	  // ----- Details (read-only) -----
	  function openDetailsForRow(row){
	    const pairs = [
	      ["ID", row.contragentid],
	      ["Client name", row.client_name],
	      ["IDNO", row.idno],
	      ["Country", row.country],
	      ["Open date", row.open_date],
	      ["Close date", row.close_date],
	      ["Admin phone", row.phone],
	      ["Admin email", row.email],
	      ["Admin name", row.admin_name],
	      ["Active", (row.is_active ? "Yes" : "No")],
	      ["Address", row.address],
	
	      ["Created at", row.created_at],
	      ["Created by (ID)", row.created_by_id_user],
	      ["Created by", row.created_by],
	      ["Created role", row.created_role_name],
	      ["Updated at", row.updated_at],
	      ["Updated by (ID)", row.updated_by_id_user],
	      ["Updated by", row.updated_by],
	      ["Updated role", row.updated_role_name]
	    ];
	
	    // Add contacts dynamically if they have data
	    [1,2,3].forEach(function(idx){
	      var name  = row["contact_person_" + idx + "_name"];
	      var phone = row["contact_person_" + idx + "_phone"];
	      var email = row["contact_person_" + idx + "_email"];
	      var roleName  = row["contact_person_" + idx + "_role_name"];
	
	      if (name || phone || email || roleName){
	        pairs.push(["Contact " + idx + " role", roleName]);
	        pairs.push(["Contact " + idx + " name", name]);
	        pairs.push(["Contact " + idx + " phone", phone]);
	        pairs.push(["Contact " + idx + " email", email]);
	      }
	    });
	
	    let html = '<table class="details-table">';
	    pairs.forEach(function(p){
	      const label = p[0];
	      const raw   = p[1];
	      const value = (raw == null || raw === "null") ? "" : raw;
	      html += "<tr><th>" + label + "</th><td>" + value + "</td></tr>";
	    });
	    html += "</table>";
	
	    detailsTable.innerHTML = html;
	    openModal(modalDetails);
	  }
	
	  // Details modal close
	  closeDetailsX.addEventListener("click", function(){
	    closeModal(modalDetails);
	  });
	  btnDetailsClose.addEventListener("click", function(){
	    closeModal(modalDetails);
	  });
	
	  // Initial load
	  clearNewForm();
	  loadCountries();
	  loadRoleTypes();
	  loadClients();
	
	})();
	</script>
	</body>
	</html>
	"""
	return {"html": html}