#!/usr/bin/env python3
"""
MCP server for FlareSolverr - Cloudflare bypass capability.
"""
import asyncio
import base64
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Literal
import httpx
from bs4 import BeautifulSoup
from readability import Document
from mcp.server import Server
from mcp.types import Tool, TextContent


@dataclass
class CachedContent:
    """Cached content for pagination."""
    url: str
    content: str
    content_html: str
    title: str
    timestamp: datetime
    session_id: str

    @property
    def estimated_tokens(self) -> int:
        return estimate_tokens(self.content)

    @property
    def is_expired(self) -> bool:
        """Check if cache entry is older than 15 minutes."""
        return datetime.now() - self.timestamp > timedelta(minutes=15)


def estimate_tokens(text: str) -> int:
    """Rough token estimation (1 token ≈ 4 chars)."""
    return len(text) // 4


def extract_main_content(html: str, url: str) -> dict[str, Any]:
    """Extract main content from HTML using readability."""
    try:
        # Use readability to extract main content
        doc = Document(html)
        title = doc.title()
        content_html = doc.summary()

        # Parse with BeautifulSoup to get clean text
        soup = BeautifulSoup(content_html, 'lxml')

        # Remove script and style tags
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()

        # Get text with some structure preserved
        text_content = soup.get_text(separator='\n', strip=True)

        # Clean up excessive whitespace
        text_content = re.sub(r'\n\s*\n', '\n\n', text_content)
        text_content = re.sub(r' +', ' ', text_content)

        return {
            "title": title,
            "content": text_content,
            "content_html": content_html,
            "estimated_tokens": estimate_tokens(text_content)
        }
    except Exception as e:
        return {
            "title": "",
            "content": f"Content extraction failed: {str(e)}",
            "content_html": html,
            "estimated_tokens": estimate_tokens(html)
        }


def truncate_content(content: str, max_tokens: int) -> tuple[str, bool]:
    """Truncate content to max tokens with warning."""
    estimated = estimate_tokens(content)
    if estimated <= max_tokens:
        return content, False

    # Truncate at character level (max_tokens * 4 chars)
    max_chars = max_tokens * 4
    truncated = content[:max_chars]

    # Try to truncate at last newline to avoid cutting mid-sentence
    last_newline = truncated.rfind('\n')
    if last_newline > max_chars * 0.8:  # If within last 20%, use it
        truncated = truncated[:last_newline]

    return truncated, True


def create_cache_key(url: str, session_id: str) -> str:
    """Create cache key from URL and session."""
    return f"{hashlib.md5(url.encode()).hexdigest()}:{session_id}"


def create_continuation_token(url: str, session_id: str, next_page: int) -> str:
    """Create continuation token for pagination."""
    token_data = f"{url}:{session_id}:{next_page}"
    return base64.b64encode(token_data.encode()).decode()


def parse_continuation_token(token: str) -> tuple[str, str, int]:
    """Parse continuation token to extract URL, session_id, and page."""
    try:
        decoded = base64.b64decode(token.encode()).decode()
        parts = decoded.rsplit(':', 2)
        if len(parts) == 3:
            url, session_id, page = parts
            return url, session_id, int(page)
    except Exception:
        pass
    raise ValueError("Invalid continuation token")


def paginate_content(
    content: str,
    page: int,
    page_size: int
) -> tuple[str, dict[str, Any]]:
    """
    Paginate content and return page data with pagination metadata.

    Returns:
        tuple of (page_content, pagination_metadata)
    """
    total_tokens = estimate_tokens(content)
    char_limit = page_size * 4  # 1 token ≈ 4 chars
    total_chars = len(content)

    # Calculate total pages
    total_pages = (total_tokens + page_size - 1) // page_size

    # Validate page number
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    # Calculate offset
    offset = (page - 1) * char_limit

    if offset >= total_chars:
        # Beyond content
        return "", {
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "total_tokens": total_tokens,
            "has_next": False,
            "has_previous": page > 1,
            "offset": offset,
            "limit": offset
        }

    # Extract page content
    end_offset = min(offset + char_limit, total_chars)
    page_content = content[offset:end_offset]

    # Smart truncation at newline if not last page
    if end_offset < total_chars:
        last_newline = page_content.rfind('\n')
        if last_newline > char_limit * 0.8:
            page_content = page_content[:last_newline]
            end_offset = offset + last_newline

    # Build pagination metadata
    pagination = {
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_tokens": total_tokens,
        "has_next": end_offset < total_chars,
        "has_previous": page > 1,
        "offset": offset,
        "limit": end_offset
    }

    return page_content, pagination


