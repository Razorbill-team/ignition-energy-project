def doGet(request, session):
# WebDev → aggrid_subcontracts/aggrid : doGet

    html = u"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Contracts & Subcontracts</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>

  <!-- Local AG Grid v34 enterprise -->
  <link rel="stylesheet" href="./v34/css/ag-grid.css">
  <link rel="stylesheet" href="./v34/css/ag-theme-alpine.css">
  <script src="./v34/ag-grid-enterprise.min.js"></script>

  <style>
    /* ====== PAGE LAYOUT (COMPACT HEADER) =============================== */
    html, body {
      height: 100%;
      margin: 0;
      font: 14px/1.4 Verdana, Geneva, Tahoma, sans-serif;
      background: radial-gradient(circle at 0 0, #20365b 0, #050815 60%, #02040b 100%);
      color: #e9f0ff;
    }

    .page {
  height: 100%;
  display: flex;
  flex-direction: column;

  /* was: align-items:center;  -> that creates side gutters */
  align-items: stretch;

  /* keep small breathing space, but not huge gutters */
  padding: 10px 12px 16px 12px;
  box-sizing: border-box;
}

.shell {
  /* was max-width:1720px; -> this is the main limiter */
  width: 100%;
  max-width: none;

  /* optional: guarantee it spans the viewport width */
  /* width: min(100%, 100vw); */

  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1 1 auto;
  min-height: 0;
}

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 0 4px;
    }

    .title-block h1 {
      margin: 0;
      font-size: 22px;
      line-height: 1.1;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #f7f9ff;
      text-shadow: 0 0 14px rgba(26, 104, 255, 0.35);
    }

    .status-pill {
      align-self: center;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 10px;
      letter-spacing: 0.03em;
      text-transform: uppercase;
      background: linear-gradient(135deg, rgba(52, 120, 255, 0.16),
                                           rgba(139, 92, 246, 0.06));
      border: 1px solid rgba(153, 194, 255, 0.35);
      color: #dbe8ff;
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
    }

    .status-dot {
      width: 6px;
      height: 6px;
      border-radius: 999px;
      background: #4ade80;
      box-shadow: 0 0 6px rgba(74, 222, 128, 0.8);
    }

    .grid-card {
      flex: 1 1 auto;
      min-height: 0;
      display: flex;
      flex-direction: column;
      background: radial-gradient(circle at top left, rgba(42, 88, 170, 0.25) 0,
                                  rgba(7, 14, 36, 0.9) 45%, #050816 100%);
      border-radius: 16px;
      padding: 10px 12px 12px 12px;
      box-shadow:
        0 24px 60px rgba(0, 0, 0, 0.7),
        0 0 0 1px rgba(148, 163, 233, 0.25);
      border: 1px solid rgba(15, 23, 42, 0.8);
      backdrop-filter: blur(8px);
    }

    .grid-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 0 0 4px 0;
      font-size: 10px;
      color: rgba(226, 232, 255, 0.72);
    }

    #grid {
      flex: 1 1 auto;
      min-height: 260px;
      border-radius: 10px;
      overflow: visible;
    }

    .footer-note {
      margin-top: 4px;
      font-size: 11px;
      opacity: 0.6;
      text-align: right;
    }

    /* ====== CONTRACTS TOOLBAR =========================================== */
    .toolbar {
      display: flex;
      align-items: flex-end;
      gap: 16px;
      margin-bottom: 8px;
      flex-wrap: wrap;
    }

    .toolbar-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .toolbar-label {
      font-size: 13px;
      color: rgba(226, 232, 255, 0.9);
    }

    .toolbar-select,
    .toolbar-input {
      min-width: 230px;
      background: #020617;
      border: 1px solid rgba(56, 189, 248, 0.7);
      border-radius: 10px;
      padding: 8px 12px;
      color: #e5edff;
      font-size: 14px;
      outline: none;
    }

    .toolbar-input::placeholder {
      color: rgba(148, 163, 233, 0.75);
    }

    .toolbar-select:focus,
    .toolbar-input:focus {
      box-shadow:
        0 0 0 1px rgba(96, 165, 250, 0.9),
        0 0 0 6px rgba(37, 99, 235, 0.35);
    }

    .toolbar-button {
      margin-left: auto;
      align-self: flex-end;
      padding: 10px 22px;
      border-radius: 999px;
      border: none;
      background: linear-gradient(135deg, #22c55e, #16a34a);
      color: #022c22;
      font-weight: 700;
      font-size: 14px;
      cursor: pointer;
      box-shadow: 0 0 18px rgba(34, 197, 94, 0.6);
      transition: transform 0.08s ease, box-shadow 0.12s ease;
      white-space: nowrap;
    }

    .toolbar-button:hover {
      transform: translateY(-1px);
      box-shadow: 0 0 22px rgba(34, 197, 94, 0.8);
    }

    .toolbar-button:active {
      transform: translateY(0);
      box-shadow: 0 0 12px rgba(22, 163, 74, 0.9);
    }

    /* ==== small action buttons in grid =================================== */
    .grid-action-buttons {
      display: flex;
      justify-content: center;
      gap: 8px;
    }

    .grid-btn {
      flex: 0 0 80px;      /* same width for Edit + Delete */
      padding: 4px 0;
      text-align: center;
      border-radius: 999px;
      border: 1px solid rgba(148, 163, 233, 0.7);
      background: #020617;
      color: #e5edff;
      font-size: 11px;
      cursor: pointer;
    }

    .grid-btn-edit {
      border-color: rgba(59, 130, 246, 0.9);
    }

    .grid-btn-edit:hover {
      background: rgba(59, 130, 246, 0.9);
    }

    .grid-btn-delete {
      border-color: rgba(248, 113, 113, 0.9);
      color: #fecaca;
    }

    .grid-btn-delete:hover {
      background: rgba(248, 113, 113, 0.9);
    }

    /* Centered "Add subcontract" button row */
    .sub-add-container {
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .grid-btn-add-sub {
      padding: 4px 24px;
      border-radius: 999px;
      border: 1px solid rgba(56, 189, 248, 0.9);
      background: #020617;
      color: #e5edff;
      font-size: 10px;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
    }

    .grid-btn-add-sub:hover {
      background: rgba(37, 99, 235, 0.9);
      border-color: rgba(129, 199, 255, 0.95);
    }

    .pill-secondary {
      padding: 8px 18px;
      border-radius: 999px;
      border: 1px solid rgba(148, 163, 233, 0.7);
      background: #020617;
      color: #e5edff;
      font-size: 13px;
      cursor: pointer;
    }

    /* ====== AG-GRID THEME TUNING ========================================= */
    .ag-theme-alpine {
      --ag-background-color: #050816;
      --ag-foreground-color: #e5edff;
      --ag-header-background-color: #0b1220;
      --ag-header-foreground-color: #eaf2ff;
      --ag-row-border-color: rgba(15, 23, 42, 0.9);
      --ag-border-color: rgba(30, 64, 175, 0.5);
      --ag-header-column-separator-color: rgba(148, 163, 233, 0.35);
      --ag-font-size: 12px;
      --ag-font-family: Verdana, Geneva, Tahoma, sans-serif;
      --ag-selected-row-background-color: rgba(96, 165, 250, 0.24);
    }

    .ag-theme-alpine .ag-header {
      border-bottom: 1px solid rgba(148, 163, 233, 0.5);
    }

    .ag-theme-alpine .ag-header-cell-label {
      justify-content: center;
    }

    .ag-theme-alpine .ag-header-cell-text,
    .ag-theme-alpine .ag-header-group-cell-label {
      color: #dbeafe !important;
      font-weight: 600;
      letter-spacing: 0.02em;
      font-size: 12px;
    }

    .ag-theme-alpine .ag-cell,
    .ag-theme-alpine .ag-cell-value {
      color: #e5edff !important;
      font-size: 12px;
    }

    .ag-theme-alpine .ag-cell {
      display: flex;
      align-items: center;
      justify-content: center;
      padding-top: 0;
      padding-bottom: 0;
    }

    .ag-theme-alpine .ag-cell-value {
      width: 100%;
    }

    .right {
      text-align: right;
      justify-content: flex-end;
    }

    .ag-theme-alpine .ag-row.ag-row-focus .ag-cell-focus {
      box-shadow: inset 0 0 0 1px rgba(248, 250, 252, 0.32);
    }

    .ag-theme-alpine .ag-group-contracted .ag-icon-tree-closed,
    .ag-theme-alpine .ag-group-expanded  .ag-icon-tree-open {
      color: #f9fafb !important;
      fill:  #f9fafb !important;
      stroke:#f9fafb !important;
      filter: drop-shadow(0 0 2px rgba(0,0,0,0.8));
      font-size: 10px;
    }

    /* === MASTER (CONTRACT) ROWS ========================================= */
    .ag-theme-alpine .ag-row.ag-row-level-0 .ag-cell {
      background-color: #020617;
      border-bottom: 1px solid #111827;
    }

    .ag-theme-alpine .ag-row.ag-row-level-0:nth-child(even) .ag-cell {
      background-color: #050b16;
    }

    .ag-theme-alpine .ag-row.ag-row-level-0:hover .ag-cell {
      background-color: #163672 !important;   /* medium hover */
    }

    .ag-theme-alpine .ag-row.ag-row-level-0.ag-row-selected .ag-cell {
      background-color: #1d4ed8 !important;
      box-shadow: inset 0 0 0 1px rgba(129, 199, 255, 0.9);
    }

    /* === FULL-WIDTH DETAIL WRAPPER ====================================== */
    .ag-theme-alpine .ag-full-width-row,
    .ag-theme-alpine .ag-full-width-row .ag-details-row,
    .ag-theme-alpine .ag-full-width-row .ag-details-grid {
      background-color: #020617 !important;
      border: none !important;
      padding: 0 !important;
      margin: 0 !important;
    }

    .ag-theme-alpine .ag-full-width-row .ag-cell {
      background-color: #040b1d !important;
    }

    .ag-theme-alpine .ag-full-width-row .ag-details-grid {
      margin-left: 24px !important;
      margin-top: 8px !important;
      border-left: 1px solid rgba(148, 163, 233, 0.4);
      padding-left: 10px;
    }

    /* === SUBCONTRACT (DETAIL GRID) STYLING ============================== */
    .ag-theme-alpine .ag-full-width-row .ag-details-grid .ag-row .ag-cell {
      background-color: #020617 !important;
      border-top: 0 !important;
      border-bottom: 0 !important;
    }

    .ag-theme-alpine .ag-full-width-row .ag-details-grid .ag-row {
      border-top: 0 !important;
      border-bottom: 1px solid #0c1f3a !important;
    }

    .ag-theme-alpine .ag-full-width-row .ag-details-grid .ag-row:nth-child(odd) .ag-cell {
      background-color: #050b16 !important;
    }

    .ag-theme-alpine .ag-full-width-row .ag-details-grid .ag-row:nth-child(even) .ag-cell {
      background-color: #081523 !important;
    }

    .ag-theme-alpine .ag-full-width-row .ag-details-grid .ag-row:hover .ag-cell {
      background-color: #163672 !important;
    }

    .ag-theme-alpine .ag-full-width-row .ag-details-grid .ag-row.ag-row-selected .ag-cell {
      background-color: #2563eb !important;
      box-shadow: inset 0 0 0 1px rgba(191, 219, 254, 0.9);
    }

    .ag-theme-alpine .ag-details-grid .ag-cell,
    .ag-theme-alpine .ag-details-grid .ag-header-cell-text,
    .ag-theme-alpine .ag-details-grid .ag-header-group-cell-label {
      font-size: 11px !important;
      line-height: 1.2;
    }

    .ag-theme-alpine .ag-details-grid .ag-header {
      height: 30px !important;
    }

    /* header bar for SUBCONTRACTS detail grid */
    #grid .ag-full-width-row .ag-details-grid .ag-header,
    #grid .ag-full-width-row .ag-details-grid .ag-header-viewport,
    #grid .ag-full-width-row .ag-details-grid .ag-header-row {
      background-color: #1d315e !important;
    }

    /* hide header icons in master grid, show in detail header */
    #grid .ag-root-wrapper .ag-header .ag-header-icon {
      display: none !important;
    }

    #grid .ag-full-width-row .ag-details-grid .ag-header .ag-header-icon {
      display: inline-flex !important;
    }

    /* base background for whole grid area */
    .ag-theme-alpine,
    .ag-theme-alpine .ag-root-wrapper,
    .ag-theme-alpine .ag-root,
    .ag-theme-alpine .ag-root-wrapper-body,
    .ag-theme-alpine .ag-body-viewport,
    .ag-theme-alpine .ag-center-cols-viewport,
    .ag-theme-alpine .ag-center-cols-clipper,
    .ag-theme-alpine .ag-center-cols-container,
    .ag-theme-alpine .ag-pinned-left-cols-container,
    .ag-theme-alpine .ag-pinned-right-cols-container,
    .ag-theme-alpine .ag-body-horizontal-scroll {
      background-color: #020617 !important;
    }

    /* === Column / filter menus ========================================== */
    .ag-theme-alpine .ag-menu {
      background-color: #020617 !important;
      color: #e5edff !important;
      border-radius: 8px;
      border: 1px solid rgba(56, 189, 248, 0.9);
      box-shadow: 0 18px 40px rgba(0, 0, 0, 0.85);
      min-width: 200px;
      max-width: 230px;
      padding: 0;
    }

    .ag-theme-alpine .ag-menu .ag-menu-list {
      width: 100%;
      max-height: 150vh;
      padding: 0;
    }

    .ag-theme-alpine .ag-menu .ag-menu-option {
      margin: 0;
      padding: 8px 14px;
      border-radius: 0;
      color: #e5edff !important;
    }

    .ag-theme-alpine .ag-menu .ag-menu-option:hover,
    .ag-theme-alpine .ag-menu .ag-menu-option-active {
      background-color: #07172b !important;
    }

    .ag-theme-alpine .ag-menu .ag-menu-option-icon .ag-icon {
      color: #38bdf8 !important;
      fill:  #38bdf8 !important;
      stroke:#38bdf8 !important;
    }

    /* === Set filter popup =============================================== */
    .ag-theme-alpine .ag-set-filter,
    .ag-theme-alpine .ag-set-filter-list,
    .ag-theme-alpine .ag-set-filter-item {
      background-color: #020617 !important;
      color: #e5edff !important;
    }

    .ag-theme-alpine .ag-set-filter .ag-input-field-input,
    .ag-theme-alpine .ag-set-filter input[type="text"] {
      background-color: #020617 !important;
      border: 1px solid rgba(56, 189, 248, 0.8) !important;
      color: #e5edff !important;
    }

    .ag-theme-alpine .ag-set-filter-item:hover {
      background-color: #0b1c32 !important;
    }

    .ag-theme-alpine .ag-set-filter-item .ag-icon {
      color: #38bdf8 !important;
      fill:  #38bdf8 !important;
      stroke:#38bdf8 !important;
    }

    /* ===== NEW CONTRACT / EDIT MODAL =================================== */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.9);
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: 40px 16px;
      z-index: 1000;
    }

    .modal-backdrop.hidden {
      display: none;
    }

    .modal {
      width: 100%;
      max-width: 1600px;
      max-height: 100%;
      background: #020617;
      border-radius: 18px;
      border: 1px solid rgba(56, 189, 248, 0.5);
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.9);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .modal-header {
      padding: 14px 20px;
      border-bottom: 1px solid rgba(30, 64, 175, 0.9);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }

    .modal-header h2 {
      margin: 0;
      font-size: 18px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }

    .modal-close {
      background: transparent;
      border: none;
      color: #e5edff;
      font-size: 24px;
      cursor: pointer;
      line-height: 1;
      padding: 0 6px;
    }

    .modal-body {
      padding: 16px 20px 12px 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .modal-footer {
      padding: 10px 20px 14px 20px;
      border-top: 1px solid rgba(30, 64, 175, 0.9);
      display: flex;
      justify-content: flex-end;
      gap: 10px;
    }

    .section-title {
      margin: 6px 0 4px 0;
      font-size: 14px;
      font-weight: 600;
      color: #e5edff;
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px 20px;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .form-label {
      font-size: 13px;
      color: rgba(226, 232, 255, 0.9);
    }

    .inline-checkbox-label {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .inline-checkbox-label.margin-label {
      margin-top: 0;
      margin-left: 0;
    }

    .nested-group {
      margin-top: -1px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .index-fields-row {
      margin-top: -1px;
      display: none;
      flex-direction: row;
      gap: 4px;
      align-items: flex-start;
    }

    .index-fields-row .nested-group {
      flex: 1 1 0;
      margin-top: 0;
    }

    .index-field-group {
      display: none;
    }

    .form-control,
    .form-textarea {
      background: #020617;
      border-radius: 10px;
      border: 1px solid rgba(56, 189, 248, 0.7);
      padding: 8px 10px;
      color: #e5edff;
      font-size: 14px;
      outline: none;
    }

    .form-textarea {
      min-height: 70px;
      resize: vertical;
    }

    .form-control:focus,
    .form-textarea:focus {
      box-shadow:
        0 0 0 1px rgba(96, 165, 250, 0.9),
        0 0 0 6px rgba(37, 99, 235, 0.35);
    }

    .periods-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }

    .period-card {
      border-radius: 14px;
      border: 1px solid rgba(30, 64, 175, 0.9);
      background: radial-gradient(circle at top left, rgba(15, 23, 42, 0.9), #020617 55%);
      padding: 10px 12px 12px 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 10px;
    }

    .period-header-line {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr)) auto;
      gap: 10px;
      align-items: flex-end;
    }

    .period-dates {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .period-date-wrapper {
      display: flex;
      align-items: stretch;
      background: #020617;
      border-radius: 10px;
      border: 1px solid rgba(56, 189, 248, 0.7);
      overflow: hidden;
    }

    .period-date-input {
      flex: 1 1 auto;
      border: none;
      background: transparent;
      padding: 7px 10px;
      color: #e5edff;
      font-size: 13px;
      outline: none;
    }

    .period-date-input::placeholder {
      color: rgba(148, 163, 233, 0.75);
    }

    .period-date-btn {
      width: 38px;
      border: none;
      border-left: 1px solid rgba(56, 189, 248, 0.7);
      background: rgba(15, 23, 42, 0.95);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      padding: 0;
    }

    .period-date-btn:hover {
      background: rgba(30, 64, 175, 0.95);
    }

    .date-btn-icon {
      width: 16px;
      height: 16px;
      border-radius: 3px;
      border: 2px solid #9ca3af;
      position: relative;
      box-sizing: border-box;
    }

    .date-btn-icon::before {
      content: "";
      position: absolute;
      left: -2px;
      right: -2px;
      top: -2px;
      height: 5px;
      border-bottom: 2px solid #9ca3af;
    }

    .period-remove-btn {
      padding: 8px 16px;
      border-radius: 999px;
      border: 1px solid rgba(248, 113, 113, 0.8);
      background: rgba(127, 29, 29, 0.9);
      color: #fee2e2;
      font-size: 12px;
      cursor: pointer;
      white-space: nowrap;
    }

    .period-grid {
      overflow-x: hidden;
    }

    .period-table {
      width: 100%;
      table-layout: fixed;
      border-collapse: collapse;
      font-size: 11px;
    }

    .period-table th,
    .period-table td {
      border: 1px solid rgba(30, 64, 175, 0.7);
      padding: 3px;
      text-align: center;
      background: #020617;
    }

    .period-table th.hour-col {
      min-width: 0;
      font-weight: 600;
      font-size: 10px;
    }

    .period-table td.label-cell {
      min-width: 120px;
      text-align: left;
      padding-left: 8px;
      background: #020617;
    }

    .period-input {
      width: 100%;
      box-sizing: border-box;
      border-radius: 7px;
      border: 1px solid rgba(37, 99, 235, 0.8);
      background: #020617;
      color: #e5edff;
      font-size: 10px;
      padding: 2px 3px;
      outline: none;
      text-align: center;
    }

    .period-input:focus {
      box-shadow: 0 0 0 1px rgba(96, 165, 250, 0.9);
    }

    .period-row-margin {
      display: none;
    }

    @media (max-width: 1200px) {
      .form-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 800px) {
      .form-grid {
        grid-template-columns: minmax(0, 1fr);
      }
      .modal {
        max-width: 100%;
      }
    }

    #nc_notes {
      width: 1200px;
      height: 30px;
      min-height: 30px;
      max-width: 100%;
    }

    /* === Small date+time popup =========================== */
    .dt-popup-backdrop {
      position: fixed;
      inset: 0;
      z-index: 3000;
      background: transparent;
    }

    .dt-popup-panel {
      position: absolute;
      min-width: 230px;
      padding: 8px 10px 10px;
      border-radius: 10px;
      background: #020617;
      border: 1px solid rgba(59, 130, 246, 0.9);
      box-shadow: 0 18px 40px rgba(0, 0, 0, 0.85);
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 12px;
    }

    .dt-popup-row {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .dt-popup-row label {
      flex: 0 0 40px;
      color: #e5edff;
      font-size: 11px;
    }

    .dt-popup-row input[type="date"],
    .dt-popup-row input[type="time"] {
      flex: 1 1 auto;
      background: #020617;
      border-radius: 6px;
      border: 1px solid rgba(148, 163, 233, 0.8);
      padding: 4px 6px;
      color: #e5edff;
      font-size: 11px;
      outline: none;
    }

    .dt-popup-row input[type="date"]:focus,
    .dt-popup-row input[type="time"]:focus {
      box-shadow:
        0 0 0 1px rgba(96, 165, 250, 0.9),
        0 0 0 4px rgba(37, 99, 235, 0.35);
    }

    .dt-popup-actions {
      margin-top: 4px;
      display: flex;
      justify-content: flex-end;
      gap: 6px;
    }

    .dt-popup-btn {
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid rgba(148, 163, 233, 0.8);
      background: #020617;
      color: #e5edff;
      font-size: 11px;
      cursor: pointer;
    }

    .dt-popup-btn.primary {
      border-color: rgba(34, 197, 94, 0.95);
      background: linear-gradient(135deg, #22c55e, #16a34a);
      color: #022c22;
    }
  </style>
</head>
"""
    html += u"""
<body>
  <div class="page">
    <div class="shell">
      <div class="topbar">
        <div class="title-block">
          <h1>CONTRACTS</h1>
        </div>
        <div class="status-pill">
          <span class="status-dot"></span>
          <span id="statusBar">Loading…</span>
        </div>
      </div>

      <div class="grid-card">
        <div class="toolbar">
          <div class="toolbar-group">
            <label class="toolbar-label" for="statusFilter">Status</label>
            <select id="statusFilter" class="toolbar-select">
              <option value="all">All contracts</option>
              <option value="active">Active only</option>
              <option value="closed">Closed only</option>
            </select>
          </div>

          <div class="toolbar-group">
            <label class="toolbar-label" for="contractFilter">Contract</label>
            <select id="contractFilter" class="toolbar-select">
              <option value="">All</option>
            </select>
          </div>

          <div class="toolbar-group">
            <label class="toolbar-label" for="contractSearch">Search by contract</label>
            <input id="contractSearch" class="toolbar-input"
                   placeholder="Type contract, country, client...">
          </div>

          <button id="newContractBtn" class="toolbar-button">
            + New contract
          </button>
        </div>

        <div class="grid-header-row">
          <span>Use the disclosure arrow ▸ on the contract row to see subcontracts. Double-click a subcontract row to open the hourly view (read-only). Use the Edit button to modify.</span>
          <span></span>
        </div>

        <div id="grid" class="ag-theme-alpine"></div>
      </div>

      <div class="footer-note">
        Powered by AG&nbsp;Grid v34 • Dark layout for trading / operations desks
      </div>
    </div>
  </div>

  <!-- ===== MODAL ====================================================== -->
  <div id="newContractModal" class="modal-backdrop hidden">
    <div class="modal">
      <div class="modal-header">
        <h2 id="modalTitle">New contract</h2>
        <button id="modalCloseBtn" class="modal-close">&times;</button>
      </div>
      <div class="modal-body">
        <!-- Contract details -->
        <div id="contractSection">
          <div class="section-title">Contract details</div>
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label" for="nc_counterparty">Counterparty</label>
              <input id="nc_counterparty" class="form-control"
                     placeholder="Type counterparty name or ID"/>
            </div>
            <div class="form-group">
              <label class="form-label" for="nc_contract_no">Contract number</label>
              <input id="nc_contract_no" class="form-control"
                     placeholder="CN-YYYY-NNN"/>
            </div>
            <div class="form-group">
              <label class="form-label" for="nc_country">Country</label>
              <select id="nc_country" class="form-control">
                <option value="">-- select country --</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="nc_date_from">Start date</label>
              <div class="period-date-wrapper">
                <input id="nc_date_from"
                       type="text"
                       class="period-date-input"
                       placeholder="YYYY-MM-DD HH:mm:ss.0">
                <button type="button"
                        class="period-date-btn"
                        title="Pick date &amp; time">
                  <span class="date-btn-icon"></span>
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label" for="nc_date_to">End date</label>
              <div class="period-date-wrapper">
                <input id="nc_date_to"
                       type="text"
                       class="period-date-input"
                       placeholder="YYYY-MM-DD HH:mm:ss.0">
                <button type="button"
                        class="period-date-btn"
                        title="Pick date &amp; time">
                  <span class="date-btn-icon"></span>
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label" for="nc_currency">CCY (contract_currencyid)</label>
              <select id="nc_currency" class="form-control">
                <option value="">-- select --</option>
              </select>
            </div>
          </div>

          <div class="form-group" style="margin-top:8px;">
            <label class="form-label" for="nc_notes">Notes</label>
            <textarea id="nc_notes" class="form-textarea"
                      placeholder="optional"></textarea>
          </div>
        </div>

        <!-- Subcontract defaults (price, quantity, index, margin, sides) -->
        <div id="subDefaultsSection" class="form-grid">
          <!-- row 1: Quantity | Price | Transport -->
          <div class="form-group">
            <label class="form-label" for="nc_qty_type">Quantity type</label>
            <select id="nc_qty_type" class="form-control">
              <option value="">-- select --</option>
              <option value="fixed">Fixed</option>
              <option value="variable">Variable</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="nc_price_type">Price type</label>
            <select id="nc_price_type" class="form-control">
              <option value="">-- select --</option>
              <option value="fixed">Fixed</option>
              <option value="variable">Variable</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="nc_transport_side">Transport costs</label>
            <select id="nc_transport_side" class="form-control">
              <option value="">-- select --</option>
              <option value="none">None</option>
              <option value="our">On our side</option>
              <option value="their">On their side</option>
            </select>
          </div>

          <!-- row 2: Border | Import | Export -->
          <div class="form-group">
            <label class="form-label" for="nc_border_side">Border costs</label>
            <select id="nc_border_side" class="form-control">
              <option value="">-- select --</option>
              <option value="none">None</option>
              <option value="our">On our side</option>
              <option value="their">On their side</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="nc_import_side">Import costs</label>
            <select id="nc_import_side" class="form-control">
              <option value="">-- select --</option>
              <option value="none">None</option>
              <option value="our">On our side</option>
              <option value="their">On their side</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="nc_export_side">Export costs</label>
            <select id="nc_export_side" class="form-control">
              <option value="">-- select --</option>
              <option value="none">None</option>
              <option value="our">On our side</option>
              <option value="their">On their side</option>
            </select>
          </div>

          <!-- row 3: Margin column (checkbox + currency under it) -->
          <div class="form-group">
            <label class="form-label inline-checkbox-label margin-label" for="nc_margin_enabled">
              <input type="checkbox" id="nc_margin_enabled">
              <span>Margin</span>
            </label>

            <div id="marginCurrencyGroup" class="nested-group" style="display:none;">
              <label class="form-label" for="nc_margin_ccy">Margin currency</label>
              <select id="nc_margin_ccy" class="form-control">
                <option value="">-- select --</option>
              </select>
            </div>
          </div>

          <!-- row 3: Index column (checkbox + type + currency on ONE line) -->
          <div class="form-group">
            <label class="form-label inline-checkbox-label margin-label" for="nc_index_enabled">
              <input type="checkbox" id="nc_index_enabled">
              <span>Index</span>
            </label>

            <div class="index-fields-row index-field-group">
              <div class="nested-group">
                <label class="form-label" for="nc_index_type">Index type</label>
                <select id="nc_index_type" class="form-control">
                  <option value="">-- select --</option>
                  <option value="RDN">RDN</option>
                  <option value="OPEM">OPEM</option>
                  <option value="OPCOM">OPCOM</option>
                </select>
              </div>

              <div class="nested-group">
                <label class="form-label" for="nc_index_ccy">Index currency</label>
                <select id="nc_index_ccy" class="form-control">
                  <option value="">-- select --</option>
                </select>
              </div>
            </div>
          </div>

          <div class="form-group"></div>
        </div>

        <!-- Hourly periods -->
        <div id="hourlyPeriodsSection">
          <div class="periods-header-row">
            <div class="section-title">Hourly periods (per subcontract)</div>
            <button id="addPeriodBtn" type="button" class="pill-secondary">+ Add period</button>
          </div>
          <div id="periodsContainer"></div>
        </div>
      </div>

      <div class="modal-footer">
        <button id="cancelContractBtn" type="button" class="pill-secondary">Cancel</button>
        <button id="saveContractBtn" type="button" class="toolbar-button">
          Save contract
        </button>
      </div>
    </div>
  </div>

  <!-- Template for hourly period -->
  <template id="periodTemplate">
    <div class="period-card">
      <div class="period-header-line">
        <div class="period-dates">
          <label class="form-label">Start Date</label>
          <div class="period-date-wrapper">
            <input type="text"
                   class="period-date-input period-start"
                   placeholder="YYYY-MM-DD HH:mm:ss.0">
            <button type="button"
                    class="period-date-btn"
                    title="Pick date &amp; time">
              <span class="date-btn-icon"></span>
            </button>
          </div>
        </div>

        <div class="period-dates">
          <label class="form-label">End Date</label>
          <div class="period-date-wrapper">
            <input type="text"
                   class="period-date-input period-end"
                   placeholder="YYYY-MM-DD HH:mm:ss.0">
            <button type="button"
                    class="period-date-btn"
                    title="Pick date &amp; time">
              <span class="date-btn-icon"></span>
            </button>
          </div>
        </div>

        <button type="button" class="period-remove-btn">Remove</button>
      </div>

      <div class="period-grid">
        <table class="period-table">
          <thead>
            <tr class="period-header-row">
              <th class="label-cell"></th>
            </tr>
          </thead>
          <tbody>
            <tr class="period-row-qty">
              <td class="label-cell">Quantity kWh</td>
            </tr>
            <tr class="period-row-price">
              <td class="label-cell">Price MWh</td>
            </tr>
            <tr class="period-row-margin">
              <td class="label-cell">Margin</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>

  <script>
    let gridApi = null;
    let currentStatusFilter = "all";
    window.contractRows = [];
    window.currencyByCode = {};

    function getContractIdFromUrl() {
      const params = new URLSearchParams(window.location.search);
      const v = params.get("contract_id");
      return v ? (parseInt(v, 10) || 0) : 0;
    }

    function setStatus(msg) {
      const el = document.getElementById("statusBar");
      if (el) el.textContent = msg;
    }

    function trimDate(value) {
      if (value == null) return "";
      if (typeof value === "string") {
        if (value.length >= 10) return value.substring(0, 10);
        return value;
      }
      try {
        var d = new Date(value);
        if (!isNaN(d.getTime())) {
          var y  = d.getFullYear();
          var m  = String(d.getMonth() + 1).padStart(2, "0");
          var d2 = String(d.getDate()).padStart(2, "0");
          return y + "-" + m + "-" + d2;
        }
      } catch (e) {}
      return value;
    }

    function formatDateTimeForDisplay(value) {
      if (!value) return "";
      var d = (value instanceof Date) ? value : new Date(value);
      if (isNaN(d.getTime())) return "";
      var y  = d.getFullYear();
      var m  = String(d.getMonth() + 1).padStart(2, "0");
      var d2 = String(d.getDate()).padStart(2, "0");
      var h  = String(d.getHours()).padStart(2, "0");
      var mi = String(d.getMinutes()).padStart(2, "0");
      var s  = String(d.getSeconds()).padStart(2, "0");
      return y + "-" + m + "-" + d2 + " " + h + ":" + mi + ":" + s + ".0";
    }

    function formatDateTimeShort(value) {
      if (!value) return "";
      var s = String(value).trim();

      if (s.length >= 16 && s[4] === "-" && s[7] === "-" && (s[10] === " " || s[10] === "T")) {
        return s.substring(0, 16);   // "YYYY-MM-DD HH:mm"
      }

      var d = new Date(s);
      if (isNaN(d.getTime())) return s;

      var y  = d.getFullYear();
      var m  = String(d.getMonth() + 1).padStart(2, "0");
      var d2 = String(d.getDate()).padStart(2, "0");
      var h  = String(d.getHours()).padStart(2, "0");
      var mi = String(d.getMinutes()).padStart(2, "0");
      return y + "-" + m + "-" + d2 + " " + h + ":" + mi;
    }

    function splitDisplayDateTime(displayValue) {
      if (!displayValue) return { date: "", time: "" };
      var txt = String(displayValue).trim();
      var datePart = txt.length >= 10 ? txt.substring(0, 10) : "";
      var timePart = txt.length >= 16 ? txt.substring(11, 16) : "";
      return { date: datePart, time: timePart };
    }

    function closeDateTimePopup() {
      var backdrop = document.getElementById("dtPopupBackdrop");
      if (backdrop && backdrop.parentNode) {
        backdrop.parentNode.removeChild(backdrop);
      }
    }

    function openDateTimePopup(targetInput) {
      closeDateTimePopup();

      var rect = targetInput.getBoundingClientRect();

      var backdrop = document.createElement("div");
      backdrop.id = "dtPopupBackdrop";
      backdrop.className = "dt-popup-backdrop";

      var panel = document.createElement("div");
      panel.className = "dt-popup-panel";
      var offsetX = 380;
      panel.style.top  = (rect.bottom + 6) + "px";
      panel.style.left = (rect.left + offsetX) + "px";

      var parts = splitDisplayDateTime(targetInput.value);

      var rowDate = document.createElement("div");
      rowDate.className = "dt-popup-row";
      var lblDate = document.createElement("label");
      lblDate.textContent = "Date";
      var inputDate = document.createElement("input");
      inputDate.type = "date";
      if (parts.date) inputDate.value = parts.date;
      rowDate.appendChild(lblDate);
      rowDate.appendChild(inputDate);

      var rowTime = document.createElement("div");
      rowTime.className = "dt-popup-row";
      var lblTime = document.createElement("label");
      lblTime.textContent = "Time";
      var inputTime = document.createElement("input");
      inputTime.type = "time";
      inputTime.step = 60;
      if (parts.time) inputTime.value = parts.time;
      rowTime.appendChild(lblTime);
      rowTime.appendChild(inputTime);

      var actions = document.createElement("div");
      actions.className = "dt-popup-actions";
      var btnCancel = document.createElement("button");
      btnCancel.type = "button";
      btnCancel.className = "dt-popup-btn";
      btnCancel.textContent = "Cancel";
      var btnApply = document.createElement("button");
      btnApply.type = "button";
      btnApply.className = "dt-popup-btn primary";
      btnApply.textContent = "Apply";
      actions.appendChild(btnCancel);
      actions.appendChild(btnApply);

      panel.appendChild(rowDate);
      panel.appendChild(rowTime);
      panel.appendChild(actions);
      backdrop.appendChild(panel);
      document.body.appendChild(backdrop);

      backdrop.addEventListener("click", function (ev) {
        if (ev.target === backdrop) closeDateTimePopup();
      });

      btnCancel.addEventListener("click", function () {
        closeDateTimePopup();
      });

      btnApply.addEventListener("click", function () {
        if (!inputDate.value) {
          closeDateTimePopup();
          return;
        }
        var timeVal = inputTime.value || "00:00";
        var formatted;
        if (timeVal.length === 5) {
          formatted = inputDate.value + " " + timeVal + ":00.0";
        } else if (timeVal.length === 8) {
          formatted = inputDate.value + " " + timeVal + ".0";
        } else {
          formatted = inputDate.value + " " + timeVal + ":00.0";
        }
        targetInput.value = formatted;
        closeDateTimePopup();
      });

      inputDate.focus();
    }

    document.addEventListener("click", function (ev) {
      var btn = ev.target.closest(".period-date-btn");
      if (!btn) return;
      var wrapper = btn.closest(".period-date-wrapper");
      if (!wrapper) return;
      var input = wrapper.querySelector(".period-date-input");
      if (!input) return;
      openDateTimePopup(input);
    });

    function decodeSide(dbValue) {
      if (dbValue == null) return "";
      var v = String(dbValue).toLowerCase();
      if (v.indexOf("our")   >= 0) return "our";
      if (v.indexOf("their") >= 0) return "their";
      return "";
    }

    function encodeSide(formValue) {
      if (formValue === "our")   return "on our side";
      if (formValue === "their") return "on their side";
      return "";
    }

    function isContractActive(data) {
      if (!data || !data.contract_date_to) return true;
      const raw = data.contract_date_to;
      const dt = new Date(raw);
      if (isNaN(dt.getTime())) return true;
      const today = new Date();
      today.setHours(0,0,0,0);
      dt.setHours(0,0,0,0);
      return dt >= today;
    }

    /* ================= COLUMN DEFINITIONS =============================== */

    const contractColumnDefs = [
      {
        field: "contract_dealno",
        headerName: "Contract",
        cellRenderer: "agGroupCellRenderer",
        width: 150,
        flex: 0,
        pinned: "left"
      },
      {
        field: "contract_contragentid",
        headerName: "Contragent",
        width: 170,
        minWidth: 170,
        maxWidth: 190,
        flex: 0
      },
      {
        field: "contract_date_from",
        headerName: "Date from",
        width: 120,
        flex: 0,
        valueFormatter: function(params){ return trimDate(params.value); }
      },
      {
        field: "contract_date_to",
        headerName: "Date to",
        width: 120,
        flex: 0,
        valueFormatter: function(params){ return trimDate(params.value); }
      },
      {
        field: "contract_sign_date",
        headerName: "Sign date",
        width: 120,
        flex: 0,
        valueFormatter: function(params){ return trimDate(params.value); }
      },
      { field: "contract_created_by", headerName: "Created by", width: 100, flex: 0 },
      {
        field: "contract_created_at",
        headerName: "Created at",
        width: 150,
        flex: 0,
        valueFormatter: function(params){ return formatDateTimeShort(params.value); }
      },
      { field: "contract_updated_by", headerName: "Updated by", width: 100, flex: 0 },
      {
        field: "contract_updated_at",
        headerName: "Updated at",
        width: 150,
        flex: 0,
        valueFormatter: function(params){ return formatDateTimeShort(params.value); }
      },
      {
        headerName: "# subcontracts",
        valueGetter: function(p){
          return (p.data && p.data.subcontracts) ? p.data.subcontracts.length : 0;
        },
        width: 100,
        flex: 0,
        cellClass: "right"
      },
      {
        headerName: "Actions",
        field: "actions",
        width: 210,
        minWidth: 210,
        maxWidth: 210,
        flex: 1,
        sortable: false,
        filter: false,
        suppressMenu: true,
        cellRenderer: function (params) {
          return '' +
            '<div class="grid-action-buttons">' +
              '<button type="button" class="grid-btn grid-btn-edit" data-action="edit">Edit</button>' +
              '<button type="button" class="grid-btn grid-btn-delete" data-action="delete">Delete</button>' +
            '</div>';
        }
      }
    ];

    const subcontractColumnDefs = [
      {
  field: "subcontract_id",
  headerName: "ID",
  width: 64,
  minWidth: 64,
  maxWidth: 64,
  flex: 0,

  // Make the "Add row" span across ALL columns
  colSpan: function (params) {
    if (params.data && params.data.__isAddRow) {
      var cols = (params.api && params.api.getAllDisplayedColumns)
        ? params.api.getAllDisplayedColumns()
        : [];
      return (cols && cols.length) ? cols.length : 1;
    }
    return 1;
  },

  cellClass: function (params) {
    return (params.data && params.data.__isAddRow) ? "sub-add-cell" : "";
  },

  cellRenderer: function (params) {
    if (params.data && params.data.__isAddRow) {
      return '' +
        '<div class="sub-add-container">' +
          '<button type="button" class="grid-btn-add-sub" data-sub-action="add">' +
            '+ Add subcontract' +
          '</button>' +
        '</div>';
    }
    return (params.value == null) ? "" : params.value;
  }
},
      {
        field: "subcontract_dealno",
        headerName: "Subcontract",
        width: 120,
        minWidth: 120,
        maxWidth: 120,
        flex: 0
      },
      {
        field: "subcontract_slot_date",
        headerName: "Date",
        width: 80,
        minWidth: 80,
        maxWidth: 80,
        flex: 0,
        valueFormatter: function(params){ return trimDate(params.value); }
      },
      {
        field: "subcontract_datetime_from",
        headerName: "From",
        width: 115,
        minWidth: 115,
        maxWidth: 115,
        valueFormatter: function(params){ return formatDateTimeShort(params.value); }
      },
      {
        field: "subcontract_datetime_to",
        headerName: "To",
        width: 115,
        minWidth: 115,
        maxWidth: 115,
        valueFormatter: function(params){ return formatDateTimeShort(params.value); }
      },
      { field: "subcontract_price_type",    headerName: "Price type", width: 110, flex: 0 },
      { field: "subcontract_quantity_type", headerName: "Qty type",   width: 110, flex: 0 },
      { field: "subcontract_index_type",    headerName: "Index type", width: 110, flex: 0 },
      { field: "subcontract_created_by",    headerName: "Created by", width: 110, flex: 0 },
      {
        field: "subcontract_created_at",
        headerName: "Created at",
        width: 115,
        minWidth: 115,
        maxWidth: 115,
        flex: 0,
        valueFormatter: function(params){ return formatDateTimeShort(params.value); }
      },
      { field: "subcontract_updated_by",    headerName: "Updated by", width: 110, flex: 0 },
      {
        field: "subcontract_updated_at",
        headerName: "Updated at",
        width: 115,
        minWidth: 115,
        maxWidth: 115,
        flex: 0,
        valueFormatter: function(params){ return formatDateTimeShort(params.value); }
      },
      {
        headerName: "Actions",
        field: "sub_actions",
        width: 170,
        minWidth: 170,
        maxWidth: 170,
        flex: 0,
        sortable: false,
        filter: false,
        suppressMenu: true,
        cellRenderer: function (params) {
          if (params.data && params.data.__isAddRow) {
            return '' +
              '<div class="grid-action-buttons">' +
                '<button type="button" class="grid-btn grid-btn-edit" data-sub-action="add">+ Add subcontract</button>' +
              '</div>';
          }
          return '' +
            '<div class="grid-action-buttons">' +
              '<button type="button" class="grid-btn grid-btn-edit" data-sub-action="edit">Edit</button>' +
              '<button type="button" class="grid-btn grid-btn-delete" data-sub-action="delete">Delete</button>' +
            '</div>';
        }
      }
    ];

    /* ================= GRID EVENT HANDLERS ============================== */

    function handleContractActionClick(params) {
      if (!params || !params.colDef || params.colDef.field !== "actions") return;
      if (!params.event || !params.event.target) return;

      var btn = params.event.target.closest("button[data-action]");
      if (!btn) return;

      var action = btn.getAttribute("data-action");
      var row    = params.data;
      if (!row) return;

      if (action === "edit") {
        openEditContractModal(row);
        return;
      }

      if (action === "delete") {
        var cid = row.contract_id;
        if (!cid) {
          alert("contract_id is missing on this row.");
          return;
        }

        var subCount = (row.subcontracts && row.subcontracts.length) ? row.subcontracts.length : 0;
        if (subCount > 0) {
          alert("This contract has " + subCount + " subcontract(s) and cannot be deleted.");
          return;
        }

        var label = row.contract_dealno || cid;
        if (!confirm("Are you sure you want to delete contract " + label + "?")) {
          return;
        }

        fetch("delete_contract", {
          method: "POST",
          credentials: "same-origin",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ contract_id: cid })
        })
          .then(function (resp) { return resp.json(); })
          .then(function (result) {
            if (result && result.ok) {
              window.contractRows = (window.contractRows || []).filter(function (r) {
                return String(r.contract_id) !== String(cid);
              });
              if (gridApi) {
                gridApi.setGridOption("rowData", window.contractRows);
              }
              setStatus("Contract " + label + " deleted.");
            } else {
              var errMsg = (result && result.error) ? result.error : "Unknown error";
              alert("Delete failed: " + errMsg);
            }
          })
          .catch(function (err) {
            console.error("Delete error:", err);
            alert("Error deleting contract: " + err);
          });
      }
    }

    function findSubcontractContext(subRow) {
      if (!subRow || subRow.subcontract_id == null) return null;
      const subIdStr = String(subRow.subcontract_id);
      let parentContract = null;
      let hourlyRows = [];
      (window.contractRows || []).forEach(function(contract) {
        if (!contract.subcontracts) return;
        const matches = contract.subcontracts.filter(function(s) {
          return String(s.subcontract_id) === subIdStr;
        });
        if (matches.length && !parentContract) {
          parentContract = contract;
          hourlyRows = matches;
        }
      });
      if (!parentContract) return null;
      return { contract: parentContract, hourly: hourlyRows };
    }

    function handleSubRowDoubleClicked(event) {
      if (event && event.data && event.data.__isAddRow) {
        const cid = event.data._parentContractId;
        if (cid != null) {
          openNewSubcontractModal(cid);
        }
        return;
      }
      const ctx = findSubcontractContext(event.data);
      if (!ctx) {
        console.warn("No parent contract found for subcontract", event.data);
        return;
      }
      openViewModalForSubcontract(ctx.contract, ctx.hourly);
    }

    function handleSubcontractActionClick(params) {
      if (!params || !params.colDef || params.colDef.field !== "sub_actions") return;
      if (!params.event || !params.event.target) return;

      var btn = params.event.target.closest("button[data-sub-action]");
      if (!btn) return;

      var action = btn.getAttribute("data-sub-action");
      var subRow = params.data;
      if (!subRow || subRow.__isAddRow) return;

      var ctx = findSubcontractContext(subRow);
      if (!ctx) {
        console.warn("No parent for subcontract", subRow);
        return;
      }

      if (action === "edit") {
        openEditModalForSubcontract(ctx.contract, ctx.hourly);
        return;
      }

      if (action === "delete") {
        var sid = subRow.subcontract_id;
        if (!sid) {
          alert("subcontract_id is missing on this row.");
          return;
        }
        var label = subRow.subcontract_dealno || sid;
        if (!confirm("Are you sure you want to delete subcontract " + label + "?")) {
          return;
        }

        fetch("delete_subcontract", {
          method: "POST",
          credentials: "same-origin",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ subcontract_id: sid })
        })
          .then(function (resp) { return resp.json(); })
          .then(function (result) {
            if (result && result.ok) {
              (window.contractRows || []).forEach(function(c) {
                if (!c.subcontracts) return;
                c.subcontracts = c.subcontracts.filter(function(s) {
                  return String(s.subcontract_id) !== String(sid);
                });
              });
              if (gridApi) {
                gridApi.setGridOption("rowData", window.contractRows);
              }
              setStatus("Subcontract " + label + " deleted.");
            } else {
              var errMsg = (result && result.error) ? result.error : "Unknown error";
              alert("Delete failed: " + errMsg);
            }
          })
          .catch(function (err) {
            console.error("Delete subcontract error:", err);
            alert("Error deleting subcontract: " + err);
          });
      }
    }

    function openNewSubcontractModal(contractId) {
      if (contractId == null) return;

      const contractRow = (window.contractRows || []).find(function (r) {
        return String(r.contract_id) === String(contractId);
      });
      if (!contractRow) {
        console.warn("openNewSubcontractModal: contract not found for id", contractId);
        return;
      }

      // start from "new contract" defaults
      resetModalForNewContract();
      showFullSubcontractMode();

      const titleEl = document.getElementById("modalTitle");
      if (titleEl) {
        titleEl.textContent = "New subcontract for " + (contractRow.contract_dealno || "");
      }

      const saveBtn = document.getElementById("saveContractBtn");
      if (saveBtn) {
        saveBtn.textContent = "Save subcontract";
        saveBtn.dataset.mode = "createSubcontract";
        saveBtn.dataset.contractId = String(contractRow.contract_id || "");
        saveBtn.dataset.subcontractId = "";
      }

      const cpEl   = document.getElementById("nc_counterparty");
      const noEl   = document.getElementById("nc_contract_no");
      const ctryEl = document.getElementById("nc_country");
      const dFromEl = document.getElementById("nc_date_from");
      const dToEl   = document.getElementById("nc_date_to");
      const ccyEl   = document.getElementById("nc_currency");
      const notesEl = document.getElementById("nc_notes");

      if (cpEl)   cpEl.value   = contractRow.contract_contragentid || "";
      if (noEl)   noEl.value   = contractRow.contract_dealno || "";
      if (ctryEl) ctryEl.value = contractRow.contract_country || "";
      if (dFromEl) dFromEl.value = formatDateTimeForDisplay(contractRow.contract_date_from || "");
      if (dToEl)   dToEl.value   = formatDateTimeForDisplay(contractRow.contract_date_to   || "");
      if (ccyEl && contractRow.contract_currencyid != null) {
        ccyEl.value = String(contractRow.contract_currencyid);
      }
      if (notesEl) notesEl.value = contractRow.contract_notes || "";

      const backdrop = document.getElementById("newContractModal");
      if (backdrop) {
        backdrop.classList.remove("hidden");
      }
    }

    function handleDetailGridCellClick(params) {
      if (!params || !params.data) return;

      const rowData = params.data;

      if (rowData.__isAddRow) {
        var btn = params.event && params.event.target
          ? params.event.target.closest("button[data-sub-action]")
          : null;

        if (!btn || btn.getAttribute("data-sub-action") === "add") {
          const cid = rowData._parentContractId;
          if (cid != null) {
            openNewSubcontractModal(cid);
          }
        }
        return;
      }

      // normal subcontract row
      handleSubcontractActionClick(params);
    }

    /* ================= GRID OPTIONS ==================================== */

    const MASTER_ROW_HEIGHT       = 34;
    const DETAIL_HEADER_HEIGHT    = 30;
    const DETAIL_ROW_HEIGHT       = 26;
    const DETAIL_VERTICAL_PADDING = 14;

    const gridOptions = {
      columnDefs: contractColumnDefs,
      defaultColDef: {
        resizable: true,
        sortable: true,
        filter: true,
      
        minWidth: 100
      },
      animateRows: true,
      masterDetail: true,
      onCellClicked: handleContractActionClick,
      popupParent: document.body,

      getQuickFilterText: function (params) {
        const d = params.data || {};
        return [
          d.contract_dealno,
          d.contract_id,
          d.contract_contragentid,
          d.contract_country,
          d.contract_notes
        ]
          .filter(function (v) {
            return v !== null && v !== undefined && v !== "";
          })
          .join(" ");
      },

      getRowHeight: function (params) {
        if (params.node && params.node.detail) {
          const subs = (params.data && params.data.subcontracts)
            ? params.data.subcontracts.length
            : 0;
          const count = Math.max(subs, 1) + 1; // +1 for "Add subcontract" row
          return DETAIL_HEADER_HEIGHT +
                 DETAIL_VERTICAL_PADDING +
                 count * DETAIL_ROW_HEIGHT;
        }
        return MASTER_ROW_HEIGHT;
      },

      detailCellRendererParams: {
        detailGridOptions: {
          columnDefs: subcontractColumnDefs,
          defaultColDef: {
            resizable: true,
            sortable: true,
            filter: true,
            flex: 1,
            minWidth: 80
          },
          getRowId: function (params) {
            // normal rows use subcontract_id; add-row has empty id
            return String(params.data.subcontract_id || "");
          },
          onRowDoubleClicked: handleSubRowDoubleClicked,
          onCellClicked: handleDetailGridCellClick,
          postSortRows: function (params) {
            var nodes = params.nodes || [];
            var idx = -1;
            for (var i = 0; i < nodes.length; i++) {
              if (nodes[i].data && nodes[i].data.__isAddRow) {
                idx = i;
                break;
              }
            }
            if (idx >= 0) {
              var addNode = nodes.splice(idx, 1)[0];
              nodes.push(addNode);
            }
          }
        },
        getDetailRowData: function (params) {
          var master = params.data || {};
          var subs = (master && master.subcontracts)
            ? master.subcontracts.slice()
            : [];
          subs.push({
            __isAddRow: true,
            _parentContractId: master.contract_id || null,
            _parentContractDealno: master.contract_dealno || ""
          });
          params.successCallback(subs);
        }
      }
    };

    /* ================= TOOLBAR / FILTERS ================================ */

    function populateContractFilter(rows) {
      const sel = document.getElementById("contractFilter");
      if (!sel) return;
      const seen = new Set();
      rows.forEach(function(r) {
        const deal = r.contract_dealno;
        if (deal && !seen.has(deal)) {
          seen.add(deal);
          const opt = document.createElement("option");
          opt.value = String(deal);
          opt.textContent = String(deal);
          sel.appendChild(opt);
        }
      });
    }

    function applyToolbarFilters() {
      if (!gridApi) return;

      var allRows = window.contractRows || [];

      var statusEl   = document.getElementById("statusFilter");
      var contractEl = document.getElementById("contractFilter");
      var searchEl   = document.getElementById("contractSearch");

      var statusVal   = statusEl   ? (statusEl.value   || "all") : "all";
      var contractVal = contractEl ? (contractEl.value || "")    : "";
      var searchVal   = searchEl   ? searchEl.value.trim().toLowerCase() : "";

      currentStatusFilter = statusVal;

      var filtered = allRows.filter(function (r) {
        if (!r) return false;

        var active = isContractActive(r);
        if (statusVal === "active" && !active) return false;
        if (statusVal === "closed" &&  active) return false;

        if (contractVal && String(r.contract_dealno) !== String(contractVal)) {
          return false;
        }

        if (searchVal) {
          var haystack = [
            r.contract_id,
            r.contract_dealno,
            r.contract_contragentid,
            r.contract_country,
            r.contract_notes
          ]
            .filter(function (v) {
              return v !== null && v !== undefined && v !== "";
            })
            .join(" ")
            .toLowerCase();

          if (haystack.indexOf(searchVal) === -1) return false;
        }

        return true;
      });

      gridApi.setGridOption("rowData", filtered);
    }

    /* ================= PERIOD TABLE / VISIBILITY ======================== */

    function buildPeriodTableHours(card) {
      const headerRow = card.querySelector(".period-header-row");
      const qtyRow    = card.querySelector(".period-row-qty");
      const priceRow  = card.querySelector(".period-row-price");
      const marginRow = card.querySelector(".period-row-margin");

      for (let h = 1; h <= 24; h++) {
        const label = String(h).padStart(2, "0");

        const th = document.createElement("th");
        th.className = "hour-col";
        th.textContent = label;
        headerRow.appendChild(th);

        const tdQty = document.createElement("td");
        const inpQty = document.createElement("input");
        inpQty.type = "text";
        inpQty.className = "period-input";
        inpQty.setAttribute("data-field", "qty");
        inpQty.setAttribute("data-hour", label);
        tdQty.appendChild(inpQty);
        qtyRow.appendChild(tdQty);

        const tdPrice = document.createElement("td");
        const inpPrice = document.createElement("input");
        inpPrice.type = "text";
        inpPrice.className = "period-input";
        inpPrice.setAttribute("data-field", "price");
        inpPrice.setAttribute("data-hour", label);
        tdPrice.appendChild(inpPrice);
        priceRow.appendChild(tdPrice);

        const tdMargin = document.createElement("td");
        const inpMargin = document.createElement("input");
        inpMargin.type = "text";
        inpMargin.className = "period-input";
        inpMargin.setAttribute("data-field", "margin");
        inpMargin.setAttribute("data-hour", label);
        tdMargin.appendChild(inpMargin);
        marginRow.appendChild(tdMargin);
      }
    }

    function updateMarginVisibility(enabled) {
      const grp = document.getElementById("marginCurrencyGroup");
      if (grp) grp.style.display = enabled ? "" : "none";
      document.querySelectorAll(".period-row-margin").forEach(function(row) {
        row.style.display = enabled ? "table-row" : "none";
      });
    }

    function updateIndexVisibility(enabled) {
      document.querySelectorAll(".index-field-group").forEach(function (el) {
        el.style.display = enabled ? "flex" : "none";
      });
    }

    function updateQuantityVisibility(mode) {
      if (mode === "none") {
        var sel = document.getElementById("nc_qty_type");
        if (sel) sel.value = "variable";
        mode = "variable";
      }
      var showRow = (mode === "fixed");
      document.querySelectorAll(".period-row-qty").forEach(function (row) {
        row.style.display = showRow ? "table-row" : "none";
      });
    }

    function updatePriceVisibility(mode) {
      if (mode === "none") {
        var sel = document.getElementById("nc_price_type");
        if (sel) sel.value = "variable";
        mode = "variable";
      }
      var showRow = (mode === "fixed");
      document.querySelectorAll(".period-row-price").forEach(function (row) {
        row.style.display = showRow ? "table-row" : "none";
      });
    }

    function showContractOnlyMode() {
      var subDef = document.getElementById("subDefaultsSection");
      var hp = document.getElementById("hourlyPeriodsSection");
      if (subDef) subDef.style.display = "none";
      if (hp)    hp.style.display = "none";
    }

    function showFullSubcontractMode() {
      var subDef = document.getElementById("subDefaultsSection");
      var hp = document.getElementById("hourlyPeriodsSection");
      if (subDef) subDef.style.display = "";
      if (hp)    hp.style.display = "";
    }

    function addPeriodBlock() {
      const tpl = document.getElementById("periodTemplate");
      const container = document.getElementById("periodsContainer");
      if (!tpl || !container) return;

      const clone = tpl.content.firstElementChild.cloneNode(true);
      buildPeriodTableHours(clone);

      const removeBtn = clone.querySelector(".period-remove-btn");
      removeBtn.addEventListener("click", function() {
        container.removeChild(clone);
      });

      container.appendChild(clone);

      const marginEnabled = document.getElementById("nc_margin_enabled");
      updateMarginVisibility(marginEnabled && marginEnabled.checked);

      const qtySel   = document.getElementById("nc_qty_type");
      const priceSel = document.getElementById("nc_price_type");
      updateQuantityVisibility(qtySel ? qtySel.value : null);
      updatePriceVisibility(priceSel ? priceSel.value : null);
    }

    /* ================= LOAD COUNTRIES / CURRENCIES ====================== */

    function loadCountries() {
      const selCountry = document.getElementById("nc_country");
      if (!selCountry) return;
      while (selCountry.options.length > 1) {
        selCountry.remove(1);
      }
      fetch("countries", { credentials: "same-origin" })
        .then(function (resp) { return resp.json(); })
        .then(function (payload) {
          const rows = payload.rows || [];
          rows.forEach(function (r) {
            const opt = document.createElement("option");
            opt.value = String(r.code);
            opt.textContent = r.code + " - " + r.name;
            opt.dataset.id = String(r.id);
            selCountry.appendChild(opt);
          });
        })
        .catch(function (err) {
          console.error("Error loading countries:", err);
        });
    }

    function loadCurrencies() {
      fetch("currencies", { credentials: "same-origin" })
        .then(function (resp) { return resp.json(); })
        .then(function (payload) {
          var rows = payload.rows || payload;
          window.currencyByCode = {};
          var dropdownIds = ["nc_currency", "nc_index_ccy", "nc_margin_ccy"];
          dropdownIds.forEach(function (id) {
            var sel = document.getElementById(id);
            if (!sel) return;
            sel.innerHTML = '<option value="">-- select --</option>';
            rows.forEach(function (r) {
              var opt = document.createElement("option");
              opt.value = String(r.id);
              opt.textContent = r.code + (r.name ? " - " + r.name : "");
              sel.appendChild(opt);
              window.currencyByCode[r.code] = { id: r.id, code: r.code, name: r.name };
            });
          });
        })
        .catch(function (err) {
          console.error("Error loading currencies:", err);
        });
    }

    /* ================= MODAL HELPERS ==================================== */

    function setModalReadOnly(isReadOnly) {
      const backdrop = document.getElementById("newContractModal");
      if (!backdrop) return;
      const modal = backdrop.querySelector(".modal");
      if (!modal) return;

      const saveBtn   = document.getElementById("saveContractBtn");
      const cancelBtn = document.getElementById("cancelContractBtn");
      const closeBtn  = document.getElementById("modalCloseBtn");

      const controls = modal.querySelectorAll("input, select, textarea, button.period-date-btn, button.period-remove-btn, #addPeriodBtn");
      controls.forEach(function(el) {
        if (el === saveBtn || el === cancelBtn || el === closeBtn) return;
        el.disabled = !!isReadOnly;
      });

      if (saveBtn) {
        if (isReadOnly) {
          saveBtn.disabled = true;
          saveBtn.style.opacity = "0.5";
          saveBtn.style.pointerEvents = "none";
        } else {
          saveBtn.disabled = false;
          saveBtn.style.opacity = "";
          saveBtn.style.pointerEvents = "";
        }
      }
    }

    function resetModalForNewContract() {
      document.getElementById("modalTitle").textContent = "New contract";
      const saveBtn = document.getElementById("saveContractBtn");
      if (saveBtn) {
        saveBtn.textContent = "Save contract";
        saveBtn.dataset.mode = "create";
        saveBtn.dataset.subcontractId = "";
        saveBtn.dataset.contractId = "";
      }

      setModalReadOnly(false);
      showFullSubcontractMode();

      document.getElementById("nc_counterparty").value = "";
      document.getElementById("nc_contract_no").value = "";
      document.getElementById("nc_country").value = "";
      document.getElementById("nc_date_from").value = "";
      document.getElementById("nc_date_to").value = "";
      document.getElementById("nc_currency").value = "";
      document.getElementById("nc_notes").value = "";

      document.getElementById("nc_qty_type").value = "";
      document.getElementById("nc_price_type").value = "";
      document.getElementById("nc_index_type").value = "";
      document.getElementById("nc_index_ccy").value = "";
      document.getElementById("nc_index_enabled").checked = false;
      document.getElementById("nc_margin_enabled").checked = false;
      document.getElementById("nc_margin_ccy").value = "";

      document.getElementById("nc_border_side").value    = "";
      document.getElementById("nc_transport_side").value = "";
      document.getElementById("nc_import_side").value    = "";
      document.getElementById("nc_export_side").value    = "";

      updateMarginVisibility(false);
      updateIndexVisibility(false);
      updateQuantityVisibility("");
      updatePriceVisibility("");

      const container = document.getElementById("periodsContainer");
      container.innerHTML = "";
      addPeriodBlock();
    }

    function openNewContractModal() {
      resetModalForNewContract();
      document.getElementById("newContractModal").classList.remove("hidden");
    }

    function closeNewContractModal() {
      document.getElementById("newContractModal").classList.add("hidden");
      closeDateTimePopup();
    }

    function openEditContractModal(contractRow) {
      if (!contractRow) return;
      const modal = document.getElementById("newContractModal");
      if (!modal) return;

      setModalReadOnly(false);
      showContractOnlyMode();

      document.getElementById("modalTitle").textContent =
        "Edit contract " + (contractRow.contract_dealno || "");

      const saveBtn = document.getElementById("saveContractBtn");
      if (saveBtn) {
        saveBtn.textContent = "Update contract";
        saveBtn.dataset.mode = "updateContract";
        saveBtn.dataset.contractId = String(contractRow.contract_id || "");
        saveBtn.dataset.subcontractId = "";
      }

      document.getElementById("nc_counterparty").value =
        contractRow.contract_contragentid || "";
      document.getElementById("nc_contract_no").value =
        contractRow.contract_dealno || "";

      const ctrySel = document.getElementById("nc_country");
      if (ctrySel && contractRow.contract_country) {
        ctrySel.value = contractRow.contract_country;
      } else if (ctrySel) {
        ctrySel.value = "";
      }

      document.getElementById("nc_date_from").value =
        formatDateTimeForDisplay(contractRow.contract_date_from || "");
      document.getElementById("nc_date_to").value =
        formatDateTimeForDisplay(contractRow.contract_date_to || "");

      const ccySel = document.getElementById("nc_currency");
      if (ccySel && contractRow.contract_currencyid != null) {
        ccySel.value = String(contractRow.contract_currencyid);
      } else if (ccySel) {
        ccySel.value = "";
      }

      document.getElementById("nc_notes").value =
        contractRow.contract_notes || "";

      modal.classList.remove("hidden");
    }

    function openEditModalForSubcontract(contractRow, hourlyRows) {
      const modal = document.getElementById("newContractModal");
      if (!modal || !contractRow) return;

      setModalReadOnly(false);
      showFullSubcontractMode();

      const first = (hourlyRows && hourlyRows.length) ? hourlyRows[0] : null;

      var titleText = "Contract " + (contractRow.contract_dealno || "");
      if (first && first.subcontract_dealno) {
        titleText += " • Subcontract " + first.subcontract_dealno;
      }
      document.getElementById("modalTitle").textContent = titleText;

      const saveBtn = document.getElementById("saveContractBtn");
      if (saveBtn) {
        saveBtn.textContent = "Update subcontract";
        saveBtn.dataset.mode = "updateSubcontract";
        saveBtn.dataset.contractId = String(contractRow.contract_id || "");
        saveBtn.dataset.subcontractId = first ? String(first.subcontract_id || "") : "";
      }

      document.getElementById("nc_counterparty").value = contractRow.contract_contragentid || "";
      document.getElementById("nc_contract_no").value  = contractRow.contract_dealno       || "";

      const ctrySel = document.getElementById("nc_country");
      if (ctrySel && contractRow.contract_country) {
        ctrySel.value = contractRow.contract_country;
      } else if (ctrySel) {
        ctrySel.value = "";
      }

      document.getElementById("nc_date_from").value =
        formatDateTimeForDisplay(contractRow.contract_date_from || "");
      document.getElementById("nc_date_to").value =
        formatDateTimeForDisplay(contractRow.contract_date_to   || "");

      if (contractRow.contract_currencyid != null) {
        document.getElementById("nc_currency").value = String(contractRow.contract_currencyid);
      } else {
        document.getElementById("nc_currency").value = "";
      }

      document.getElementById("nc_notes").value = contractRow.contract_notes || "";

      const qtySel      = document.getElementById("nc_qty_type");
      const priceSel    = document.getElementById("nc_price_type");
      const idxType     = document.getElementById("nc_index_type");
      const idxCcy      = document.getElementById("nc_index_ccy");
      const idxChk      = document.getElementById("nc_index_enabled");
      const marginChk   = document.getElementById("nc_margin_enabled");
      const marginCcy   = document.getElementById("nc_margin_ccy");
      const borderSide  = document.getElementById("nc_border_side");
      const transpSide  = document.getElementById("nc_transport_side");
      const importSide  = document.getElementById("nc_import_side");
      const exportSide  = document.getElementById("nc_export_side");

      if (first) {
        var qType = first.subcontract_quantity_type || "";
        if (qType === "none") qType = "variable";
        qtySel.value = qType;

        var pType = first.subcontract_price_type || "";
        if (pType === "none") pType = "variable";
        priceSel.value = pType;

        if (first.subcontract_index_type) {
          idxChk.checked = true;
          var ixVal = String(first.subcontract_index_type).trim();
          idxType.value = ixVal;
        } else {
          idxChk.checked = false;
          idxType.value = "";
        }

        if (
          first.subcontract_index_currency &&
          window.currencyByCode[first.subcontract_index_currency]
        ) {
          idxCcy.value =
            String(window.currencyByCode[first.subcontract_index_currency].id);
        } else {
          idxCcy.value = "";
        }

        borderSide.value = decodeSide(first.subcontract_border_costs);
        transpSide.value = decodeSide(first.subcontract_transport_costs);
        importSide.value = decodeSide(first.subcontract_import_costs);
        exportSide.value = decodeSide(first.subcontract_export_costs);
      } else {
        qtySel.value   = "";
        priceSel.value = "";
        idxType.value  = "";
        idxCcy.value   = "";
        idxChk.checked = false;
        borderSide.value = "";
        transpSide.value = "";
        importSide.value = "";
        exportSide.value = "";
      }

      let hasMargin = false;
      (hourlyRows || []).forEach(function(r) {
        if (r.subcontract_margin !== undefined &&
            r.subcontract_margin !== null &&
            r.subcontract_margin !== "") {
          hasMargin = true;
        }
        if (r.subcontract_margin_currency) {
          hasMargin = true;
        }
      });
      marginChk.checked = hasMargin;

      if (first && first.subcontract_margin_currency &&
          window.currencyByCode[first.subcontract_margin_currency]) {
        marginCcy.value =
          String(window.currencyByCode[first.subcontract_margin_currency].id);
      } else {
        marginCcy.value = "";
      }

      const container = document.getElementById("periodsContainer");
      container.innerHTML = "";

      if (!hourlyRows || !hourlyRows.length) {
        addPeriodBlock();
      } else {
        const byDate = {};
        hourlyRows.forEach(function(r) {
          const key = trimDate(
            r.subcontract_slot_date ||
            r.subcontract_datetime_from ||
            contractRow.contract_date_from
          );
          if (!byDate[key]) byDate[key] = [];
          byDate[key].push(r);
        });

        Object.keys(byDate).sort().forEach(function(dateKey) {
          const tpl  = document.getElementById("periodTemplate");
          const card = tpl.content.firstElementChild.cloneNode(true);
          buildPeriodTableHours(card);

          const rowsForDate = byDate[dateKey];

          let minFrom = null;
          let maxTo   = null;

          rowsForDate.forEach(function(r) {
            const hInt = parseInt(r.subcontract_slot_hour, 10);
            if (!hInt || hInt < 1 || hInt > 24) return;
            const hh = String(hInt).padStart(2, "0");

            const qtyVal    = (r.subcontract_quantity_kwh != null) ? r.subcontract_quantity_kwh : "";
            const priceVal  = (r.subcontract_price_mwh   != null) ? r.subcontract_price_mwh     : "";
            const marginVal = (r.subcontract_margin      != null) ? r.subcontract_margin        : "";

            const qInput = card.querySelector('input.period-input[data-field="qty"][data-hour="' + hh + '"]');
            if (qInput) qInput.value = qtyVal;

            const pInput = card.querySelector('input.period-input[data-field="price"][data-hour="' + hh + '"]');
            if (pInput) pInput.value = priceVal;

            const mInput = card.querySelector('input.period-input[data-field="margin"][data-hour="' + hh + '"]');
            if (mInput) mInput.value = marginVal;

            if (r.subcontract_datetime_from) {
              const df = new Date(r.subcontract_datetime_from);
              if (!isNaN(df.getTime())) {
                if (!minFrom || df < minFrom) minFrom = df;
              }
            }
            if (r.subcontract_datetime_to) {
              const dt = new Date(r.subcontract_datetime_to);
              if (!isNaN(dt.getTime())) {
                if (!maxTo || dt > maxTo) maxTo = dt;
              }
            }
          });

          const startEl = card.querySelector(".period-start");
          const endEl   = card.querySelector(".period-end");

          if (startEl) {
            startEl.value = minFrom ? formatDateTimeForDisplay(minFrom) : dateKey;
          }
          if (endEl) {
            endEl.value   = maxTo   ? formatDateTimeForDisplay(maxTo)   : dateKey;
          }

          const removeBtn = card.querySelector(".period-remove-btn");
          removeBtn.addEventListener("click", function() {
            container.removeChild(card);
          });

          container.appendChild(card);
        });
      }

      updateMarginVisibility(marginChk.checked);
      updateIndexVisibility(document.getElementById("nc_index_enabled").checked);
      updateQuantityVisibility(qtySel.value);
      updatePriceVisibility(priceSel.value);

      modal.classList.remove("hidden");
    }

    function openViewModalForSubcontract(contractRow, hourlyRows) {
      openEditModalForSubcontract(contractRow, hourlyRows);

      const titleEl = document.getElementById("modalTitle");
      if (titleEl) {
        titleEl.textContent = "View subcontract - " + titleEl.textContent;
      }

      const saveBtn = document.getElementById("saveContractBtn");
      if (saveBtn) {
        saveBtn.dataset.mode = "viewSubcontract";
      }

      setModalReadOnly(true);
    }

    /* ================= DOM READY ======================================= */

    document.addEventListener("DOMContentLoaded", function() {
      const gridDiv = document.getElementById("grid");
      gridApi = agGrid.createGrid(gridDiv, gridOptions);

      loadCurrencies();
      loadCountries();

      const statusFilter   = document.getElementById("statusFilter");
      const contractFilter = document.getElementById("contractFilter");
      const searchInput    = document.getElementById("contractSearch");
      const newBtn         = document.getElementById("newContractBtn");
      const modalCloseBtn  = document.getElementById("modalCloseBtn");
      const cancelBtn      = document.getElementById("cancelContractBtn");
      const addPeriodBtn   = document.getElementById("addPeriodBtn");
      const saveBtn        = document.getElementById("saveContractBtn");
      const marginEnabled  = document.getElementById("nc_margin_enabled");
      const indexEnabled   = document.getElementById("nc_index_enabled");
      const qtyTypeSel     = document.getElementById("nc_qty_type");
      const priceTypeSel   = document.getElementById("nc_price_type");

      if (statusFilter)   statusFilter.addEventListener("change", applyToolbarFilters);
      if (contractFilter) contractFilter.addEventListener("change", applyToolbarFilters);
      if (searchInput)    searchInput.addEventListener("input",  applyToolbarFilters);

      if (newBtn)        newBtn.addEventListener("click", openNewContractModal);
      if (modalCloseBtn) modalCloseBtn.addEventListener("click", closeNewContractModal);
      if (cancelBtn)     cancelBtn.addEventListener("click", closeNewContractModal);
      if (addPeriodBtn)  addPeriodBtn.addEventListener("click", addPeriodBlock);

      if (saveBtn) {
        saveBtn.addEventListener("click", function () {
          const mode       = saveBtn.dataset.mode || "create";
          const subId      = saveBtn.dataset.subcontractId || "";
          const contractId = saveBtn.dataset.contractId || "";

          if (mode === "create") {
            alert("TODO: CREATE new contract (call /save endpoint).");
          } else if (mode === "createSubcontract") {
            alert("TODO: CREATE new subcontract for contract " + contractId + " (call /save endpoint).");
          } else if (mode === "updateContract") {
            alert("TODO: UPDATE contract " + contractId + " (call /save endpoint for contracts).");
          } else if (mode === "updateSubcontract") {
            alert("TODO: UPDATE subcontract " + subId + " (call /update endpoint for hourly data).");
          } else if (mode === "viewSubcontract") {
            // read-only
          } else {
            alert("Unknown save mode: " + mode);
          }
        });
      }

      if (marginEnabled) {
        marginEnabled.addEventListener("change", function() {
          updateMarginVisibility(this.checked);
        });
        updateMarginVisibility(marginEnabled.checked);
      }

      if (indexEnabled) {
        indexEnabled.addEventListener("change", function() {
          updateIndexVisibility(this.checked);
        });
        updateIndexVisibility(indexEnabled.checked);
      }

      if (qtyTypeSel) {
        qtyTypeSel.addEventListener("change", function () {
          if (this.value === "none") this.value = "variable";
          updateQuantityVisibility(this.value);
        });
      }

      if (priceTypeSel) {
        priceTypeSel.addEventListener("change", function () {
          if (this.value === "none") this.value = "variable";
          updatePriceVisibility(this.value);
        });
      }

      document.addEventListener("keydown", function (ev) {
        if (ev.key === "Escape") {
          closeNewContractModal();
          return;
        }

        if (ev.key === "Enter") {
          var input = ev.target;
          if (!input.classList || !input.classList.contains("period-input")) {
            return;
          }

          ev.preventDefault();

          var td = input.closest("td");
          if (!td) return;

          var nextTd = td.nextElementSibling;
          if (!nextTd) return;

          var nextInput = nextTd.querySelector(".period-input");
          if (nextInput) {
            nextInput.focus();
            nextInput.select();
          }
        }
      });

      const contractId = getContractIdFromUrl();
      let dataUrl = "data";

      if (contractId > 0) {
        dataUrl += "?contract_id=" + encodeURIComponent(contractId);
        setStatus("Loading contract " + contractId + "…");
      } else {
        setStatus("Loading all contracts…");
      }

      fetch(dataUrl, { credentials: "same-origin" })
        .then(function (resp) { return resp.json(); })
        .then(function (payload) {
          const rows = Array.isArray(payload)
            ? payload
            : (payload.rows || []);

          window.contractRows = rows || [];

          if (!rows.length) {
            if (contractId > 0) {
              setStatus("No data for contract " + contractId);
            } else {
              setStatus("No contracts found");
            }
            if (gridApi) {
              gridApi.setGridOption("rowData", []);
            }
            return;
          }

          if (gridApi) {
            gridApi.setGridOption("rowData", rows);
          }

          populateContractFilter(rows);
          applyToolbarFilters();

          if (contractId > 0) {
            const subCount = rows[0].subcontracts
              ? rows[0].subcontracts.length
              : 0;
            setStatus("Contract " + contractId + " • " + subCount + " subcontracts");
          } else {
            setStatus("Loaded " + rows.length + " contracts");
          }
        })
        .catch(function (err) {
          console.error(err);
          if (contractId > 0) {
            setStatus("Error loading contract " + contractId);
          } else {
            setStatus("Error loading contracts");
          }
        });
    });
  </script>
</body>
</html>
"""
    return {"html": html}