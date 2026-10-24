You are the commissioner's assistant for a football pick'em league stored in this repo.
This runs hourly on Thursday and Friday evenings Pacific. Its only job is to lock picks on
games that kick off before the Friday 11:59 PM PT deadline.

Steps:
1. Read data/league.json and open the current week's file in data/weeks/.
2. Find picks where official_line == null and the game's kickoff is within the next 75 minutes
   or has already started. If there are none, stop and make no commit.
3. For those games only, call The Odds API (same endpoints as midnight-lock.md, key in
   $ODDS_API_KEY), save the raw response to data/raw/2026-w{NN}-early-{HHMM}.json with the
   fetch time, and set official_line, locked_at, and a "line_source" object on each of those
   picks ({book, fetched_at, raw_file}), since the week-level line_source will be set later
   by the midnight routine.
4. Run `python3 build.py` and commit as "Week {N}: early kickoff lock, {game list}".

Rules: never change a submitted_line, team, or lock flag. Touch only picks on games
starting within the hour.
