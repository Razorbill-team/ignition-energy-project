def doGet(request, session):
	import system, traceback
	from java.text import SimpleDateFormat
	from java.util import TimeZone
	from java.text import SimpleDateFormat
	
	sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssXXX")  # <-- adds +03:00 / +02:00
	sdf.setTimeZone(TimeZone.getTimeZone("Europe/Chisinau"))
	
	def to_iso(dt):
		if dt is None:
			return None
		try:
			return sdf.format(dt)
		except:
			return str(dt)
			
	try:
		# 1) Get farms from query params
		farms_param = request["params"]  # dict with 'farms'
		today_str = system.date.format(system.date.now(), "yyyy-MM-dd")
		# 2) Run your named query (unchanged)
		results = system.db.runNamedQuery("events_table", {"farm_id_list": farms_param["farms"], "today_date": today_str})
		
		# 3) Build resources + events (unchanged field access)
		resources_map = {}   # farmid -> {"id": "...", "name": "..."}
		events = []
		for i, r in enumerate(results):
			farmid = r["farmid"]
			farm_name = r["farm_name"]
			setpoint_log_id = r["setpoint_log_id"]
			setpoint_name = r["setpoint_name"]
			setpointid = r["setpointid"]
			
			if str(farmid) + '_' + str(setpointid) not in resources_map:
				resources_map[str(farmid) + '_' + str(setpointid)] = {"id": str(farmid) + '_' + str(setpointid), "name": farm_name + ' ' + setpoint_name}
				
			ev_id = r["setpoint_log_id"]
			#if ev_id is None or ev_id == "":
			#	ev_id = "%s_%s_%s" % (r["setpointid"], r["farmid"], i)
				
			start_iso = to_iso(r["action_from"])  # now includes +03:00 (or +02:00 in winter)
			end_iso   = to_iso(r["action_to"])
			
			if not start_iso or not end_iso:
				continue
				
			events.append({
				"id": str(ev_id),
				"text": r["setpoint_value"],
				"start": start_iso,
				"end": end_iso,
				"resource": str(farmid) + '_' + str(setpointid) if farmid is not None or setpointid is not None else "unassigned"
				
			})
			
		resources = resources_map.values()
		resources_json = system.util.jsonEncode(list(resources))
		events_json = system.util.jsonEncode(events)
		
		#return {'json': resources_json}
		# 4) HTML/JS (red overlay line; no cell highlight)
		html = """
		<!DOCTYPE html>
		<html>
		<head>
		  <meta charset="utf-8">
		  <title>Scheduler</title>
		  <script src="http://localhost:8088/system/webdev/DemoVersion_16_09_2025_Final/test_calendar/daypilot-all_min.js"></script>
		  <style>
		    /* Reserve space for overlay scrollbars inside the grid */
			  .scheduler_default_scrollable,
			  .scheduler_white_scrollable,
			  .scheduler_blue_scrollable,
			  .scheduler_transparent_scrollable {
			    padding-bottom: 10px !important;
			    box-sizing: content-box;
			    scrollbar-gutter: stable both-edges; /* where supported */
			  }
			/* Wrap text inside event boxes (default is nowrap) */
				.scheduler_default_event_inner,
				.scheduler_white_event_inner,
				.scheduler_blue_event_inner {
				  white-space: normal !important;
				  line-height: 1.2;
				}
				
				/* Wrap resource names in the left header if they’re long */
				.scheduler_default_rowheader_inner,
				.scheduler_white_rowheader_inner,
				.scheduler_blue_rowheader_inner {
				  white-space: normal !important;
				  line-height: 1.2;
				}
		    html, body { height: 100%; margin: 0; }
		    #scheduler   { width: 100%; height: 100%; }
		  </style>
		</head>
		<body>
		  <div id="scheduler"></div>
			<script>
				document.addEventListener("DOMContentLoaded", function () {
				  var dp = new DayPilot.Scheduler("scheduler");
				
				  // timeline: today + tomorrow, 15-min grid, full 24h
				  dp.startDate = DayPilot.Date.today();
				  dp.days = 2;
				  dp.scale = "CellDuration";
				  dp.cellDuration = 15;
				  dp.timeHeaders = [
				    { groupBy: "Day",  format: "dddd MMM d" },
				    { groupBy: "Hour", format: "HH" },
				    { groupBy: "Cell", format: "mm" }
				  ];
				  dp.businessBeginsHour = 0;
				  dp.businessEndsHour   = 24;
				  dp.showNonBusiness    = true;
				  dp.eventSnapToGrid    = true;
				  dp.cellWidth          = 40;
				  dp.eventHeight        = 22;
				  dp.rowHeaderWidth     = 140;   // adjust if your left header differs
				  dp.eventHeight   = 40;   // give space for 2 wrapped lines (try 48–60 for more)
				  dp.rowMinHeight  = 40;   // row must be tall enough for wrapped text
				  dp.rowHeaderWidth = 220;
				
				  // lanes + events injected by server (strings like 2025-09-05T07:30:00+03:00)
				  dp.resources   = __RESOURCES__;
				  dp.events.list = __EVENTS__;
				
				  // ---- TZ NORMALIZE (local wall-clock) + COMPENSATE (LibreWolf) ----
				  (function tzNormalizeAndCompensate(dp){
				    if (!dp.events.list || !dp.events.list.length) return;
				
				    function pad(n){ return (n<10?'0':'') + n; }
				
				    // Convert an ISO string (with offset) into a *local, no-offset* DayPilot.Date
				    function toLocalNoOffsetDP(iso){
				      // JS Date respects the offset in the string
				      var d = new Date(String(iso));
				      var s = d.getFullYear() + "-" + pad(d.getMonth()+1) + "-" + pad(d.getDate()) +
				              "T" + pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds());
				      // No offset in 's' => DayPilot treats it as local wall-clock
				      return new DayPilot.Date(s);
				    }
				
				    function offsetMinutesFromIso(s){
				      s = String(s);
				      if (s.endsWith("Z")) return 0;
				      var m = s.match(/([+-])(\d{2}):(\d{2})$/); // +HH:MM / -HH:MM
				      if (!m) return null;
				      var sign = m[1] === '-' ? -1 : 1;
				      return sign*(parseInt(m[2],10)*60 + parseInt(m[3],10));
				    }
				
				    var first = dp.events.list[0];
				    var evOff = offsetMinutesFromIso(first.start);         // e.g., +180 if +03:00
				    var browserOff = - new Date().getTimezoneOffset();     // +180 in MD, 0 in LibreWolf (UTC spoof)
				    if (evOff == null) evOff = browserOff;                 // if server ever sent no offset
				
				    var delta = evOff - browserOff;                        // Firefox: 0; LibreWolf: +180
				    console.log("TZ normalize: evOff=",evOff," browserOff=",browserOff," delta=",delta);
				
				    // Normalize all event times to local, no-offset; then apply delta if spoofed
				    dp.events.list = dp.events.list.map(function(e){
				      var s  = toLocalNoOffsetDP(e.start);
				      var en = toLocalNoOffsetDP(e.end);
				      if (delta) { s = s.addMinutes(delta); en = en.addMinutes(delta); }
				      return { id: e.id, text: e.text, resource: e.resource, start: s, end: en };
				    });
				
				    // Shift the timeline start as well so day boundaries match in spoofed browsers
				    if (delta) {
				      dp.startDate = dp.startDate.addMinutes(delta);
				    }
				
				    // Provide adjusted "now" for the red line below
				    window.__nowDP = function(){ 
				      var n = DayPilot.Date.now();
				      return delta ? n.addMinutes(delta) : n;
				    };
				  })(dp);
				  // -----------------------------------------------------------------
				
				  dp.init();
				  dp.scrollTo(window.__nowDP ? window.__nowDP() : DayPilot.Date.now());
				
				  // --- RED "NOW" LINE OVERLAY (uses adjusted now) ---
				  (function setupNowLine(){
				    var host = document.getElementById("scheduler");
				    host.style.position = "relative";
				
				    var line = document.createElement("div");
				    line.style.position = "absolute";
				    line.style.width = "2px";
				    line.style.background = "#e74c3c";
				    line.style.pointerEvents = "none";
				    line.style.zIndex = "9999";
				    host.appendChild(line);
				
				    function q(sel){ return host.querySelector(sel); }
				    var scrollEl = q('.scheduler_default_scrollable') || q('[class*="scrollable"]') || host;
				    var headerEl = q('.scheduler_default_timeheader') || q('[class*="timeheader"]');
				    function headerH(){ return headerEl ? headerEl.offsetHeight : 0; }
				    function minutesBetween(a,b){ return (b.getTime() - a.getTime())/60000; }
				
				    function update(){
				      var nowJs = (window.__nowDP ? window.__nowDP() : DayPilot.Date.now()).toDate();
				      var startJs = dp.startDate.toDate();
				      var mins = minutesBetween(startJs, nowJs);
				      var px = (mins / dp.cellDuration) * dp.cellWidth;
				      var left = Math.round(dp.rowHeaderWidth + px - (scrollEl.scrollLeft || 0));
				      var top = headerH();
				      line.style.top = top + "px";
				      line.style.height = Math.max(0, host.clientHeight - top) + "px";
				      line.style.left = left + "px";
				      line.style.display = (left >= 0 && left <= host.clientWidth) ? "block" : "none";
				    }
				    scrollEl.addEventListener("scroll", update);
				    window.addEventListener("resize", update);
				    update();
				    setInterval(update, 1000);
				  })();
				  // -------------------------------------------------
				});
				</script>
		</body>
		</html>
		""".replace('__EVENTS__', events_json).replace('__RESOURCES__', resources_json)
		return {"contentType": "text/html", "html": html}
	except Exception:
		tb = traceback.format_exc()
		system.util.getLogger("webdev.scheduler").error(tb)
		return {"contentType": "text/html", "html": "<pre style='white-space:pre-wrap'>" + tb + "</pre>"}