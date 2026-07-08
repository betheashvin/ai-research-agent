from typing import TypedDict

from langgraph.graph import StateGraph, END

from services.research import search_web
from services.llm import generate_report
from services.memory import (
    memory_exists,
    get_best_match,
    store_memory,
)
from services.quality import evaluate_report


class ResearchState(TypedDict):
    topic: str
    search_results: str
    report: str
    quality: dict
    used_memory: bool
    retries: int
    error: str
    
def memory_node(state: ResearchState):

    topic = state["topic"]

    if memory_exists(topic):

        memory = get_best_match(topic)

        state["report"] = memory["report"]
        state["used_memory"] = True

    else:

        state["used_memory"] = False

    return state

def search_node(state: ResearchState):

    topic = state["topic"]

    if "error" not in state:
        state["error"] = ""

    try:
        results = search_web(topic)
        
        if not results["success"]:
            state["error"] = f"Search failed: {results.get('message', 'Unknown error')}"
            return state
            
        state["search_results"] = results["formatted_results"]
    except Exception as e:
        state["error"] = f"Search exception: {str(e)}"
        
    return state

def generate_node(state: ResearchState):

    if state["used_memory"] or state.get("error"):
        return state

    try:
        report = generate_report(state["search_results"])
        state["report"] = report
    except Exception as e:
        state["error"] = f"Generation exception: {str(e)}"

    return state

def quality_node(state: ResearchState):

    if state["used_memory"]:
        state["quality"] = {
            "score": 10,
            "passed": True,
            "feedback": "Retrieved from semantic memory."
        }
        return state

    if state.get("error"):
        state["quality"] = {
            "score": 0,
            "passed": False,
            "feedback": f"Skipped evaluation due to upstream error: {state['error']}"
        }
        return state

    try:
        evaluation = evaluate_report(state["report"])
        state["quality"] = evaluation
    except Exception as e:
        state["quality"] = {
            "score": 0,
            "passed": False,
            "feedback": f"Evaluation system crashed: {str(e)}"
        }

    return state

def store_node(state: ResearchState):

    if not state["used_memory"]:

        if state["quality"]["passed"]:

            store_memory(
                state["topic"],
                state["report"]
            )

    return state

def quality_router(state: ResearchState):
  
  if state.get("error"):
    return "exit_on_error"

  if state["quality"]["passed"]:
    return "store"

  if state["retries"] >= 1:
    return "store"

  state["retries"] += 1
  return "search"


# ---------------------------------------------
# Build Workflow
# ---------------------------------------------

builder = StateGraph(ResearchState)

builder.add_node("memory", memory_node)
builder.add_node("search", search_node)
builder.add_node("generate", generate_node)
builder.add_node("quality", quality_node)
builder.add_node("store", store_node)

builder.set_entry_point("memory")

def memory_router(state: ResearchState):

    if state["used_memory"]:
        return "store"

    return "search"

builder.add_conditional_edges(
    "memory",
    memory_router,
    {
        "search": "search",
        "store": "store",
    },
)

builder.add_edge(
    "search",
    "generate",
)

builder.add_edge(
    "generate",
    "quality",
)

builder.add_conditional_edges(
    "quality",
    quality_router,
    {
        "search": "search",
        "store": "store",
        "exit_on_error": END,
    },
)

builder.add_edge(
    "store",
    END,
)

graph = builder.compile()

