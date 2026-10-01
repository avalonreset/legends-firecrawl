# 0.3.0 evidence workflow verification

The release adds offline, scoped evidence reuse and portable handoff. It does not replace Firecrawl, claim source parity, bypass source controls or assert a savings percentage.

## Reproducible local measurement

Run `python scripts/benchmark_evidence.py --destination NEW_DIRECTORY --records 1000`. On Windows with Python 3.11.7, a single synthetic run produced:

| Check | Measured |
|---|---:|
| Export 1,000 distinct 1 KB observations | 1.999 seconds |
| First manifest-only inventory, 1,000 packages | 11.713 seconds |
| Subsequent manifest-only filtered find | 1.056 seconds |
| Export 10,000,043-byte response | 0.030 seconds |
| Verify and select a bounded view of that response | 0.089 seconds |
| Selected output | 2,230 bytes |
| Peak Python traced allocation for selected view | 30,009,221 bytes |

The slow first inventory is recorded rather than hidden. This is a linear filesystem scan with path safety and manifest checks, not an indexed database; filesystem caching and security software can affect latency. It does not read raw response bodies. Large-response verification and view parse complete JSON, so memory grows with response size. These observations do not establish multi-gigabyte performance, concurrent-writer throughput, API scalability, savings, or a service-level guarantee.

Behavioral checks cover unchanged raw bytes, semantic capture export, duplicate export, moved packages, stale/future/wrong-client reuse, unknown/pending/error states, hash tampering, interrupted exports, duplicate/nonfinite JSON, bounded/full views, output-only receipt mode, and provider failure capture without re-submission. The extracted release runs the same Python and Node tests without ambient source paths.
