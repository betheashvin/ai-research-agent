import os
from tavily import TavilyClient
from google import genai

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def research_topic(topic):
    search_results = tavily.search(query=topic, max_results=5)
    
    if not search_results["results"]:
       return """
No reliable information was found for this topic.

Try:
- Using a more specific search query
- Searching for a known company, technology, or person
"""

    results_text = ""

    for result in search_results["results"]:
        results_text += f"""
        Title : {result['title']}
        Content : {result['content']}
        URL : {result['url']} 
        """
        
    prompt = f"""
You are a research analyst.

Using the search results provided, write a professional research report.

Requirements:

- Use clear section titles without markdown symbols (#, ##, *, etc.).
- Write in a natural business-report style.
- Do not use hashtags.
- Do not mention that you are an AI.
- Do not include phrases such as "based on the search results provided".
- Avoid unncessary repetition.
- If information is uncertain, explicitly state that it could not be verified.
- Do not invent facts, statistics, dates, funding amounts, people, or events.
- Use only information supported by the sources.
- If insufficient information exists, state that clearly.
- If the search results are weak, incomplete, or unrelated to the query,
state that reliable information could not be found instead of guessing.

Structure:

Executive Summary

Overview

Key Findings

Products or Services

Recent Developments

Competitors or Alternatives

Risks and Challenges

Key Takeaways

Sources

Search Results: {results_text}
"""
    
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
) 
    return response.text