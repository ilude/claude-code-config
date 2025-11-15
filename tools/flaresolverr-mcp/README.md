# FlareSolverr MCP Server

MCP server wrapper for FlareSolverr to bypass Cloudflare bot protection and fetch protected web content.

## What This Does

Provides Claude Code with the ability to fetch content from websites protected by Cloudflare's bot detection, including:
- OpenAI documentation (platform.openai.com/docs)
- Any site returning 403/challenge responses
- Sites with JavaScript challenges

## Setup

### 1. Start FlareSolverr Container

```bash
cd ~/.claude/tools/flaresolverr-mcp
docker compose up -d
```

Verify running:
```bash
docker ps | grep flaresolverr
curl http://localhost:8191/v1
```

### 2. Install Python Dependencies (if needed)

The MCP server requires several packages for HTML processing and content extraction:
```bash
cd ~/.claude/tools/flaresolverr-mcp
uv pip install --system -r requirements.txt
```

Dependencies include:
- `mcp>=1.0.0` - MCP server framework
- `httpx>=0.27.0` - HTTP client for FlareSolverr API
- `beautifulsoup4>=4.12.0` - HTML parsing
- `readability-lxml>=0.8.1` - Content extraction
- `lxml>=4.9.0` - XML/HTML processing

### 3. Test MCP Server

Test that the server works:
```bash
cd ~/.claude/tools/flaresolverr-mcp
python test_flaresolverr.py
```

This should successfully fetch OpenAI docs and display the HTML content.

### 4. Configuration

The MCP server is ready to use. Configuration details are in `mcp-catalog.json`.

**To activate:** Tell Claude Code:
```
Add the flaresolverr MCP server from ~/.claude/tools/flaresolverr-mcp/
```

## Usage

Once added, Claude Code can use these tools:

### fetch_url
Fetch URL content bypassing Cloudflare protection with intelligent content extraction.

**Parameters:**
- `url` (string, required): The URL to fetch
- `max_timeout` (integer, optional): Max timeout in milliseconds (default: 60000)
- `extract_content` (boolean, optional): Extract main content only, removing navigation/ads/scripts (default: true)
- `max_tokens` (integer, optional): Maximum tokens per page (default: 20000)
- `return_format` (string, optional): Output format - "auto", "content_only", "full_html", or "metadata" (default: "auto")
- `page` (integer, optional): Page number to retrieve (default: 1)
- `continuation_token` (string, optional): Token from previous response for fetching next page
- `cache_content` (boolean, optional): Cache content for pagination (default: true)

**Returns:**
When `extract_content=true`:
- `title`: Page title
- `content`: Extracted main text content (cleaned)
- `content_html`: HTML of main content area
- `estimated_tokens`: Approximate token count
- `was_truncated`: Whether content was truncated to fit max_tokens
- `cookies`: Session cookies
- `userAgent`: User agent used
- `status`: HTTP status code
- `url`: Final URL after redirects
- `html`: Full HTML (only if return_format="full_html")

When `extract_content=false`:
- `html`: Full page HTML
- `cookies`, `userAgent`, `status`, `url`: As above

**Pagination Response Fields:**
- `pagination` (object): Pagination metadata (when content is paginated)
  - `page` (integer): Current page number
  - `page_size` (integer): Tokens per page
  - `total_pages` (integer): Total number of pages
  - `total_tokens` (integer): Total estimated tokens in full content
  - `has_next` (boolean): Whether more pages are available
  - `has_previous` (boolean): Whether previous page exists
  - `continuation_token` (string): Token for fetching next page (only if has_next is true)
  - `offset` (integer): Character offset of current page
  - `limit` (integer): Character limit of current page
- `from_cache` (boolean): Whether content was retrieved from cache

**Examples:**

**Basic usage (auto extracts main content):**
```python
# Fetches OpenAI docs with content extraction
fetch_url(url="https://platform.openai.com/docs/overview")
# Returns ~5-10K tokens instead of 48K
```

**Get only the text content:**
```python
# Returns just the cleaned text, no HTML or metadata
fetch_url(
    url="https://platform.openai.com/docs/overview",
    return_format="content_only"
)
```

**Get full HTML (no extraction):**
```python
# Disables content extraction, returns full HTML
fetch_url(
    url="https://platform.openai.com/docs/overview",
    extract_content=false,
    return_format="full_html"
)
```

**Get metadata only:**
```python
# Returns title, token count, URL - no content/HTML
fetch_url(
    url="https://platform.openai.com/docs/overview",
    return_format="metadata"
)
```

**Custom token limit:**
```python
# Limits response to 10K tokens with smart truncation
fetch_url(
    url="https://platform.openai.com/docs/overview",
    max_tokens=10000
)
```

**Why use content extraction?**
- **Token savings**: 70-90% reduction (48K → 5-10K tokens typical)
- **Better focus**: Removes navigation, ads, scripts, footers
- **Cleaner output**: Just the documentation/article content
- **MCP limits**: Stays under 25K token MCP response limit

## Pagination Examples

For large articles that exceed the token limit, use pagination to retrieve content in chunks.

### Example 1: Sequential Page Fetching

