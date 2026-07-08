import json
from services.llm import client


def evaluate_report(report: str):
    """
    Evaluate the quality of a generated report.

    Returns:
    {
        "score": 8,
        "passed": True,
        "feedback": "..."
    }
    """

    prompt = f"""
You are a senior research reviewer.

Evaluate the following report.

Score it from 1 to 10 based on:
- Accuracy
- Completeness
- Structure
- Readability
- Hallucination Risk
- Source Usage

Return ONLY valid JSON containing the exact keys "score", "passed", and "feedback".

Example:
{{
    "score": 8,
    "passed": true,
    "feedback": "Good report but missing competitors."
}}

Report:
{report}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Clean up common markdown wrappers from the LLM response
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "").strip()

    try:
        result = json.loads(text)
    except Exception:
        # Emergency backup dictionary if the JSON parser crashes
        result = {
            "score": 5,
            "feedback": "Unable to parse JSON evaluation from model."
        }

    # SAFEGUARD: Ensure the "passed" key exists no matter what Gemini returns
    if "passed" not in result:
        # If Gemini gave a score but forgot the boolean, calculate it manually
        if "score" in result and isinstance(result["score"], (int, float)):
            result["passed"] = result["score"] >= 7
        else:
            result["passed"] = False
            result["score"] = 0

    return result


def needs_improvement(report: str):
    """
    Returns True if the report should be regenerated.
    """

    evaluation = evaluate_report(report)

    return not evaluation["passed"]


def quality_summary(report: str):
    """
    Returns only the evaluation feedback.
    """

    evaluation = evaluate_report(report)

    return evaluation["feedback"]