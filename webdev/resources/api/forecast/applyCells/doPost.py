def doPost(request, session):
	import system, re, traceback
	log = system.util.getLogger("applyCells")
	
	USER_ID = 1001
	TIME_RE = re.compile(r"^\d{2}:\d{2}$")
	
	def ok(obj, code=200): return {"status": code, "json": obj}
	
	def to_iso_date(d):
	    if not d: return ""
	    d = d.strip()
	    if len(d)==10 and d[4]=='-' and d[7]=='-': return d
	    if len(d)==10 and d[2]=='-' and d[5]=='-':
	        dd,mm,yyyy = d.split('-'); return "%s-%s-%s"%(yyyy,mm,dd)
	    return d
	
	def slot_ts(date_iso, hhmm): return "%s %s:00"%(date_iso, hhmm)
	
	def time_fields(row):
	    # Fallback only (kept for backward compatibility)
	    return sorted([k for k in row.keys() if TIME_RE.match(str(k))])
	
	def to_num(x):
	    if x is None: return None
	    s = str(x).replace(u"\u00A0", u"").replace(" ", "").replace(",", ".").strip()
	    if s in ("","null","NULL"): return None
	    try: return float(s)
	    except: return None
	
	# source -> named query
	NQ = {
	    "avg_sources":     "Forecast/UpsertAvgSources",
	    "auto_correction": "Forecast/UpsertAutoCorrection",
	    "final_forecast":  "Forecast/UpsertFinalForecast",
	}
	
	try:
	    raw = request.get("body") or request.get("data") or ""
	    try:
	        payload = raw if isinstance(raw, (dict, list)) else system.util.jsonDecode(str(raw))
	    except Exception as ex:
	        log.error("JSON decode failed: %s | raw type=%s"%(ex, type(raw)))
	        return ok({"ok": False, "msg": "Invalid JSON", "detail": str(ex)}, 400)
	
	    edits = payload.get("edits") or []
	    rows  = payload.get("rows")  or payload.get("allRows") or []
	    timeCols = payload.get("timeCols") or []   # <<< NEW
	
	    # normalize/validate timeCols once
	    if timeCols:
	        # ensure strings, and (optionally) validate HH:mm
	        timeCols = [str(c) for c in timeCols if isinstance(c, (str, unicode))]  # Jython unicode
	        # no sorting here; the client already provided the final order
	
	    log.info("applyCells: edits=%d rows=%d timeCols=%d"%(len(edits), len(rows), len(timeCols)))
	
	    # ---------- transaction wrapper stays the same ----------
	    tx = system.db.beginTransaction(timeout=120000)
	    try:
	        # manual edits
	        saved_m = skipped_m = 0
	        errors_m = []
	        for i, e in enumerate(edits):
	            try:
	                siteid  = int(e.get("siteid", 0))
	                farmid  = int(e.get("farmid", 0))
	                dateISO = to_iso_date(e.get("date", "") or "")
	                hhmm    = (e.get("field", "") or "").strip()
	                v       = float(e.get("value"))
	                if not dateISO or not hhmm: raise ValueError("Missing date/field")
	                p = {
	                    "p_slot_ts": slot_ts(dateISO, hhmm),
	                    "p_siteid":  siteid,
	                    "p_farmid":  farmid,
	                    "p_value":   v,
	                    "p_userid":  USER_ID,
	                }
	                system.db.runNamedQuery("Forecast/UpsertManualCorrection", p, tx)
	                saved_m += 1
	            except Exception as ex:
	                skipped_m += 1
	                errors_m.append("manual #%d: %s | %r"%(i, ex, e))
	
	        # computed rows
	        saved_c = skipped_c = 0
	        errors_c = []
	        for idx, r in enumerate(rows):
	            try:
	                src = (r.get("Source_name") or "").strip().lower()
	                nq  = NQ.get(src)
	                if not nq:
	                    continue
	                dateISO = to_iso_date(r.get("date","") or "")
	                siteid  = int(r.get("siteid",0))
	                farmid  = int(r.get("farmid",0))
	                if not dateISO:
	                    skipped_c += 1; errors_c.append("row #%d invalid date"%idx); continue
	
	                # <<< NEW: iterate provided timeCols if present; fallback to regex otherwise
	                cols = timeCols if timeCols else time_fields(r)
	
	                for hhmm in cols:
	                    val = to_num(r.get(hhmm))
	                    if val is None:  # keep zeros; skip only null/empty
	                        continue
	                    p = {
	                        "p_slot_ts": slot_ts(dateISO, hhmm),
	                        "p_siteid":  siteid,
	                        "p_farmid":  farmid,
	                        "p_value":   val,
	                        "p_userid":  USER_ID,
	                    }
	                    system.db.runNamedQuery(nq, p, tx)
	                    saved_c += 1
	            except Exception as exr:
	                skipped_c += 1
	                errors_c.append("row #%d: %s | %r"%(idx, exr, r))
	
	        system.db.commitTransaction(tx)
	
	        return ok({
	            "ok": True,
	            "received_edits": len(edits),
	            "received_rows": len(rows),
	            "saved_manual":  saved_m,
	            "skipped_manual": skipped_m,
	            "saved_calc":    saved_c,
	            "skipped_calc":  skipped_c,
	            "errors_manual": errors_m,
	            "errors_calc":   errors_c
	        }, 200)
	
	    except:
	        system.db.rollbackTransaction(tx)
	        raise
	    finally:
	        system.db.closeTransaction(tx)
	
	except Exception as ex:
	    log.error("applyCells crashed: %s"%ex)
	    log.error(traceback.format_exc())
	    return ok({"ok": False, "msg": "applyCells crashed", "detail": str(ex)}, 200)