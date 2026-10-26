"""Run the Python snippets in the tracker, contacts, and scan history reference files against sample files.

The skills tell the agent to copy these snippets, so the snippets are the plugin's only code.
This pulls every ```python block out of:
    skills/application-tracker/references/tracker-schema.md
    skills/contacts/references/contacts-schema.md
    skills/find-jobs/references/scan-history.md
runs them in a temporary folder against sample trackers, contacts files, LinkedIn exports, and
scan histories, and checks what they print and what they write. Nothing in the repo or your own
folders is touched.

Run from anywhere:
    python3 tools/check_snippets.py
    python3 tools/check_snippets.py --rev 2b95a6b      # how an older commit does on today's checks
    python3 tools/check_snippets.py --from <folder>    # the same, for a copy that isn't committed

Cases covered: a fresh tracker from create to rejection, a header-only, an empty, and a missing
file (and a missing contacts file on a rerun), the finished-row fallback (a new role at a
company with only finished rows, and one open row with a different title), a shorter company
name ("Northstar" for "Northstar Learning"), files saved by Excel ("CSV UTF-8" with its start
mark, kept on save and given to new files; Windows' plain CSV in cp1252; a Mac's plain CSV with
é, ñ, ó, ü, ø, or ß, which stops; plain CSV through a file tool, which stops; bare carriage
returns and a copy whose rows ran together, tracker or contacts, with any date format or a link,
into the header, into each other under an intact header, or with only the first row in the header;
dates rewritten as 9/15/2026), a new value that already holds the replacement character, file
permissions kept on save, a 0.4 tracker's booked dates taken from notes, rejection dates typed
as 10/5/2026, the near-miss rejection title, a confirmed prospect rerun with its title, accented and emoji names with Windows' default
encoding, columns the user added (tracker and contacts), a save that fails because the file is
open in Excel, what "PM" means (product by default, project when PM_MEANS says so, and left as
it is with None), and the contacts import (LinkedIn's note lines, near misses, recruiter and
same-role tags, a same-role pattern for project management, a rerun, a wrong file).

Scan history: a missing file and the first record that creates it, a role seen again within 30
days and new again after, a role recorded twice, a link-only match, a normalized title ("Sr. PM"
at "Fernhill, Inc." for "Senior Product Manager" at "Fernhill"), a near match that isn't seen, a
61-day-old row dropped on write, a role shown 35 days ago that comes back from shown_earlier (and a
61-day-old one that matches nothing), an empty and a header-only file, an unreadable file left
alone while the scan goes on (including rows run together under an intact header), set_aside
(renamed, never over an earlier one, never a readable file), accented names with Windows' default
encoding, permissions kept on save, a save blocked by another app, and titles and companies
normalized the way the tracker does.
"""
import argparse, os, pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRACKER_MD = "skills/application-tracker/references/tracker-schema.md"
CONTACTS_MD = "skills/contacts/references/contacts-schema.md"
SCAN_MD = "skills/find-jobs/references/scan-history.md"
TODAY = "2026-10-06"

# To count how many checks an older version fails: --rev <commit> (from git) or --from <folder> (a copy
# that isn't committed). A setting the older snippets don't have yet (confirmed_row, for one) is added at
# the top of the snippet, where it does nothing, so the check that depends on it fails instead of stopping the run.
# A file the older version doesn't have yet (scan-history.md) gives an empty snippet, so its checks fail the same way.
ARGS = argparse.ArgumentParser(description="Run the tracker, contacts, and scan history snippets against sample files.")
ARGS.add_argument("--rev", help="check the snippets as they were at this git commit")
ARGS.add_argument("--from", dest="src", help="check the snippets in another copy of the plugin (a folder with skills/)")
OPTS = ARGS.parse_args([a for a in sys.argv[1:]] if __name__ == "__main__" else [])
LENIENT = bool(OPTS.rev or OPTS.src)

def source(rel):
    if OPTS.rev:
        return subprocess.run(["git", "-C", str(ROOT), "show", f"{OPTS.rev}:{rel}"],
                              capture_output=True, text=True, check=True, encoding="utf-8").stdout
    return (pathlib.Path(OPTS.src or ROOT) / rel).read_text(encoding="utf-8")

# Windows Python before 3.15 opens text files as cp1252 when no encoding is given.
WINDOWS = '''
import builtins, os as _os
_open, _fdopen = builtins.open, _os.fdopen
def _cp_open(file, mode="r", buffering=-1, encoding=None, *a, **k):
    if "b" not in mode and encoding is None: encoding = "cp1252"
    return _open(file, mode, buffering, encoding, *a, **k)
def _cp_fdopen(fd, mode="r", buffering=-1, encoding=None, *a, **k):
    if "b" not in mode and encoding is None: encoding = "cp1252"
    return _fdopen(fd, mode, buffering, encoding, *a, **k)
builtins.open, _os.fdopen = _cp_open, _cp_fdopen
'''
# The file is open in Excel on Windows: replacing it fails.
EXCEL_LOCK = '''
import os as _os
def _locked(*a, **k): raise PermissionError(13, "The process cannot access the file")
_os.replace = _locked
'''

H12 = "company,role,location,comp,url,source,status,score,date_added,date_applied,last_update,notes\n"
H14 = H12.replace("notes\n", "notes,furthest_stage,next_date\n")
TRACKER_PATH = "job-search/job-tracker.csv"


# ---------- pulling the snippets out ----------

def blocks(rel, optional=False):
    try:
        return re.findall(r"```python\n(.*?)```", source(rel), re.S)
    except (subprocess.CalledProcessError, FileNotFoundError):
        if optional:                    # an older version without this file: its checks fail instead of stopping the run
            return []
        raise

def pick(found, marker, what):
    hits = [b for b in found if marker in b]
    if len(hits) != 1:
        sys.exit(f"Can't find the {what} snippet (looked for {marker!r}, found {len(hits)}).")
    return hits[0]

TB = blocks(TRACKER_MD)
BASE = pick(TB, "def load(", "load and save")
CREATE = pick(TB, 'print("created")', "create")
ADD = pick(TB, "added, dupes", "add prospects")
UPDATE = pick(TB, "new_status", "update")
REJECT = pick(TB, "include_prospects", "rejection")
RECORD = pick(TB, "added as rejected", "record as rejected")
READBACK = pick(TB, "follow-ups:", "read back")
IMPORT = pick(blocks(CONTACTS_MD), "Connections.csv", "contacts import")
SB = blocks(SCAN_MD, optional=LENIENT)
SCAN = pick(SB, "def seen_before(", "scan history") if SB or not LENIENT else ""


def setvar(code, name, value):
    """Replace the first line that assigns `name` (a plain or tuple assignment) with a new value."""
    new, n = re.subn(rf"^{re.escape(name)}\s*=.*$", lambda m: f"{name} = {value!r}", code, count=1, flags=re.M)
    if not n:
        if LENIENT:                     # an older version: add the setting where it does nothing
            return f"{name} = {value!r}\n" + code
        sys.exit(f"No line assigning {name!r} in a snippet; did its wording change?")
    return new

def pin_today(code, day=TODAY):
    return re.sub(r"^TODAY = .*$", f"TODAY = {day!r}", code, count=1, flags=re.M)

def shift(days):
    """TODAY moved by a number of days, for a later scan or an older row."""
    import datetime
    return (datetime.date.fromisoformat(TODAY) + datetime.timedelta(days=days)).isoformat()

def update(company, role, status, **kw):
    code = setvar(UPDATE, "company, role, new_status", (company, role, status))
    for k, v in kw.items():
        code = setvar(code, k, v)
    return code

def reject(company, role=None, **kw):
    code = setvar(setvar(REJECT, "company", company), "role", role)
    for k, v in kw.items():
        code = setvar(code, k, v)
    return code

def add(rows):
    code, n = re.subn(r"^new = \[.*?^\]\n", lambda m: "new = " + repr(rows) + "\n", ADD, count=1, flags=re.M | re.S)
    if not n:
        sys.exit("Can't find the `new = [...]` list in the add snippet.")
    return code


# ---------- running them ----------

WORK = pathlib.Path(tempfile.mkdtemp(prefix="rbff-snippets-"))

def folder(name, tracker=None, enc="utf-8", files=None):
    d = WORK / name
    (d / "job-search").mkdir(parents=True)
    if tracker is not None:
        (d / TRACKER_PATH).write_bytes(tracker.encode(enc))
    for rel, text in (files or {}).items():
        (d / rel).write_text(text, encoding="utf-8")
    return d

def run(d, code, base=True, pre="", env=None, today=TODAY):
    """Write the snippet to a .py file (the way the skill says to) and run it in folder d.
    base: True puts the load and save snippet first, a string puts that version of it first (a changed setting),
    and False runs the snippet on its own. today: the date the snippet runs on."""
    script = d / "_snippet.py"
    body = (pin_today(BASE if base is True else base, today) + "\n" if base else "") + pin_today(code, today)
    script.write_text(pre + "\n" + body, encoding="utf-8")
    e = dict(os.environ, **(env or {}))
    p = subprocess.run([sys.executable, str(script)], cwd=d, capture_output=True, env=e)
    script.unlink()
    return (p.stdout + p.stderr).decode("utf-8", "replace").strip()

