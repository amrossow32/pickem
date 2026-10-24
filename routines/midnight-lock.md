You are the commissioner's assistant for a football pick'em league stored in this repo.
Run this at Saturday 12:00 AM Pacific. Your job is to lock in the official line for every
pick in the current week and leave proof.

Steps:
1. Read data/league.json. Note official_book, current_week, and timezone.
2. Open data/weeks/2026-w{current_week:02d}.json (for example 2026-w05.json).
   If the week's status is not "open", stop and make no commit. If every pick already has an
   official_line (they were locked as they came in), skip steps 3 to 5 and go straight to
   step 6: the week must still be marked locked or it will never be graded.
3. Call The Odds API with the key in $ODDS_API_KEY. Endpoints:
   - NFL: https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?regions=us&markets=spreads,totals&bookmakers={official_book}&apiKey=$ODDS_API_KEY
   - College: https://api.the-odds-api.com/v4/sports/americanfootball_ncaaf/odds/?regions=us&markets=spreads,totals&bookmakers={official_book}&apiKey=$ODDS_API_KEY
   Save both raw responses, untouched, to data/raw/2026-w{NN}-midnight.json along with
   the exact UTC time you fetched them. This file is the proof. Never edit it later.
4. For every pick in the week file that has official_line == null and whose game has not
   kicked off yet: find the game in the raw response by matching away and home team names
   (be careful with college names; "Ole Miss" may appear as "Mississippi"). Take the spread
   for the team the person picked (p.side tells you away or home). Write it to official_line,
   set locked_at to the fetch time, and leave submitted_line exactly as it was.
   If official_line differs from submitted_line, that is expected and is what the dashboard
   shows as a line move. Do not round or "fix" anything.
   Picks have a "market": "spread" picks take the team's spread from the spreads market;
   "total" picks (side "over" or "under") take the game total from the totals market.
   "spread_h1" (first-half) picks cannot be priced from this feed: put them in needs_review.
   Only use odds for games whose commence_time is still in the future; never take a live line.
5. If a picked game cannot be found at the official book, try the other books in the
   response, use that line, and record which book in a "line_note" field on the pick.
   If it cannot be found at all, leave official_line null and add it to a "needs_review"
   list at the top level of the week file so the commissioner sees it.
6. Set the week's "line_source" to {book, fetched_at, raw_file} (if no fetch was needed, use
   {book, fetched_at: now, raw_file: null, note: "all picks locked individually"}) and status to "locked".
   Picks already locked by the early-game routine keep their existing values.
7. Run `python3 build.py` so docs/index.html is rebuilt. Commit everything with the message
   "Week {N}: lines locked at {fetch time PT}".

Rules: never change a submitted_line, a team, or a lock flag. Never delete a pick. If
anything is ambiguous, leave it unlocked and put it in needs_review rather than guessing.
