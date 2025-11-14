"""Research tools for Writers Factory.

This module provides integration with external research platforms like NotebookLM.
"""

from .notebooklm_client import NotebookLMClient, AuthenticationError, NotebookNotFoundError, QueryTimeoutError

__all__ = [
    'NotebookLMClient',
    'AuthenticationError',
    'NotebookNotFoundError',
    'QueryTimeoutError',
]
