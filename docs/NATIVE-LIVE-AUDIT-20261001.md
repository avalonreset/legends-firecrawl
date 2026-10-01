# Direct database access: live audit

Historical experiment. Superseded by release 0.2.0: all direct-source substitution is retired, including Treasury. Findings below preserve the audit-stage evidence, not current product behavior.

## Decision

There is a defensible direct-source opportunity for selected official database
queries. It is materially different from replicating a search/backlink index.
The current native router is not a verified universal replacement for Alexandria.
Its public-data percentage and safety labels do not measure usable coverage,
credit savings, access rights or high-volume reliability.

## What was previously tested

The preserved `release/benchmark.md` says 36 trials, 100% pass, and explicitly
identifies deterministic contract evaluation with no baseline. The corresponding
runner exercises offline CLI contracts; it is not a paired database benchmark.
Preserved native captures before this audit were Treasury debt-to-the-penny.
No earlier broad live direct-versus-Alexandria comparison was found in the
inspected repository evidence. This is a bounded finding, not a claim about all
historical sessions or external files.

## New live experiment

2026-10-01, NERV. Twelve deliberate direct adapter calls across eight adapters,
six paid Alexandria calls across five providers, and twelve additional paced
direct observations across Treasury debt/rates and USAspending agency lookup.
The paid tool contracts were refreshed through free `firecrawl/find-tools` before
execution. Six successful paid envelopes reported **22 credits total** (1+1+5+5+5+5).
Discovery reported zero. No dollar conversion or account-wide percentage inferred.
No paid retry or new provider-terms acceptance occurred.

The initial direct batch returned data on 11/12 calls; this is transport yield,
not correctness. The twelfth, Wayback availability, returned HTTP 429 and was
not retried. The paced follow-up returned data on 12/12 observations with at
least 1.5 seconds between requests. It demonstrates short-run behavior only,
not maximum throughput, burst tolerance or long-term availability. Two doctor
runs also made Treasury probes, separately from the 24 deliberate test calls.

| Route tested | Measured comparison | Decision |
| --- | --- | --- |
| Treasury debt-to-the-penny | All 3 rows and 33 field values exactly match the paid response | Direct is a credible route for this bounded query |
| Treasury average interest rates | All 3 rows and 33 field values exactly match the paid response | Same narrow acceptance |
| SEC company by explicit CIK | 11/12 mapped fields exactly match; website differs only as empty string versus null | Direct company data useful; serialization/derived fields need an explicit contract |
| USAspending agency | 10/11 shared fields exactly match; nested disaster-code structures differ | Useful source, not full parity; paid response reports 3 upstream requests and includes an awards summary |
| CourtListener copyright search | Both return 20 records; all 20 cluster IDs overlap | Record-identity match, not full field/pagination/access parity |
| YC company search | Direct returns 3 Hacker News stories; paid returns 20 company records | Existing adapter is semantically wrong for the requested capability |
| ESPN roster | Direct requests the league teams endpoint, returns `sports` | Existing adapter is semantically wrong for roster retrieval |
| Wayback history | HTTP 429 on first direct attempt; code uses closest-snapshot API | Neither availability nor complete-history semantics established |
| Treasury exchange rates, USAspending award search, SEC concept, Yahoo search | Data returned in initial direct tests; no paid pair | Reachability only; not accepted as equivalent |

Same-source values and public-record contents were checked, not just HTTP 200.
Calls were sequential and modest. First-party JSON adapters do not use a proxy
fleet; no commercial frontend challenge bypass was attempted.

## Reproduced implementation defects

Offline instrumented fetches confirmed that Treasury `auctions/upcoming` silently
uses the debt-to-the-penny endpoint. Its `page[number]` and `fields` options are
ignored. At scale, ignored pagination can repeatedly return the same first page
while appearing successful. These are code defects, not limitations of Treasury.

Eight adapter modules exist, not 26 independently validated native providers.
The catalog contains 114 provider labels and 797 capabilities; that does not
mean those capabilities have direct implementations. Treasury maps nine routes,
while its cached catalog lists twelve capabilities. Other adapters use substring
dispatch/default routes rather than complete capability-specific contracts.

The router's generic native catch automatically switches to the paid gateway.
Its `creditsCost || 1` invents a one-credit value when the real value is zero or
missing. Its result extraction does not validate every per-tool error. No shared
host pacing, durable cooldown or response-size bound is implemented in these
native adapters. Some HTTP timeouts exist, while Treasury itself lacks one.
The audit harness adds a 25-second abort and pacing for its own runs; these are
not improvements shipped in the production router.

## Scaling decision

Use allowlisted official API operations with validated input/output semantics,
bounded pagination, cache/reuse, source-specific pacing and explicit throttling
handling. Prefer official bulk downloads when appropriate. Do not treat a
public endpoint as unlimited, or rotate IPs to evade its quotas.

SEC documents unauthenticated submissions/XBRL APIs and nightly bulk archives,
and its fair-access policy limits automated traffic to 10 requests/second across
machines. A bulk import plus local queries can be a better scaling design than
one remote request per user action. These are source contracts, not a guarantee
our current adapter implements them correctly. [SEC APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
and [fair access](https://www.sec.gov/filergroup/announcements-old/new-rate-control-limits).

CourtListener describes API access through memberships/commercial agreements.
The unauthenticated query working today is not proof of unlimited entitlement or
stable access. [Provider documentation](https://www.courtlistener.com/help/api/).

Firecrawl explicitly provides free discovery and charges the listed execution
price. Source access, normalization, enrichment and managed operation can add
value even when underlying records are public. Its gateway does not prove every
tool uses residential proxies. [Alexandria contract](https://docs.firecrawl.dev/features/alexandria).

## Recommendation

Keep the hybrid idea, but narrow promotion to verified operations. Treasury and
SEC are credible initial candidates; USAspending requires matching its enrichment
scope. Repair pagination and exact capability dispatch before scaling. Remove YC
company and ESPN roster direct substitutions from any trusted workflow until fixed.
Retain managed routes for unsupported coverage, commercial collection and licensed
sources. Do not advertise 63.2% savings or safe-at-scale routing from this evidence.

## Artifacts and changes

Raw requests, results, comparisons and reproducible scripts use private evidence
set `var/native-audit-20261001`. Credentials are never saved. Raw artifacts are
not included in public report copy. Audit scripts are under `scripts/audit_*`
and `scripts/compare_native_audit.py`; paid script has an exclusive reservation
and no retries. Run only within an explicitly authorized benchmark scope.

Doctor initially failed because it required the retired `LEGENDS.md`, which
existing tests explicitly forbid. Repaired root detection to check the actual
module marker and router skill; added positive/negative regressions. Doctor then
passed. Its legacy wrapper also creates a Treasury capture even in offline mode;
the audit did not mistake that side effect for a pure offline readiness check.
No production routing behavior was changed, and no release was published.
