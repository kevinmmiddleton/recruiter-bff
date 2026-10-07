# Tracker Schema and Snippets

The full definition of `job-search/job-tracker.csv`, plus Python you can adapt for safe edits. Always change the CSV through the `csv` module from the shell. Never hand-type rows.

## Columns

| Column | Meaning |
|--------|---------|
| `company` | Company name |
| `role` | Role title as posted |
| `location` | Location and work mode (remote, hybrid, onsite) |
| `comp` | Pay as the posting listed it, ranges written with "to" (`$175k to $205k`); blank if not listed |
| `url` | Direct link to the posting |
| `source` | Where the role came from, not how it reached you: `linkedin` (including pasted LinkedIn results), `ats-board`, `watchlist`, `referral`, `recruiter`, the board's name in lowercase, or `pasted` only when the origin is unknown. Write new rows with these values. Older rows may say `LinkedIn`; leave them as they are and count them as the same source. |
| `status` | Where it stands now (see below) |
| `score` | 1 to 5 fit score (5 is exceptional), blank if never scored. Evaluations from `evaluate-role` write the score with one decimal, rounded half up (4.6); quick scans write 4 for STRONG and 3 for INCLUDE. Rows from older versions may have 1 to 3 scan scores. A row whose notes record a fit check ("Evaluated 2026-10-06: 4.6/5," "Fit check: 4.4") counts as a fit check whatever its score looks like: 0.4 trackers and Excel can turn 4.6 into 5. Use the score from the notes then. |
| `date_added` | ISO date the row entered the tracker |
| `date_applied` | ISO date the user applied (blank until then) |
| `last_update` | ISO date anything last happened: a status change, or a message either way |
| `notes` | Free text, newest line last: resume version, contacts, round notes, promises made |
| `furthest_stage` | The furthest stage this role ever reached. Never lowered, even on a rejection. |
| `next_date` | ISO date of the next thing: an interview, a deadline, a follow-up the user promised. Blank if none. |

`furthest_stage` and `next_date` are new in 1.0. A tracker from an older version won't have them. The `load` snippet below adds them the next time the file is written and fills `furthest_stage` from each row's current status. Older versions kept booked dates only in `notes`, so for active processes (screening, interview, final, offer) it also fills `next_date` when the row's notes hold exactly one full date after today (`2026-10-13` or `10/13/2026`); with none, or more than one, it leaves `next_date` blank. The save prints any it filled. Nothing else changes. Tell the user once: "Your tracker has two new columns now: the furthest stage each role reached, and the date of the next thing. Everything else is the same." If a date was filled, name it in the same line ("I took Fernhill's next date, Tue Oct 13, from your notes; tell me if that's wrong").

## Statuses

