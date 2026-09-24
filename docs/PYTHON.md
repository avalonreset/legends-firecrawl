# Python consumer surface

Add `E:\legends-firecrawl\python` to `PYTHONPATH` or install the local
package in the consumer's environment.

```python
from legends_firecrawl import FirecrawlClient

client = FirecrawlClient(consumer="my-product")
page = client.scrape("https://example.com", formats=["markdown", "links"])
urls = client.map_site("https://example.com", limit=100)
```

Legends Packet can use:

```python
from legends_firecrawl.packet_compat import discover_site_pages, scrape_page
```

The compatibility module reuses the Kit's credential lookup, URL safety,
defaults, and ledger. Consumers should not create their own Firecrawl credential
file or require a vendor SDK/MCP server.

