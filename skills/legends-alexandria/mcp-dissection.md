# Architecture Dissection: Firecrawl MCP vs Pure Markdown

This analysis details why a pure markdown-based agent skill outperforms Firecrawl's hosted Model Context Protocol (MCP) server (`https://mcp.firecrawl.dev/v2/mcp`) for autonomous coding assistants (Grok, Codex, Claude, Gemini, Antigravity).

## 1. The MCP Illusion: Only 3 Generic Tools

Firecrawl advertises Alexandria as having 797 tools. However, inspecting the actual JSON-RPC protocol output of `https://mcp.firecrawl.dev/v2/mcp` (via `tools/list`) reveals that the server exposes **only 3 meta-tools**:

1. `firecrawl_scrape`: General scraper with an embedded `alexandria` JSON option.
2. `firecrawl_search`: Web search with a `sources: ["alexandria"]` flag.
3. `firecrawl_parse`: Document parser.

The 797 specialized capabilities are **not** registered as native MCP tools. Instead, the MCP server acts as a thin pass-through proxy.

## 2. The Multi-Hop Latency & Token Penalty

To query an Alexandria capability through MCP, an agent must execute a brittle 3-step conversation loop:

1. **Step 1: Discovery.** Agent calls `firecrawl_search` with `sources: ["alexandria"]` or calls a discovery prompt. The MCP server streams back raw text or unstructured search results. (Cost: 1000+ tokens, 1-3 seconds latency).
2. **Step 2: Schema Inspection.** Agent calls `firecrawl_scrape` or an internal `find-tools` command to read the tool contract options, types, and defaults. (Cost: 1500+ tokens, 1-2 seconds latency).
3. **Step 3: Execution.** Agent parses the contract, constructs the JSON payload, and calls `firecrawl_scrape` with `alexandria: { provider, capability, options }`. (Cost: credits billed to user account, 1-4 seconds latency).

**Total overhead per query:** 3 separate LLM generation cycles, 3 round-trip HTTP requests, 2,500+ tokens burned, and 4 to 9 seconds of wall-clock delay.

## 3. The Great Arbitrage: Paying for Free Public Data

The most critical defect of the MCP route is that it blinds the agent to the underlying data source. When an agent queries US Treasury debt, SEC filings, or ESPN scores through Firecrawl MCP:
- The user is billed Firecrawl credits.
- The request passes through Firecrawl's infrastructure, introducing an unnecessary third-party point of failure.
- Rate limits and terms gates apply.

In reality, **63.2% of the catalog (72 of 114 providers)** is unauthenticated public REST data funded by taxpayers or exposed openly on public web frontends.

## 4. The Legends Markdown Architecture: Instant, Lean, Sovereign

The `legends-firecrawl` replaces the MCP daemon with local markdown reference cards and native zero-credit adapters:

| Attribute | Firecrawl MCP Server | Legends Alexandria Markdown Skill |
|---|---|---|
| **Daemon Requirement** | Persistent process / SSE network connection | Zero background processes. Pure markdown files. |
| **Tool Discovery** | 2-3 network round trips over JSON-RPC | Instant local file read (`view_file`) or local CLI search in <5ms |
| **Token Consumption** | 2,500+ tokens burned across discovery hops | Under 200 tokens. Agent loads only the exact provider card needed. |
| **Credit Cost** | 1 to 5+ credits per query on all endpoints | **0 credits** on 63.2% of catalog via direct official REST APIs |
| **Reliability** | Susceptible to SSE stream disconnects and API outages | Direct connection to authoritative public sources (SEC, Treasury, etc.) |
| **Agent Portability** | Requires client MCP configuration (claude_desktop, etc.) | Universally supported by any LLM with file-reading tools |

## 5. Agent Workflow in Markdown Mode

1. **Identify Need:** Agent needs structured data (e.g. US Treasury National Debt).
2. **Consult Reference:** Agent checks `references/bypasses/us-treasury.md` or `references/categories/government.md`.
3. **Select Route:**
   - If public (Tier 1, 2, 3): Agent executes direct curl / fetch or uses `lax.ps1 query <provider> <tool>`. Cost: **$0.00 / 0 credits**.
   - If proprietary (Tier 4): Agent sends exact payload directly to Firecrawl API or uses `lax.ps1 query <provider> <tool> --gateway`.

