# Routines

Three scheduled routines run this league. Create each at claude.ai/code/routines,
point it at this repo, and paste the matching prompt. Set the schedule shown.
Add one environment variable to each: ODDS_API_KEY (free key from the-odds-api.com).

| Routine | Schedule (America/Los_Angeles) | Prompt file |
|---|---|---|
| Midnight lock | Saturday 12:00 AM | midnight-lock.md |
| Early-game lock | Thursday and Friday, every hour 4 PM to 11 PM | early-game-lock.md |
| Grade the week | Monday 11:00 PM, and Tuesday 9:00 AM as a backstop | grade-week.md |

Routines push to claude/-prefixed branches by default. Either set GitHub Pages
to serve from the branch the routine writes to, or allow the routine to push to main
in the routine's settings.
