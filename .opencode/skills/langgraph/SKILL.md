---
name: langgraph
description: Expert in LangGraph - the production-grade framework for building stateful, multi-actor AI applications. Covers graph construction, state management, cycles and branches, persistence with checkpointers, human-in-the-loop patterns, and the ReAct agent pattern.
license: Apache-2.0
compatibility: opencode
metadata:
  source: vibeship-spawner-skills
  framework: LangGraph
  python: ">=3.9"
---

# LangGraph

Expert in LangGraph - the production-grade framework for building stateful, multi-actor
AI applications. Covers graph construction, state management, cycles and branches,
persistence with checkpointers, human-in-the-loop patterns, and the ReAct agent pattern.
Used in production at LinkedIn, Uber, and 400+ companies. This is LangChain's recommended
approach for building agents.

**Role**: LangGraph Agent Architect

You are an expert in building production-grade AI agents with LangGraph. You
understand that agents need explicit structure - graphs make the flow visible
and debuggable. You design state carefully, use reducers appropriately, and
always consider persistence for production. You know when cycles are needed
and how to prevent infinite loops.

## Expertise

- Graph topology design
- State schema patterns
- Conditional branching
- Persistence strategies
- Human-in-the-loop
- Tool integration
- Error handling and recovery

## Capabilities

- Graph construction (StateGraph)
- State management and reducers
- Node and edge definitions
- Conditional routing
- Checkpointers and persistence
- Human-in-the-loop patterns
- Tool integration
- Streaming and async execution

## Prerequisites

- Python proficiency
- LLM API basics
- Async programming concepts
- Graph theory fundamentals
- Required: Python 3.9+, langgraph package, LLM API access (OpenAI, Anthropic, etc.)

## Scope

- Python-only (TypeScript in early stages)
- Learning curve for graph concepts
- State management complexity
- Debugging can be challenging

## Ecosystem

### Primary
- LangGraph
- LangChain
- LangSmith (observability)

### Common Integrations
- OpenAI / Anthropic / Google
- Tavily (search)
- SQLite / PostgreSQL (persistence)
- Redis (state store)

### Platforms
- Python applications
- FastAPI / Flask backends
- Cloud deployments

## Patterns

### Basic Agent Graph

Simple ReAct-style agent with tools. Use when: single agent with tool calling.

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# 1. Define State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Define Tools
@tool
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))

tools = [search, calculator]

# 3. Create LLM with tools
llm = ChatOpenAI(model="gpt-4o").bind_tools(tools)

# 4. Define Nodes
def agent(state: AgentState) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)

# 5. Define Routing
def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 6. Build Graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, ["tools", END])
graph.add_edge("tools", "agent")

# 7. Compile
app = graph.compile()

# 8. Run
result = app.invoke({
    "messages": [("user", "What is 25 * 4?")]
})
```

### State with Reducers

Complex state management with custom reducers. Use when: multiple agents updating shared state.

```python
from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import StateGraph

def merge_dicts(left: dict, right: dict) -> dict:
    return {**left, **right}

class ResearchState(TypedDict):
    messages: Annotated[list, add_messages]
    findings: Annotated[dict, merge_dicts]
    sources: Annotated[list[str], add]
    current_step: str
    errors: Annotated[int, lambda a, b: a + b]

def researcher(state: ResearchState) -> dict:
    return {
        "findings": {"topic_a": "New finding"},
        "sources": ["source1.com"],
        "current_step": "researching"
    }

def writer(state: ResearchState) -> dict:
    all_findings = state["findings"]
    all_sources = state["sources"]
    return {
        "messages": [("assistant", f"Report based on {len(all_sources)} sources")],
        "current_step": "writing"
    }

graph = StateGraph(ResearchState)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
```

### Conditional Branching

Route to different paths based on state. Use when: multiple possible workflows.

```python
from langgraph.graph import StateGraph, START, END

class RouterState(TypedDict):
    query: str
    query_type: str
    result: str

def classifier(state: RouterState) -> dict:
    query = state["query"].lower()
    if "code" in query or "program" in query:
        return {"query_type": "coding"}
    elif "search" in query or "find" in query:
        return {"query_type": "search"}
    else:
        return {"query_type": "chat"}

def route_query(state: RouterState) -> str:
    return state["query_type"]

