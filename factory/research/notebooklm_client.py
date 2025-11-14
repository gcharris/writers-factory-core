"""NotebookLM client for querying Google NotebookLM notebooks.

This client uses Playwright for browser automation to interact with NotebookLM,
as there is no official API. It handles authentication, query execution, and
citation extraction.
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout


class AuthenticationError(Exception):
    """Raised when authentication with Google fails or is missing."""
    pass


class NotebookNotFoundError(Exception):
    """Raised when notebook URL is invalid or inaccessible."""
    pass


class QueryTimeoutError(Exception):
    """Raised when a query takes too long to complete."""
    pass


class NotebookLMClient:
    """Client for querying Google NotebookLM.

    Uses Playwright browser automation to interact with NotebookLM since there's
    no official API. Handles authentication, queries, and citation extraction.
    """

    def __init__(self, auth_tokens_path: Optional[Path] = None):
        """Initialize NotebookLM client.

        Args:
            auth_tokens_path: Path to store authentication tokens.
                            Defaults to ~/.writers-factory/notebooklm_auth.json
        """
        self.auth_tokens_path = auth_tokens_path or (
            Path.home() / ".writers-factory" / "notebooklm_auth.json"
        )
        self.auth_tokens_path.parent.mkdir(parents=True, exist_ok=True)
        self.browser = None
        self.context = None
        self.page = None

    async def authenticate(self) -> bool:
        """Authenticate with Google (one-time setup).

        Opens a browser window for the user to complete Google login. Saves
        authentication cookies for future use.

        Returns:
            True if authentication successful

        Raises:
            AuthenticationError: If login fails
        """
        try:
            async with async_playwright() as p:
                # Launch visible browser for user to log in
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()

                # Navigate to NotebookLM
                await page.goto("https://notebooklm.google.com", wait_until="networkidle")

                # Wait for user to complete login
                # We'll wait for the page to contain a specific element that appears after login
                print("Please complete Google login in the browser window...")

                try:
                    # Wait for the main app to load (indicates successful login)
                    # Adjust selector based on actual NotebookLM interface
                    await page.wait_for_selector('[data-testid="notebook-list"]', timeout=120000)
                except PlaywrightTimeout:
                    # Try alternative selectors
                    try:
                        await page.wait_for_selector('.notebook-container', timeout=10000)
                    except PlaywrightTimeout:
                        # Just check if URL changed from login page
                        current_url = page.url
                        if "accounts.google.com" in current_url:
                            raise AuthenticationError("Login not completed within timeout")

                # Save auth cookies
                cookies = await context.cookies()
                storage_state = await context.storage_state()

                with open(self.auth_tokens_path, 'w') as f:
                    json.dump(storage_state, f, indent=2)

                await browser.close()
                print("Authentication successful! Credentials saved.")
                return True

        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {str(e)}")

    async def query(
        self,
        question: str,
        notebook_url: str,
        timeout: int = 30
    ) -> Dict:
        """Query a NotebookLM notebook.

        Args:
            question: Question to ask the notebook
            notebook_url: Full URL of the notebook to query
            timeout: Maximum wait time in seconds for response

        Returns:
            {
                "answer": str,                  # The answer text
                "sources": [                    # List of source citations
                    {
                        "title": str,
                        "excerpt": str,
                        "page": int or None
                    }
                ],
                "notebook_name": str,           # Name of the notebook
                "timestamp": str                # ISO timestamp
            }

        Raises:
            AuthenticationError: If not authenticated
            NotebookNotFoundError: If notebook doesn't exist or is inaccessible
            QueryTimeoutError: If query takes too long
        """
        if not await self._is_authenticated():
            raise AuthenticationError(
                "Not authenticated with Google. Please run authenticate() first."
            )

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await self._create_authenticated_context(browser)
            page = await context.new_page()

            try:
                # Navigate to notebook
                print(f"Opening notebook: {notebook_url}")
                try:
                    await page.goto(notebook_url, wait_until="networkidle", timeout=15000)
                except PlaywrightTimeout:
                    raise NotebookNotFoundError(
                        f"Could not load notebook at {notebook_url}. "
                        "Check URL and permissions."
                    )

                # Check if we're on an error page
                if "404" in await page.content() or "not found" in await page.content().lower():
                    raise NotebookNotFoundError(f"Notebook not found: {notebook_url}")

                # Find chat input (adjust selectors based on actual NotebookLM interface)
                # These are example selectors - will need to be updated based on actual HTML
                chat_input = None
                input_selectors = [
                    'textarea[placeholder*="Ask"]',
                    'textarea[placeholder*="Question"]',
                    'textarea[aria-label*="chat"]',
                    'textarea',  # Fallback
                    'input[type="text"]'  # Last resort
                ]

                for selector in input_selectors:
                    try:
                        chat_input = await page.wait_for_selector(selector, timeout=5000)
                        if chat_input:
                            break
                    except PlaywrightTimeout:
                        continue

                if not chat_input:
                    raise QueryTimeoutError(
                        "Could not find chat input. NotebookLM interface may have changed."
                    )

                # Type question
                print(f"Asking: {question}")
                await chat_input.fill(question)

                # Submit query (try Enter key first, then look for button)
                await chat_input.press("Enter")

                # Wait for response
                print("Waiting for response...")
                response_selectors = [
                    '.response-container',
                    '[data-testid="response"]',
                    '.assistant-message',
                    '.answer-content'
                ]

                response_element = None
                for selector in response_selectors:
                    try:
                        response_element = await page.wait_for_selector(
                            selector,
                            timeout=timeout * 1000
                        )
                        if response_element:
                            break
                    except PlaywrightTimeout:
                        continue

                if not response_element:
                    raise QueryTimeoutError(
                        f"No response received within {timeout} seconds. "
                        "Try increasing timeout or check notebook accessibility."
                    )

                # Extract answer
                answer = await response_element.inner_text()

                # Extract citations
                sources = await self._extract_citations(page)

                # Extract notebook name
                notebook_name = await self._get_notebook_name(page)

                result = {
                    "answer": answer,
                    "sources": sources,
                    "notebook_name": notebook_name,
                    "timestamp": datetime.now().isoformat()
                }

                print(f"Query successful. Answer length: {len(answer)} chars")
                return result

            except PlaywrightTimeout as e:
                raise QueryTimeoutError(f"Query timed out: {str(e)}")
            except (AuthenticationError, NotebookNotFoundError, QueryTimeoutError):
                raise
            except Exception as e:
                raise Exception(f"Query failed: {str(e)}")
            finally:
                await browser.close()

    async def _extract_citations(self, page) -> List[Dict]:
        """Extract source citations from response.

        Args:
            page: Playwright page object

        Returns:
            List of citation dictionaries
        """
        citations = []

        # Try multiple citation selectors
        citation_selectors = [
            '.citation',
            '[data-testid="citation"]',
            '.source-reference',
            'a[href*="source"]'
        ]

        for selector in citation_selectors:
            try:
                citation_elements = await page.query_selector_all(selector)

                for elem in citation_elements:
                    try:
                        citation = {
                            "title": await elem.get_attribute("data-title") or
                                    await elem.get_attribute("title") or
                                    await elem.inner_text(),
                            "excerpt": await elem.inner_text(),
                            "page": await elem.get_attribute("data-page")
                        }
                        citations.append(citation)
                    except Exception:
                        # Skip citations that fail to extract
                        continue

                if citations:
                    break  # Found citations, stop trying other selectors

            except Exception:
                continue

        return citations

    async def _get_notebook_name(self, page) -> str:
        """Extract notebook name from page.

        Args:
            page: Playwright page object

        Returns:
            Notebook name or "Unknown Notebook"
        """
        name_selectors = [
            'h1[data-testid="notebook-title"]',
            'h1',
            '[data-testid="title"]',
            '.notebook-title'
        ]

        for selector in name_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    name = await element.inner_text()
                    if name and len(name) > 0:
                        return name.strip()
            except Exception:
                continue

        return "Unknown Notebook"

    async def _is_authenticated(self) -> bool:
        """Check if user is authenticated.

        Returns:
            True if auth tokens exist
        """
        return self.auth_tokens_path.exists()

    async def _create_authenticated_context(self, browser):
        """Create browser context with saved authentication.

        Args:
            browser: Playwright browser instance

        Returns:
            Authenticated browser context
        """
        # Load saved storage state (cookies, localStorage, etc.)
        with open(self.auth_tokens_path, 'r') as f:
            storage_state = json.load(f)

        context = await browser.new_context(storage_state=storage_state)
        return context

    async def test_connection(self) -> bool:
        """Test if NotebookLM is accessible.

        Returns:
            True if NotebookLM can be reached
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto("https://notebooklm.google.com", timeout=10000)
                await browser.close()
                return True
        except Exception:
            return False
