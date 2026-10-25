# Scan History

`job-search/scan-history.csv` remembers the roles earlier scans showed the user, so a role from last week's scan that the user didn't add to the tracker doesn't come back as new. The plugin writes it; users don't need to open it. It's UTF-8 with a header, one row per role a scan showed: `date_seen,company,role,url,source,tier`. `date_seen` is the last date a scan showed the role to the user, `source` uses the tracker's values (`linkedin`, `ats-board`, `watchlist`), and `tier` is `STRONG` or `INCLUDE`. Only roles the user was shown are recorded: a role a scan held back as already shown isn't recorded again, so it keeps its old date. Rows older than 60 days drop off the next time the file is written.

## What counts as seen

- **Shown in the last 30 days:** already seen. Leave it out of this scan (`seen_before`).
- **Last shown 31 to 60 days ago:** it came back. Show it, tagged with when it was shown ("shown Oct 24, still open"), not as brand new (`shown_earlier`).

Either way, a role matches a row with:

- **the same link**, or
- **the same company and the same role** after normalizing the way the tracker does (rule 1 of "Matching a role" in `../application-tracker/references/tracker-schema.md`), so "Sr. PM" at "Fernhill, Inc." is "Senior Product Manager" at "Fernhill." Set `PM_MEANS` the way the tracker's load snippet says, from the profile's target titles (`None` if the profile's target titles include more than one kind of PM role), so the two agree.

A near match is not seen: "Senior Product Manager" and "Senior Product Manager, Platform" at the same company can be different jobs (see "Checking against the tracker" in `references/classification-rubric.md`). A missing file means nothing was seen yet; the first `record` creates it. A file the snippet can't read never stops a scan: it says so in one line, every role counts as new, and the file is left as it is.

## The snippet

Run Python the way `tracker-schema.md` says (which Python, a temporary `.py` file, never a heredoc): copy the snippet, then add the calls after it. Use it as written; don't write your own CSV code for this file, even a one-liner, since the snippet keeps the old rows, their dates, and the checks. If the shell can't see the job-search folder, copy `scan-history.csv` in with the tracker when the user's folder has one, each row on its own line; a copy without it starts a new history, and writing that back would replace the old one. The snippet always names the encoding, since Windows Python otherwise reads and writes cp1252.

```python
import csv, io, os, re, sys, datetime, shutil, tempfile
for s in (sys.stdout, sys.stderr):      # Windows consoles: print any name without crashing
    try: s.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

HISTORY = "job-search/scan-history.csv"
COLS = ["date_seen","company","role","url","source","tier"]
TODAY = datetime.date.today().isoformat()   # if the shell's clock may differ from the user's, use today's date from the conversation
PM_MEANS = "product manager"                # as in the tracker's load snippet: "project manager" or "program manager" for those fields; None if the profile's target titles include more than one kind of PM role
KEEP_DAYS = 60                              # rows older than this drop off the next time the file is written
WARNED = []                                 # an unreadable file is mentioned once per run

def norm(s):                            # the tracker's normalizing, so the two agree on what's the same role
    s = (s or "").lower().replace("&", " and ")
    s = re.sub(r"\bsr\b\.?", "senior", s)
    if PM_MEANS:
        s = re.sub(r"\bpm\b", PM_MEANS.lower(), s)
    s = re.sub(r"[^\w\s]", " ", s)
    return " ".join(s.split())

def norm_company(s):
    s = re.sub(r"\(.*?\)", " ", (s or ""))
    s = norm(s)
    for _ in range(3):
        s = re.sub(r"\s*\b(inc|incorporated|llc|ltd|limited|corp|corporation|co|plc|gmbh)$", "", s).strip()
    return s

def link(u):
    """A posting link without its scheme, www., anchor, or trailing slash. A blank link never matches."""
    u = (u or "").strip().lower().split("#")[0]
    return re.sub(r"^https?://(www\.)?", "", u).rstrip("/")

def day(s):
    """date_seen as a date, or None if it isn't one (that row counts as old)."""
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):     # a spreadsheet app may have rewritten it
        try: return datetime.datetime.strptime((s or "").strip(), fmt).date()
        except ValueError: pass
    return None

def ago(d):
    """Days from a date to TODAY, or None for no date."""
    return (datetime.date.fromisoformat(TODAY) - d).days if d else None

PLACEHOLDERS = {"stealth", "stealth startup", "stealth mode", "stealth mode startup", "stealth company",
                "confidential", "confidential company", "undisclosed", "company name withheld"}

def same(r, card):
    """The same posting: the same link, or the same company and the same role after normalizing.
    A near match ("Senior Product Manager, Platform" for "Senior Product Manager") is a different role.
    A placeholder name ("Stealth Startup") could be any employer: when both postings have links, only the link
    decides; without a link, it falls back to the name and role like any other card."""
    if link(card.get("url")) and link(r.get("url")) == link(card.get("url")):
        return True
    company, role = norm_company(card.get("company")), norm(card.get("role"))
    if company in PLACEHOLDERS and link(card.get("url")) and link(r.get("url")):
        return False
    return bool(company and role) and norm_company(r.get("company")) == company and norm(r.get("role")) == role

def last_shown(rows, card):
    """The last date a scan showed the user this card's role, or None."""
    dates = [day(r["date_seen"]) for r in rows if day(r["date_seen"]) and same(r, card)]
    return max(dates) if dates else None

def read_history(quiet=False):
    """(rows, cols, why). A missing or empty file is an empty history. For a file that can't be read, why says what's
    wrong: it counts as empty, one line says so (unless quiet), and record() leaves it as it is."""
    if not os.path.exists(HISTORY):
        return [], list(COLS), ""
    try:
        with open(HISTORY, newline="", encoding="utf-8-sig") as f:
            text = f.read()
        if not text.strip():
            return [], list(COLS), ""
        reader = csv.DictReader(io.StringIO(text, newline=""))
        found = list(reader.fieldnames or [])
        if not set(COLS) <= set(found):    # also catches a copy whose rows ran together into the header
            raise ValueError("no date_seen,company,role,url,source,tier header")
        raw = list(reader)
        if any(None in r for r in raw):     # a row with more values than the header has columns: rows that ran together
            raise ValueError("its rows ran together, so a copy lost the line breaks")
        rows = [{c: (r.get(c) or "") for c in found} for r in raw]
        return rows, COLS + [c for c in found if c not in COLS], ""
    except (OSError, ValueError, csv.Error) as e:
        why = "not UTF-8 text" if isinstance(e, UnicodeDecodeError) else str(e)
        if not quiet and not WARNED:
            print("CAN'T READ " + HISTORY + " (" + why + "): every role counts as new this scan, and the file is left as it "
                  "is. With the user's yes, set_aside() moves it out of the way.")
            WARNED.append(why)
        return [], list(COLS), why

def write_history(rows, cols):
    """Write the whole file through a temp file, so a failed write can't leave half of it. Keeps its permissions."""
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(HISTORY) or ".", suffix=".csv")
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        try:                            # a temp file starts owner-only: give it the old file's permissions
            if os.path.exists(HISTORY):
                shutil.copymode(HISTORY, tmp)
            else:
                um = os.umask(0); os.umask(um); os.chmod(tmp, 0o666 & ~um)
        except OSError:
            pass
        os.replace(tmp, HISTORY)
        return True
    except OSError as e:                # open in another app, a read-only folder, or no job-search folder here
        print("scan history not saved (" + (e.strerror or str(e)) + "); the scan itself is fine.")
        return False
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)

def seen_before(cards, days=30):
    """The cards (dicts with company, role, url) a scan showed the user in the last `days` days: leave them out of this
    scan, and don't record them. Prints how many, and which."""
    rows = read_history()[0]
    seen = [(c, last_shown(rows, c)) for c in cards]
    seen = [(c, d) for c, d in seen if d and ago(d) <= days]
    print(f"already shown in the last {days} days: {len(seen)} of {len(cards)}")
    for c, d in seen:
        print(f'  {c.get("company")} | {c.get("role")} | shown {d.isoformat()}')
    return [c for c, d in seen]

def shown_earlier(cards, days=30, keep=KEEP_DAYS):
    """(card, date) pairs for the cards a scan last showed the user more than `days` days ago but within `keep` days:
    roles that came back, to show as "shown Oct 24, still open" rather than as new. Prints how many, and which."""
    rows = read_history()[0]
    back = [(c, last_shown(rows, c)) for c in cards]
    back = [(c, d.isoformat()) for c, d in back if d and days < ago(d) <= keep]
    print(f"shown earlier, {days + 1} to {keep} days ago: {len(back)} of {len(cards)}")
    for c, d in back:
        print(f'  {c.get("company")} | {c.get("role")} | shown {d}')
    return back

def record(cards):
    """Save only the cards the user was shown in this scan (dicts with company, role, url, source, tier), dated today.
    Cards held back as already shown aren't passed in, so they keep their old date. A role already in the history gets
    today's date; rows older than KEEP_DAYS drop off. Never writes over a file it couldn't read."""
    rows, cols, why = read_history()
    if why:
        return
    kept = [r for r in rows if day(r["date_seen"]) and ago(day(r["date_seen"])) <= KEEP_DAYS]
    dropped, new, again = len(rows) - len(kept), 0, 0
    for r in kept:
        r["date_seen"] = day(r["date_seen"]).isoformat()   # back to YYYY-MM-DD
    for c in cards:
        r = next((r for r in kept if same(r, c)), None)
        if r is None:
            r = {k: "" for k in cols}
            kept.append(r); new += 1
        else:
            again += 1
        r.update({k: str(c[k]).strip() for k in COLS[1:] if c.get(k)})
        r["date_seen"] = TODAY
    if write_history(kept, cols):
        print(f"scan history: {new} new, {again} shown again, {dropped} older than {KEEP_DAYS} days dropped")

def set_aside():
    """Only with the user's yes: rename an unreadable history to scan-history-unreadable-YYYY-MM-DD.csv (never deleted,
    never over an earlier one), so the next record() starts a new one. Returns the new name, or None."""
    why = read_history(quiet=True)[2]
    if not why:
        print("nothing set aside: " + HISTORY + (" reads fine." if os.path.exists(HISTORY) else " doesn't exist."))
        return None
    stem = os.path.join(os.path.dirname(HISTORY), "scan-history-unreadable-" + TODAY)
    new, n = stem + ".csv", 1
    while os.path.exists(new):
        n += 1
        new = f"{stem}-{n}.csv"
    try:
        os.rename(HISTORY, new)
    except OSError as e:                # open in another app, or a read-only folder
        print("nothing set aside (" + (e.strerror or str(e)) + "); " + HISTORY + " is left as it is.")
        return None
    print("set aside: " + HISTORY + " is now " + new + " (" + why + "); the next record starts a new history.")
    return new
```

## The calls

- **`seen_before(cards, days=30)`**: `cards` is a list of the scan's job cards, each a dict with `company`, `role`, and `url` (blank when the scan had no link). Returns the cards a scan showed the user in the last `days` days, and prints `already shown in the last 30 days: 2 of 9`, then one line for each (`  Acme | Senior Product Manager | shown 2026-10-01`). Leave these out of the scan, and don't pass them to `record`.
- **`shown_earlier(cards, days=30, keep=KEEP_DAYS)`**: the same cards. Returns `(card, date)` pairs for roles a scan last showed more than `days` days ago but within the 60-day history (`date` is YYYY-MM-DD), and prints `shown earlier, 31 to 60 days ago: 1 of 9`, then one line for each (`  Tallyho | Product Lead | shown 2026-09-01`). Show these, tagged "shown Sep 1, still open," not as brand new.
- **`record(cards)`**: only the cards the user was shown in this scan, each a dict with `company`, `role`, `url`, `source`, and `tier`. That includes roles `shown_earlier` tagged, once they're shown. Saves them dated today (a role already in the history gets today's date), drops rows older than 60 days, and prints `scan history: 7 new, 2 shown again, 1 older than 60 days dropped`. Returns nothing.
- **`set_aside()`**: only after the user says yes, for a file the snippet can't read. Renames it to `scan-history-unreadable-YYYY-MM-DD.csv` in the same folder (with `-2`, `-3` if that name is taken; it never deletes anything), so the next `record` starts a new history. Prints `set aside: job-search/scan-history.csv is now job-search/scan-history-unreadable-2026-10-24.csv (...); the next record starts a new history.` and returns the new name. A file that reads fine, or no file, is left alone: it prints `nothing set aside: ...` and returns None.

`record` gets only the cards the user was shown, never the ones `seen_before` held back. Those keep their old `date_seen`, so a role still posted 30 days after the user last saw it comes back once, and `shown_earlier` tags it.

When the file can't be read, the first call in a run prints `CAN'T READ job-search/scan-history.csv (...)` once: `seen_before` and `shown_earlier` then find nothing, `record` writes nothing, and the scan carries on. That includes a copy whose rows ran together. `record` prints `scan history not saved (...)` instead of its line when the file is open in another app or the folder can't be written; the scan itself is fine.
