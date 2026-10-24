# Routines

Three scheduled tasks run this league (already set up). Each starts a fresh Claude Code
session that follows the matching prompt file and pushes to main. They read the Odds API
key from the ODDS_API_KEY environment variable. Every run is idempotent: if there is
nothing to do it stops without a commit.

| Routine | Schedule (America/Los_Angeles) | Prompt file |
|---|---|---|
| Midnight lock | Saturday 12:00 AM | midnight-lock.md |
| Early-game lock | Thursday and Friday, every hour 4 PM to 11 PM | early-game-lock.md |
| Grade the week | Monday and Tuesday, 8:44 AM and 10:44 PM | grade-week.md |