def text(d, rel=TRACKER_PATH):
    return (d / rel).read_text(encoding="utf-8-sig")    # has_mark() checks the start mark itself

def has_mark(d, rel=TRACKER_PATH):
    return (d / rel).read_bytes().startswith(b"\xef\xbb\xbf")

def mode(d, rel=TRACKER_PATH):
    return (d / rel).stat().st_mode & 0o777

def default_mode():
    um = os.umask(0); os.umask(um)
    return 0o666 & ~um

def leftovers(d):
    return sorted(p.name for p in (d / "job-search").iterdir() if p.name.startswith("tmp"))


# ---------- checking ----------

passed, failed, skipped = 0, [], []
WIN = os.name == "nt"   # Windows has no POSIX file modes: chmod only sets or clears the read-only flag

for _s in (sys.stdout, sys.stderr):   # a detail line can hold an emoji; Windows' console encoding can't print it
    try: _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError): pass

def skip(name, why):
    skipped.append(name)
    print(f"  skip  {name} ({why})")

def check(name, ok, detail=""):
    global passed
    if ok:
        passed += 1
        print(f"  ok    {name}")
    else:
        failed.append(name)
        print(f"  FAIL  {name}")
        if detail:
            print("        " + str(detail).replace("\n", "\n        ")[:1500])


