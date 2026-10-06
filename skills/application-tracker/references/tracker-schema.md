# Tracker Schema + Snippets

Full definition of `job-search/applications.csv` and ready-to-adapt Python for safe edits. Always operate on the CSV through the `csv` module via the shell — never hand-type rows.

## Columns

| Column | Meaning |
|--------|---------|
| `company` | Company name |
| `role` | Role title as posted |
| `location` | Location and/or work mode (remote/hybrid/onsite) |
| `comp` | Compensation, only if the posting listed it |
| `url` | Direct link to the posting |
| `source` | Where it came from (LinkedIn, Indeed, referral, etc.) |
| `status` | Lifecycle stage (see below) |
| `score` | 1–5 fit score (5 = exceptional); blank if never scored. Deep evaluations from `evaluate-role` use the full range; quick scans write 4 for STRONG, 3 for INCLUDE. Rows from older versions may carry legacy 1–3 scan scores. |
| `date_added` | ISO date the row entered the tracker |
| `date_applied` | ISO date the user applied (blank until applied) |
| `last_update` | ISO date of the most recent status change |
| `notes` | Free text: resume version, contacts, round notes, follow-up reminders |

## Status values

| Status | Meaning |
|--------|---------|
| `prospect` | Surfaced by a scan, not yet acted on |
| `applied` | Application submitted |
| `screening` | Recruiter screen scheduled/done |
| `interview` | In an interview loop (hiring manager, panel) |
| `final` | Final round |
| `offer` | Offer extended |
| `rejected` | Declined by the company |
| `skipped` | User chose not to apply (kept for dedup) |
| `ghosted` | No response after a long gap |
| `withdrawn` | User pulled out |
| `hold` | Parked for now, revisit later |

"Active" statuses (for stale-follow-up checks): `applied`, `screening`, `interview`, `final`.

## Snippets

Adapt paths and values. Run via the shell. These keep quoting correct and edits atomic.

### Create if missing

```python
import csv, os
path = "job-search/applications.csv"
cols = ["company","role","location","comp","url","source","status","score","date_added","date_applied","last_update","notes"]
if not os.path.exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        csv.writer(f).writerow(cols)
    print("created")
else:
    print("exists")
```

### Append rows (e.g., scan prospects), skipping duplicates

```python
import csv, datetime
path = "job-search/applications.csv"
today = datetime.date.today().isoformat()
# rows to add: list of dicts with at least company, role, location, comp, url, source, score
new_rows = [
    {"company":"Acme","role":"Senior Product Manager","location":"Remote (US)","comp":"","url":"https://...","source":"LinkedIn","score":"3"},
]
with open(path, newline="") as f:
    existing = list(csv.DictReader(f))
def norm(s): return " ".join(s.lower().replace("sr.","senior").replace("sr ","senior ").split())
seen = {(norm(r["company"]), norm(r["role"])) for r in existing}
cols = ["company","role","location","comp","url","source","status","score","date_added","date_applied","last_update","notes"]
added = 0
with open(path, "a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    for r in new_rows:
        key = (norm(r["company"]), norm(r.get("role","")))
        if key in seen:
            continue
        row = {c:"" for c in cols}
        row.update(r)
        row["status"] = "prospect"
        row["date_added"] = today
        row["last_update"] = today
        w.writerow(row)
        added += 1
print(f"added {added}")
```

### Update status by company + role (fuzzy)

```python
import csv, datetime
path = "job-search/applications.csv"
today = datetime.date.today().isoformat()
target_company, target_role, new_status = "Acme", "Senior Product Manager", "applied"
cols = ["company","role","location","comp","url","source","status","score","date_added","date_applied","last_update","notes"]
def norm(s): return " ".join((s or "").lower().replace("sr.","senior").replace("sr ","senior ").split())
with open(path, newline="") as f:
    reader = csv.DictReader(f); rows = list(reader)
    cols = reader.fieldnames or cols  # the header row, even when there are no data rows yet
hit = 0
for r in rows:
    if norm(r["company"]) == norm(target_company) and target_role.split()[0].lower() in norm(r["role"]):
        r["status"] = new_status
        r["last_update"] = today
        if new_status == "applied" and not r["date_applied"]:
            r["date_applied"] = today
        hit += 1
with open(path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(cols)); w.writeheader(); w.writerows(rows)
print(f"updated {hit}")
```

### Batch rejections

Loop the update snippet over a list of `(company, role)` pairs with `new_status="rejected"`, or filter on a list of companies. Report the total updated.

### Read back / scorecard

```python
import csv, datetime
path = "job-search/applications.csv"
with open(path, newline="") as f:
    rows = list(csv.DictReader(f))
from collections import Counter
by_status = Counter(r["status"] for r in rows)
active = {"applied","screening","interview","final"}
today = datetime.date.today()
def days_since(d):
    try: return (today - datetime.date.fromisoformat(d)).days
    except: return None
stale = [r for r in rows if r["status"] in active and (days_since(r["last_update"]) or 0) >= 7]
print("by status:", dict(by_status))
print("stale actives:", [(r["company"], r["role"], r["last_update"]) for r in stale])
```

Always print a confirmation and, after writes, read the file back so you can tell the user exactly what changed.
