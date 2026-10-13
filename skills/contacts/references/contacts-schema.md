# Contacts: File Format and Import

`job-search/contacts.csv` holds the people who matter to this search: people at companies the user is pursuing, people who've helped their career, and anyone they've reached out to. It's not a copy of their whole network. Change it through the `csv` module from the shell, never by hand. Run Python the way `../application-tracker/references/tracker-schema.md` says (which Python to use, and what to do if the shell can't see the folder). Through the file tools, copy every file the import reads: `Connections.csv`, the tracker, the profile, and `contacts.csv` if the folder has one. Without `contacts.csv` in the copy, the import would start a new one, and writing that back would replace the user's. A long export may need more than one file-tool read; check the copy has every line before you run it.

## Columns

| Column | Meaning |
|---|---|
| `name` | Full name |
| `company` | Where they work now |
| `title` | Their title |
| `tags` | Any of: `recruiter`, `same-role` (works in the user's own function), `engineering`, `design`, `leader`, `helped-me`, `referrer` (separated by `;`). Older files may say `product`, which means the same thing as `same-role`. |
| `closeness` | `close` (would pick up the phone), `friendly` (worked together or know well), `loose` (met, shared contact), `never-spoke` (connected, no real contact) |
| `linkedin_url` | Their profile link, if known |
| `last_contact` | ISO date of the last real exchange either way. Blank means never. |
| `next_move` | One of: `reply`, `follow up`, `ask for an intro`, `ask for a referral`, `nudge`, `keep warm`, `thank`, `none` |
| `next_date` | ISO date for the next move, if any |
| `notes` | Dated lines, newest last: what was said, what was asked, what was promised |
| `source` | `linkedin-export`, `added`, or `gratitude-list` |

**Honest warmth:** a connection with no logged contact is `never-spoke`, however familiar the name. Closeness changes only when the user says so or a real exchange is logged. If the user says they know someone but doesn't know when they last spoke, set the closeness and leave `last_contact` blank with a note ("date unknown"); blank means "never" only for `never-spoke`.

**Check-in rhythm** (for `keep warm`): about every 30 days for `close`, 90 for `friendly`, 180 for `loose`. Never schedule check-ins for `never-spoke`. Each person has two clocks worth showing together: the opportunity ("Fernhill: screening, 6 days") and the relationship ("last spoke 29 days ago," or "never spoke").

**Logging a touch:** the date, the channel (email, LinkedIn, text, call, in person), and the direction ("they reached out" or "I reached out").

## Getting the LinkedIn connections export

The user downloads it themselves; it takes a few minutes:

1. On LinkedIn: **Me > Settings & Privacy > Data privacy > Get a copy of your data.**
2. Choose **"Want something in particular?"**, tick **Connections**, and request the archive.
3. LinkedIn emails a download link, usually within about 10 minutes. The file inside is `Connections.csv`.
4. Save it into the folder you use for your job search (anywhere in it is fine; `job-search/` is tidy).

The file starts with a few lines of notes from LinkedIn, then a header row: `First Name, Last Name, URL, Email Address, Company, Position, Connected On`. Email is usually blank. Company and Position are whatever each person last put on their profile, so they can be out of date.

## Import and match

Matches the export against the companies the user is pursuing (open rows in the tracker plus companies to watch in the profile) and adds only those people to `contacts.csv`. Exact matches after cleanup; no fuzzy guessing.

```python
import csv, os, sys, re, io, datetime
for s in (sys.stdout, sys.stderr):      # Windows consoles: print any name without crashing
    try: s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

EXPORT = next((p for p in ["job-search/Connections.csv", "Connections.csv"] if os.path.exists(p)),
              "Connections.csv")              # or wherever the user saved it
TRACKER = next((p for p in ["job-search/job-tracker.csv", "job-search/applications.csv"] if os.path.exists(p)),
               "job-search/job-tracker.csv")  # the 0.4 names in a folder that hasn't been renamed
PROFILE = next((p for p in ["job-search/search-profile.md", "job-search/profile.md"] if os.path.exists(p)),
               "job-search/search-profile.md")
CONTACTS = "job-search/contacts.csv"
FIRST_IMPORT = False   # True only when the user's own folder has no contacts.csv yet (check there, not in a copy)
COLS = ["name","company","title","tags","closeness","linkedin_url","last_contact",
        "next_move","next_date","notes","source"]
ALIASES = {  # the user's own clean-ups: export spelling -> tracker spelling
    # "alphabet": "google",
}
TODAY = datetime.date.today().isoformat()   # if the shell's clock may differ from the user's, use today's date from the conversation

def is_date(s):
    """A date in any format a spreadsheet app writes (the same ones the tracker's iso() reads)."""
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y/%m/%d", "%d.%m.%Y", "%b %d, %Y", "%d-%b-%y"):
        try:
            datetime.datetime.strptime((s or "").strip(), fmt)
            return True
        except ValueError:
            pass
    return False

def read_csv(path):
    """Rows and columns. Reads Excel's "CSV UTF-8" (with its invisible start mark) and Windows' plain CSV."""
    for enc in ("utf-8-sig", "cp1252"):
        try:
            with open(path, newline="", encoding=enc) as f:
                text = f.read()
            if "�" in text:           # a file tool read a file that wasn't UTF-8: Excel's plain CSV, from a Mac or Windows
                raise SystemExit("CAN'T READ " + path + " safely: the copy shows the replacement character (�), so the file "
                                 "isn't CSV UTF-8. Ask the user to save it from Excel as CSV UTF-8, then close it in Excel, "
                                 "then run this again. Never write this copy back.")
            if enc == "cp1252" and re.search("[ÒÓÔÕŽ]|[A-Za-z][\u2021\u02c6\u2030\u0160\u2039\u0152\u2018\u201c\u201d\u2022\u2013\u2014\u02dc\u2122\u0161\u203a\u0153\u017e\u0178\u00a7\u00bf\u00be][a-z]|[\u0192\u2020][a-z]", text):
                # accented letters, quotes, and apostrophes from Excel's plain CSV on a Mac: the real letters are lost
                raise SystemExit("CAN'T READ " + path + " safely: it looks like Excel saved it as plain CSV, and its accented letters may not read correctly. "
                                 "Ask the user to save it as CSV UTF-8, then close it in Excel, then run this again.")
            reader = csv.DictReader(io.StringIO(text, newline=""))
            rows, cols = list(reader), list(reader.fieldnames or [])
            if (any(is_date(c) or "://" in c for c in cols)
                    or not rows and set(cols) & {"never-spoke", "loose", "friendly", "close", "prospect", "applied", "screening",
                                                 "interview", "final", "offer", "hold", "rejected", "closed", "ghosted", "withdrawn"}):
                # every contact has a closeness and every tracker row a status, and a real header holds no dates or links,
                # so a header holding one has swallowed rows
                raise SystemExit("CAN'T READ " + path + ": its rows ran together into the header, so a copy lost the line "
                                 "breaks (Excel on a Mac can end rows with a bare carriage return). Write the copy again with "
                                 "each row on its own line, then run this again. Never write this copy back.")
            if any(None in r for r in rows):
                # a row with more values than the header has columns: rows that ran together, or a comma outside quotes;
                # a save would drop what doesn't fit
                raise SystemExit("CAN'T READ " + path + ": a row has more values than the header has columns. Either rows "
                                 "ran together into one (a copy lost the line breaks) or a value has a comma that isn't in quotes, "
                                 "and saving now would drop data. Don't repair it without the user's yes: the fix is each row on its own line "
                                 "and any comma inside a value in quotes. Then run this again. Never write this copy back.")
            return rows, cols
        except UnicodeDecodeError:
            continue
    raise SystemExit("CAN'T READ " + path + ": ask the user to save it from their spreadsheet app as CSV UTF-8.")

def write_csv(path, rows, cols):
    """Write the whole file in place (so it keeps its permissions), in UTF-8. A new file gets Excel's start mark, so Excel
    shows accented names correctly; an existing one is written back the way it was read (an empty file counts as new)."""
    if any("\ufffd" in v for r in rows for v in r.values() if isinstance(v, str)):   # read_csv refuses a file with it, so it's new
        raise SystemExit("NOT SAVED: a new value holds the replacement character (\ufffd), so a letter was lost on the way in "
                         "(often an export opened and saved again in Excel). Use Connections.csv as LinkedIn sent it, or ask "
                         "the user for the real spelling, then run this again.")
    bom = True
    if os.path.exists(path):
        with open(path, "rb") as f:
            bom = f.read(3) in (b"\xef\xbb\xbf", b"")
    try:
        with open(path, "w", newline="", encoding="utf-8-sig" if bom else "utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader(); w.writerows(rows)
    except PermissionError as e:
        # usually the file is open in a spreadsheet app (Windows locks it); in a sandboxed session the folder may not be writable
        raise SystemExit("NOT SAVED: " + path + " couldn't be written (" + str(e) + "). It's usually open in a spreadsheet "
                         "app, or the file is marked locked or read-only: ask the user to close it or unlock it, then run "
                         "this again. If neither, this session may not be allowed to write to that folder; say so and ask the "
                         "user to check the folder's access.")

SUFFIX = r"\s+(inc|incorporated|llc|ltd|limited|corp|corporation|co|company|plc|gmbh|sa|ag|nv)$"  # legal suffixes only: "Fernhill Labs" is not "Fernhill"
def clean(name):
    s = re.sub(r"\(.*?\)", " ", (name or "")).lower().replace("&", " and ")
    s = re.sub(r"[^\w\s]", " ", s)
    s = " ".join(s.split())
    s = re.sub(r"^the\s+", "", s)
    for _ in range(3):                  # strip up to three trailing legal suffixes, never words in the middle
        s = re.sub(SUFFIX, "", s)
    return ALIASES.get(s, s)

# Same-function titles: set these from the user's target function. The tag is "same-role" whatever the function.
# Product management shown here; neighbors that share a word ("Product Designer," "Product Marketing") are left out on purpose.
SAME_FUNCTION = r"product manager|product management|head of product|(vp|vice president|director)\W+(of\s+)?product\b(?!\s+(design|marketing))|\bcpo\b|chief product|product owner|product lead|\bpm\b"
def tags_for(title):
    t = (title or "").lower(); tags = []
    if re.search(r"recruit|talent acquisition|talent partner|\bsourc(er|ing)\b|people ops|head of (people|talent)|\bhrbp\b|human resources|staffing", t): tags.append("recruiter")
    if re.search(SAME_FUNCTION, t): tags.append("same-role")
    if re.search(r"engineer|developer|\bcto\b", t): tags.append("engineering")
    if re.search(r"design|\bux\b", t): tags.append("design")
    if re.search(r"\b(vp|vice president|director|head of|chief|founder|co-founder|ceo|coo|cpo|gm|general manager|partner)\b", t) and "recruiter" not in tags: tags.append("leader")
    return ";".join(tags)

# 1. read the export, skipping LinkedIn's note lines above the header
with open(EXPORT, newline="", encoding="utf-8-sig") as f:
    lines = f.read().splitlines()
start = next((i for i, l in enumerate(lines) if l.startswith("First Name")), None)
if start is None:
    raise SystemExit("No 'First Name' header in " + EXPORT + ". Is it LinkedIn's Connections.csv?")
people = list(csv.DictReader(io.StringIO("\n".join(lines[start:]))))

# 2. the companies the user is pursuing
targets = {}
OPEN = {"prospect","applied","screening","interview","final","offer","hold"}
if os.path.exists(TRACKER):
    for r in read_csv(TRACKER)[0]:
        if r.get("status") in OPEN:
            targets[clean(r["company"])] = r["company"]
else:
    print("NO TRACKER found, so this matches companies to watch only. If the user has a tracker, copy it in and rerun.")
if os.path.exists(PROFILE):
    text = open(PROFILE, encoding="utf-8").read()
    if "## Companies to Watch" in text:
        block = text.split("## Companies to Watch", 1)[1].split("\n## ", 1)[0]
        for m in re.finditer(r"\*\*(.+?)\*\*", block):
            name = m.group(1).strip("[]: ")
            if name and name.lower() != "company":
                targets.setdefault(clean(name), name)

# 3. existing contacts (never duplicate a person)
rows, cols = [], list(COLS)
if os.path.exists(CONTACTS):
    rows, found = read_csv(CONTACTS)
    cols += [c for c in found if c not in cols]   # keep columns the user added
elif not FIRST_IMPORT:                            # a missing contacts file is never treated as an empty one
    raise SystemExit("NO CONTACTS FILE at " + os.path.abspath(CONTACTS) + ". If the user has never had one, rerun with "
                     "FIRST_IMPORT = True. Otherwise this is the wrong folder, or a copy that wasn't made: stop, and never "
                     "write a new contacts file over the real one.")
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

write_csv(CONTACTS, rows, cols)
print(f"{len(people)} connections read; {sum(len(v) for v in added.values())} added at {len(added)} companies")
for co, names in sorted(added.items()):
    print(f"  {co}: " + "; ".join(names))

# 5. near misses: same first words, different company. Ask the user; never add them automatically.
near = sorted({(p.get("Company",""), targets[t]) for p in people for t in targets
               if clean(p.get("Company")) != t and clean(p.get("Company")).startswith(t + " ")})
if near:
    print("near misses to ask about:", "; ".join(f"{c} (vs {t})" for c, t in near))
```

Small startups often aren't in an export at all, and titles are whatever people last put on their profile. Re-run the import when the user downloads a fresh export or the tracker grows.

After the import, walk through the matches with the user, company by company, recruiters first, then people in the user's own function, then leaders, then everyone else: "Do you actually know Priya? How well?" Set `closeness` from their answers. Everyone they don't recognize stays `never-spoke`.

## Adding and updating by hand

For people from the gratitude list, a new conversation, or an intro: load the file with `read_csv` from the import above (no `contacts.csv`? check the user's own folder before starting one, as the import does), append or update the row, write it all back with `write_csv` (same columns, including any the user added; it handles Excel's start mark and keeps the file's permissions), and read it back to confirm. Log every real exchange as a dated note and update `last_contact`.
