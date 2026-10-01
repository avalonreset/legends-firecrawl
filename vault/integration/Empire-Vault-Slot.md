---
type: integration-guide
title: "Legends Empire Vault Integration"
status: living
created: 2026-09-24
updated: 2026-09-24
tags:
  - empire-vault
  - module-slot
  - kit-architecture
---

# How Legends Alexandria Slots Into Legends Empire Vault

The living **Legends Empire Vault** (`E:\empire`) organizes a founder's entire life and operations across seven constitutional provinces:
1. `[[wiki/work/Work|Work]]`: Value creation, delivery, systems, obligations.
2. `[[wiki/money/Money|Money]]`: What is owned, owed, protected, or grown.
3. `[[wiki/craft/Craft|Craft]]`: Skills and tool mastery.
4. `[[wiki/home/Home|Home]]`: Physical world and household stewardship.
5. `[[wiki/people/People|People]]`: Deliberate relationship memory.
6. `[[wiki/self/Self|Self]]`: Identity, health, and personal records.
7. `[[wiki/dreams/Dreams|Dreams]]`: Life-level purpose spanning provinces.

## The Two-Home Kit Architecture

Every Legends Kit follows the strict two-home separation of concerns:

| Layer | Canonical Location | Description |
|---|---|---|
| **Product Workbench & Runtime** | `E:\legends-firecrawl` | Official Firecrawl wrappers, CLI (`lax`), tests, offline catalog cache (`data/`), and research vault. |
| **Knowledge Source of Truth (SoT)** | `E:\empire\wiki\library\legends-firecrawl\` | The durable shelf where agents and Obsidian read domain knowledge on the monobrain. |

## Province Routing & Integration Touchpoints

1. **Library Shelf:**
   - Shelf Index: `E:\empire\wiki\library\legends-firecrawl\_Index.md`
   - Cataloged in `E:\empire\wiki\library\_Index.md` (Product and Domain Library).
2. **Work Province (`[[wiki/work/Work|Work]]`):**
   - Registered under The Map as an active data acquisition and intelligence capability.
   - Powers agent data pipelines, research, and competitive intelligence with reviewed official Firecrawl execution and saved provenance.
3. **Money Province (`[[wiki/money/Money|Money]]`):**
   - Catalogs macroeconomic and fiscal sources. Catalog presence does not imply a direct integration; all supported data execution uses official Firecrawl.
4. **Digital Territory Registry (`[[wiki/meta/Territories|Territories]]`):**
   - Registered under the root digital territory map at `E:\legends-firecrawl`.
5. **Project Card:**
   - Workbench tracking card at `E:\empire\projects\legends-firecrawl.md`.

## The Legends Obsidian Wiki Standard for Kits

Every kit vault adheres to the canonical wiki standard:
- `_Index.md` (and `index.md`): Master front door and catalog.
- `hot.md`: Short current-context cache (under 500 words) defining live state, quick commands, and hot paths.
- `log.md`: Chronological structural changelog.
- Dedicated topic directories: `manifesto/`, `tiers/`, `categories/`, `bypasses/`, `integration/`.
- Strict style rule: zero em dashes and zero en dashes across all markdown files.