def tracker_cases():
    print("Tracker")

    # A fresh tracker, start to finish
    d = folder("fresh")
    out = run(d, CREATE)
    check("create writes the header and nothing else", out == "created" and text(d).strip() == H14.strip(), out)
    check("a new tracker starts with Excel's mark, so Excel shows accented names correctly", has_mark(d),
          (d / TRACKER_PATH).read_bytes()[:12])
    out = run(d, add([
        {"company": "Fernhill", "role": "Senior Product Manager, Growth", "location": "New York (hybrid)",
         "comp": "$175k to $205k", "url": "https://example.com/1", "source": "linkedin", "score": "4"},
        {"company": "Northstar Learning", "role": "Senior PM, Retention", "location": "Remote (US)",
         "url": "https://example.com/2", "source": "linkedin", "score": "4"},
        {"company": "Acme", "role": "Product Lead", "url": "https://example.com/3", "source": "ats-board", "score": "3"},
        {"company": "Acme", "role": "Senior Product Manager", "url": "https://example.com/4", "source": "ats-board", "score": "3"},
    ]))
    check("add four prospects", out.startswith("added 4"), out)
    out = run(d, add([{"company": "Fernhill, Inc.", "role": "Sr. PM - Growth", "source": "linkedin", "score": "4"}]))
    check("a near-identical company and title is a duplicate", out.startswith("added 0") and "Fernhill, Inc." in out, out)
    out = run(d, update("Fernhill", "Senior PM, Growth", "applied"))
    check("update by normalized title", "updated: Fernhill | Senior Product Manager, Growth -> applied" in out, out)
    out = run(d, update("Acme", "Product Manager", "applied"))
    check("a vague title with two open rows asks which one", out.startswith("AMBIGUOUS"), out)
    out = run(d, update("Acme", "Product Lead", "applied", on_date="2026-10-05"))
    out += "\n" + run(d, update("Acme", "Senior Product Manager", "applied"))
    check("each exact title updates its own row", out.count("updated: Acme") == 2 and "2026-10-05" in text(d), out)
    out = run(d, update("Fernhill", "Senior PM, Growth", "screening", next_date="2026-10-08"))
    check("a booked screen leaves furthest stage at applied", "furthest: applied" in out, out)
    out = run(d, update("Fernhill", "Senior PM, Growth", "screening", completed=True))
    check("the screen happened: furthest stage moves to screening", "furthest: screening" in out, out)
    out = run(d, reject("Acme"))
    check("a general no with two open applications asks which one", "WHICH ONE?" in out and "NO EXACT" not in out, out)
    out = run(d, reject("Acme", "Product Lead", stage_note="before any screen"))
    check("a no that names the role marks that row", out.startswith("rejected: Product Lead"), out)
    out = run(d, reject("Acme"))
    check("a general no with one open application left marks it", out.startswith("rejected: Senior Product Manager"), out)
    out = run(d, reject("Northstar Learning"))
    check("a company that's only a prospect asks first", out.startswith("ONLY PROSPECTS"), out)
    out = run(d, reject("Northstar Learning", include_prospects=True, date_applied="2026-10-01"))
    check("a confirmed prospect is rejected, and the message says the stage moved up",
          "rejected: Senior PM, Retention | furthest stage now applied (was prospect)" in out, out)
    out = run(d, setvar(RECORD, "company, role", ("Fernhill", "Product Lead")))
    check("recording a rejection at a tracked company sends you to the rejection snippet", out.startswith("ALREADY TRACKED"), out)
    out = run(d, setvar(RECORD, "company, role", ("Tallyho", "Product Manager")))
    check("record an untracked role as rejected", out.startswith("added as rejected: Tallyho"), out)
    out = run(d, READBACK)
    check("read back runs", "by status:" in out and "follow-ups:" in out, out)

    # Header-only and empty files (the 0.4.1 fix)
    d = folder("header_only", H14)
    out = run(d, update("Acme", "PM", "applied"))
    check("header-only file: update says it isn't tracked and keeps the header",
          out.startswith("NOT TRACKED") and text(d) == H14, out)
    d = folder("empty", "")
    out = run(d, add([{"company": "Acme", "role": "PM", "source": "linkedin", "score": "4"}]))
    check("empty file: add writes a header and the row",
          out.startswith("added 1") and text(d).splitlines()[0] == H14.strip() and len(text(d).splitlines()) == 2, out)

    # A missing tracker is never treated as an empty one (the wrong folder, or a copy that wasn't made)
    d = folder("missing")
    out = run(d, add([{"company": "Acme", "role": "PM", "source": "linkedin", "score": "4"}]))
    check("a missing tracker: add stops and creates nothing", out.startswith("NO TRACKER") and not (d / TRACKER_PATH).exists(), out)

    # A shorter or longer company name
    before = H14 + "Northstar Learning,\"Senior Product Manager, Retention\",Remote (US),,u,linkedin,prospect,4,2026-10-01,,2026-10-01,,prospect,\n"
    d = folder("short_name", before)
    out = run(d, reject("Northstar"))
    check("a rejection from 'Northstar' finds 'Northstar Learning' and asks first, nothing written",
          out.startswith("CHECK FIRST") and "Northstar Learning" in out and text(d) == before, out)
    out = run(d, update("Northstar", "Senior PM, Retention", "applied"))
    check("an update for 'Northstar' asks first, nothing written",
          out.startswith("CHECK FIRST") and "Northstar Learning" in out and text(d) == before, out)
    out = run(d, setvar(RECORD, "company, role", ("Northstar", "")))
    check("recording 'Northstar' as a new rejected row is held until the user confirms",
          out.startswith("CHECK FIRST, not added") and text(d) == before, out)
    out = run(d, add([{"company": "Northstar", "role": "Product Lead", "source": "linkedin", "score": "4"}]))
    check("adding a prospect at 'Northstar' is held until the user confirms",
          out.startswith("added 0") and "CHECK FIRST" in out and "Northstar Learning" in out, out)
    out = run(d, reject("North"))
    check("a name that only shares letters ('North') is not a near match", out.startswith("NO MATCH"), out)
    d = folder("long_name", H14 + "Northstar,PM,Remote,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,,applied,\n")
    out = run(d, reject("Northstar Learning, Inc."))
    check("the longer name finds the shorter one too", out.startswith("CHECK FIRST") and "'Northstar'" in out, out)
    out = run(d, setvar(setvar(RECORD, "company, role", ("Northstar Learning", "")), "confirmed_new_company", True))
    check("after the user says it's a different company, it's recorded", out.startswith("added as rejected: Northstar Learning"), out)

    # File permissions survive a save
    d = folder("perms", H14 + "Fernhill,Senior PM,NYC,,u,linkedin,applied,4,2026-09-01,2026-09-02,2026-09-20,,applied,\n")
    (d / TRACKER_PATH).chmod(0o644)
    want = mode(d)   # 0o644, or 0o666 on Windows, where only the read-only flag exists
    out = run(d, update("Fernhill", "Senior PM", "screening"))
    check("a save keeps the tracker's permissions", out.startswith("updated:") and mode(d) == want, oct(mode(d)))
    d = folder("perms_new")
    run(d, CREATE)
    check("a new tracker gets normal permissions, not owner-only", mode(d) == default_mode(), oct(mode(d)))

    # The finished-row fallback
    before = H12 + "Acme,Senior Product Manager,Remote,,u,linkedin,rejected,3,2026-08-01,2026-08-02,2026-08-20,2026-08-20: rejected\n"
    d = folder("finished_rejected", before)
    out = run(d, update("Acme", "Product Lead", "applied"))
    check("a new role where the only row is rejected: not tracked, old row untouched",
          out.startswith("NOT TRACKED as an open role") and text(d) == before, out)
    before = H12 + "Acme,Senior Product Manager,Remote,,u,linkedin,skipped,3,2026-08-01,,2026-08-20,\n"
    d = folder("finished_skipped", before)
    out = run(d, update("Acme", "Head of Growth", "screening", next_date="2026-10-09"))
    check("a new role where the only row is skipped: not tracked, old row untouched",
          out.startswith("NOT TRACKED as an open role") and text(d) == before, out)
    before = H14 + "Acme,Senior Product Manager,NY,,u,linkedin,prospect,4,2026-10-01,,2026-10-01,,prospect,\n"
    d = folder("one_open", before)
    out = run(d, update("Acme", "Staff PM", "applied"))
    check("one open row with a different title: CHECK FIRST, nothing written",
          out.startswith("CHECK FIRST") and text(d) == before, out)
    out = run(d, update("Acme", "Staff PM", "applied", confirmed_row=True))
    check("after the user confirms, it updates that row",
          "updated: Acme | Senior Product Manager -> applied" in out and ",applied," in text(d), out)
    # "I applied to Acme" with only the company named: one open row and one finished row at Acme
    before = (H14 + "Acme,Senior Product Manager,NY,,u,linkedin,prospect,4,2026-10-01,,2026-10-01,,prospect,\n"
              + "Acme,Data Analyst,NY,,u,linkedin,rejected,3,2026-08-01,2026-08-02,2026-08-20,,applied,\n")
    d = folder("company_only", before)
    out = run(d, update("Acme", "", "applied", confirmed_row=True))
    check("company named only (role \"\", confirmed): the one open row is updated, the finished row is left alone",
          "updated: Acme | Senior Product Manager -> applied" in out and "Acme,Data Analyst,NY,,u,linkedin,rejected" in text(d), out)

    # Excel "CSV UTF-8" adds a start mark (BOM)
    d = folder("bom", "\ufeff" + H12 + "Fernhill,Senior PM,NYC,,u,linkedin,screening,4,2026-09-01,2026-09-02,2026-09-20,\n")
    out = run(d, update("Fernhill", "Senior PM", "interview"))
    body = (d / TRACKER_PATH).read_text(encoding="utf-8-sig")
    header = body.splitlines()[0]
    check("Excel CSV UTF-8 file: update finds the row", out.startswith("updated: Fernhill"), out)
    check("Excel CSV UTF-8 file: one clean company column after the write",
          header.startswith("company,") and header.count("company") == 1 and "\ufeff" not in body, header)
    check("Excel CSV UTF-8 file: the start mark is kept on save", has_mark(d), (d / TRACKER_PATH).read_bytes()[:12])
    out = run(d, add([{"company": "Fernhill", "role": "Senior PM", "source": "linkedin", "score": "4"}]))
    check("Excel CSV UTF-8 file: duplicates are still caught", out.startswith("added 0"), out)
    d = folder("no_mark", H14 + "Fernhill,Senior PM,NYC,,u,linkedin,applied,4,2026-09-01,2026-09-02,2026-09-20,,applied,\n")
    run(d, update("Fernhill", "Senior PM", "screening"))
    check("a file without the mark is written without one", not has_mark(d), (d / TRACKER_PATH).read_bytes()[:12])

    # A 0.4 tracker's booked dates live in notes
    d = folder("dates_in_notes", H12
               + "Fernhill,Senior PM,NYC,,u,LinkedIn,interview,5,10/1/2026,10/1/2026,10/2/2026,\"Evaluated 2026-10-01: 4.6/5. Hiring manager round 2026-10-13 2pm\"\n"
               + "Northstar Learning,PM,Remote,,u,LinkedIn,screening,4,10/1/2026,10/1/2026,10/2/2026,\"screen 10/20/2026, then a panel 2026-10-22\"\n"
               + "Brightloop,Senior PM,Remote,,u,LinkedIn,applied,4,10/1/2026,10/1/2026,10/2/2026,\"recruiter call 2026-10-15\"\n"
               + "Tallyho,PM,Remote,,u,LinkedIn,interview,4,9/1/2026,9/1/2026,9/2/2026,\"screen held 2026-09-30\"\n"
               + "Acme,PM,Remote,,u,LinkedIn,screening,4,10/1/2026,10/1/2026,10/2/2026,\"screen Tuesday the 13th\"\n")
    out = run(d, update("Brightloop", "Senior PM", "screening"))
    import csv as _csv, io as _io
    nd = {r["company"]: r["next_date"] for r in _csv.DictReader(_io.StringIO(text(d)))}
    check("0.4 notes: one clear future date on an active row becomes next_date, and the save says so",
          nd["Fernhill"] == "2026-10-13" and "next_date filled from notes" in out and "Fernhill" in out, out)
    check("0.4 notes: two dates, a past date, a date with no year, and a cold application stay blank",
          nd["Northstar Learning"] == nd["Tallyho"] == nd["Acme"] == nd["Brightloop"] == "", nd)
    out = run(d, update("Fernhill", "Senior PM", "interview", completed=True))
    check("0.4 notes: only the first 1.0 write fills dates", "filled from notes" not in out, out)

    # Excel dates
    d = folder("excel_dates", H14 + "Fernhill,Senior PM,NYC,,u,linkedin,interview,4,9/1/2026,9/2/2026,9/15/2026,,screening,\n"
                                  "Northstar Learning,PM,Remote,,u,linkedin,screening,4,9/1/26,9/2/26,9/5/26,,applied,10/13/26\n")
    out = run(d, READBACK)
    check("Excel dates: a quiet interview still gets its follow-up",
          "('Fernhill', 'Senior PM', 'interview', 21, 'chase or close')" in out, out)
    check("Excel dates: an interview on 10/13/26 still shows as coming up", "('2026-10-13', 'Northstar Learning', 'PM')" in out, out)
    d = folder("excel_dates_reject", H12 + "Acme,PM,Remote,,u,linkedin,applied,4,10/2/2026,10/2/2026,10/2/2026,\n")
    out = run(d, reject("Acme", email_date="2026-10-05"))
    check("Excel dates: a rejection finds an application from 10/2/2026", out.startswith("rejected: PM"), out)
    check("Excel dates: written back as YYYY-MM-DD", "2026-10-02" in text(d) and "10/2/2026" not in text(d), text(d))

    # Rejection dates typed the way an email shows them, and a second email for a finished role
    d = folder("email_date_mdy", H14 + "Acme,PM,NY,,u,linkedin,applied,4,2026-10-01,2026-10-02,2026-10-02,,applied,\n")
    out = run(d, reject("Acme", email_date="10/5/2026"))
    check("a rejection dated 10/5/2026 finds the application from Oct 2", out.startswith("rejected: PM"), out)
    before = H14 + ("Acme,Senior PM,NY,,u,linkedin,rejected,4,2026-08-01,2026-08-02,2026-08-20,,applied,\n"
                    "Acme,Product Lead,NY,,u,linkedin,applied,4,2026-09-01,2026-09-02,2026-09-02,,applied,\n")
    d = folder("finished_exact", before)
    out = run(d, reject("Acme", "Senior PM", email_date="2026-10-05"))
    check("a rejection for a role already marked rejected lists the company's rows, nothing written",
          out.startswith("NO MATCH") and "rows there" in out and "'rejected'" in out and text(d) == before, out)

    # Windows' plain "CSV" save (cp1252)
    d = folder("cp1252", H12 + "Café Société,Senior PM,Paris,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,\n", enc="cp1252")
    out = run(d, update("Café Société", "Senior PM", "screening"))
    check("Windows CSV (cp1252): reads, updates, and writes UTF-8",
          out.startswith("updated: Café Société") and "Café Société" in text(d), out)

    # Excel on a Mac saves plain CSV in Mac Roman: stop instead of misreading it
    before = (H12 + "Café Labs,PM,NYC,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,Dana\u2019s team\n").encode("mac_roman")
    d = folder("mac_roman")
    (d / TRACKER_PATH).write_bytes(before)
    out = run(d, update("Café Labs", "PM", "screening"))
    check("Excel on a Mac, plain CSV: stops, says to save as CSV UTF-8 and close Excel, file untouched",
          out.startswith("CAN'T READ") and "CSV UTF-8" in out and "close it in Excel" in out
          and (d / TRACKER_PATH).read_bytes() == before, out)
    # Other accents from a Mac's plain CSV (ñ, ó, ü) also stop, while the same names saved on Windows still work
    before = (H12 + "Muñoz Labs,PM,NYC,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,met María López\n").encode("mac_roman")
    d = folder("mac_roman_n")
    (d / TRACKER_PATH).write_bytes(before)
    out = run(d, update("Muñoz Labs", "PM", "screening"))
    check("Excel on a Mac, plain CSV with ñ and ó: stops, file untouched",
          out.startswith("CAN'T READ") and (d / TRACKER_PATH).read_bytes() == before, out)
    for i, name in enumerate(("Müller Analytics", "Søren Labs", "Großmann AG", "Élise Labs")):
        d = folder(f"mac_roman_{i}")
        (d / TRACKER_PATH).write_bytes((H12 + name + ",PM,NYC,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01," + chr(10)).encode("mac_roman"))
        out = run(d, update(name, "PM", "screening"))
        check("Excel on a Mac, plain CSV with " + name.split()[0] + ": stops", out.startswith("CAN'T READ"), out)
    d = folder("cp1252_n", H12 + "Muñoz Labs,PM,NYC,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,met María López \u2013 Dana\u2019s pick\n", enc="cp1252")
    out = run(d, update("Muñoz Labs", "PM", "screening"))
    check("Windows CSV with ñ, ó, an en dash, and an apostrophe: still updates", out.startswith("updated: Muñoz Labs"), out)
    # The same file read by a file tool first: é arrives as the replacement character, in valid UTF-8
    before = H12 + "Caf\ufffd Labs,PM,NYC,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,Dana\ufffds team\n"
    d = folder("replacement_char", before)
    out = run(d, update("Caf\ufffd Labs", "PM", "screening"))
    check("a copy made by a file tool from a Mac CSV (replacement characters): stops, nothing written",
          out.startswith("CAN'T READ") and "close it in Excel" in out and text(d) == before, out)

    # LibreOffice with Semicolon ticked as a separator: the notes split, the header gains a column with no name,
    # and every value after the split sits under the wrong heading. Same column count on every row, so only the header shows it.
    mangled = (H14.replace("next_date\n", "next_date,\n")
               + "Fernhill Logistics,Senior Project Manager,,,,pasted,applied,,2026-10-25,2026-10-25,2026-10-25,"
                 "2026-10-25: Recruiter: Ren\u00e9e Dubois, phone screen Thursday,applied,,\n")
    d = folder("libreoffice_semicolon", mangled)
    out = run(d, update("Fernhill Logistics", "Senior Project Manager", "screening"))
    check("a header with a column with no name (LibreOffice split the notes): stops, names the separator, file untouched",
          out.startswith("CAN'T READ") and "Semicolon" in out and text(d) == mangled, out)
    dup = H14.replace("next_date\n", "next_date,notes\n") + "Acme,PM,NYC,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,a,,,b\n"
    d = folder("duplicate_header", dup)
    out = run(d, update("Acme", "PM", "screening"))
    check("a header with the same column name twice: stops, file untouched", out.startswith("CAN'T READ") and text(d) == dup, out)

    # A new value that already holds the replacement character (a mangled dash in a pasted title) is never saved
    d = folder("new_value_replacement_char", H14)
    out = run(d, add([{"company": "Brightloop", "role": "Senior PM \ufffd Growth", "source": "linkedin", "score": "4"}]))
    check("a new value with the replacement character isn't saved, so the tracker stays readable",
          out.startswith("NOT SAVED") and text(d) == H14, out)

    # Windows' plain CSV read by a file tool first (Cowork): the message names CSV UTF-8, not a Mac
    before = (H12 + "Café Société,PM,NYC,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,Dana\u2019s team" + chr(10)
              ).encode("cp1252").decode("utf-8", "replace")
    d = folder("cp1252_via_file_tool", before)
    out = run(d, update("Caf\ufffd Soci\ufffdt\ufffd", "PM", "screening"))
    check("a copy made by a file tool from a Windows CSV: stops, says CSV UTF-8 without blaming a Mac, nothing written",
          out.startswith("CAN'T READ") and "CSV UTF-8" in out and "Mac" not in out and text(d) == before, out)

    # Excel on a Mac can end rows with a bare carriage return; a copy that loses them runs every row into the header
    before = (H12 + "Fernhill,Senior PM,NYC,,u,linkedin,screening,4.6,2026-10-01,2026-10-01,2026-10-01," + chr(10)
              + "Acme,PM,Remote,,u,ats-board,prospect,4,2026-10-02,,2026-10-02," + chr(10)).replace(chr(10), "")
    d = folder("rows_ran_together", before)
    out = run(d, add([{"company": "Brightloop", "role": "PM", "source": "linkedin", "score": "4"}]))
    check("rows run together into the header: stops instead of saving a one-row tracker",
          out.startswith("CAN'T READ") and "ran together" in out and text(d) == before, out)
    d = folder("cr_only", (H12 + "Fernhill,Senior PM,NYC,,u,linkedin,screening,4.6,2026-10-01,2026-10-01,2026-10-01," + chr(10)
                           ).replace(chr(10), chr(13)))
    out = run(d, update("Fernhill", "Senior PM", "interview"))
    check("a file with bare carriage returns, read directly, still updates", out.startswith("updated: Fernhill"), out)
    for i, day in enumerate(("10/1/26", "01.10.2026", "1-Oct-26")):   # Excel for Mac writes dates the way the Mac shows them
        before = (H12 + "Fernhill,Senior PM,NYC,,u,linkedin,screening,4.6," + ",".join([day] * 3) + "," + chr(10)
                  + "Acme,PM,Remote,,u,ats-board,prospect,4," + day + ",," + day + "," + chr(10)).replace(chr(10), "")
        d = folder(f"rows_ran_together_{i}", before)
        out = run(d, add([{"company": "Brightloop", "role": "PM", "source": "linkedin", "score": "4"}]))
        check("rows run together with dates like " + day + ": stops too",
              out.startswith("CAN'T READ") and "ran together" in out and text(d) == before, out)
    before = (H12 + "Acme,PM,Remote,,https://example.com/jobs/1,ats-board,prospect,4,,,," + chr(10)).replace(chr(10), "")
    d = folder("rows_ran_together_link", before)
    out = run(d, add([{"company": "Brightloop", "role": "PM", "source": "linkedin", "score": "4"}]))
    check("rows run together with no dates but a link: stops too",
          out.startswith("CAN'T READ") and "ran together" in out and text(d) == before, out)
    before = (H12 + "Fernhill,Senior PM,NYC,,,linkedin,screening,4.6,15/10/2026,15/10/2026,15/10/2026,coffee chat" + chr(10)
              + "Acme,PM,Remote,,,ats-board,prospect,4,16/10/2026,,16/10/2026," + chr(10)).replace(chr(10), "")
    d = folder("rows_ran_together_day_first", before)
    out = run(d, add([{"company": "Brightloop", "role": "PM", "source": "linkedin", "score": "4"}]))
    check("rows run together with day-first dates and no links: stops on the status",
          out.startswith("CAN'T READ") and "ran together" in out and text(d) == before, out)

    # The header kept its line but the rows ran together into one (run 10a): a save would keep 1 row of 3
    rows3 = ("Fernhill,Senior PM,NYC,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,,applied," + chr(10)
             + "Acme,PM,Remote,,u,ats-board,prospect,4,2026-10-02,,2026-10-02,,prospect," + chr(10)
             + "Brightloop,Senior PM,Remote,,u,linkedin,screening,4,2026-10-03,2026-10-03,2026-10-03,,applied," + chr(10))
    before = H14 + rows3.replace(chr(10), "")
    d = folder("rows_ran_together_header_intact", before)
    out = run(d, update("Fernhill", "Senior PM", "screening"))
    out2 = run(d, add([{"company": "Tallyho", "role": "PM", "source": "linkedin", "score": "4"}]))
    check("header intact, rows run together into one: update and add stop, and all three rows are untouched",
          out.startswith("CAN'T READ") and "ran together into one" in out and out2.startswith("CAN'T READ")
          and "ran together into one" in out2 and text(d) == before, out + chr(10) + out2)
    (d / TRACKER_PATH).write_text(H14 + rows3, encoding="utf-8")
    out = run(d, update("Fernhill", "Senior PM", "screening"))
    check("written again with each row on its own line, the update goes through and keeps all three rows",
          out.startswith("updated: Fernhill") and len(text(d).splitlines()) == 4, out + chr(10) + text(d))
    before = H14.replace(chr(10), "") + rows3
    d = folder("header_ran_into_first_row", before)
    out = run(d, update("Acme", "PM", "applied"))
    check("the header ran into the first row and the rest kept their lines: stops, nothing written",
          out.startswith("CAN'T READ") and "ran together into the header" in out and text(d) == before, out)

    # A 0.4 folder the rename couldn't reach: the snippets use applications.csv
    d = WORK / "old_names"
    (d / "job-search").mkdir(parents=True)
    (d / "job-search/applications.csv").write_text(
        H12 + "Fernhill,Senior PM,NYC,,u,LinkedIn,applied,4,2026-10-01,2026-10-01,2026-10-01,\n", encoding="utf-8")
    out = run(d, update("Fernhill", "Senior PM", "screening", date_applied="2026-10-01"))
    check("0.4 names: an update lands in applications.csv and no job-tracker.csv appears",
          out.startswith("updated: Fernhill") and ",screening," in (d / "job-search/applications.csv").read_text(encoding="utf-8")
          and not (d / TRACKER_PATH).exists(), out)

    # A prospect that goes straight to a screen
    d = folder("prospect_to_screen", H14 + "Northstar Learning,PM,Remote,,u,linkedin,prospect,4,2026-10-01,,2026-10-01,,prospect,\n")
    out = run(d, update("Northstar Learning", "PM", "screening", next_date="2026-10-15"))
    check("a prospect booked for a screen with no application date: the snippet says to ask when they applied",
          "updated:" in out and "ASK: when did they apply?" in out, out)
    out = run(d, update("Northstar Learning", "PM", "screening", date_applied="10/2/2026"))
    check("with the date given, it's saved and nothing more is asked",
          "ASK:" not in out and ",2026-10-02," in text(d), out)
    d = folder("recruiter_first", H14 + "Tallyho,PM,Remote,,u,linkedin,prospect,4,2026-10-01,,2026-10-01,,prospect," + chr(10))
    out = run(d, update("Tallyho", "PM", "screening", source="recruiter"))
    check("the recruiter reached out first: source becomes recruiter and nothing more is asked",
          out.startswith("updated: Tallyho") and "ASK:" not in out and ",recruiter,screening," in text(d), out)

    # The near-miss rejection title
    before = H14 + "Fernhill,Senior Product Manager,NY,,u,linkedin,applied,4.6,2026-09-20,2026-09-21,2026-09-21,,applied,\n"
    d = folder("near_miss", before)
    out = run(d, reject("Fernhill", "Senior Product Manager, Growth", email_date="2026-10-05"))
    check("a rejection naming a close title asks which one instead of saying nothing is open",
          "NO EXACT MATCH" in out and "WHICH ONE?" in out and "Senior Product Manager" in out and text(d) == before, out)

    # Two prospects at the company: the confirmed one is rerun with its title as role, so it isn't asked about again
    d = folder("two_prospects", H14 + 'Northstar Learning,"Senior PM, Retention",Remote,,u,linkedin,prospect,4,2026-10-01,,2026-10-01,,prospect,' + chr(10)
                                    + "Northstar Learning,Product Lead,Remote,,u,linkedin,prospect,4,2026-10-01,,2026-10-01,,prospect," + chr(10))
    out = run(d, reject("Northstar Learning"))
    out2 = run(d, reject("Northstar Learning", "Senior PM, Retention", include_prospects=True))
    status = {r["role"]: r["status"] for r in _csv.DictReader(_io.StringIO(text(d)))}
    check("two prospects: the snippet says to rerun with role set, and that rerun rejects the confirmed one without asking again",
          out.startswith("ONLY PROSPECTS") and "role set to that title" in out and out2.startswith("rejected: Senior PM, Retention")
          and status == {"Senior PM, Retention": "rejected", "Product Lead": "prospect"}, (out, out2, status))

    # "PM" means the user's kind of PM: product by default, project or program from the profile, or left as it is (None)
    project, either = setvar(BASE, "PM_MEANS", "project manager"), setvar(BASE, "PM_MEANS", None)
    applied = ",NY,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,,applied," + chr(10)
    before = H14 + "Fernhill,Senior Product Manager" + applied
    d = folder("pm_product", before)
    out = run(d, update("Fernhill", "Senior PM", "screening"), base=project)
    check("PM_MEANS project manager: 'Senior PM' isn't an exact match for Senior Product Manager; asks first, nothing written",
          out.startswith("CHECK FIRST") and text(d) == before, out)
    out = run(d, update("Fernhill", "Senior PM", "screening"), base=either)
    d2 = folder("pm_both", H14 + "Acme,Senior Product Manager" + applied + "Acme,Senior Project Manager" + applied)
    before2 = text(d2)
    out2 = run(d2, update("Acme", "Senior PM", "screening"), base=either)
    check("PM_MEANS None: 'Senior PM' matches neither title exactly; asks first (one open row or two), nothing written",
          out.startswith("CHECK FIRST") and out2.startswith("AMBIGUOUS") and text(d) == before and text(d2) == before2,
          out + chr(10) + out2)
    out = run(d, update("Fernhill", "Senior PM", "screening"))
    check("PM_MEANS default: 'Senior PM' updates the Senior Product Manager row",
          "updated: Fernhill | Senior Product Manager -> screening" in out, out)
    out = run(d2, update("Acme", "Senior PM", "screening"), base=project)
    status = {r["role"]: r["status"] for r in _csv.DictReader(_io.StringIO(text(d2)))}
    check("PM_MEANS project manager: 'Senior PM' updates the Senior Project Manager row, not the Senior Product Manager one",
          "updated: Acme | Senior Project Manager -> screening" in out
          and status == {"Senior Product Manager": "applied", "Senior Project Manager": "screening"}, (out, status))

    # Accented and emoji names, with Windows' default encoding and a cp1252 console
    d = folder("windows", H14 + "Fernhill,Senior Product Manager,NY,,u,linkedin,applied,4.6,2026-09-20,2026-09-21,"
                                "2026-09-21,Dana said \u201cwe\u2019ll move fast\u201d,applied,\n")
    out = run(d, add([{"company": "Łódź Labs", "role": "PM, Growth \U0001F680", "url": "u", "source": "linkedin", "score": "3"}]),
              pre=WINDOWS, env={"PYTHONIOENCODING": "cp1252"})
    check("Windows: curly quotes, accents, and emoji read, write, and print",
          out.startswith("added 1") and "Łódź Labs" in text(d) and "\u201cwe\u2019ll" in text(d) and not leftovers(d), out)
    out = run(d, update("Łódź Labs", "PM, Growth \U0001F680", "applied"), pre=WINDOWS, env={"PYTHONIOENCODING": "cp1252"})
    check("Windows: an update on that row prints without crashing", out.startswith("updated:"), out)

    # Columns the user added (a 0.4 tracker with an extra column)
    d = folder("user_columns", "company,role,location,comp,url,source,status,score,date_added,date_applied,last_update,notes,my_priority\n"
               'Fernhill,Senior PM,NYC,,u,linkedin,interview,4,2026-09-01,2026-09-02,2026-09-20,"note, with comma",high\n'
               "Brightloop,Senior PM,Remote,,u,linkedin,prospect,3,2026-09-05,,2026-09-05,,\n")
    out = run(d, update("Brightloop", "Senior PM", "applied"))
    lines = text(d).splitlines()
    check("0.4 tracker: the user's column stays, the two new columns are added at the end",
          out.startswith("updated: Brightloop") and lines[0].endswith(",notes,my_priority,furthest_stage,next_date"), lines[0])
    check("0.4 tracker: values and quoted commas survive",
          '"note, with comma",high,screening,' in lines[1], lines[1])

    # The file is open in Excel
    before = H14 + "Fernhill,Senior PM,NYC,,u,linkedin,applied,4,2026-09-01,2026-09-02,2026-09-20,,applied,\n"
    d = folder("locked", before)
    out = run(d, update("Fernhill", "Senior PM", "screening"), pre=EXCEL_LOCK)
    check("a save blocked by Excel says to close the file, and leaves no temp file",
          "NOT SAVED" in out and "close it" in out and text(d) == before and not leftovers(d), out)

    # A folder this session can't write to (a sandboxed session): NOT SAVED, not a raw traceback
    name = "a folder this session can't write to says NOT SAVED and names the folder's access, with no traceback"
    if WIN:
        skip(name, "chmod can't make a Windows folder unwritable; the Excel-lock check covers a refused save there")
    else:
        d = folder("readonly_folder", before)
        jd = (d / TRACKER_PATH).parent
        os.chmod(jd, 0o555)
        try:
            out = run(d, update("Fernhill", "Senior PM", "screening"))
        finally:
            os.chmod(jd, 0o755)
        check(name, "NOT SAVED" in out and "folder's access" in out and "Traceback" not in out and text(d) == before
              and not leftovers(d), out)


