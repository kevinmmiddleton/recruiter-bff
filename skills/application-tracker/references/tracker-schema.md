# Tracker Schema and Snippets

The full definition of `job-search/applications.csv`, plus Python you can adapt for safe edits. Always change the CSV through the `csv` module from the shell. Never hand-type rows.

## Columns

| Column | Meaning |
|--------|---------|
| `company` | Company name |
| `role` | Role title as posted |
| `location` | Location and work mode (remote, hybrid, onsite) |
| `comp` | Pay, only if the posting listed it |
| `url` | Direct link to the posting |
| `source` | Where it came from: `linkedin`, `ats-board`, `watchlist`, `referral`, `recruiter`, `pasted`, or the board's name |
| `status` | Where it stands now (see below) |
| `score` | 1 to 5 fit score (5 is exceptional), blank if never scored. Evaluations from `evaluate-role` write the score with one decimal (4.6); quick scans write 4 for STRONG and 3 for INCLUDE. Rows from older versions may have 1 to 3 scan scores. |
| `date_added` | ISO date the row entered the tracker |
| `date_applied` | ISO date the user applied (blank until then) |
| `last_update` | ISO date anything last happened: a status change, or a message either way |
| `notes` | Free text, newest line last: resume version, contacts, round notes, promises made |
| `furthest_stage` | The furthest stage this role ever reached. Never lowered, even on a rejection. |
| `next_date` | ISO date of the next thing: an interview, a deadline, a follow-up the user promised. Blank if none. |

`furthest_stage` and `next_date` are new in 1.0. A tracker from an older version won't have them. The `load` snippet below adds them the next time the file is written, fills `furthest_stage` from each row's current status, and changes nothing else. Tell the user once: "Your tracker has two new columns now: the furthest stage each role reached, and the date of the next thing. Everything else is the same."

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
3. **No exact match, but one role at that company:** it's almost certainly that one. Say which row you're updating before you do it.
4. **No exact match and several roles at that company:** don't guess. Show the candidates and ask which one.
5. **Never update by the first word of a title,** and never update every row at a company unless the user asks for exactly that.

## Rejections, safely

**Recognizing one.** Typical phrases: "will not be moving forward," "decided to pursue other candidates," "after careful consideration," "decided not to advance," "going in a different direction," "no longer under consideration," "position has been filled," "regret to inform," "another candidate," and "unfortunately" near "application" or "candidacy." A confirmation ("thank you for applying," "we received your application") is not a rejection; if an email has both kinds of language, the rejection wins. "The position has been filled" before the user was ever considered is `closed`, not `rejected`. A pause ("on hold," "paused hiring") is `hold`.

Rejection emails are often vague ("we've decided to move forward with other candidates"), and people often apply to several roles at one company. Rules:

- **Only rows applied on or before the rejection.** An application sent after the email's date can't be the one it's rejecting. Skip it.
- **Job ID first.** If the email has a requisition or job ID and it appears in a row's `url` or `notes`, that's the row, even among several open roles at the company.
- **Exact role next.** If the email names the role, match it exactly (rules above).
- **Company name from the sender, too.** If the email's company name doesn't match, try the sender's domain ("careers@fernhillhealth.com") and the normalized name before saying "not in the tracker." Only then, if the user wants, add a new row as `rejected`.
- **Generic rejection, one open application at that company:** that's the one. Update it.
- **Generic rejection, several open applications at that company:** put it on a **"which one?"** list and ask. Don't guess.
- Set `status` to `rejected`, update `last_update`, leave `furthest_stage` alone, and add a dated note with the stage it ended at if known ("2026-10-06: rejected after the hiring manager round").

For a batch, finish with a summary that includes days since applying: "Marked 4 rejected (after 6, 11, 19, and 30 days). 1 is on the which-one list: Acme sent a general no, and you have two roles open there."

## Snippets

Adapt paths and values, and run them from the shell. They keep quoting correct, write the whole file in one step, and never drop columns the user added by hand.

### Load and save (use these in every snippet)

