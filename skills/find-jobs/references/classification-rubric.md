# Classification Rubric

How to tag each scanned role STRONG, INCLUDE, or EXCLUDE. The user's `profile.md` (and `preferences.md`, if it exists) are the rules; this file is the method. Run it per role, quickly and the same way every time.

## Decision order

Check in this order. The first rule a role fails sends it to EXCLUDE, with that reason.

1. **Skip list or excluded company type.** A named company on the skip list, or a staffing firm or job aggregator (see below) when the profile excludes those, is EXCLUDE: "staffing firm" or "skip list."
2. **Wrong level.** Seniority clearly below the target, or far above it, is EXCLUDE: "wrong level." Be generous with unclear titles: a bare "Product Manager" can be senior, so don't cut it on level alone.
3. **Excluded function, unless an exception applies.** If the role is an excluded function, check the exception written next to it first. "Data science PM out, growth analytics in": a growth analytics PM role passes. No exception applies: EXCLUDE, "excluded function."
4. **Excluded industry.** Judge by the company's core business, not one product line. A company whose core business is on the exclusions or the preferences page's "no thanks" list: EXCLUDE, "excluded industry." A software company that sells *to* that industry: show it with a flag.
5. **Location.** On-site only somewhere the user won't work, or a place they ruled out: EXCLUDE, "location." Remote or unstated always passes.
6. **Pay.** Only when the posting lists a range and the whole range is below the floor: EXCLUDE, "pay below floor." A range that starts below the floor but reaches it passes, with a heads-up in "why it fits." Unlisted pay always passes.

A role that survives all six is at least INCLUDE. Then:

7. **Strong signal.** Hits one or more strong signals: upgrade to **STRONG**.
8. **Parked lanes** don't upgrade anything. A role that mainly hits a parked lane is INCLUDE, listed after the STRONG roles, with the reason and a revisit note ("a lane you've parked: Group PM with reports").
9. **Weak signals** are soft warnings. They never cut a role and never upgrade one: flag it ("heads-up: contract-to-hire") and rank it lower within its tier.
10. **Unknown company:** INCLUDE, with an "unknown company" flag. Missing pay or location: INCLUDE.

Signals rank; exclusions cut. Keep the two apart.

## The tie-breaker

**When genuinely unsure, INCLUDE.** A scan that only shows perfect matches misses good roles with imperfect titles. A false include costs the user a two-second skip; a false exclude costs them a role they never see.

## Staffing firms and job aggregators

Staffing firms post roles on behalf of unnamed clients; aggregators repost other companies' roles, often after the original closed. Both crowd out the real postings. Excluded by default; the user can turn it off.

**Name tells** (when the profile excludes staffing firms): "Staffing," "Talent," "Recruiting," "Search Partners," "Consulting Group" on an otherwise unknown company, or a company that posts the same role in many cities at once.

**The rule for an unknown company:** a name that isn't widely recognizable, and a posting that mentions consulting, staffing, talent solutions, recruitment process outsourcing (RPO), staff or talent augmentation, "on behalf of our client," "W2 or C2C," or contract-to-hire: probably staffing. Exclude it, and say so in the tally.

**Types to exclude:** staffing and recruiting agencies (including niche and interim staffing firms); IT consulting and staff-augmentation firms that place contractors; RPO firms; aggregators that repost other companies' roles under their own name (remote-job aggregators, newsletter job boards, "AI job matching" boards); and candidate-matching services.

**Well-known examples** (seed list; the user's skip list adds to it):

- **Staffing and recruiting firms:** Robert Half, Randstad, Kforce, CyberCoders, Harnham, BCForward, Insight Global, TEKsystems, Aerotek, Adecco, Jobot, Motion Recruitment.
- **Aggregators that repost roles as their own:** "Jobs via Dice," Lensa, Ladders, Jobgether, RemoteHunter, hackajob.

**Block by full name, never by a shared word;** a staffing firm can share a word with a real employer. **Don't block discovery sources** like LinkedIn, Indeed, ZipRecruiter, or Built In: they're where roles are found, not who's hiring.

If a role from an aggregator looks strong, don't throw the job away: look for the same role on the hiring company's own site and show that version instead.

## Level from titles

Titles are messy. Map them loosely:

- **Below a senior search:** Intern, Junior, Associate, Coordinator, Analyst.
- **At target:** Product Manager, Senior PM, Staff PM, Principal PM, Lead PM, Group PM, Product Lead, and Head of Product or Director of Product for director-level searches.
- **Above target:** VP of Product, CPO. Show these with a note rather than cutting them, in case the user wants a stretch.

Adjust the same idea for other fields: the user's target titles and seniority set the line.

**Titles mean different things at different employers.** "VP" and "Director" are individual-contributor levels at many banks and executive roles elsewhere. A title that usually means managing people gets shown when the posting reads as hands-on, with a flag.

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