EXPORT = '''Notes:
"When exporting your connection data, you may notice that some of the email addresses are missing."

First Name,Last Name,URL,Email Address,Company,Position,Connected On
Priya,Shah,https://www.linkedin.com/in/priya,,"Fernhill, Inc.",Senior Talent Partner,12 Mar 2021
Marco,Diaz,https://www.linkedin.com/in/marco,,Fernhill,"Director, Product Design",01 Jan 2020
Dana,Reyes,https://www.linkedin.com/in/dana,,Fernhill,Talent Acquisition Partner,02 Feb 2022
José,Núñez,https://www.linkedin.com/in/jose,,Fernhill,Group Product Manager \U0001F680,03 Mar 2023
Tom,Wu,https://www.linkedin.com/in/tom,,Northstar Learning,Group Product Manager,05 May 2019
Lee,Park,https://www.linkedin.com/in/lee,,Fernhill Labs,Engineer,05 May 2019
Ana,Ruiz,https://www.linkedin.com/in/ana,,The Brightloop Company,VP of Product,05 May 2019
'''
PROFILE = """# Job Search Profile

## Companies to Watch

- **[Company]:** board URL
- **Brightloop:** boards.greenhouse.io/brightloop

## Background
- **Name:** Sam Okafor
"""
CTRACKER = (H14 + "Fernhill,Senior PM,NYC,,u,linkedin,applied,4,2026-10-01,2026-10-01,2026-10-01,,applied,\n"
            "Northstar Learning,PM,Remote,,u,linkedin,rejected,4,2026-10-01,2026-10-01,2026-10-01,,applied,\n")