```python
import csv, os, datetime, re, tempfile

PATH = "job-search/applications.csv"
COLS = ["company","role","location","comp","url","source","status","score",
        "date_added","date_applied","last_update","notes","furthest_stage","next_date"]
STAGES = ["prospect","applied","screening","interview","final","offer"]
TODAY = datetime.date.today().isoformat()

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

def load(path=PATH):
    """Rows plus the column list. Creates nothing. Adds new 1.0 columns in memory."""
    if not os.path.exists(path):
        return [], list(COLS)
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = list(reader.fieldnames or COLS)
    for c in COLS:                      # add missing standard columns, keep any extras the user added
        if c not in cols:
            cols.append(c)
    for r in rows:
        for c in cols:
            r.setdefault(c, "")
            if r[c] is None:
                r[c] = ""
        if not r["furthest_stage"] and r["status"] in STAGES:
            raise_stage(r, r["status"])         # conservative: a current screen counts as applied until it happens
    return rows, cols

def save(rows, cols, path=PATH):
    """Write the whole file at once, through a temp file, so a failed write can't leave half a tracker."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".", suffix=".csv")
    with os.fdopen(fd, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)

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
```

### Create the file if it's missing

```python
rows, cols = load()
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
     "url":"https://...","source":"linkedin","score":"4"},
]
added, dupes = 0, []
for n in new:
    matches, _ = find(rows, n["company"], n["role"])
    if matches:
        dupes.append(f'{n["company"]}: {n["role"]}'); continue
    r = {c: "" for c in cols}
    r.update(n)
    r.update({"status":"prospect","furthest_stage":"prospect","date_added":TODAY,"last_update":TODAY})
    rows.append(r); added += 1
save(rows, cols)
print(f"added {added}; already tracked: {dupes}")
```

### Update a status (one role), following the matching rules

```python
company, role, new_status = "Acme", "Senior Product Manager", "screening"
completed = False    # True when this round has already happened (a debrief); False when it's only booked
note = ""            # optional context, e.g. "screen with Dana Thursday"
next_date = ""       # optional ISO date of the next thing

rows, cols = load()
matches, same = find(rows, company, role)
fallback = False
if not matches and len(same) == 1:
    matches, fallback = same, True   # the only role at this company: tell the user which row
if not matches and not same:
    print("NOT IN TRACKER: add it first with the add snippet, then update")
elif len(matches) != 1:
    print("AMBIGUOUS, ask the user:", [(r["company"], r["role"], r["status"]) for r in (matches or same)])
else:
    r = matches[0]
    r["status"] = new_status
    r["last_update"] = TODAY
    if new_status == "applied" and not r["date_applied"]:
        r["date_applied"] = TODAY
    raise_stage(r, new_status, completed)
    if next_date:
        r["next_date"] = next_date
    if note:
        r["notes"] = (r["notes"] + " | " if r["notes"] else "") + f"{TODAY}: {note}"
    save(rows, cols)
    print("updated:", r["company"], "|", r["role"], "->", new_status, "| furthest:", r["furthest_stage"],
          "| (the only role at this company)" if fallback else "")
```

If the role isn't in the tracker at all (the user applied outside a scan), append it with the add snippet first, then update.

### Apply a rejection safely

```python
company = "Acme"
role = None                 # the role named in the email, or None if it's a general no
email_date = "2026-10-06"   # the date the rejection arrived
stage_note = ""             # e.g. "after the hiring manager round"

OPEN = {"applied","screening","interview","final","offer","hold"}
rows, cols = load()
matches, same = find(rows, company, role)
pool = matches if role else same
pool = [r for r in pool if r["status"] in OPEN
        and (r["date_applied"] or r["date_added"]) <= email_date]
if len(pool) == 1:
    r = pool[0]
    r["status"] = "rejected"; r["last_update"] = TODAY
    r["notes"] = (r["notes"] + " | " if r["notes"] else "") + f"{email_date}: rejected" + (f" {stage_note}" if stage_note else "")
    save(rows, cols)
    print("rejected:", r["role"], "| furthest stage stays", r["furthest_stage"])
elif not pool:
    print("NO MATCH: nothing open at", company, "applied on or before", email_date)
else:
    print("WHICH ONE? ask the user:", [(r["role"], r["status"], r["date_applied"]) for r in pool])
```

### Read back: counts, the follow-up ladder, and furthest stages

```python
from collections import Counter
rows, cols = load()
today = datetime.date.today()
def days(d):
    try: return (today - datetime.date.fromisoformat(d)).days
    except Exception: return None
ACTIVE = {"screening","interview","final","offer"}
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
