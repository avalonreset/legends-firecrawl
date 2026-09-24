---
category: "health"
type: reference-card
provider_count: 1
---

# Category: health

> Population health statistics: life expectancy, mortality, disease burden, immunization coverage, risk factors, health systems and WASH by country, region and year.

**Providers in this category:** 1

| Provider ID | Provider Name | Capabilities | Tier | Cost | Bypass Route |
|---|---|---|---|---|---|
| `ihme-gbd-results` | **IHME GBD Results** | 4 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |

## Capabilities Overview

### IHME GBD Results (`ihme-gbd-results`)

IHME Global Burden of Disease Results tool metadata: release versions and the full cause, location, age, sex, measure, metric and risk-factor (REI) hierarchies for GBD 2021 and GBD 2023.

- **`gbd/children`** (Hierarchy children): Traverse one level down a hierarchy: the direct children of a cause, location or rei node (e.g. GBD region Western Europe to its 24 countries), plus the parent node and its ancestors. [Cost: 1 credit]  
  *Options:* `type` *(required)*, `id` *(required)*, `gbd_round` *(required)*, `proxy`
- **`gbd/lookup`** (Entity lookup): Resolve one entity (cause, location, age, sex, measure, metric or rei) by GBD id in a GBD round: its hierarchy_node record plus ancestors (root first) and direct children. [Cost: 1 credit]  
  *Options:* `type` *(required)*, `id` *(required)*, `gbd_round` *(required)*, `proxy`
- **`gbd/metadata`** (Hierarchy page): One page of hierarchy_node records for an entity type (cause, location, age, sex, measure, metric, rei) in a GBD round: id, name, parent_id, level, tree placement and the raw source entry. Tree types come in depth-first hierarchy order; page with cursor until next_cursor is null. [Cost: 1 credit]  
  *Options:* `type` *(required)*, `gbd_round` *(required)*, `page_size`, `cursor`, `proxy`
- **`gbd/versions`** (Release versions): List the GBD Results tool release versions (version id, GBD round, release stamp, model description, exposed measure ids) for one or both supported rounds. Use it to pin gbd_round/version_id and read the tool's stated release date. [Cost: 1 credit]  
  *Options:* `gbd_round`, `proxy`

