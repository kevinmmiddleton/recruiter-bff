#!/usr/bin/env python3
"""Build, check, and package Recruiter BFF. Standard library only; run from anywhere.

    python3 tools/build.py            regenerate the derived files (the Codex manifest and both marketplace files)
    python3 tools/build.py --check    fail if any derived file is stale
    python3 tools/build.py --test     run the snippet checks and the copy checks
    python3 tools/build.py --dist     regenerate, test, then write the release files to dist/

The repo root is the plugin. The skills live in skills/<name>/. Derived files are committed, so the plugin
installs straight from GitHub in Claude Code and Codex; this script keeps them in sync with
.claude-plugin/plugin.json, the one place the name, version, and description are written.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "recruiter-bff"
OLD_NAME = "job-search-agent"   # the 0.4.0 rename: releases also carry an identical file under the old name
SKILLS = ROOT / "skills"
KIT = ROOT / "extras" / "no-install-kit"
DIST = ROOT / "dist"
MARKETPLACE = NAME   # install as recruiter-bff@recruiter-bff, straight from this repo

OPENAI_INTERFACE = {
    "displayName": "Recruiter BFF",
    "shortDescription": "Find out if you're a match before you apply, then walk in prepared.",
    "longDescription": ("Paste a job posting and it tells you honestly whether you fit, gaps included, and whether to apply. "
                        "When the interview comes, it builds a guide from your own background. It never applies for you, "
                        "and that's the point: fewer, better applications, sent sooner."),
    "developerName": "Kevin Middleton",
    "category": "Productivity",
    "capabilities": ["Read", "Write"],
    "websiteURL": "https://github.com/kevinmmiddleton/recruiter-bff",
    "defaultPrompt": ["Set me up for my job search", "Is this role a good fit for me?", "Prep me for my interview"],
    "brandColor": "#5FD6A4",
    "composerIcon": "./assets/brand/favicon/icon-192.png",
    "logo": "./assets/brand/png/recruiter-bff-app-icon-1024.png",
}


def claude_manifest() -> dict:
    return json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))


def portable_manifest() -> str:
    """Root plugin.json in the Agent Plugins format, for Codex. Identity comes from .claude-plugin/plugin.json."""
    cp = claude_manifest()
    out = {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"}
    for k in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords"):
        if k in cp:
            out[k] = cp[k]
    out["extensions"] = {"com.openai": {"interface": OPENAI_INTERFACE}}
    return json.dumps(out, indent=2) + "\n"


def marketplace_json() -> str:
    """Claude Code marketplace: this repo installs itself (/plugin marketplace add kevinmmiddleton/recruiter-bff)."""
    cp = claude_manifest()
    out = {
        "name": MARKETPLACE,
        "description": OPENAI_INTERFACE["shortDescription"],
        "owner": cp["author"],
        "plugins": [{"name": cp["name"], "source": "./", "description": cp["description"], "homepage": cp["repository"]}],
    }
    return json.dumps(out, indent=2) + "\n"


def codex_marketplace_json() -> str:
    """Codex marketplace, in the .agents layout (codex plugin marketplace add kevinmmiddleton/recruiter-bff)."""
    cp = claude_manifest()
    out = {
        "name": MARKETPLACE,
        "interface": {"displayName": OPENAI_INTERFACE["displayName"]},
        "plugins": [{
            "name": cp["name"],
            "source": {"source": "local", "path": "./"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": OPENAI_INTERFACE["category"],
        }],
    }
    return json.dumps(out, indent=2) + "\n"


def derived() -> dict[str, str]:
    return {
        ".claude-plugin/marketplace.json": marketplace_json(),
        ".agents/plugins/marketplace.json": codex_marketplace_json(),
        "plugin.json": portable_manifest(),
    }


def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd if cmd[0] != sys.executable else ["python3", *cmd[1:]]), flush=True)
    return subprocess.call(cmd, cwd=ROOT)


def write_derived() -> None:
    for rel, text in derived().items():
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists() or p.read_text(encoding="utf-8") != text:
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            print("wrote", rel)


def check() -> int:
    bad = [rel for rel, text in derived().items()
           if not (ROOT / rel).exists() or (ROOT / rel).read_text(encoding="utf-8") != text]
    for rel in bad:
        print("stale:", rel)
    for rel in ("assets/brand/favicon/icon-192.png", "assets/brand/png/recruiter-bff-app-icon-1024.png"):
        if not (ROOT / rel).exists():
            print("missing image the Codex manifest names:", rel)
            bad.append(rel)
    if bad:
        print("Run: python3 tools/build.py   (then commit the changes)")
        return 1
    print("derived files are current")
    return 0


def test() -> int:
    rc = 0
    rc |= run([sys.executable, str(ROOT / "tools" / "check_snippets.py")])
    rc |= check_copy()
    print("ALL TESTS PASSED" if rc == 0 else "SOME TESTS FAILED")
    return 1 if rc else 0


def _description(frontmatter: str) -> str:
    """The description field, folded (description: >) or on one line."""
    m = re.search(r"^description:\s*>-?\s*\n((?:[ \t]+.*\n?)+)", frontmatter, re.M)
    if m:
        return " ".join(line.strip() for line in m.group(1).splitlines() if line.strip())
    m = re.search(r'^description:\s*"?(.*?)"?\s*$', frontmatter, re.M)
    return m.group(1) if m else ""


def check_copy() -> int:
    """Skill frontmatter, no em dashes in user-facing copy, and no tree or arrow glyphs in what agents read."""
    problems = []
    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    for d in skill_dirs:
        text = (d / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            problems.append(f"skills/{d.name}/SKILL.md has no frontmatter")
            continue
        name = re.search(r"^name:\s*(\S+)", m.group(1), re.M)
        if not name or name.group(1) != d.name:
            problems.append(f"skills/{d.name}/SKILL.md name must be {d.name}")
        desc = _description(m.group(1))
        if not desc or len(desc) > 1024:
            problems.append(f"skills/{d.name}/SKILL.md description missing or over 1024 characters ({len(desc)})")
    agent_reads = [p for d in skill_dirs for p in sorted(d.rglob("*.md"))] + sorted(KIT.glob("*.md"))
    for p in [ROOT / "README.md", ROOT / "CONNECTORS.md", ROOT / "CHANGELOG.md", *agent_reads]:
        if "—" in p.read_text(encoding="utf-8"):
            problems.append(f"{p.relative_to(ROOT).as_posix()} has an em dash")
    # Windows PowerShell 5.1 reads BOM-less UTF-8 as the ANSI code page, so tree lines and arrows garble for an
    # agent reading the skills there (found in Unpaid Intern's Windows field test). Curly quotes are fine.
    for p in agent_reads:
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            bad = sorted({f"U+{ord(ch):04X}" for ch in line if 0x2500 <= ord(ch) <= 0x257F or 0x2190 <= ord(ch) <= 0x21FF})
            if bad:
                problems.append(f"{p.relative_to(ROOT).as_posix()}:{n} has box-drawing or arrow characters "
                                f"({', '.join(bad)}); use plain indents and ->")
    inst = KIT / "INSTRUCTIONS.md"
    if inst.exists() and len(inst.read_text(encoding="utf-8")) > 8000:
        problems.append(f"extras/no-install-kit/INSTRUCTIONS.md is {len(inst.read_text(encoding='utf-8'))} characters; "
                        "ChatGPT's project instructions hold 8,000")
    for msg in problems:
        print("  FAIL ", msg)
    print(f"copy checks: {'ok' if not problems else str(len(problems)) + ' problem(s)'}")
    return 1 if problems else 0


# ---------------------------------------------------------------- release files

# The .plugin holds only what the Claude desktop app reads: the Claude manifest, the docs, the skills, and the
# app icon the manifest names. The README loads its other images from GitHub, so the plugin doesn't need them.
PLUGIN_FILES = (".claude-plugin/plugin.json", "LICENSE", "README.md", "CHANGELOG.md", "CONNECTORS.md", "skills",
                "assets/brand/png/recruiter-bff-app-icon-1024.png")


def _zip_tree(zf: zipfile.ZipFile, base: Path, arc_prefix: str, only=()) -> None:
    for p in sorted(base.rglob("*")):
        rel = p.relative_to(base).as_posix()
        if p.is_dir() or "__pycache__" in rel or p.name in (".DS_Store", ".gitignore", ".gitattributes") or rel.endswith(".pyc"):
            continue
        if only and not any(rel == x or rel.startswith(x + "/") for x in only):
            continue
        info = zipfile.ZipInfo(arc_prefix + rel, date_time=(2026, 1, 1, 0, 0, 0))   # fixed date: same input, same zip
        info.external_attr = (0o755 if os.access(p, os.X_OK) else 0o644) << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, p.read_bytes())


KIT_PROJECT_FILES = (
    "evaluate-role/references/scoring-rubric.md",
    "find-jobs/references/classification-rubric.md",
    "interview-guide-engine/references/guide-template.md",
    "interview-guide-engine/references/answers-and-scripts.md",
    "interview-guide-engine/references/story-bank-template.md",
    "your-materials/references/review-pass.md",
    "job-search-setup/references/building-a-saved-search.md",
    "job-search-setup/references/ats-search-links.md",
)


def tracker_columns() -> list[str]:
    """The tracker's columns, read from the snippets in tracker-schema.md, so the kit's blank tracker always matches."""
    text = (SKILLS / "application-tracker" / "references" / "tracker-schema.md").read_text(encoding="utf-8")
    m = re.search(r"^COLS = \[(.*?)\]", text, re.M | re.S)
    if not m:
        raise SystemExit("tracker-schema.md has no COLS list; update tracker_columns() in tools/build.py")
    return re.findall(r'"([a-z_]+)"', m.group(1))


def dist() -> int:
    write_derived()
    if test():
        return 1
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    # 1. The plugin file for the Claude desktop app, plus an identical copy under the old name
    with zipfile.ZipFile(DIST / f"{NAME}.plugin", "w") as zf:
        _zip_tree(zf, ROOT, "", PLUGIN_FILES)
    shutil.copy(DIST / f"{NAME}.plugin", DIST / f"{OLD_NAME}.plugin")
    # 2. No-install kit, for ChatGPT, Copilot, Gemini, or Claude without Cowork: the instructions, the method files
    #    copied from the skills (so the kit never drifts from the plugin), and a job-search folder with a blank tracker
    if KIT.exists():
        kit = f"{NAME}-no-install-kit"
        with tempfile.TemporaryDirectory() as tmp:
            k = Path(tmp) / kit
            k.mkdir()
            for p in sorted(KIT.glob("*.md")):
                shutil.copy(p, k / p.name)
            (k / "Project files").mkdir()
            for rel in KIT_PROJECT_FILES:
                shutil.copy(SKILLS / rel, k / "Project files" / Path(rel).name)
            (k / "job-search").mkdir()
            with open(k / "job-search" / "job-tracker.csv", "w", encoding="utf-8-sig", newline="") as fh:
                fh.write(",".join(tracker_columns()) + "\r\n")   # Excel's "CSV UTF-8": the start mark keeps accented names right
            with zipfile.ZipFile(DIST / f"{kit}.zip", "w") as zf:
                _zip_tree(zf, k, f"{kit}/")
    for p in sorted(DIST.iterdir()):
        print(f"  {p.name:40} {p.stat().st_size // 1024:>6} KB")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="fail if derived files are stale")
    g.add_argument("--test", action="store_true", help="run the snippet checks and the copy checks")
    g.add_argument("--dist", action="store_true", help="build release files into dist/")
    a = ap.parse_args()
    if a.check:
        return check()
    if a.test:
        return test()
    if a.dist:
        return dist()
    write_derived()
    return 0


if __name__ == "__main__":
    sys.exit(main())