class FlareSolverrServer:
    """MCP server wrapping FlareSolverr API."""

    def __init__(self, api_url: str = "http://localhost:8191/v1"):
        self.api_url = api_url
        self.server = Server("flaresolverr")
        self.session_id: str | None = None
        self.content_cache: dict[str, CachedContent] = {}
        self.max_cache_entries = 10

        # Register handlers
        self.server.list_tools()(self.list_tools)
        self.server.call_tool()(self.call_tool)

    def _clean_expired_cache(self):
        """Remove expired cache entries."""
        expired_keys = [
            key for key, cached in self.content_cache.items()
            if cached.is_expired
        ]
        for key in expired_keys:
            del self.content_cache[key]

    def _enforce_cache_limit(self):
        """Enforce max cache entries limit (FIFO)."""
        if len(self.content_cache) > self.max_cache_entries:
            # Remove oldest entry
            oldest_key = min(
                self.content_cache.keys(),
                key=lambda k: self.content_cache[k].timestamp
            )
            del self.content_cache[oldest_key]

    def _cache_content(
        self,
        url: str,
        content: str,
        content_html: str,
        title: str
    ):
        """Cache content for pagination."""
        if not self.session_id:
            return

        self._clean_expired_cache()

        cache_key = create_cache_key(url, self.session_id)
        self.content_cache[cache_key] = CachedContent(
            url=url,
            content=content,
            content_html=content_html,
            title=title,
            timestamp=datetime.now(),
            session_id=self.session_id
        )

        self._enforce_cache_limit()

    def _get_cached_content(self, url: str) -> CachedContent | None:
        """Get cached content if available and not expired."""
        if not self.session_id:
            return None

        cache_key = create_cache_key(url, self.session_id)
        cached = self.content_cache.get(cache_key)

        if cached and not cached.is_expired:
            return cached

        # Remove expired entry
        if cached:
            del self.content_cache[cache_key]

        return None

    async def list_tools(self) -> list[Tool]:
        """List available MCP tools."""
        return [
            Tool(
                name="fetch_url",
                description="Fetch URL content bypassing Cloudflare protection. Returns HTML content, cookies, and metadata.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to fetch"
                        },
                        "max_timeout": {
                            "type": "integer",
                            "description": "Maximum timeout in milliseconds (default: 60000)",
                            "default": 60000
                        },
                        "extract_content": {
                            "type": "boolean",
                            "description": "Extract main content only, removing navigation/ads/scripts (default: true)",
                            "default": True
                        },
                        "max_tokens": {
                            "type": "integer",
                            "description": "Maximum tokens per page (default: 20000)",
                            "default": 20000
                        },
                        "return_format": {
                            "type": "string",
                            "enum": ["auto", "content_only", "full_html", "metadata"],
                            "description": "Response format (default: auto)",
                            "default": "auto"
                        },
                        "page": {
                            "type": "integer",
                            "description": "Page number to retrieve (default: 1)",
                            "default": 1
                        },
                        "continuation_token": {
                            "type": "string",
                            "description": "Continuation token from previous response for next page"
                        },
                        "cache_content": {
                            "type": "boolean",
                            "description": "Cache content for pagination (default: true)",
                            "default": True
                        }
                    },
                    "required": ["url"]
                }
            ),
            Tool(
                name="create_session",
                description="Create a persistent FlareSolverr session to reuse cookies across requests.",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="destroy_session",
                description="Destroy the current FlareSolverr session.",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]

    async def create_session(self) -> str:
        """Create a new FlareSolverr session."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                json={"cmd": "sessions.create"},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "ok":
                self.session_id = data.get("session")
                return self.session_id
            else:
                raise Exception(f"Failed to create session: {data.get('message')}")

    async def destroy_session(self) -> bool:
        """Destroy current session."""
        if not self.session_id:
            return False

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                json={"cmd": "sessions.destroy", "session": self.session_id},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "ok":
                self.session_id = None
                self.content_cache.clear()
                return True
            return False

    async def fetch_url(
        self,
        url: str,
        max_timeout: int = 60000,
        extract_content: bool = True,
        max_tokens: int = 20000,
        return_format: Literal["auto", "content_only", "full_html", "metadata"] = "auto",
        page: int = 1,
        continuation_token: str | None = None,
        cache_content: bool = True
    ) -> dict[str, Any]:
        """Fetch URL using FlareSolverr with pagination support."""
        # Handle continuation token
        if continuation_token:
            try:
                token_url, token_session, token_page = parse_continuation_token(continuation_token)
                url = token_url
                page = token_page
                # Validate session matches
                if token_session != self.session_id:
                    raise ValueError("Continuation token session mismatch")
            except ValueError as e:
                raise Exception(f"Invalid continuation token: {str(e)}")

        # Check cache first
        cached = self._get_cached_content(url) if cache_content else None

        if cached:
            # Use cached content for pagination
            full_content = cached.content
            title = cached.title
            content_html = cached.content_html
            html = None  # Don't need full HTML from cache

            # Build base result from cache
            result = {
                "url": url,
                "title": title,
                "from_cache": True
            }
        else:
            # Fetch fresh content
            if not self.session_id:
                await self.create_session()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json={
                        "cmd": "request.get",
                        "url": url,
                        "maxTimeout": max_timeout,
                        "session": self.session_id
                    },
                    timeout=max_timeout / 1000 + 10
                )
                response.raise_for_status()
                data = response.json()

                if data.get("status") != "ok":
                    raise Exception(f"Failed to solve challenge: {data.get('message')}")

                solution = data.get("solution", {})
                html = solution.get("response")

                # Build base result
                result = {
                    "cookies": solution.get("cookies", []),
                    "userAgent": solution.get("userAgent"),
                    "status": solution.get("status"),
                    "url": solution.get("url"),
                    "from_cache": False
                }

                # Extract content if requested
                if extract_content and html:
                    extracted = extract_main_content(html, url)
                    full_content = extracted["content"]
                    title = extracted["title"]
                    content_html = extracted["content_html"]

                    # Cache for pagination
                    if cache_content:
                        self._cache_content(url, full_content, content_html, title)
                else:
                    # No extraction - return full HTML without pagination
                    result["html"] = html
                    return result

        # Apply pagination to extracted content
        page_content, pagination_meta = paginate_content(full_content, page, max_tokens)

        # Add continuation token if there's a next page
        if pagination_meta["has_next"] and self.session_id:
            pagination_meta["continuation_token"] = create_continuation_token(
                url,
                self.session_id,
                page + 1
            )

        # Update result with paginated content
        result.update({
            "title": title,
            "content": page_content,
            "content_html": content_html if return_format == "full_html" else None,
            "estimated_tokens": estimate_tokens(page_content),
            "pagination": pagination_meta
        })

        # Include full HTML only if explicitly requested and not from cache
        if return_format == "full_html" and html:
            result["html"] = html

        return result

    async def call_tool(self, name: str, arguments: dict) -> list[TextContent]:
        """Handle tool calls."""
        try:
            if name == "fetch_url":
                url = arguments["url"]
                max_timeout = arguments.get("max_timeout", 60000)
                extract_content = arguments.get("extract_content", True)
                max_tokens = arguments.get("max_tokens", 20000)
                return_format = arguments.get("return_format", "auto")
                page = arguments.get("page", 1)
                continuation_token = arguments.get("continuation_token")
                cache_content = arguments.get("cache_content", True)

                result = await self.fetch_url(
                    url,
                    max_timeout,
                    extract_content,
                    max_tokens,
                    return_format,
                    page,
                    continuation_token,
                    cache_content
                )

                # Format response based on return_format
                if return_format == "metadata":
                    # Only return metadata, no content
                    metadata = {k: v for k, v in result.items()
                               if k not in ["html", "content", "content_html"]}
                    response_text = json.dumps(metadata, indent=2)
                elif return_format == "content_only":
                    # Only return extracted content
                    response_text = result.get("content", result.get("html", ""))
                else:
                    # auto or full_html - return complete result
                    response_text = json.dumps(result, indent=2)

                return [
                    TextContent(
                        type="text",
                        text=response_text
                    )
                ]

            elif name == "create_session":
                session_id = await self.create_session()
                return [
                    TextContent(
                        type="text",
                        text=f"Session created: {session_id}"
                    )
                ]

            elif name == "destroy_session":
                success = await self.destroy_session()
                return [
                    TextContent(
                        type="text",
                        text=f"Session destroyed: {success}"
                    )
                ]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]

    async def run(self):
        """Run the MCP server."""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Entry point."""
    server = FlareSolverrServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
