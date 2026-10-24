# The Pick'em

Six picks a week against the spread, NFL or college, one lock worth double.
Picks due Friday 11:59 PM PT. Lines lock automatically at midnight with proof.
Graded automatically Monday night. Dashboard: docs/index.html (served by GitHub Pages).

## One-time setup (about 20 minutes, no coding)

1. **GitHub.** Create a free account if you don't have one, create a new private
   repo called `pickem`, and upload this folder's contents to it.
2. **GitHub Pages.** Repo Settings > Pages > Source: Deploy from a branch > `main`,
   folder `/docs`. Save. In a minute you get a link like
   `https://yourname.github.io/pickem/`. That's the dashboard link for the group.
   (Private repos need GitHub Pro for Pages. A public repo is fine too; there's
   nothing sensitive in here, just picks and lines.)
3. **The Odds API.** Sign up free at the-odds-api.com and copy your key. The free
   tier covers a few hundred requests a month; these routines use roughly 15.
4. **Routines.** Go to claude.ai/code/routines and create the three routines in
   `routines/README.md`, each pointed at this repo with the env var ODDS_API_KEY.
5. **Names.** Edit `data/league.json`: replace the player names, keep the ids simple
   (lowercase, no spaces). Delete `data/weeks/2026-w04.json` (sample) and set
   `current_week` to the week you're starting on.

## Weekly, what you do

**Entering picks (any time before the deadline).** Open Claude Code on this repo
(or the Claude app, chat pointed at the repo) and paste the group's texts:

    Jake: Bills +2.5 LOCK, Penn State -3, Texas -4.5, Ravens -1, Ole Miss -6.5, Eagles +1
    Mike: ...

Say "load these picks for week 5." Claude writes them into the week file, flags anything
ambiguous ("which Michigan game?"), runs build.py, and commits. The dashboard updates
in about a minute. People can change picks the same way until the deadline.

**Everything else is automatic.** Midnight Saturday the lines lock. Monday night it grades.

## Backfilling earlier weeks

Paste past weeks in the same format plus the lines and finals, and say
"backfill week 3." Claude creates the week file with status "graded".

## Rules encoded here

- Win +1, loss -1, push 0. Lock of the week counts double in every outcome.
- Picks are graded at the official line from the book in `league.json`, captured at
  Saturday 12:00 AM PT (or kickoff, for games that start earlier).
- The raw API responses in `data/raw/` are the proof and are never edited.
- Cancelled or postponed games are a push for everyone.

## Data files

- `data/league.json` : players, scoring, book, current week
- `data/weeks/2026-wNN.json` : games, picks, lines, finals for one week
- `data/raw/` : untouched API responses with timestamps
- `site/template.html` + `build.py` -> `docs/index.html`