graph = StateGraph(RouterState)
graph.add_node("classifier", classifier)
graph.add_node("coding", coding_agent)
graph.add_node("search", search_agent)
graph.add_node("chat", chat_agent)
graph.add_edge(START, "classifier")
graph.add_conditional_edges(
    "classifier", route_query,
    {"coding": "coding", "search": "search", "chat": "chat"}
)
graph.add_edge("coding", END)
graph.add_edge("search", END)
graph.add_edge("chat", END)
app = graph.compile()
```

### Persistence with Checkpointer

Save and resume agent state. Use when: multi-turn conversations, long-running agents.

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

# SQLite for development
memory = SqliteSaver.from_conn_string(":memory:")
# Or persistent file
memory = SqliteSaver.from_conn_string("agent_state.db")

# PostgreSQL for production
# memory = PostgresSaver.from_conn_string(DATABASE_URL)

# Compile with checkpointer
app = graph.compile(checkpointer=memory)

# Run with thread_id for conversation continuity
config = {"configurable": {"thread_id": "user-123-session-1"}}

# First message
result1 = app.invoke(
    {"messages": [("user", "My name is Alice")]},
    config=config
)

# Second message - agent remembers context
result2 = app.invoke(
    {"messages": [("user", "What's my name?")]},
    config=config
)

# Get conversation history
state = app.get_state(config)
print(state.values["messages"])

# List all checkpoints
for checkpoint in app.get_state_history(config):
    print(checkpoint.config, checkpoint.values)
```

### Human-in-the-Loop

Pause for human approval before actions. Use when: sensitive operations, review before execution.

```python
from langgraph.graph import StateGraph, START, END

class ApprovalState(TypedDict):
    messages: Annotated[list, add_messages]
    pending_action: dict | None
    approved: bool

def agent(state: ApprovalState) -> dict:
    action = {"type": "send_email", "to": "user@example.com"}
    return {"pending_action": action, "messages": [("assistant", f"I want to: {action}")]}

def execute_action(state: ApprovalState) -> dict:
    action = state["pending_action"]
    result = f"Executed: {action['type']}"
    return {"messages": [("assistant", result)], "pending_action": None}

def should_execute(state: ApprovalState) -> str:
    if state.get("approved"):
        return "execute"
    return END

graph = StateGraph(ApprovalState)
graph.add_node("agent", agent)
graph.add_node("execute", execute_action)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_execute, ["execute", END])
graph.add_edge("execute", END)

app = graph.compile(checkpointer=memory, interrupt_before=["execute"])

# Run until interrupt
config = {"configurable": {"thread_id": "approval-flow"}}
result = app.invoke({"messages": [("user", "Send report")]}, config)

# Human approves - update state and continue
app.update_state(config, {"approved": True})
result = app.invoke(None, config)  # Resume
```

### Parallel Execution (Map-Reduce)

Run multiple branches in parallel. Use when: parallel research, batch processing.

```python
from langgraph.graph import StateGraph, START, END, Send

class ParallelState(TypedDict):
    topics: list[str]
    results: Annotated[list[str], add]
    summary: str

def research_topic(state: dict) -> dict:
    topic = state["topic"]
    return {"results": [f"Research on {topic}..."]}

def summarize(state: ParallelState) -> dict:
    return {"summary": f"Summary of {len(state['results'])} topics"}

def fanout_topics(state: ParallelState) -> list[Send]:
    return [Send("research", {"topic": topic}) for topic in state["topics"]]

graph = StateGraph(ParallelState)
graph.add_node("research", research_topic)
graph.add_node("summarize", summarize)
graph.add_conditional_edges(START, fanout_topics, ["research"])
graph.add_edge("research", "summarize")
graph.add_edge("summarize", END)

app = graph.compile()

result = app.invoke({"topics": ["AI", "Climate", "Space"], "results": []})
```

## Related Skills

Works well with: `langfuse` (observability), `structured-output` (structured LLM responses), `crewai` (multi-agent), `agent-evaluation` (testing agents)

## When to Use

- User mentions or implies: langgraph
- User mentions or implies: langchain agent
- User mentions or implies: stateful agent
- User mentions or implies: agent graph
- User mentions or implies: react agent
- User mentions or implies: agent workflow
- User mentions or implies: multi-step agent
- User mentions or implies: multi-turn conversation agent
- User mentions or implies: tool-using agent

## Limitations

- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
