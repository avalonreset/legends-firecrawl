# Candidate verification: 0.2.0rc1

Historical candidate only. Superseded by 0.2.0: all direct-source substitution has been retired. This report does not describe the active release.

October 1, 2026. Prepared locally; not published.

- 36 Python tests passed in the checkout and extracted archive.
- 19 independently authored Node regression tests passed in both environments.
- Offline doctor passed without making a Treasury request or saving a capture.
- Three fresh direct requests passed: debt, average interest rates, and debt page 2 restricted to two fields. Raw results: `var/native-audit-20261001/candidate-live.json` (local evidence, excluded from release).
- Original paired audit measured 33/33 equal field values for each Treasury operation. That bounded sample remains the evidence for the two accepted routes; fresh direct requests alone do not prove broader parity.
- Release builder excludes personal captures, seven unvalidated adapter implementations, historical provider safety classifications, and original exploratory scripts that depend on those adapters.
- Clean-room verification checks version, routes, crawl preview, catalog audit, Python tests and Node tests. Machine-readable receipts are under `release/` alongside the ZIP.

The candidate corrects exact dispatch, fields and pagination, zero versus unknown credit accounting, provider response preservation, explicit paid confirmation and duplicate capture filenames. Direct failures never silently bill. Source pacing is process-local only. There is no sustained-load or multi-process reliability claim and no measured overall user savings.

Remaining commercial decision: treat this as an operator workflow with two modest credit-saving operations. Do not advertise it as a broad cheaper replacement for Alexandria. Expand only around real workloads with equivalent output and measured reliability.
