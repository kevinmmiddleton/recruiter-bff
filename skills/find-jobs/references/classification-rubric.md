# Classification Rubric

How to tag each scanned role STRONG, INCLUDE, or EXCLUDE. The user's `profile.md` (and `preferences.md`, if it exists) are the rules; this file is the method. Run it per role, quickly and the same way every time.

## Decision order

Check in this order. The first rule a role fails sends it to EXCLUDE, with that reason.

1. **Skip list or excluded company type.** A named company on the skip list, or a staffing firm or job aggregator (see below) when the profile excludes those, is EXCLUDE: "staffing firm" or "skip list."
2. **Wrong level.** Seniority clearly below the target, or far above it, is EXCLUDE: "wrong level." Be generous with unclear titles: a bare "Product Manager" can be senior, so don't cut it on level alone.
3. **Excluded function, unless an exception applies.** If the role is an excluded function, check the exception written next to it first. "Data science PM out, growth analytics in": a growth analytics PM role passes. No exception applies: EXCLUDE, "excluded function."
4. **Excluded industry.** An industry on the profile's exclusions or the preferences page's "no thanks" list: EXCLUDE, "excluded industry."
5. **Location.** On-site only somewhere the user won't work, or a place they ruled out: EXCLUDE, "location." Remote or unstated always passes.
6. **Pay.** Only when the posting lists a range and the whole range is below the floor: EXCLUDE, "pay below floor." A range that starts below the floor but reaches it passes, with a heads-up in "why it fits." Unlisted pay always passes.

A role that survives all six is at least INCLUDE. Then:

7. **Strong signal.** Hits one or more strong signals: upgrade to **STRONG**.
8. **Weak signals** never make a role STRONG on their own. They can tip a borderline call into INCLUDE, and they're worth naming in "why it fits."
9. **Parked signals** don't upgrade anything. If a role mainly hits a parked signal, show it as INCLUDE with a note ("touches something you parked: Group PM with reports").

## The tie-breaker

**When genuinely unsure, INCLUDE.** A scan that only shows perfect matches misses good roles with imperfect titles. A false include costs the user a two-second skip; a false exclude costs them a role they never see.

## Staffing firms and job aggregators

Staffing firms post roles on behalf of unnamed clients; aggregators repost other companies' roles, often after the original closed. Both crowd out the real postings. Excluded by default; the user can turn it off.

**Name tells** (when the profile excludes staffing firms): "Staffing," "Talent," "Recruiting," "Search Partners," "Consulting Group" on an otherwise unknown company, or a company that posts the same role in many cities at once.

**Text tells** for an unknown company: "on behalf of our client," "our client is seeking," "staff augmentation," "contract-to-hire," "W2 or C2C," or a confidential company name. Two or more of these and the company is probably staffing.

**Well-known examples** (seed list; the user's skip list adds to it):

- **Staffing and recruiting firms:** Robert Half, TEKsystems, Insight Global, Randstad, Adecco, Kforce, Aerotek, Jobot, CyberCoders, Motion Recruitment.
- **Aggregators that repost roles:** Lensa, Jooble, Talent.com, Adzuna, SimplyHired.

If a role from an aggregator looks strong, don't throw the job away: look for the same role on the hiring company's own site and show that version instead.

## Level from titles

Titles are messy. Map them loosely:

- **Below a senior search:** Intern, Junior, Associate, Coordinator, Analyst.
- **At target:** Product Manager, Senior PM, Staff PM, Principal PM, Lead PM, Group PM, Product Lead, and Head of Product or Director of Product for director-level searches.
- **Above target:** VP of Product, CPO. Show these with a note rather than cutting them, in case the user wants a stretch.

Adjust the same idea for other fields: the user's target titles and seniority set the line.

## Checking against the tracker

Normalize company and role the same way the tracker does (lowercase, drop punctuation, `sr` to `senior`, `pm` to `product manager`, `&` to `and`; keep seniority words).

- **Same company, same role:** already tracked. Drop it from the list and count it in the "already tracked" tally.
- **Same company, different role:** show it, tagged **New role at a company you know**, with one line of history from the tracker: "You applied for Senior PM in August; it closed after the recruiter screen." The user decides. A rejection for one role says little about another, and a company that liked them once is worth a look.
- **Same role, but the old row is `closed` or `hold`:** it may be back. Show it with the history line ("This closed in September; it looks reposted").

Don't treat near-matches as already seen. "Senior Product Manager" and "Senior Product Manager, Platform" at the same company can be different jobs, so show the new one with its history and let the user dismiss it.

## Output per role

For each role that's shown:

- the tier (STRONG or INCLUDE)
- one line of "why it fits" naming the signal it hit, plus any heads-up (pay starts below the floor, posted long ago)
- the fields the tracker needs: company, role, location, comp (if listed), posted, url

For hidden roles, keep only a tally by reason for the "Hid N" line. Always carry the real posting URL from the page, never one the model rewrote.
