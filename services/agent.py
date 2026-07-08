from services.graph import graph


def research_with_agent(topic: str):
    """
    Execute the LangGraph workflow.
    """

    initial_state = {
        "topic": topic,
        "search_results": "",
        "report": "",
        "quality": {},
        "used_memory": False,
        "retries": 0,
    }

    result = graph.invoke(initial_state)

    return result["report"]