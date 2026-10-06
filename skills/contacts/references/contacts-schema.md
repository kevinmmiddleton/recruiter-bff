# Contacts: File Format and Import

`job-search/contacts.csv` holds the people who matter to this search: people at companies the user is pursuing, people who've helped their career, and anyone they've reached out to. It's not a copy of their whole network. Change it through the `csv` module from the shell, never by hand.

## Columns

| Column | Meaning |
|---|---|
| `name` | Full name |
| `company` | Where they work now |
| `title` | Their title |
| `tags` | Any of: `recruiter`, `product`, `engineering`, `design`, `leader`, `helped-me`, `referrer` (separated by `;`) |
| `closeness` | `close` (would pick up the phone), `friendly` (worked together or know well), `loose` (met, shared contact), `never-spoke` (connected, no real contact) |
| `linkedin_url` | Their profile link, if known |
| `last_contact` | ISO date of the last real exchange either way. Blank means never. |
| `next_move` | One of: `reply`, `follow up`, `ask for an intro`, `ask for a referral`, `nudge`, `keep warm`, `thank`, `none` |
| `next_date` | ISO date for the next move, if any |
| `notes` | Dated lines, newest last: what was said, what was asked, what was promised |
| `source` | `linkedin-export`, `added`, or `gratitude-list` |

**Honest warmth:** a connection with no logged contact is `never-spoke`, however familiar the name. Closeness changes only when the user says so or a real exchange is logged.

**Check-in rhythm** (for `keep warm`): about every 30 days for `close`, 90 for `friendly`, 180 for `loose`. Never schedule check-ins for `never-spoke`.

## Getting the LinkedIn connections export

The user downloads it themselves; it takes a few minutes:

1. On LinkedIn: **Me → Settings & Privacy → Data privacy → Get a copy of your data.**
2. Choose **"Want something in particular?"**, tick **Connections**, and request the archive.
3. LinkedIn emails a download link, usually within about 10 minutes. The file inside is `Connections.csv`.
4. Save it into the Cowork folder (anywhere is fine; `job-search/` is tidy).

The file starts with a few lines of notes from LinkedIn, then a header row: `First Name, Last Name, URL, Email Address, Company, Position, Connected On`. Email is usually blank. Company and Position are whatever each person last put on their profile, so they can be out of date.

## Import and match

Matches the export against the companies the user is pursuing (open rows in the tracker plus companies to watch in the profile) and adds only those people to `contacts.csv`. Exact matches after cleanup; no fuzzy guessing.

```python
import csv, os, re, io, datetime

EXPORT = "job-search/Connections.csv"      # wherever the user saved it
TRACKER = "job-search/applications.csv"
PROFILE = "job-search/profile.md"
CONTACTS = "job-search/contacts.csv"
COLS = ["name","company","title","tags","closeness","linkedin_url","last_contact",
        "next_move","next_date","notes","source"]
ALIASES = {  # the user's own clean-ups: export spelling -> tracker spelling
    # "alphabet": "google",
}
TODAY = datetime.date.today().isoformat()

SUFFIX = r"\b(inc|incorporated|llc|ltd|limited|corp|corporation|co|company|plc|gmbh|the)\b"
def clean(name):
    s = (name or "").lower().replace("&", " and ")
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(SUFFIX, " ", s)
    s = " ".join(s.split())
    return ALIASES.get(s, s)

def tags_for(title):
    t = (title or "").lower(); tags = []
    if re.search(r"recruit|talent|\bsourc(er|ing)\b|people partner", t): tags.append("recruiter")
    if re.search(r"\bproduct\b|\bpm\b", t): tags.append("product")
    if re.search(r"engineer|developer|\bcto\b", t): tags.append("engineering")
    if re.search(r"design|\bux\b", t): tags.append("design")
    if re.search(r"\b(vp|vice president|director|head of|chief|founder|co-founder|ceo|coo|cpo|gm|general manager)\b", t): tags.append("leader")
    return ";".join(tags)

# 1. read the export, skipping LinkedIn's note lines above the header
with open(EXPORT, newline="", encoding="utf-8-sig") as f:
    lines = f.read().splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith("First Name"))
people = list(csv.DictReader(io.StringIO("\n".join(lines[start:]))))

# 2. the companies the user is pursuing
targets = {}
OPEN = {"prospect","applied","screening","interview","final","offer","hold"}
if os.path.exists(TRACKER):
    with open(TRACKER, newline="") as f:
        for r in csv.DictReader(f):
            if r.get("status") in OPEN:
                targets[clean(r["company"])] = r["company"]
if os.path.exists(PROFILE):
    text = open(PROFILE).read()
    if "## Companies to Watch" in text:
        block = text.split("## Companies to Watch", 1)[1].split("\n## ", 1)[0]
        for m in re.finditer(r"\*\*(.+?)\*\*", block):
            name = m.group(1).strip("[]: ")
            if name and name.lower() != "company":
                targets.setdefault(clean(name), name)

# 3. existing contacts (never duplicate a person)
rows = []
if os.path.exists(CONTACTS):
    with open(CONTACTS, newline="") as f:
        rows = list(csv.DictReader(f))
seen = {(r["name"].lower(), clean(r["company"])) for r in rows}

# 4. match and add
added = {}
for p in people:
    key = clean(p.get("Company"))
    if key not in targets: continue
    name = f'{p.get("First Name","").strip()} {p.get("Last Name","").strip()}'.strip()
    if not name or (name.lower(), key) in seen: continue
    rows.append({"name": name, "company": targets[key], "title": p.get("Position",""),
                 "tags": tags_for(p.get("Position")), "closeness": "never-spoke",
                 "linkedin_url": p.get("URL",""), "last_contact": "", "next_move": "none",
                 "next_date": "", "notes": f'{TODAY}: from LinkedIn export (connected {p.get("Connected On","")})',
                 "source": "linkedin-export"})
    seen.add((name.lower(), key))
    added.setdefault(targets[key], []).append(f'{name} ({p.get("Position","")})')

with open(CONTACTS, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
    w.writeheader(); w.writerows(rows)
print(f"{len(people)} connections read; {sum(len(v) for v in added.values())} added at {len(added)} companies")
for co, names in sorted(added.items()):
    print(f"  {co}: " + "; ".join(names))
```

After the import, walk through the matches with the user, company by company: "Do you actually know Priya? How well?" Set `closeness` from their answers. Everyone they don't recognize stays `never-spoke`.

## Adding and updating by hand

For people from the gratitude list, a new conversation, or an intro: load the file with `csv.DictReader`, append or update the row, write it all back with `csv.DictWriter` (same columns), and read it back to confirm. Log every real exchange as a dated note and update `last_contact`.
