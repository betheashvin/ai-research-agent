import os
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_report(search_results: str, report_type="Research Report"):
    """
    Generate a structured report from web search results.
    """

    prompt = f"""
You are an experienced research analyst.

Your task is to write a professional {report_type}.

Requirements:

- Use only the provided search results.
- Never invent facts.
- If information cannot be verified, clearly state that.
- Do NOT use markdown (#, ##, *, **).
- Do NOT use hashtags.
- Avoid repetition.
- Keep a professional writing style.
- Mention uncertainty whenever appropriate.

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

Search Results:

{search_results}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def evaluate_report(report: str):
    """
    Evaluate report quality and return a numeric score plus feedback.
    """

    prompt = f"""
You are reviewing an AI-generated research report.

Evaluate it using the following criteria:

- Completeness
- Accuracy
- Organization
- Hallucination Risk
- Source Usage

Return ONLY valid JSON.

Example:

{{
    "score":8,
    "feedback":"Well structured but missing competitors."
}}

Report:

{report}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def summarize_text(text: str):
    """
    Generate a concise summary.
    """

    prompt = f"""
Summarize the following text in 5-7 concise bullet points.

{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def compare_reports(report_one: str, report_two: str):
    """
    Compare two reports and highlight similarities and differences.
    """

    prompt = f"""
Compare these two research reports.

Include:

Overview

Similarities

Differences

Strengths

Weaknesses

Conclusion

Report A:

{report_one}

---------------------------------------

Report B:

{report_two}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def rewrite_report(report: str, style="Executive Summary"):
    """
    Rewrite an existing report into another format.
    """

    prompt = f"""
Rewrite this report into the following format:

{style}

Possible styles:

- Executive Summary
- Startup Analysis
- SWOT Analysis
- Interview Preparation Notes
- Investor Brief

Report:

{report}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text