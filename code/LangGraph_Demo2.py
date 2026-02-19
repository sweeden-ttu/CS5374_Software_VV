from __future__ import annotations

import json
from typing_extensions import TypedDict, Literal
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END

from langchain_ollama import ChatOllama


Route = Literal["question", "compliment"]


class State(TypedDict, total=False):
    payload: list[dict]
    text: str
    route: Route
    answer: str


# --- Node 1: extract text from payload ---
def extract_content(state: State) -> dict:
    return {"text": state["payload"][0]["customer_remark"]}


# --- Node 1.5: LLM router (decide question vs compliment) ---
def llm_route(state: State) -> dict:
    """
    Uses an LLM (Ollama) to classify the customer remark into:
    - "question"
    - "compliment"

    Returns: {"route": "..."}
    """
    llm = ChatOllama(model="granite-code:20b", temperature=0)

    system = (
        "You are a strict text classifier.\n"
        'Return ONLY valid JSON with exactly one key: "route".\n'
        'The value must be either "question" or "compliment".\n'
        "No extra keys, no explanation, no markdown."
    )
    user = (
        f'Text: "{state["text"]}"\n\n'
        "Classify the text as either:\n"
        '- "question": asks for information, includes inquiries, confusion, requests.\n'
        '- "compliment": praise, appreciation, positive feedback.\n\n'
        "Return JSON now."
    )

    raw = llm.invoke([("system", system), ("user", user)]).content.strip()

    # Robust parsing: try JSON first; fallback to substring detection.
    try:
        obj = json.loads(raw)
        route = obj.get("route", "").strip().lower()
    except Exception:
        route = raw.lower()

    if "question" in route:
        return {"route": "question"}
    if "compliment" in route:
        return {"route": "compliment"}

    # Default fallback if model output is unexpected
    return {"route": "question"}


# --- Router: returns the route string for conditional edges ---
def route_from_state(state: State) -> Route:
    return state["route"]


# --- Node 2a: handle compliment ---
def run_compliment_code(state: State) -> dict:
    return {"answer": "Thanks for the compliment."}


# --- Node 2b: handle question ---
def run_question_code(state: State) -> dict:
    return {"answer": "Thanks for your question. We will look into it."}


# --- Node 3: beautify using LLM (Ollama) ---
def beautify_llm(state: State) -> dict:
    llm = ChatOllama(model="granite-code:20b", temperature=0)

    prompt = (
        "Rewrite the following customer-service reply politely in ONE short sentence.\n"
        "Do not add new facts.\n\n"
        f"Reply: {state['answer']}"
    )

    pretty = llm.invoke(prompt).content.strip()
    return {"answer": pretty}


def build_graph():
    graph_builder = StateGraph(State)

    graph_builder.add_node("extract_content", extract_content)
    graph_builder.add_node("llm_route", llm_route)
    graph_builder.add_node("run_question_code", run_question_code)
    graph_builder.add_node("run_compliment_code", run_compliment_code)
    graph_builder.add_node("beautify_llm", beautify_llm)

    graph_builder.add_edge(START, "extract_content")
    graph_builder.add_edge("extract_content", "llm_route")

    graph_builder.add_conditional_edges(
        "llm_route",
        route_from_state,
        {
            "compliment": "run_compliment_code",
            "question": "run_question_code",
        },
    )

    graph_builder.add_edge("run_question_code", "beautify_llm")
    graph_builder.add_edge("run_compliment_code", "beautify_llm")
    graph_builder.add_edge("beautify_llm", END)

    return graph_builder.compile()


if __name__ == "__main__":
    graph = build_graph()

    # --- Save diagram as PNG (terminal-friendly) ---
    png_bytes = graph.get_graph().draw_mermaid_png()
    with open("langgraph_demo2_diagram.png", "wb") as f:
        f.write(png_bytes)
    print("Diagram saved as: langgraph_demo2_diagram.png")

    # --- Example payloads ---
    payload_question = [
        {
            "time_of_comment": "2025-01-20",
            "customer_remark": "Why has the packaging changed?",
            "social_media_channel": "facebook",
            "number_of_likes": 100,
        }
    ]

    payload_compliment = [
        {
            "time_of_comment": "2025-01-21",
            "customer_remark": "I love your product—great job!",
            "social_media_channel": "instagram",
            "number_of_likes": 42,
        }
    ]

    print("\n=== RUN: QUESTION ===")
    result = graph.invoke({"payload": payload_question})
    print("FINAL RESULT:\n", result)

    print("\nSTREAM:\n")
    for step in graph.stream({"payload": payload_question}):
        print(step)

    print("\n=== RUN: COMPLIMENT ===")
    result = graph.invoke({"payload": payload_compliment})
    print("FINAL RESULT:\n", result)

    print("\nSTREAM:\n")
    for step in graph.stream({"payload": payload_compliment}):
        print(step)
