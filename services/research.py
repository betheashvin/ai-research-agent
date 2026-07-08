import os
from tavily import TavilyClient

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_web(topic: str, max_results: int = 5):
    """
    Search the web using Tavily.

    Returns a dictionary containing:
    - formatted_results (string for Gemini)
    - raw_results (original Tavily response)
    """
    search_results = tavily.search(
    query=topic,
    max_results=max_results,
    search_depth="advanced",
    include_answer=False,
    include_images=False,
    include_raw_content=False
    )

    if not search_results.get("results"):
        return {
            "success": False,
            "message": """
No reliable information was found.

Try:
- Using a more specific topic
- Searching for a company, technology, or person
""",
            "formatted_results": "",
            "raw_results": None
        }

    formatted_results = format_search_results(
        search_results["results"]
    )

    return {
        "success": True,
        "formatted_results": formatted_results,
        "raw_results": search_results
    }


def format_search_results(results):
    """
    Convert Tavily results into a clean prompt
    for the LLM.
    """

    text = ""

    for i, result in enumerate(results, start=1):

        text += f"""
Source {i}

Title:
{result.get("title", "N/A")}

Content:
{result.get("content", "N/A")}

URL:
{result.get("url", "N/A")}

----------------------------------------
"""

    return text


def extract_sources(search_results):
    """
    Return only the source URLs.

    Useful for future citations.
    """

    if not search_results:
        return []

    return [
        result["url"]
        for result in search_results["results"]
    ]


def extract_titles(search_results):
    """
    Return titles of retrieved webpages.
    """

    if not search_results:
        return []

    return [
        result["title"]
        for result in search_results["results"]
    ]


def search_successful(search_response):
    """
    Utility function used by the agent.
    """

    return search_response["success"]