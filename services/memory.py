from datetime import datetime
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="research_reports"
)


def store_memory(topic: str, report: str):
    """
    Store a research report inside semantic memory.
    """

    created_at = datetime.now().isoformat()

    document = f"""
Topic:
{topic}

Report:
{report}
"""

    collection.add(
        ids=[f"{topic}_{created_at}"],
        documents=[document],
        metadatas=[{
            "topic": topic,
            "created_at": created_at
        }]
    )


def query_semantic_memory(query: str, n_results: int = 3):
    """
    Search semantic memory.

    Returns the raw ChromaDB response.
    """

    return collection.query(
        query_texts=[query],
        n_results=n_results
    )


def memory_exists(query: str, threshold: float = 0.30):
    """
    Determine whether we already have a similar report.

    Returns:
        True / False
    """

    results = collection.query(
        query_texts=[query],
        n_results=1
    )

    if not results["documents"][0]:
        return False

    if "distances" not in results:
        return True

    distance = results["distances"][0][0]

    return distance < threshold


def get_best_match(query: str):
    """
    Return the most relevant previous report.
    """

    results = collection.query(
        query_texts=[query],
        n_results=1
    )

    if not results["documents"][0]:
        return None

    return {
        "topic": results["metadatas"][0][0]["topic"],
        "created_at": results["metadatas"][0][0]["created_at"],
        "report": results["documents"][0][0]
    }


def delete_memory(memory_id: str):
    """
    Delete one memory.
    """

    collection.delete(ids=[memory_id])


def clear_memory():
    """
    Delete every stored report.
    Useful during development.
    """

    all_items = collection.get()

    if all_items["ids"]:
        collection.delete(ids=all_items["ids"])


def memory_count():
    """
    Number of reports stored.
    """

    return collection.count()