CONTACTS_PATH = "job-search/contacts.csv"

def contacts_folder(name, tracker=CTRACKER, enc="utf-8", export=EXPORT, contacts=None):
    files = {"Connections.csv": export, "job-search/search-profile.md": PROFILE}
    if contacts:
        files[CONTACTS_PATH] = contacts
    return folder(name, tracker, enc=enc, files=files)

def contact_rows(d):
    import csv, io
    return {r["name"]: r for r in csv.DictReader(io.StringIO(text(d, CONTACTS_PATH)))}


def contacts_cases():
    print("Contacts import")
    FIRST = setvar(IMPORT, "FIRST_IMPORT", True)    # the user's folder has no contacts.csv yet

    d = contacts_folder("contacts")
    out = run(d, FIRST, base=False, pre=WINDOWS, env={"PYTHONIOENCODING": "cp1252"})
    rows = contact_rows(d) if (d / CONTACTS_PATH).exists() else {}
    check("skips LinkedIn's note lines and adds people at open and watched companies only",
          out.startswith("7 connections read; 5 added at 2 companies") and "Tom Wu" not in rows and "Lee Park" not in rows, out)
    check("accented names and emoji survive Windows' default encoding",
          "José Núñez" in rows and "\U0001F680" in rows.get("José Núñez", {}).get("title", ""), out)
    check("a new contacts file starts with Excel's mark", (d / CONTACTS_PATH).exists() and has_mark(d, CONTACTS_PATH), out)
    check("near misses are listed, not added", "near misses to ask about: Fernhill Labs (vs Fernhill)" in out, out)
    check("talent partners are recruiters, not leaders",
          rows.get("Priya Shah", {}).get("tags") == "recruiter" and rows.get("Dana Reyes", {}).get("tags") == "recruiter",
          {k: v["tags"] for k, v in rows.items()})
    check("a director of product design is design and leader", rows.get("Marco Diaz", {}).get("tags") == "design;leader",
          {k: v["tags"] for k, v in rows.items()})
    check("a product manager, in the user's own function, is tagged same-role", rows.get("José Núñez", {}).get("tags") == "same-role",
          {k: v["tags"] for k, v in rows.items()})
    out = run(d, IMPORT, base=False)
    check("a rerun adds nobody twice", out.startswith("7 connections read; 0 added"), out)

    # Another field: SAME_FUNCTION set for project management, and the tag is still same-role
    d = contacts_folder("contacts_project", export=EXPORT + "Rae,Moreno,https://www.linkedin.com/in/rae,,Fernhill,Senior Project Manager,04 Apr 2024\n")
    out = run(d, setvar(FIRST, "SAME_FUNCTION", r"project manager|project management|program manager|delivery manager|\bpm\b"),
              base=False)
    rows = contact_rows(d) if (d / CONTACTS_PATH).exists() else {}
    check("SAME_FUNCTION for project management: a Senior Project Manager is same-role, a product manager isn't",
          rows.get("Rae Moreno", {}).get("tags") == "same-role" and rows.get("José Núñez", {}).get("tags", "same-role") == "",
          (out, {k: v["tags"] for k, v in rows.items()}))

    d = contacts_folder("contacts_bom", tracker="\ufeff" + CTRACKER)
    out = run(d, FIRST, base=False)
    check("a tracker saved as Excel CSV UTF-8 still works", " added at 2 companies" in out, out)

    d = contacts_folder("contacts_cp1252", tracker=CTRACKER.replace("Fernhill,", "Fernhill Café,", 1)
                        .replace(",Fernhill,", ",Fernhill Café,").replace('"Fernhill, Inc."', "Fernhill Café"), enc="cp1252",
                        export=EXPORT.replace(",Fernhill,", ",Fernhill Café,").replace('"Fernhill, Inc."', "Fernhill Café"))
    out = run(d, FIRST, base=False)
    check("a tracker saved as Windows CSV (cp1252) still works", "Fernhill Café:" in out, out)

    d = contacts_folder("contacts_user_column", contacts=
        "name,company,title,tags,closeness,linkedin_url,last_contact,next_move,next_date,notes,source,how_we_met\n"
        "Priya Shah,Fernhill,Talent,recruiter,close,,2026-09-01,follow up,,,added,product meetup\n")
    out = run(d, IMPORT, base=False)
    lines = text(d, CONTACTS_PATH).splitlines()
    check("the user's own column stays, with its values",
          lines[0].endswith(",source,how_we_met") and lines[1].endswith(",product meetup"), lines[:2])
    check("someone already in contacts isn't added again", sum(l.startswith("Priya Shah,") for l in lines) == 1, lines)

    d = contacts_folder("contacts_mark_and_mode", contacts=
        "\ufeffname,company,title,tags,closeness,linkedin_url,last_contact,next_move,next_date,notes,source\n"
        "Priya Shah,Fernhill,Talent,recruiter,close,,2026-09-01,follow up,,,added\n")
    (d / CONTACTS_PATH).chmod(0o644)
    want = mode(d, CONTACTS_PATH)
    out = run(d, IMPORT, base=False)
    body = (d / CONTACTS_PATH).read_text(encoding="utf-8-sig")
    check("contacts saved by Excel keep their start mark and permissions, with one clean name column",
          has_mark(d, CONTACTS_PATH) and mode(d, CONTACTS_PATH) == want and body.startswith("name,company,")
          and "\ufeff" not in body and body.count("Priya Shah,") == 1, out)

    d = contacts_folder("contacts_not_copied")
    out = run(d, IMPORT, base=False)
    check("no contacts.csv and not a first import: stops, writes nothing (a copy that wasn't made)",
          out.startswith("NO CONTACTS FILE") and not (d / CONTACTS_PATH).exists(), out)

    before = ("name,company,title,tags,closeness,linkedin_url,last_contact,next_move,next_date,notes,source" + chr(13)
              + "Priya Shah,Fernhill,Talent,recruiter,close,,,follow up,,coffee; offered an intro,added" + chr(13)
              + "Alex Kim,Brightloop,Mentor,helped-me,friendly,,,keep warm,,my first manager,gratitude-list" + chr(13)).replace(chr(13), "")
    d = contacts_folder("contacts_ran_together", contacts=before)
    out = run(d, IMPORT, base=False)
    check("a contacts.csv copy whose rows ran together: stops, file untouched",
          out.startswith("CAN'T READ") and "ran together" in out and text(d, CONTACTS_PATH) == before, out)
    before = ("name,company,title,tags,closeness,linkedin_url,last_contact,next_move,next_date,notes,source" + chr(10)
              + "Priya Shah,Fernhill,Talent,recruiter,,https://www.linkedin.com/in/priya,9/1/26,follow up,,,added" + chr(10)
              ).replace(chr(10), "")
    d = contacts_folder("contacts_ran_together_link", contacts=before)
    out = run(d, IMPORT, base=False)
    check("a contacts copy that ran together, caught by its link and date: stops, file untouched",
          out.startswith("CAN'T READ") and "ran together" in out and text(d, CONTACTS_PATH) == before, out)
    before = ("name,company,title,tags,closeness,linkedin_url,last_contact,next_move,next_date,notes,source" + chr(10)
              + ("Priya Shah,Fernhill,Talent,recruiter,close,,,follow up,,coffee; offered an intro,added" + chr(10)
                 + "Alex Kim,Brightloop,Mentor,helped-me,friendly,,,keep warm,,my first manager,gratitude-list" + chr(10)
                 + "Sam Lee,Fernhill,Engineer,engineering,loose,,,none,,,linkedin-export" + chr(10)).replace(chr(10), ""))
    d = contacts_folder("contacts_ran_together_header_intact", contacts=before)
    out = run(d, IMPORT, base=False)
    check("contacts.csv with its header intact but rows run together into one: stops, all three people untouched",
          out.startswith("CAN'T READ") and "ran together into one" in out and text(d, CONTACTS_PATH) == before, out)
    tracker = H14 + CTRACKER[len(H14):].replace(chr(10), "")
    d = contacts_folder("contacts_tracker_ran_together", tracker=tracker)
    out = run(d, FIRST, base=False)
    check("a tracker with its header intact but rows run together: the import stops before writing contacts",
          out.startswith("CAN'T READ") and "ran together into one" in out and not (d / CONTACTS_PATH).exists()
          and text(d) == tracker, out)

    d = contacts_folder("contacts_export_replacement_char", export=EXPORT.replace("José", "Jos\ufffd"))
    out = run(d, FIRST, base=False)
    check("an export copy with the replacement character: nothing saved, so contacts.csv stays readable",
          out.startswith("NOT SAVED") and not (d / CONTACTS_PATH).exists(), out)

    d = contacts_folder("contacts_wrong_file", export="first name,last name,url\nA,B,c\n")
    out = run(d, IMPORT, base=False)
    check("a file that isn't LinkedIn's export gets a clear message", "No 'First Name' header" in out, out)

    d = contacts_folder("contacts_replacement_char", tracker=CTRACKER.replace("Fernhill,", "Fernhill Caf\ufffd,", 1))
    out = run(d, IMPORT, base=False)
    check("a tracker with replacement characters stops the import, nothing written",
          out.startswith("CAN'T READ") and "close it in Excel" in out and not (d / CONTACTS_PATH).exists(), out)

    d = WORK / "contacts_old_names"
    (d / "job-search").mkdir(parents=True)
    (d / "Connections.csv").write_text(EXPORT, encoding="utf-8")
    (d / "job-search/profile.md").write_text(PROFILE, encoding="utf-8")
    (d / "job-search/applications.csv").write_text(CTRACKER, encoding="utf-8")
    out = run(d, FIRST, base=False)
    check("0.4 names: the import reads profile.md and applications.csv", " added at 2 companies" in out, out)


