#!/usr/bin/env python3
"""Fill finals (and first-half scores for 1H picks) for a locked week.
Usage: ODDS_API_KEY=... python3 tools/update_scores.py WEEK
Prints the games finalized; writes the raw responses to data/raw."""
import json, sys, os, datetime, urllib.request, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
wk = int(sys.argv[1]); key = os.environ["ODDS_API_KEY"]
now = datetime.datetime.now(datetime.timezone.utc)
F = now.strftime("%Y-%m-%dT%H:%M:%SZ"); T = now.strftime("%m%d-%H%M")
get = lambda u: json.load(urllib.request.urlopen(u, timeout=30))
sc = {sp: get(f"https://api.the-odds-api.com/v4/sports/{sp}/scores/?daysFrom=3&apiKey={key}")
      for sp in ["americanfootball_nfl", "americanfootball_ncaaf"]}
p = root/f"data/weeks/2026-w{wk:02d}.json"; w = json.load(open(p))
if w["status"] != "locked": print("week not locked; nothing to do"); sys.exit(0)
byid = {e["id"]: e for v in sc.values() for e in v}; changed = False; new = []
for g in w["games"]:
    e = byid.get(g.get("odds_event_id"))
    if g["final"] is None and e and e.get("completed"):
        d = {x["name"]: int(x["score"]) for x in e["scores"]}
        g["final"] = {"away": d[e["away_team"]], "home": d[e["home_team"]]}; changed = True; new.append(g["id"])
        print("FINAL", g["away"], g["final"]["away"], g["home"], g["final"]["home"])
h1 = {k["game_id"] for k in w["picks"] if k.get("market") == "spread_h1" and not k.get("manual_result")}
espn = {}
for g in w["games"]:
    if g["id"] in h1 and g["final"] and not g.get("final_h1"):
        sport = "nfl" if g["league"] == "NFL" else "college-football"
        day = (datetime.datetime.fromisoformat(g["kickoff"].replace("Z", "+00:00")) - datetime.timedelta(hours=8)).strftime("%Y%m%d")
        data = get(f"https://site.api.espn.com/apis/site/v2/sports/football/{sport}/scoreboard?dates={day}"); espn[g["id"]] = data
        for ev in data.get("events", []):
            comps = ev["competitions"][0]["competitors"]
            names = {c["homeAway"]: c["team"]["displayName"] for c in comps}
            if g["home"] in names.get("home", "") and g["away"] in names.get("away", ""):
                h = {c["homeAway"]: sum(l["value"] for l in c.get("linescores", [])[:2]) for c in comps}
                g["final_h1"] = {"away": int(h["away"]), "home": int(h["home"])}; changed = True; new.append(g["id"])
                print("1H", g["away"], g["final_h1"]["away"], g["home"], g["final_h1"]["home"])
if changed:
    json.dump({"fetched_at": F, "daysFrom": 3, "responses": sc, "espn_first_half": espn},
              open(root/f"data/raw/2026-w{wk:02d}-scores-{T}.json", "w"), indent=1)
    json.dump(w, open(p, "w"), indent=1); open(p, "a").write("\n")
json.dump(new, open(root/".last_update.json", "w"))
print("changed", changed, "pending", sum(1 for g in w["games"] if g["final"] is None))
