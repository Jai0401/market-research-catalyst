from langchain.tools import BaseTool
from exa_py import Exa
from typing import Optional, Type

from config import EXA_API_KEY


class WebBrowserTool(BaseTool):
    name: str = "web_browser"
    description: str = "Useful for browsing the web and retrieving information. Input should be a search query."

    def _run(self, query: str) -> str:
        """Use the tool to search the web."""
        exa = Exa(EXA_API_KEY)
        search_results = exa.search_and_rerank(query, num_results=5) # Adjust num_results as needed
        content = ""
        for result in search_results.results:
            try:
                page_content = exa.get_content(result.url).text
                content += f"URL: {result.url}\nContent:\n{page_content[:500]}...\n---\n" # Limit content to avoid token issues
            except Exception as e: # Catch exceptions if page content retrieval fails
                content += f"Could not retrieve content from {result.url}. Error: {e}\n---\n"
        return content

    async def _arun(self, query: str) -> str:
        """Use the tool to search the web asynchronously."""
        raise NotImplementedError("This tool does not support asynchronous operations yet.")