| Status | Meaning |
|--------|---------|
| `prospect` | Found, not acted on yet |
| `applied` | Application sent, no reply yet |
| `screening` | Recruiter screen scheduled or done |
| `interview` | In the interview loop (hiring manager, panel) |
| `final` | Final round |
| `offer` | Offer extended |
| `accepted` | The user accepted an offer. `furthest_stage` stays `offer`; it drops off the active list. |
| `rejected` | The company said no to the user |
| `closed` | The role went away: filled by someone else before the user was considered, cancelled, or frozen. Not a rejection. |
| `hold` | Paused by the company or the user. A hiring pause is not a no. |
| `ghosted` | No reply after a long gap in an active process. Reversible: if they reply, move it back. |
| `withdrawn` | The user pulled out |
| `skipped` | The user chose not to apply (kept so scans don't show it again) |

**Be honest with statuses.** A posting taken down before anyone called is `closed`, not `rejected`. A recruiter saying "we've paused the search" is `hold`. Recording these as rejections makes the search look worse than it is and hides roles that may come back.

**Stages, in order:** `prospect` < `applied` < `screening` < `interview` < `final` < `offer`. `furthest_stage` is the furthest stage that has actually **happened**. A screen that's only scheduled doesn't count yet: when a row moves to `screening` because a screen is booked, `furthest_stage` becomes `applied`; once the screen takes place (the user debriefs, or the row moves on to `interview`), it becomes `screening`. Applying and receiving an offer count the moment they happen. Never lower it: rejected, closed, held, ghosted, withdrawn, and accepted change `status` only. Counting booked rounds as reached inflates the numbers; counting only what happened keeps "where do I usually stall?" honest.

**Active processes** (for follow-ups): `screening`, `interview`, `final`, `offer`. A cold `applied` row is not active: silence on a cold application is normal, so it never gets a follow-up flag.

## The follow-up ladder (active processes only)

Days since `last_update`:

| Days quiet | What to suggest |
|---|---|
| 0 to 6 | Nothing. Give it time. |
| 7 to 13 | **Nudge:** a short, friendly check-in. Offer to draft it. |
| 14 to 29 | **Chase or close:** ask directly where things stand, or decide to let it go. |
| 30 or more | **Mark it ghosted?** Ask first. It's reversible. |

If `next_date` is in the future (an interview is booked, or they said "we'll know by Friday"), the role isn't quiet. Don't flag it until that date has passed.

## Matching a role (the rules every update follows)

Updating the wrong row is worse than updating none. So:

1. **Same company, same role, after normalizing.** Roles: lowercase, drop punctuation, `sr`/`sr.` becomes `senior`, `pm` becomes `product manager`, `&` becomes `and`, collapse spaces; keep seniority words, since "Senior Product Manager" and "Product Manager" are different roles. Companies: the same, plus drop trailing legal suffixes (Inc, LLC, Ltd, Corp, Co) and anything in parentheses, so "Fernhill, Inc." matches "Fernhill." 
2. **One match:** update it.
3. **No exact match, but one open role at that company:** ask whether that's the one before updating it. Finished rows (rejected, closed, withdrawn, skipped, ghosted, accepted) are never a fallback: a new role at a company with only finished rows gets its own row.
4. **No exact match and several roles at that company:** don't guess. Show the candidates and ask which one.
5. **Never update by the first word of a title,** and never update every row at a company unless the user asks for exactly that.
6. **A shorter or longer company name** ("Northstar" for "Northstar Learning"): when there's no exact company match, a tracked company whose name starts with the other one at a word boundary is a near match. The snippets print CHECK FIRST with those rows. Ask which one the user means, and never add a new row until they say it's a different company.

## Rejections, safely

**Recognizing one.** Typical phrases: "will not be moving forward," "decided to pursue other candidates," "after careful consideration," "decided not to advance," "going in a different direction," "no longer under consideration," "position has been filled," "regret to inform," "another candidate," and "unfortunately" near "application" or "candidacy." A confirmation ("thank you for applying," "we received your application") is not a rejection; if an email has both kinds of language, the rejection wins. "The position has been filled" before the user was ever considered is `closed`, not `rejected`. A pause ("on hold," "paused hiring") is `hold`.

Rejection emails are often vague ("we've decided to move forward with other candidates"), and people often apply to several roles at one company. Rules:

- **Only rows applied on or before the rejection.** An application sent after the email's date can't be the one it's rejecting. Skip it.
- **Job ID first.** If the email has a requisition or job ID and it appears in a row's `url` or `notes`, that's the row, even among several open roles at the company.
- **Exact role next.** If the email names the role, match it exactly (rules above). If the title is close but not exact ("Senior Product Manager, Growth" against a "Senior Product Manager" row), show the company's open rows and ask which one; never say nothing is open.
- **Company name from the sender, too.** If the email's company name doesn't match, try the sender's domain ("careers@fernhillhealth.com"), the normalized name, and near matches (rule 6: "Northstar" for "Northstar Learning") before saying "not in the tracker." Only then, if the user wants, add a new row as `rejected`.
- **Generic rejection, one open application at that company:** that's the one. Update it.
- **Generic rejection, several open applications at that company:** put it on a **"which one?"** list and ask. Don't guess.
- **The company is in the tracker only as a prospect** (the user never logged applying): they probably applied and forgot to say so. Ask one question: "I have the Senior PM, Retention role as a prospect. Is that the one you applied to?" On yes, or "you pick," mark that row: set `date_applied` if they know it, `status` to `rejected`, and `furthest_stage` to `applied`. Run the rejection snippet with `include_prospects = True`.
- **The company isn't in the tracker at all:** if the user wants it recorded, add it as rejected with the snippet below.
- Set `status` to `rejected`, update `last_update`, leave `furthest_stage` alone, and add a dated note with the stage it ended at if known ("2026-10-06: rejected after the hiring manager round").

For a batch, finish with a summary that includes days since applying: "Marked 4 rejected (after 6, 11, 19, and 30 days). 1 is on the which-one list: Acme sent a general no, and you have two roles open there."

## Snippets

Adapt paths and values, save the code to a temporary `.py` file, and run it with the first Python that prints a version: `python3`, then `python`, then `py -3` on Windows (Windows' `python3` can be a Microsoft Store shortcut that does nothing). Don't use a shell heredoc; PowerShell doesn't have one. If the shell can't see the job-search folder (in Cowork's cloud sessions the shell runs on Anthropic's servers), read the file with the file tool, write that text to a copy in the shell's folder, run the snippet on the copy, write the whole result back with the file tool, and read it back. Put each row on its own line in the copy, even if the file tool shows them run together (Excel on a Mac can end rows with a bare carriage return); if the rows still run into the header, the snippets stop. A round trip through the file tools may drop Excel's start mark and change the line endings: the rows are the same, but Excel may show accented names wrongly until the file is saved as CSV UTF-8 again. `PATH` finds `job-tracker.csv`, or `applications.csv` in a 0.4 folder that hasn't been renamed (see Step 0 of `job-search-setup`). The snippets keep quoting correct, write the whole file in one step, and never drop columns the user added by hand.

They also cope with a file saved from a spreadsheet app: Excel's "CSV UTF-8" (which adds an invisible mark at the start), Windows' plain "CSV", and dates rewritten as `9/15/2026`. Dates go back to YYYY-MM-DD on the next write; when that happens, tell the user once. Excel on a Mac saves plain "CSV" in an older encoding the snippets can't read safely, so they stop and say to save it as CSV UTF-8 and close it in Excel. They also stop when the text holds the replacement character (�): the file wasn't UTF-8 when the file tool read it (Excel's plain CSV, from a Mac or Windows), and writing it back would lose the real letters for good. The snippets write UTF-8: a new tracker starts with Excel's mark, so Excel shows accented names correctly, and an existing one the snippet reads itself is written back the way it was read, with the mark or without. A save keeps the file's permissions. A missing tracker is never treated as an empty one: every snippet but "create" stops with NO TRACKER. If a save fails because the file is open in Excel, ask the user to close it, then run the snippet again.

### Load and save (use these in every snippet)

```python
import csv, io, os, sys, datetime, re, shutil, tempfile
for s in (sys.stdout, sys.stderr):      # Windows consoles: print any name without crashing
    try: s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

PATH = next((p for p in ("job-search/job-tracker.csv", "job-search/applications.csv") if os.path.exists(p)),
            "job-search/job-tracker.csv")   # the 0.4 name in a folder that hasn't been renamed
COLS = ["company","role","location","comp","url","source","status","score",
        "date_added","date_applied","last_update","notes","furthest_stage","next_date"]
STAGES = ["prospect","applied","screening","interview","final","offer"]
ACTIVE = {"screening","interview","final","offer"}
DATES = ["date_added","date_applied","last_update","next_date"]
TODAY = datetime.date.today().isoformat()   # if the shell's clock may differ from the user's, use today's date from the conversation
FILLED = []                                 # next dates taken from notes on a tracker's first 1.0 write

def norm(s):
    s = (s or "").lower().replace("&", " and ")
    s = re.sub(r"\bsr\b\.?", "senior", s)
    s = re.sub(r"\bpm\b", "product manager", s)
    s = re.sub(r"[^\w\s]", " ", s)
    return " ".join(s.split())

def norm_company(s):
    s = re.sub(r"\(.*?\)", " ", (s or ""))
    s = norm(s)
    for _ in range(3):
        s = re.sub(r"\s*\b(inc|incorporated|llc|ltd|limited|corp|corporation|co|plc|gmbh)$", "", s).strip()
    return s

def iso(d):
    """Dates back to YYYY-MM-DD if a spreadsheet app reformatted them (US month first assumed)."""
    d = (d or "").strip()
    if not d or re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        return d
    for fmt in ("%m/%d/%Y", "%m/%d/%y", "%Y/%m/%d", "%d.%m.%Y", "%b %d, %Y", "%d-%b-%y"):
        try: return datetime.datetime.strptime(d, fmt).date().isoformat()
        except ValueError: pass
    return d

def load(path=PATH, must_exist=True):
    """Rows plus the column list. Creates nothing. Adds new 1.0 columns in memory."""
    if not os.path.exists(path):
        if must_exist:                  # a missing tracker is never treated as an empty one
            raise SystemExit("NO TRACKER at " + os.path.abspath(path) + ". If the user has never had one, run the create "
                             "snippet first. Otherwise this is the wrong folder, or a copy that wasn't made: stop, and "
                             "never write a new tracker over the real one.")
        return [], list(COLS)
    for enc in ("utf-8-sig", "cp1252"):  # utf-8-sig drops the mark Excel adds to "CSV UTF-8"; cp1252 is Excel's plain CSV on Windows
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
            rows = list(reader)
            cols = list(reader.fieldnames or COLS)
            if not rows and any(re.fullmatch(r"\d{4}-\d{2}-\d{2}", iso(c)) or "://" in c for c in cols):
                # a real header holds no dates (in any format iso() reads) and no links, so this one swallowed the rows
                raise SystemExit("CAN'T READ " + path + ": its rows ran together into the header, so a copy lost the line "
                                 "breaks (Excel on a Mac can end rows with a bare carriage return). Write the copy again with "
                                 "each row on its own line, then run this again. Never write this copy back.")
            break
        except UnicodeDecodeError:
            continue
    else:
        raise SystemExit("CAN'T READ " + path + ": ask the user to save it from their spreadsheet app as CSV UTF-8.")
    had_next_date = "next_date" in cols
    for c in COLS:                      # add missing standard columns, keep any extras the user added
        if c not in cols:
            cols.append(c)
    for r in rows:
        for c in cols:
            r.setdefault(c, "")
            if r[c] is None:
                r[c] = ""
        for c in DATES:
            r[c] = iso(r[c])
        if not r["furthest_stage"] and r["status"] in STAGES:
            raise_stage(r, r["status"])         # conservative: a current screen counts as applied until it happens
        if not had_next_date and r["status"] in ACTIVE:
            # older trackers kept booked dates in notes: use one only if it's the only full date after today
            found = {iso(d) for d in re.findall(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{4}\b", r["notes"])}
            future = sorted(d for d in found if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) and d > TODAY)
            if len(future) == 1:
                r["next_date"] = future[0]
                FILLED.append((r["company"], r["role"], future[0]))
    return rows, cols

def save(rows, cols, path=PATH):
    """Write the whole file at once, through a temp file, so a failed write can't leave half a tracker."""
    if any("\ufffd" in v for r in rows for v in r.values() if isinstance(v, str)):   # load() refuses a file with it, so it's new
        raise SystemExit("NOT SAVED: a new value holds the replacement character (\ufffd), so a letter was lost on the way in. "
                         "Ask the user for the real spelling, then run this again.")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    bom = True                          # a new tracker gets Excel's start mark, so Excel shows accented names correctly
    if os.path.exists(path):            # an existing one is written back the way it was read (an empty file counts as new)
        with open(path, "rb") as f:
            head = f.read(3)
        bom = head in (b"\xef\xbb\xbf", b"")
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".", suffix=".csv")
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8-sig" if bom else "utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        try:                            # a temp file starts owner-only: give it the tracker's permissions
            if os.path.exists(path):
                shutil.copymode(path, tmp)
            else:
                um = os.umask(0); os.umask(um); os.chmod(tmp, 0o666 & ~um)
        except OSError:
            pass
        os.replace(tmp, path)
        if FILLED:
            print("next_date filled from notes (tell the user):", FILLED)
            FILLED.clear()
    except PermissionError:
        raise SystemExit("NOT SAVED: " + path + " is probably open in Excel. Ask the user to close it, then run this again.")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

def raise_stage(r, status, completed=False):
    """Furthest stage that actually happened. A booked round counts once it's completed."""
    if status not in STAGES:
        return
    i = STAGES.index(status)
    if not completed and status not in ("prospect", "applied", "offer"):
        i -= 1                          # booked, not held yet: the stage before it is what happened
    cur = r.get("furthest_stage") or ""
    if cur not in STAGES or i > STAGES.index(cur):
        r["furthest_stage"] = STAGES[i]

def find(rows, company, role=None):
    """Exact company + normalized role. Returns (matches, same_company)."""
    same = [r for r in rows if norm_company(r["company"]) == norm_company(company)]
    if role is None:
        return same, same
    return [r for r in same if norm(r["role"]) == norm(role)], same

def near(rows, company):
    """No exact company match: rows whose company name starts with the other one at a word boundary
    ("Northstar" and "Northstar Learning"). Never act on these without asking."""
    c = norm_company(company)
    return [r for r in rows if c and norm_company(r["company"]) and norm_company(r["company"]) != c
            and (norm_company(r["company"]).startswith(c + " ") or c.startswith(norm_company(r["company"]) + " "))]
```

### Create the file if it's missing

Check the user's own folder first (with the file tool, in Cowork). A copy in the shell's folder that has no tracker proves nothing.

```python
rows, cols = load(must_exist=False)
if not os.path.exists(PATH):
    save([], cols)
    print("created")
else:
    print("exists")
```

### Add prospects (from a scan or an evaluation), skipping exact duplicates

```python
rows, cols = load()
new = [
    {"company":"Acme","role":"Senior Product Manager","location":"Remote (US)","comp":"",
     "url":"https://...","source":"linkedin","score":"4",
     "notes":"2026-10-06: from the scan (STRONG). Range starts under the floor."},   # notes optional
]
confirmed_new_company = False   # True once the user says a near-match name below is a different company
added, dupes, check = 0, [], []
for n in new:
    matches, same = find(rows, n["company"], n["role"])
    if matches:
        dupes.append(f'{n["company"]}: {n["role"]}'); continue
    close = [] if (same or confirmed_new_company) else near(rows, n["company"])
    if close:
        check.append((n["company"], n["role"], sorted({r["company"] for r in close}))); continue
    r = {c: "" for c in cols}
    r.update(n)
    r.update({"status":"prospect","furthest_stage":"prospect","date_added":TODAY,"last_update":TODAY})
    rows.append(r); added += 1
save(rows, cols)
print(f"added {added}; already tracked: {dupes}")
if check:
    print("CHECK FIRST, not added. Same company as one already tracked?", check,
          "Same: rerun with the tracker's spelling. Different: rerun with confirmed_new_company = True.")
```

### Update a status (one role), following the matching rules

```python
company, role, new_status = "Acme", "Senior Product Manager", "screening"
completed = False    # True when this round has already happened (a debrief); False when it's only booked
note = ""            # optional context, e.g. "screen with Dana Thursday"
next_date = ""       # optional ISO date of the next thing
on_date = TODAY      # the date it happened, if the user said ("I applied yesterday")
confirmed_row = False  # True once the user says the one open role at this company is the one they mean
date_applied = ""    # ISO date they applied, if they say (asked for when a prospect goes straight to a screen)
source = ""          # "recruiter" if the recruiter reached out first (asked for with date_applied)
on_date, next_date, date_applied = iso(on_date), iso(next_date), iso(date_applied)   # in case a date came as 10/8/2026

rows, cols = load()
matches, same = find(rows, company, role)
open_same = [r for r in same if r["status"] in {"prospect","applied","screening","interview","final","offer","hold"}]
if not matches and len(open_same) == 1 and confirmed_row:
    matches = open_same
close = [] if same else near(rows, company)
if close:
    print("CHECK FIRST, is it one of these?", [(r["company"], r["role"], r["status"]) for r in close],
          "Yes: rerun with the company spelled as in the tracker. A different company: add it with the add",
          "snippet (confirmed_new_company = True), then update.")
elif not matches and len(open_same) == 1:
    r = open_same[0]
    print("CHECK FIRST, is it this row?", (r["company"], r["role"], r["status"]),
          "Yes: rerun with confirmed_row = True. A different role: add it with the add snippet, then update.")
elif not matches and not open_same:
    print("NOT TRACKED as an open role: add it first with the add snippet, then update."
          + (" Finished rows stay as they are: " + str([(r["role"], r["status"]) for r in same]) if same else ""))
elif len(matches) != 1:
    print("AMBIGUOUS, ask the user:", [(r["company"], r["role"], r["status"]) for r in (matches or open_same)])
else:
    r = matches[0]
    r["status"] = new_status
    r["last_update"] = on_date
    if date_applied and not r["date_applied"]:
        r["date_applied"] = date_applied
    if source:
        r["source"] = source
    if new_status == "applied" and not r["date_applied"]:
        r["date_applied"] = on_date
    raise_stage(r, new_status, completed)
    if next_date:
        r["next_date"] = next_date
    elif completed and r["next_date"] and r["next_date"] <= TODAY:
        r["next_date"] = ""          # the round it pointed to has happened
    if note:
        r["notes"] = (r["notes"] + " | " if r["notes"] else "") + f"{on_date}: {note}"
    save(rows, cols)
    print("updated:", r["company"], "|", r["role"], "->", new_status, "| furthest:", r["furthest_stage"])
    if new_status in STAGES[2:] and not r["date_applied"] and r["source"] != "recruiter":
        print("ASK: when did they apply? date_applied is blank. Rerun with note = \"\" (this note is saved) and date_applied set,",
              "or, if the recruiter reached out first, with source = \"recruiter\".")
```

If the role isn't in the tracker at all (the user applied outside a scan), append it with the add snippet first, then update.

### Apply a rejection safely

```python
company = "Acme"
role = None                 # the role named in the email, or None if it's a general no
email_date = TODAY          # the date the rejection arrived (YYYY-MM-DD), if the user says or the email shows it
stage_note = ""             # e.g. "after the hiring manager round"
include_prospects = False   # True only after the user confirms a prospect row is the one they applied to
date_applied = ""           # if the user says when they applied (ISO date); used for a confirmed prospect

OPEN = {"applied","screening","interview","final","offer","hold"} | ({"prospect"} if include_prospects else set())
email_date, date_applied = iso(email_date), iso(date_applied)   # in case a date came as 10/5/2026
rows, cols = load()
matches, same = find(rows, company, role)
close = [] if same else near(rows, company)          # "Northstar" for "Northstar Learning"
pool = matches if (role and matches) else same      # a named role with no exact match falls back to the company's open rows
named_unmatched = bool(role) and not matches
pool = [r for r in pool if r["status"] in OPEN
        and (r["date_applied"] or r["date_added"]) <= email_date]
if close:
    print("CHECK FIRST, is it one of these?", [(r["company"], r["role"], r["status"]) for r in close],
          "Yes: rerun with the company spelled as in the tracker. Don't add a new row unless the user says",
          "it's a different company.")
elif len(pool) == 1 and not named_unmatched:
    r = pool[0]
    before = r["furthest_stage"]
    if r["status"] == "prospect":
        r["furthest_stage"] = "applied"   # they applied; it just wasn't logged
        r["date_applied"] = r["date_applied"] or date_applied
    r["status"] = "rejected"; r["last_update"] = TODAY
    r["notes"] = (r["notes"] + " | " if r["notes"] else "") + f"{email_date}: rejected" + (f" {stage_note}" if stage_note else "")
    save(rows, cols)
    fs = r["furthest_stage"]
    print("rejected:", r["role"], "| furthest stage", ("stays " + fs) if fs == before else f"now {fs} (was {before or 'blank'})")
elif not pool:
    prospects = [r["role"] for r in same if r["status"] == "prospect"]
    if prospects and not include_prospects:
        print("ONLY PROSPECTS at", company, "- ask if they applied to one of:", prospects)
    else:
        print("NO MATCH: nothing open at", company, "applied on or before", email_date,
              "| rows there:", [(r["role"], r["status"], r["date_applied"]) for r in same])
else:
    print(("THE EMAIL NAMES " + repr(role) + ", NO EXACT MATCH. " if named_unmatched else "") + "WHICH ONE? ask the user:",
          [(r["role"], r["status"], r["date_applied"]) for r in pool])
```

### Record a role that isn't tracked, as rejected

```python
company, role = "Acme", "Senior Product Manager"   # role "" if the email doesn't say
email_date = "2026-10-06"
confirmed_new_company = False   # True once the user says a near-match name is a different company
rows, cols = load()
same, close = find(rows, company)[1], near(rows, company)
if same:
    print("ALREADY TRACKED at", company, "- use the rejection snippet:", [(r["role"], r["status"]) for r in same])
elif close and not confirmed_new_company:
    print("CHECK FIRST, not added. Is it one of these?", [(r["company"], r["role"], r["status"]) for r in close],
          "Same: use the rejection snippet with the tracker's spelling. Different: rerun with confirmed_new_company = True.")
else:
    r = {c: "" for c in cols}
    r.update({"company": company, "role": role or "(role not stated)", "source": "pasted",
              "status": "rejected", "furthest_stage": "applied", "date_added": TODAY,
              "last_update": TODAY, "notes": f"{email_date}: rejected (applied outside the tracker)"})
    rows.append(r); save(rows, cols)
    print("added as rejected:", company, "|", r["role"])
```

### Read back: counts, the follow-up ladder, and furthest stages

```python
from collections import Counter
rows, cols = load()
today = datetime.date.fromisoformat(TODAY)
def days(d):
    try: return (today - datetime.date.fromisoformat(d)).days
    except Exception: return None
ladder = []
for r in rows:
    if r["status"] not in ACTIVE: continue
    if r["next_date"] and r["next_date"] >= today.isoformat(): continue
    q = days(r["last_update"])
    if q is None or q < 7: continue
    step = "nudge" if q < 14 else "chase or close" if q < 30 else "mark ghosted?"
    ladder.append((r["company"], r["role"], r["status"], q, step))
print("by status:", dict(Counter(r["status"] for r in rows)))
print("furthest stage:", dict(Counter(r["furthest_stage"] for r in rows if r["furthest_stage"])))
print("follow-ups:", ladder)
print("coming up:", sorted((r["next_date"], r["company"], r["role"]) for r in rows
                           if r["next_date"] and r["next_date"] >= today.isoformat()))
```

After any write, read the file back so you can tell the user exactly what changed.
