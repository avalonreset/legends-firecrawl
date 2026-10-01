# Retired research: Treasury direct operations

> Retired. Version 0.2.0 supports official Firecrawl execution only. No direct operation, including Treasury, is available as a supported substitution. Findings below describe the abandoned experiment.

Provider: `treasury-fiscal-data`. Historical experiment: 0.2.0rc1, superseded by official-only 0.2.0.

The retired candidate allowlist contained exactly `debt/to-the-penny` and `debt/average-interest-rates`. Each tested query returned three rows whose 33 field values matched the paid response. Each paid comparison cost one Firecrawl credit. Direct execution avoids that Firecrawl charge; it is not zero operating cost.

Official endpoints: `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny` and `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates`. Other Treasury operations are not promoted by these tests. Pagination and requested fields must be honored, not silently discarded.

This historical note preserves the earlier research path for existing links; it is not an execution guide. Read [release scope](../../docs/RELEASE-SCOPE.md) and [live audit](../../docs/NATIVE-LIVE-AUDIT-20261001.md). Historical captures are retained unchanged; their old safety labels are not current guarantees.
