---
type: category
id: "ai-models"
title: "Ai Models"
providers_count: 2
---

# Category: Ai Models

> Machine-learning models and datasets: cards, licenses, downloads, tasks, tags and files.

Part of [[_Index|Legends Alexandria]] and the [[manifesto/The-Great-AI-Data-Arbitrage|Great AI Data Arbitrage]].

## Cataloged Providers (2)

| Provider | Capabilities | Data Tier | Direct Bypass Available? |
|---|---|---|---|
| `huggingface-co` (**Hugging Face**) | 5 | Open Non-Profit, Legal & Community Ecosystems | Yes (Direct community/non-profit REST API) |
| `openrouter-ai` (**OpenRouter**) | 8 | Proprietary Commercial B2B Data Brokers | No (Proprietary) |

## Tools & Capabilities

### Hugging Face (`huggingface-co`)

Search Hugging Face models and datasets, inspect repository metadata, and read public model and dataset cards.

- **`hub/card`** (Card): The README model or dataset card of one repository at a revision: raw YAML front matter, markdown body, section headings, word count and the Hub's parsed card data, plus license and gating. Works for gated repositories; `has_card` is false when the repository has no README. (Cost: 5 credit)
- **`hub/dataset`** (Dataset): One dataset repository: canonical id, author, license(s), task categories, languages, size categories, 30-day and all-time downloads, likes, gating, tags, description, citation, file list, configs, dataset_info (features and splits) and the parsed dataset-card front matter. (Cost: 5 credit)
- **`hub/datasets`** (Datasets): Search and list datasets by free text, author, task category, language, license, size category and tags, sorted by downloads, likes, trending, last modified or created; up to 100 per page with an opaque cursor. Each result carries license, downloads, likes, task categories, size and gating. (Cost: 5 credit)
- **`hub/model`** (Model): One model repository: canonical id, author, license(s), pipeline tag, library, 30-day and all-time downloads, likes, trending score, gating, tags, languages, base models, training datasets, file list, safetensors parameter counts, config architecture, inference providers and the parsed model-card front matter. (Cost: 5 credit)
- **`hub/models`** (Models): Search and list models by free text, author, task (pipeline tag), library, language, license and tags, sorted by downloads, likes, trending, last modified or created; up to 100 per page with an opaque cursor for the next page. Each result carries license, downloads, likes, gating and tags. (Cost: 5 credit)

### OpenRouter (`openrouter-ai`)

OpenRouter model catalog and marketplace data: search models by modality, author, provider and price; per-model provider endpoints with pricing, limits, data policy and uptime; effective and listed price history; usage and availability stats; the provider directory; author lineups; and documentation pages such as the Decisions API reference and the Jev decision-model guide. Anonymous public endpoints only; no inference.

- **`model-marketplace/get_docs_page`** (Get docs page): To read the typed Decisions API contract, confidence interpretation or any other OpenRouter guide without an API key. The index of all pages is `llms.txt`. (Cost: 5 credit)
- **`model-marketplace/get_model`** (Get model): Verify that a model exists and see which providers serve it at what price; take `canonical_slug` from here into the permaslug-keyed functions. (Cost: 5 credit)
- **`model-marketplace/get_model_endpoints`** (Get model endpoints): After get_model, when you need endpoint UUIDs, rate limits, data policy or latency percentiles per provider. (Cost: 5 credit)
- **`model-marketplace/get_model_pricing`** (Get model pricing): To answer 'what does this model cost today and has it changed' for a permaslug from search_models/get_model. (Cost: 5 credit)
- **`model-marketplace/get_model_stats`** (Get model stats): To judge whether a model is actively used and reliably available before building on it. (Cost: 5 credit)
- **`model-marketplace/list_author_models`** (List author models): To enumerate a vendor's whole lineup (e.g. everything by `typesafe` or `openai`) with permaslugs for the stats functions. (Cost: 5 credit)
- **`model-marketplace/list_providers`** (List providers): To resolve a provider slug for search_models `providers=` or to review data policies across providers. (Cost: 5 credit)
- **`model-marketplace/search_models`** (Search models): Start here to find a model slug and permaslug, e.g. `q=jev, output_modalities=decisions` to check whether the TypeSafe Jev decision model is listed; then call get_model / get_model_endpoints / get_model_pricing. (Cost: 5 credit)


