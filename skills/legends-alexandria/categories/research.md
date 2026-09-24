---
category: "research"
type: reference-card
provider_count: 1
---

# Category: research

> Scientific papers, abstracts, relevant full-text passages and citation relationships.

**Providers in this category:** 1

| Provider ID | Provider Name | Capabilities | Tier | Cost | Bypass Route |
|---|---|---|---|---|---|
| `firecrawl-research-index` | **Research Index** | 4 | Proprietary Commercial B2B Data Brokers | Credits Required or Paid Vendor Key | Use Alexandria credits or direct vendor account |

## Capabilities Overview

### Research Index (`firecrawl-research-index`)

Find scientific papers, inspect metadata, read relevant passages and follow citation relationships.

- **`inspect`** (Inspect paper): Read a paper's metadata and abstract without retrieving full text. [Cost: 0 credit]  
  *Options:* `paperId` *(required)*
- **`read`** (Read paper passages): Retrieve paper passages relevant to a question. Empty passages do not mean the full paper was read. [Cost: 0 credit]  
  *Options:* `paperId` *(required)*, `query` *(required)*, `k`
- **`related`** (Find related papers): Find similar work, papers citing a seed or its references, ranked for your research question. [Cost: 0 credit]  
  *Options:* `paperId` *(required)*, `intent` *(required)*, `k`, `mode`, `anchor`, `rerank`
- **`search`** (Search papers): Find scientific papers about a research question, then use indexed paperIds for follow-up calls. [Cost: 0 credit]  
  *Options:* `query` *(required)*, `k`, `authors`, `categories`, `from`, `to`

