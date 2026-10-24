#!/usr/bin/env python3
"""Inline data/*.json into site/template.html -> dist/index.html. Run after any data change."""
import json, glob, os, pathlib
root = pathlib.Path(__file__).parent
league = json.load(open(root/"data/league.json"))
weeks = [json.load(open(f)) for f in sorted(glob.glob(str(root/"data/weeks/*.json")))]
payload = json.dumps({"league": league, "weeks": weeks}, separators=(",",":")).replace("</", "<\\/")
html = open(root/"site/template.html").read().replace("/*__DATA__*/", payload)
os.makedirs(root/"dist", exist_ok=True)
open(root/"dist/index.html","w").write(html)
print(f"built dist/index.html with {len(weeks)} week(s)")