SCAN_PATH = "job-search/scan-history.csv"
SCAN_HEADER = "date_seen,company,role,url,source,tier"

def scan(calls, pm_means=False):
    """The scan history snippet, then the calls a scan makes (with PM_MEANS changed, if given)."""
    return (SCAN if pm_means is False else setvar(SCAN, "PM_MEANS", pm_means)) + "\n" + calls

def card(company, role, url="", source="linkedin", tier="STRONG"):
    return {"company": company, "role": role, "url": url, "source": source, "tier": tier}

def seen(cards):
    return f"print('SEEN', [(c['company'], c['role']) for c in seen_before({cards!r})])\n"

def earlier(cards):
    return f"print('EARLIER', [(c['company'], c['role'], d) for c, d in shown_earlier({cards!r})])\n"

def recorded(cards):
    return f"record({cards!r})\n"

def scan_text(d):
    p = d / SCAN_PATH
    return p.read_text(encoding="utf-8-sig") if p.exists() else ""

def scan_rows(d):
    import csv, io
    return list(csv.DictReader(io.StringIO(scan_text(d))))


def scan_history_cases():
    print("Scan history")
    if not SCAN:
        print("  (this version has no scan-history.md, so these checks fail)")
    FERN = card("Fernhill", "Senior Product Manager", "https://www.linkedin.com/jobs/view/4476505407/")
    ACME = card("Acme", "Product Lead", "https://jobs.lever.co/acme/1", source="watchlist", tier="INCLUDE")

    # No history yet: nothing is seen, and the first record creates the file
    d = folder("scan_new")
    out = run(d, scan(seen([FERN])), base=False)
    check("no history yet: nothing is seen and no file is made",
          "already shown in the last 30 days: 0 of 1" in out and "SEEN []" in out and not (d / SCAN_PATH).exists(), out)
    out = run(d, scan(recorded([FERN])), base=False)
    check("the first record creates the file with its header and the role, dated today",
          out.startswith("scan history: 1 new, 0 shown again") and scan_text(d).splitlines()[:1] == [SCAN_HEADER]
          and [(r["date_seen"], r["company"], r["role"], r["source"], r["tier"]) for r in scan_rows(d)]
          == [(TODAY, "Fernhill", "Senior Product Manager", "linkedin", "STRONG")], out + chr(10) + scan_text(d))
    check("a new history gets normal permissions, not owner-only, and leaves no temp file",
          (d / SCAN_PATH).exists() and mode(d, SCAN_PATH) == default_mode() and not leftovers(d), out)

    # A later scan
    out = run(d, scan(seen([FERN, ACME])), base=False, today=shift(14))
    check("a scan 14 days later: the role it showed is seen, with its date, and a new one isn't",
          "already shown in the last 30 days: 1 of 2" in out and "SEEN [('Fernhill', 'Senior Product Manager')]" in out
          and "shown " + TODAY in out, out)
    out = run(d, scan(seen([FERN])), base=False, today=shift(30))
    out2 = run(d, scan(seen([FERN])), base=False, today=shift(31))
    check("still seen 30 days later, new again at 31", "SEEN [('Fernhill'" in out and "SEEN []" in out2, out + chr(10) + out2)
    out = run(d, scan(recorded([FERN, ACME])), base=False, today=shift(14))
    rows = scan_rows(d)
    check("recording a role again moves its date to today without a second row",
          out.startswith("scan history: 1 new, 1 shown again") and [(r["company"], r["date_seen"]) for r in rows]
          == [("Fernhill", shift(14)), ("Acme", shift(14))], out + chr(10) + scan_text(d))

    # Matching: a link, a normalized title, and a near match
    d = folder("scan_link", files={SCAN_PATH: SCAN_HEADER + chr(10)
                                   + shift(-5) + ",Acme,Product Lead,https://www.linkedin.com/jobs/view/4476505407/,linkedin,INCLUDE" + chr(10)
                                   + shift(-5) + ",Acme,Data Analyst,,linkedin,INCLUDE" + chr(10)})
    out = run(d, scan(seen([card("Acme", "Group Product Manager", "https://linkedin.com/jobs/view/4476505407"),
                            card("Acme", "Senior PM, Platform")])), base=False)
    check("the same link is seen whatever the title says, and a blank link never matches",
          "SEEN [('Acme', 'Group Product Manager')]" in out, out)
    d = folder("scan_title", files={SCAN_PATH: SCAN_HEADER + chr(10)
                                    + shift(-3) + ",Fernhill,Senior Product Manager,,linkedin,STRONG" + chr(10)
                                    + shift(-3) + ',Brightloop,"Senior Product Manager, Platform",,linkedin,STRONG' + chr(10)})
    out = run(d, scan(seen([card("Fernhill, Inc.", "Sr. PM", "https://example.com/fernhill/9")])), base=False)
    check("'Sr. PM' at 'Fernhill, Inc.' is the Senior Product Manager role a scan showed at Fernhill",
          "SEEN [('Fernhill, Inc.', 'Sr. PM')]" in out, out)
    out = run(d, scan(seen([card("Fernhill", "Senior Product Manager, Platform", "https://example.com/fernhill/10"),
                            card("Brightloop", "Senior Product Manager", "https://example.com/brightloop/4")])), base=False)
    check("a near match (Senior Product Manager, Platform, either way round) isn't seen", "SEEN []" in out and "0 of 2" in out, out)
    d = folder("scan_placeholder", files={SCAN_PATH: SCAN_HEADER + chr(10)
                                          + shift(-3) + ",Stealth Startup,Senior Product Manager,https://example.com/s/1,linkedin,STRONG" + chr(10)})
    out = run(d, scan(seen([card("Stealth Startup", "Senior Product Manager", "https://example.com/s/2"),
                            card("Stealth Startup", "Senior Product Manager", "")])), base=False)
    out2 = run(d, scan(seen([card("Stealth Startup", "Senior Product Manager", "https://example.com/s/1")])), base=False)
    check("a placeholder name ('Stealth Startup'): with links on both, only the link decides; with no link, name and role match",
          "SEEN [('Stealth Startup', 'Senior Product Manager')]" in out and "1 of 2" in out
          and "SEEN [('Stealth Startup'" in out2, out + chr(10) + out2)

    # Old rows
    d = folder("scan_prune", files={SCAN_PATH: SCAN_HEADER + chr(10)
                                    + shift(-61) + ",Brightloop,Senior PM,https://example.com/b/1,linkedin,STRONG" + chr(10)
                                    + shift(-60) + ",Tallyho,Product Lead,https://example.com/t/1,ats-board,INCLUDE" + chr(10)})
    out = run(d, scan(seen([card("Brightloop", "Senior PM", "https://example.com/b/1")]) + recorded([ACME])), base=False)
    check("a 61-day-old row isn't seen and drops off on the next write; a 60-day-old one stays",
          "SEEN []" in out and "1 new, 0 shown again, 1 older than 60 days dropped" in out
          and [r["company"] for r in scan_rows(d)] == ["Tallyho", "Acme"], out + chr(10) + scan_text(d))

    # Roles that came back: last shown more than 30 days ago, within the 60-day history
    TALLY = card("Tallyho", "Product Lead", "https://example.com/t/2", tier="INCLUDE")
    BRIGHT = card("Brightloop", "Senior PM", "https://example.com/b/2")
    FERN3 = card("Fernhill", "Senior Product Manager", "https://example.com/f/3")
    d = folder("scan_shown_earlier", files={SCAN_PATH: SCAN_HEADER + chr(10)
                                            + shift(-35) + ",Tallyho,Product Lead,https://example.com/t/2,ats-board,INCLUDE" + chr(10)
                                            + shift(-61) + ",Brightloop,Senior PM,https://example.com/b/2,linkedin,STRONG" + chr(10)
                                            + shift(-40) + ",Fernhill,Senior Product Manager,,linkedin,STRONG" + chr(10)
                                            + shift(-10) + ",Fernhill,Senior Product Manager,,linkedin,STRONG" + chr(10)})
    out = run(d, scan(seen([TALLY, BRIGHT, FERN3]) + earlier([TALLY, BRIGHT, FERN3])), base=False)
    check("a role last shown 35 days ago comes back from shown_earlier with its date, not from seen_before; "
          "one shown 10 days ago is only seen",
          "SEEN [('Fernhill', 'Senior Product Manager')]" in out
          and f"EARLIER [('Tallyho', 'Product Lead', '{shift(-35)}')]" in out
          and "shown earlier, 31 to 60 days ago: 1 of 3" in out and f"  Tallyho | Product Lead | shown {shift(-35)}" in out, out)
    out = run(d, scan(recorded([ACME]) + seen([BRIGHT]) + earlier([BRIGHT])), base=False)
    check("a 61-day-old row matches neither call, and a write prunes it",
          "1 older than 60 days dropped" in out and "SEEN []" in out and "EARLIER []" in out
          and "Brightloop" not in scan_text(d), out + chr(10) + scan_text(d))

    # The header kept its line but the rows ran together into one: a save would wipe the roles it lost
    before = SCAN_HEADER + chr(10) + (shift(-5) + ",Fernhill,Senior Product Manager,https://example.com/f/1,linkedin,STRONG" + chr(10)
                                      + shift(-4) + ",Acme,Product Lead,https://example.com/a/1,watchlist,INCLUDE" + chr(10)
                                      + shift(-3) + ",Brightloop,Senior PM,https://example.com/b/1,linkedin,STRONG" + chr(10)
                                      ).replace(chr(10), "")
    d = folder("scan_ran_together", files={SCAN_PATH: before})
    out = run(d, scan(seen([card("Acme", "Product Lead", "https://example.com/a/1")]) + recorded([FERN])), base=False)
    check("a history with its header intact but rows run together: CAN'T READ, nothing written, all three rows untouched",
          out.startswith("CAN'T READ") and "ran together" in out and "scan history:" not in out and scan_text(d) == before, out)

    # Empty and header-only files
    for name, body in (("an empty", ""), ("a header-only", SCAN_HEADER + chr(10))):
        d = folder("scan_" + name.split()[-1], files={SCAN_PATH: body})
        out = run(d, scan(seen([FERN]) + recorded([FERN])), base=False)
        lines = scan_text(d).splitlines()
        check(name + " history: nothing is seen, then the header and the role are written",
              "SEEN []" in out and "CAN'T READ" not in out and "scan history: 1 new" in out
              and lines[:1] == [SCAN_HEADER] and len(lines) == 2, out + chr(10) + scan_text(d))

    # A file the snippet can't read: say so once, carry on, and never write over it
    for name, body in (("a binary file", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00"),
                       ("a file without the header", "Notes to self\nAcme, Product Lead\n".encode("utf-8"))):
        d = folder("scan_unreadable_" + name.split()[-1])
        (d / SCAN_PATH).write_bytes(body)
        out = run(d, scan(seen([FERN]) + "print('THE SCAN GOES ON')\n" + recorded([FERN])), base=False)
        out2 = run(d, scan(recorded([FERN])), base=False)
        check(name + " in its place: one line says so, nothing is seen, the scan goes on, the file is untouched",
              out.count("CAN'T READ") == 1 and "SEEN []" in out and "THE SCAN GOES ON" in out and "scan history:" not in out
              and "CAN'T READ" in out2 and "scan history:" not in out2 and (d / SCAN_PATH).read_bytes() == body
              and not leftovers(d), out + chr(10) + out2)

    # Setting an unreadable history aside (with the user's yes): renamed, never deleted, never over an earlier one
    first, second = b"\x89PNG\r\n\x1a\n\x00\x00", "Notes to self\nAcme, Product Lead\n".encode("utf-8")
    d = folder("scan_set_aside")
    aside, aside2 = (d / "job-search" / f"scan-history-unreadable-{TODAY}{n}.csv" for n in ("", "-2"))
    (d / SCAN_PATH).write_bytes(first)
    out = run(d, scan("set_aside()\n" + recorded([FERN])), base=False)
    check("set_aside renames an unreadable history with today's date, and the next record starts a new one",
          f"set aside: {SCAN_PATH} is now job-search{os.sep}scan-history-unreadable-{TODAY}.csv" in out
          and aside.exists() and aside.read_bytes() == first and "scan history: 1 new" in out and not leftovers(d)
          and scan_text(d).splitlines()[:1] == [SCAN_HEADER], out)
    (d / SCAN_PATH).write_bytes(second)
    out = run(d, scan("set_aside()\n"), base=False)
    out2 = run(d, scan(recorded([FERN]) + "set_aside()\n"), base=False)
    kept = scan_text(d)
    check("a second one the same day gets -2 and the first stays; a history that reads fine is never set aside",
          "is now job-search" in out and aside2.exists() and aside2.read_bytes() == second
          and aside.exists() and aside.read_bytes() == first and "nothing set aside" in out2 and "reads fine" in out2
          and kept.startswith(SCAN_HEADER) and (d / SCAN_PATH).exists(), out + chr(10) + out2)

    # Accented and emoji names, with Windows' default encoding and a cp1252 console
    d = folder("scan_windows")
    win = {"pre": WINDOWS, "env": {"PYTHONIOENCODING": "cp1252"}}
    out = run(d, scan(recorded([card("Łódź Labs", "Senior PM, Growth \U0001F680", "https://example.com/l/1"),
                                card("Café Société", "Product Lead")])), base=False, **win)
    out += chr(10) + run(d, scan(seen([card("Łódź Labs, Inc.", "Senior Product Manager, Growth \U0001F680"),
                                       card("Café Société (Paris)", "Product Lead")])), base=False, **win)
    check("Windows: accented and emoji names are written as UTF-8, found again, and print without crashing",
          "scan history: 2 new" in out and "already shown in the last 30 days: 2 of 2" in out and "Traceback" not in out
          and "Łódź Labs" in scan_text(d) and "Café Société" in scan_text(d) and "\U0001F680" in scan_text(d), out)

    # Saving
    before = SCAN_HEADER + chr(10) + shift(-2) + ",Acme,Product Lead,,linkedin,INCLUDE" + chr(10)
    d = folder("scan_perms", files={SCAN_PATH: before})
    (d / SCAN_PATH).chmod(0o640)
    want = mode(d, SCAN_PATH)   # 0o640, or 0o666 on Windows
    out = run(d, scan(recorded([FERN])), base=False)
    check("a save keeps the history's permissions and leaves no temp file",
          out.startswith("scan history: 1 new") and mode(d, SCAN_PATH) == want and not leftovers(d), out + " " + oct(mode(d, SCAN_PATH)))
    d = folder("scan_locked", files={SCAN_PATH: before})
    out = run(d, scan(recorded([FERN]) + "print('THE SCAN GOES ON')\n"), base=False, pre=EXCEL_LOCK)
    check("a save blocked by another app says so in one line, the scan goes on, and the old history stays",
          "scan history not saved" in out and "THE SCAN GOES ON" in out and scan_text(d) == before and not leftovers(d), out)

    # The scan and the tracker agree on what's the same role
    probe = ("print([norm(t) for t in " + repr(["Sr. PM - Growth", "Senior PM, Retention", "Product & Growth Lead", "PM II",
                                                "Senior Project Manager", "sr pm"])
             + "], [norm_company(c) for c in " + repr(["Fernhill, Inc.", "Northstar Learning (NYC)", "Acme Corp.", "Łódź Labs LLC",
                                                       "AT&T", "PM Partners Co"]) + "])\n")
    d = folder("scan_norm")
    same = []
    for value in ("product manager", "project manager", None):
        a, b = run(d, probe, base=setvar(BASE, "PM_MEANS", value)), run(d, scan(probe, pm_means=value), base=False)
        same.append((value, a == b and a.startswith("["), a, b))
    check("titles and companies are normalized the way the tracker does, whatever PM_MEANS says",
          all(s[1] for s in same), [s for s in same if not s[1]])


def main():
    try:
        tracker_cases()
        contacts_cases()
        scan_history_cases()
    finally:
        shutil.rmtree(WORK, ignore_errors=True)
    print()
    note = f" ({len(skipped)} skipped on this system)" if skipped else ""
    if failed:
        print(f"{len(failed)} of {passed + len(failed)} checks failed{note}.")
        sys.exit(1)
    print(f"All {passed} checks passed{note}.")


if __name__ == "__main__":
    main()