```python
# First page (auto-detected pagination)
response1 = fetch_url(url="https://archive.ph/17bPN", max_tokens=10000)
print(f"Page {response1['pagination']['page']} of {response1['pagination']['total_pages']}")
print(f"Content: {response1['content'][:200]}...")

# Check if more pages exist
if response1['pagination']['has_next']:
    # Get next page using continuation token
    response2 = fetch_url(
        url="https://archive.ph/17bPN",
        continuation_token=response1['pagination']['continuation_token']
    )
    print(f"Page {response2['pagination']['page']}: {response2['content'][:200]}...")
```

### Example 2: Direct Page Access

```python
# Jump directly to page 3
response = fetch_url(
    url="https://archive.ph/17bPN",
    page=3,
    max_tokens=10000
)

print(f"Fetched page {response['pagination']['page']} of {response['pagination']['total_pages']}")
print(f"From cache: {response['from_cache']}")
```

### Example 3: Retrieve All Pages (Loop)

```python
# Pseudo-code for client-side pagination loop
url = "https://archive.ph/17bPN"
all_content = []
continuation = None
page_num = 1

while True:
    response = fetch_url(
        url=url,
        continuation_token=continuation,
        max_tokens=10000
    )
    
    all_content.append(response["content"])
    print(f"Fetched page {page_num}/{response['pagination']['total_pages']}")
    
    if not response["pagination"]["has_next"]:
        break
    
    continuation = response["pagination"]["continuation_token"]
    page_num += 1

# Join all pages
full_content = "
".join(all_content)
print(f"Total content length: {len(full_content)} chars")
```

### Example 4: Check Content Size Before Fetching

```python
# Get metadata only to see total size
response = fetch_url(
    url="https://archive.ph/17bPN",
    return_format="metadata"
)

print(f"Total pages: {response['pagination']['total_pages']}")
print(f"Total tokens: {response['pagination']['total_tokens']}")

# Decide if you want to fetch all pages
if response['pagination']['total_pages'] <= 3:
    # Fetch all pages...
    pass
```

### Pagination Behavior

**Caching:**
- Content is cached for 15 minutes after first fetch
- Subsequent page requests use cached content (faster, no re-fetch)
- Cache is per-session and cleared when session is destroyed
- Maximum 10 URLs cached per session (FIFO eviction)

**Continuation Tokens:**
- Tokens are base64-encoded and contain: URL, session ID, and next page number
- Tokens are session-specific and won't work across different sessions
- Tokens are stateless - you can fetch pages in any order

**Token Limits:**
- Each page respects the `max_tokens` parameter (default: 20000)
- Smart truncation at newline boundaries to avoid cutting mid-sentence
- Total content size is estimated and reported in `total_tokens`

**Performance:**
- First fetch: ~15-30 seconds (Cloudflare solving + content extraction)
- Subsequent pages: <100ms (served from cache)
- Cache hit indicated by `from_cache: true` in response

### create_session
Create a persistent session to reuse cookies across multiple requests.

**Example:**
```
User: Create a FlareSolverr session for multiple requests
```

### destroy_session
Destroy the current session.

## Content Extraction Features

The server automatically extracts main content from web pages using Mozilla's Readability algorithm (same as Firefox Reader View):

**What gets extracted:**
- Main article/documentation content
- Page title and structure
- Relevant images and code blocks

**What gets removed:**
- Navigation menus and sidebars
- Advertisements and tracking scripts
- Headers and footers
- Cookie banners and popups
- Comments sections

**Token Estimation:**
Uses rough estimation (1 token ≈ 4 characters) to stay within MCP's 25K token response limit.

**Smart Truncation:**
If content exceeds `max_tokens`, it truncates at natural break points (newlines) to avoid cutting mid-sentence.

## How It Works

1. FlareSolverr container runs headless Chrome to solve Cloudflare challenges
2. MCP server communicates with FlareSolverr API (port 8191)
3. Returns HTML content + cookies for further requests
4. Sessions persist cookies for efficiency
5. Content is cached for pagination (15-minute TTL, max 10 URLs per session)

## Troubleshooting

**Container not running:**
```bash
docker compose up -d
docker logs flaresolverr
```

**Port 8191 in use:**
Edit `docker-compose.yml` and change port mapping:
```yaml
ports:
  - "8192:8191"  # Use 8192 instead
```
Then update `server.py` api_url.

**Timeout errors:**
Increase `max_timeout` parameter (Cloudflare challenges can take 15-30 seconds).

**Still getting 403:**
- Check if site uses CAPTCHA (FlareSolverr can't solve these)
- Try destroying and recreating session
- Check FlareSolverr logs: `docker logs flaresolverr`

## Limitations

- Cannot solve CAPTCHAs (only JavaScript challenges)
- Slower than direct requests (15-30s per solve)
- Some sites may detect headless Chrome
- Success rate: ~85% for typical Cloudflare protection
- Content extraction works best on article/documentation sites (may miss content on complex web apps)

## Maintenance

**Stop container:**
```bash
cd ~/.claude/tools/flaresolverr-mcp
docker compose down
```

**Update FlareSolverr:**
```bash
docker compose pull
docker compose up -d
```

**Check logs:**
```bash
docker logs -f flaresolverr
```
