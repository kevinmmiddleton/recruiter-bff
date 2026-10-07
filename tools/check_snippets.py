"""Run the Python snippets in the tracker and contacts reference files against sample files.

The skills tell the agent to copy these snippets, so the snippets are the plugin's only code.
This pulls every ```python block out of:
    skills/application-tracker/references/tracker-schema.md
    skills/contacts/references/contacts-schema.md
runs them in a temporary folder against sample trackers, contacts files, and LinkedIn exports,
and checks what they print and what they write. Nothing in the repo or your own folders is touched.

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
returns and a copy whose rows ran together, tracker or contacts, with any date format or a link;
dates rewritten as 9/15/2026), a new value that already holds the replacement character, file
permissions kept on save, a 0.4 tracker's booked dates taken from notes, rejection dates typed
as 10/5/2026, the near-miss rejection title, accented and emoji names with Windows' default
encoding, columns the user added (tracker and contacts), a save that fails because the file is
open in Excel, and the contacts import (LinkedIn's note lines, near misses, recruiter tags, a
rerun, a wrong file).
"""
import argparse, os, pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRACKER_MD = "skills/application-tracker/references/tracker-schema.md"
CONTACTS_MD = "skills/contacts/references/contacts-schema.md"
TODAY = "2026-10-06"

# To count how many checks an older version fails: --rev <commit> (from git) or --from <folder> (a copy
# that isn't committed). A setting the older snippets don't have yet (confirmed_row, for one) is added at
# the top of the snippet, where it does nothing, so the check that depends on it fails instead of stopping the run.
ARGS = argparse.ArgumentParser(description="Run the tracker and contacts snippets against sample files.")
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

def blocks(rel):
    return re.findall(r"```python\n(.*?)```", source(rel), re.S)

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


def setvar(code, name, value):
    """Replace the first line that assigns `name` (a plain or tuple assignment) with a new value."""
    new, n = re.subn(rf"^{re.escape(name)}\s*=.*$", lambda m: f"{name} = {value!r}", code, count=1, flags=re.M)
    if not n:
        if LENIENT:                     # an older version: add the setting where it does nothing
            return f"{name} = {value!r}\n" + code
        sys.exit(f"No line assigning {name!r} in a snippet; did its wording change?")
    return new

def pin_today(code):
    return re.sub(r"^TODAY = .*$", f"TODAY = {TODAY!r}", code, count=1, flags=re.M)

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

def run(d, code, base=True, pre="", env=None):
    """Write the snippet to a .py file (the way the skill says to) and run it in folder d."""
    script = d / "_snippet.py"
    body = (pin_today(BASE) + "\n" if base else "") + pin_today(code)
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

passed, failed = 0, []

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
    out = run(d, update("Fernhill", "Senior PM", "screening"))
    check("a save keeps the tracker's permissions", out.startswith("updated:") and mode(d) == 0o644, oct(mode(d)))
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
    out = run(d, IMPORT, base=False)
    check("a rerun adds nobody twice", out.startswith("7 connections read; 0 added"), out)

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
    out = run(d, IMPORT, base=False)
    body = (d / CONTACTS_PATH).read_text(encoding="utf-8-sig")
    check("contacts saved by Excel keep their start mark and permissions, with one clean name column",
          has_mark(d, CONTACTS_PATH) and mode(d, CONTACTS_PATH) == 0o644 and body.startswith("name,company,")
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


def main():
    try:
        tracker_cases()
        contacts_cases()
    finally:
        shutil.rmtree(WORK, ignore_errors=True)
    print()
    if failed:
        print(f"{len(failed)} of {passed + len(failed)} checks failed.")
        sys.exit(1)
    print(f"All {passed} checks passed.")


if __name__ == "__main__":
    main()
