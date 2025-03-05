from langchain.tools import BaseTool
from exa_py import Exa
from typing import Optional, Type

from config import EXA_API_KEY

class WebBrowserTool(BaseTool):
    name: str = "web_browser"
    description: str = "Useful for browsing the web and retrieving information. Input should be a search query."

    def _run(self, query: str) -> str:
        """Use the tool to search the web."""
        # Always use the current value from config
        from config import EXA_API_KEY
        
        exa = Exa(EXA_API_KEY)
        # Use type="auto" to combine neural and keyword search (adjust as needed)
        search_results = exa.search_and_contents(query, num_results=5, type="auto")
        content = f"Found {len(search_results.results)} results.\n\n"
        for result in search_results.results:
            try:
                # Use the text already provided if available, otherwise fetch page content.
                text_content = result.text if hasattr(result, "text") and result.text else exa.get_content(result.url).text
                content += (
                    f"Title: {result.title}\n"
                    f"URL: {result.url}\n"
                    f"Content:\n{text_content[:500]}...\n"
                    f"---\n"
                )
            except Exception as e:
                content += f"Could not retrieve content from {result.url}. Error: {e}\n---\n"
        return content

    async def _arun(self, query: str) -> str:
        """Use the tool to search the web asynchronously."""
        raise NotImplementedError("This tool does not support asynchronous operations yet.")
