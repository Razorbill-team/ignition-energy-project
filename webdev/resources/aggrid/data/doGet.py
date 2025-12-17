def doGet(request, session):

	import system
	from datetime import datetime
	from java.text import SimpleDateFormat
	from java.util import TimeZone
	try:
		from java.sql import Timestamp as JTimestamp
		from java.util import Date as JDate
	except:
		JTimestamp = None
		JDate = None

	LOG = system.util.getLogger("WebDev.AgGrid.Data")
	
	# ---------- helpers ----------
	def to_dt(x):
		"""Convert java.sql.Timestamp / java.util.Date / epoch (ms or sec) / common strings -> Python datetime or None."""
		if x is None:
			return None
		# Java Date/Timestamp?
		try:
			if (JTimestamp and isinstance(x, JTimestamp)) or (JDate and isinstance(x, JDate)):
				return datetime.fromtimestamp(x.getTime() / 1000.0)
		except:
			pass
		# Numeric epoch? try ms then sec
		try:
			fx = float(x)
			if fx > 1e11:  # treat as ms
				return datetime.fromtimestamp(fx / 1000.0)
			return datetime.fromtimestamp(fx)  # seconds
		except:
			pass
		# Strings: try a few formats
		s = str(x).strip()
		for fmt in ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M", "%d-%m-%Y", "%Y/%m/%d %H:%M:%S"):
			try:
				return datetime.strptime(s, fmt)
			except:
				continue
		return None

	# ---------- 1) Read params ----------
	p = request.get("params", {}) or {}
	date_from_in = p.get("date_from", "")     # e.g. 20250909080000
	date_to_in   = p.get("date_to", "")       # e.g. 20250909200000
	farms_in     = p.get("farms", "")         # "1,24" or [1,24]

	# ---------- 2) Reformat dates to SQL 'yyyy-MM-dd HH:mm:ss' ----------
	TZ = TimeZone.getTimeZone("Europe/Chisinau")
	IN_FMT  = SimpleDateFormat("yyyyMMddHHmmss"); IN_FMT.setTimeZone(TZ)
	OUT_SQL = SimpleDateFormat("yyyy-MM-dd HH:mm:ss"); OUT_SQL.setTimeZone(TZ)
	# If you want ISO instead, define OUT_ISO and use it in reformat.

	def reformat(s, out_fmt):
		if not s:
			return ""
		try:
			d = IN_FMT.parse(s)
			return out_fmt.format(d)
		except:
			return s  # leave as-is if already formatted

	date_from = reformat(date_from_in, OUT_SQL)
	date_to   = reformat(date_to_in,   OUT_SQL)

	# Keep farms as string if your NQ expects "1,24".
	# Convert to list ONLY if your NQ param type is List<Integer>.
	farms_param = farms_in
	# Example conversion (uncomment if needed):
	# try:
	#     if isinstance(farms_in, basestring):
	#         farms_param = [int(x) for x in farms_in.split(",") if x.strip().isdigit()]
	#     elif isinstance(farms_in, (list, tuple)):
	#         farms_param = [int(x) for x in farms_in]
	#     else:
	#         farms_param = []
	# except:
	#     farms_param = []

	# ---------- 3) Run Named Query ----------
	params = {
		"date_from":     date_from,
		"date_to":       date_to,
		"param_farmids": farms_param,
	}

	try:
		ds = system.db.runNamedQuery("Reports/ForecastTable", params)
	except Exception as ex:
		LOG.error("NamedQuery failed: %r" % ex)
		return {"json": [], "error": "NamedQuery error: %s" % ex}

	# ---------- 4) Dataset -> list[dict] ----------
	try:
		pds  = system.dataset.toPyDataSet(ds)
		cols = list(pds.getColumnNames())
		data = [{c: r[c] for c in cols} for r in pds]
	except Exception as ex:
		LOG.error("Dataset conversion failed: %r" % ex)
		return {"json": [], "error": "Dataset conversion error: %s" % ex}

	if not data:
		return {"json": []}

	# ---------- 5) Build ordered slot (column) list ----------
	slot_dt_set = set()
	for row in data:
		dt = to_dt(row.get("slot_ts"))
		if dt:
			slot_dt_set.add(dt)
	slot_dt_list = sorted(slot_dt_set)
	slot_columns_full = [dt.strftime("%d-%m-%Y %H:%M") for dt in slot_dt_list]

	# ---------- 6) Bucket rows (date, site, farm, status, source) ----------
	buckets = {}  # key -> {"siteid":..,"farmid":.., "<dd-mm-YYYY HH:MM>": value, ...}
	for row in data:
		siteid      = row.get("siteid")
		farmid      = row.get("farmid")
		site_name   = row.get("site_name")
		farm_name   = row.get("farm_name")
		status_name = row.get("status_name")
		id_source   = row.get("id_source")

		date_dt   = to_dt(row.get("date"))
		date_label = date_dt.strftime("%d-%m-%Y") if date_dt else str(row.get("date") or "")
		
		slot_dt   = to_dt(row.get("slot_ts"))
		slot_label = slot_dt.strftime("%d-%m-%Y %H:%M") if slot_dt else str(row.get("slot_ts") or "")
		
		# Sources 1..3
		if id_source in (1, 2, 3):
			source_name = "Source_" + str(int(id_source))
			key = (date_label, site_name, farm_name, status_name, source_name)
			b = buckets.get(key)
			if b is None:
				b = buckets[key] = {"siteid": siteid, "farmid": farmid}
			b[slot_label] = row.get("forecasted_power_kw")

		# Synthetic rows
		for sname, scol in [
			("AVG_Sources",       "avg_sources"),
			("Manual_correction", "manual_correction"),
			("Auto_correction",   "auto_correction"),
			("Final_Forecast",    "final_forecast")
		]:
			key = (date_label, site_name, farm_name, status_name, sname)
			b = buckets.get(key)
			if b is None:
				b = buckets[key] = {"siteid": siteid, "farmid": farmid}
			b[slot_label] = row.get(scol)

	# ---------- 7) Build output rows (dicts) ----------
	out_rows = []
	for (date_s, site_name, farm_name, status_name, source_name), slotmap in buckets.items():
		row_obj = {
			"date": date_s,
			"site_name": site_name,
			"farm_name": farm_name,
			"status_name": status_name,
			"Source_name": str(source_name).lower(),  # match your sorting map
			"siteid": slotmap.get("siteid"),
			"farmid": slotmap.get("farmid")
		}
		for col in slot_columns_full:
			v = slotmap.get(col, None)
			try:
				v = 0 if v is None else int(float(v))
			except:
				v = 0
			row_obj[col] = v
		out_rows.append(row_obj)

	# ---------- 8) Sort ----------
	source_order = {
		"source_1": 1,
		"source_2": 2,
		"source_3": 3,
		"avg_sources": 4,
		"auto_correction": 5,
		"manual_correction": 6,
		"final_forecast": 7}
	out_rows.sort(key=lambda r: (
		str(r.get("site_name","")),
		str(r.get("farm_name","")),
		source_order.get(str(r.get("Source_name","")).lower(), 999)
	))

	# ---------- 9) Optional: duplicate full datetime columns as HH:MM ----------
	# If you want keys "HH:MM" instead of "dd-mm-YYYY HH:MM", we copy them:
	hhmm_map = {full: (full.split(" ")[1] if " " in full else full) for full in slot_columns_full}
	final_rows = []
	for r in out_rows:
		rr = dict(r)
		for full, short in hhmm_map.items():
			if full in rr and short not in rr:
				rr[short] = rr.pop(full)
		final_rows.append(rr)
		 # ---------- 10) Sort rows and keep ONLY ONE total_general at top ----------
	
	# remove any existing total_general rows that may have come from upstream
	body_rows = [r for r in final_rows
	             if str(r.get("Source_name", "")).lower() != "total_general"]
	
	# sort by site_name, then farm_name, then by custom Source_name order
	def none_last_key(v):
		try:
			s = str(v)
		except:
			s = ""
		# (None or empty last) then case-insensitive string for stable order
		return (v is None or s.strip() == "", s)
	
	def src_rank(v):
		try:
			s = str(v).lower()
		except:
			s = ""
		return {
			"source_1": 1,
			"source_2": 2,
			"source_3": 3,
			"avg_sources": 4,
			"auto_correction": 5,
			"manual_correction": 6,
			"final_forecast": 7,
		}.get(s, 999)
	
	body_rows.sort(key=lambda r: (
		none_last_key(r.get("site_name")),
		none_last_key(r.get("farm_name")),
		src_rank(r.get("Source_name"))
	))
	
	# build the ordered HH:MM list from slot_dt_list (already computed)
	hhmm_headers = [dt.strftime("%H:%M") for dt in slot_dt_list]
	
	# sum FINAL_FORECAST across all rows for the grand total first row
	sums = dict((h, 0.0) for h in hhmm_headers)
	for r in body_rows:
		if str(r.get("Source_name", "")).lower() == "final_forecast":
			for h in hhmm_headers:
				v = r.get(h)
				if v is None:
					continue
				try:
					sums[h] += float(v)
				except:
					try:
						sums[h] += float(str(v).replace(",", "."))
					except:
						pass
	
	# create the single total_general row and PREPEND it
	total_row = {
		"date": "",
		"site_name": "",
		"farm_name": "",
		"status_name": "",
		"Source_name": "total_general",
		"siteid": None,
		"farmid": None,
	}
	for h in hhmm_headers:
		total_row[h] = sums[h]
	
	final_rows = [total_row] + body_rows
	return {"json": final_rows}