---
name: mastering-langgraph
description: Build stateful AI agents and agentic workflows with LangGraph in Python. Covers tool-using agents with LLM-tool loops, branching workflows, conversation memory, human-in-the-loop oversight, multi-agent systems, and production deployment. Use for building agents that use tools, creating multi-step workflows with conditional branches, adding persistence across turns, implementing human approval flows, and debugging via time-travel or LangSmith.
license: MIT
compatibility: opencode
metadata:
  version: 1.0.0
  framework: LangGraph
  python: ">=3.9"
---

# Mastering LangGraph Development Guide

Build stateful AI agents and workflows by defining graphs of nodes (steps) connected by edges (transitions).

## Contents

- [Quick Start](#quick-start)
- [Core Principles](#core-principles)
- [Development Workflow](#development-workflow)
- [Common Build Scenarios](#common-build-scenarios)
- [Common Pitfalls](#common-pitfalls)
- [Environment Setup](#environment-setup)
- [API Essentials](#api-essentials)
- [Reference Documents](#reference-documents)

---

## Quick Start

Minimal chatbot with memory:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

# 1. Define state
class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]  # Append mode

# 2. Define node
llm = ChatOpenAI(model="gpt-4")

def chat(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build graph
graph = StateGraph(State)
graph.add_node("chat", chat)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# 4. Compile with memory
chain = graph.compile(checkpointer=InMemorySaver())

# 5. Invoke with thread_id for persistence
result = chain.invoke(
    {"messages": [HumanMessage(content="Hello!")]},
    config={"configurable": {"thread_id": "user-123"}}
)
print(result["messages"][-1].content)
```

**Key patterns:**
- `Annotated[list, operator.add]` — append to list instead of replace
- `InMemorySaver()` — enables memory across invocations
- `thread_id` — identifies conversation for persistence

---

## Core Principles

### 1. Keep State Raw
Store facts, not formatted prompts. Each node can format data as needed.

```python
# ✓ Good: raw data
class State(TypedDict):
    user_question: str
    retrieved_docs: list[str]
    intent: str

# ✗ Bad: pre-formatted
class State(TypedDict):
    full_prompt: str  # Mixes data with formatting
```

### 2. Single-Purpose Nodes
Each node does one thing. Name it descriptively.

```python
# ✓ Good: clear responsibilities
graph.add_node("classify_intent", classify_intent)
graph.add_node("search_knowledge", search_knowledge)
graph.add_node("generate_response", generate_response)
```

### 3. Explicit Routing
Use conditional edges for decisions. Don't hide routing logic inside nodes.

```python
def route_by_intent(state) -> str:
    if state["intent"] == "billing":
        return "billing_handler"
    return "general_handler"

graph.add_conditional_edges(
    "classify", route_by_intent,
    ["billing_handler", "general_handler"]
)
```

### 4. Use Aggregators for Lists
Any list field that accumulates values needs `operator.add`:

```python
class State(TypedDict):
    messages: Annotated[list, operator.add]      # ✓ Appends
    current_step: str                             # Replaces (no annotation)
```

### 5. Handle Errors Deliberately

| Error Type | Strategy |
|------------|----------|
| Transient (network) | Use `RetryPolicy` on node |
| LLM-recoverable (parse fail) | Feed error to LLM via state, loop back |
| User-fixable (missing info) | Use `interrupt()` to pause and ask |
| Unexpected (bugs) | Let bubble up for debugging |

---

## Development Workflow

1. **Define Steps** — Break task into discrete operations (each becomes a node)
2. **Categorize Steps** — LLM call? Data retrieval? Action? User input?
3. **Design State** — TypedDict with all needed fields; keep it raw
4. **Implement Nodes** — `def node(state) -> dict` for each step
5. **Connect Graph** — `add_node()`, `add_edge()`, `add_conditional_edges()`
6. **Compile & Test** — `graph.compile()`, test with sample inputs

---

## Common Build Scenarios

| Scenario | Description | Reference |
|----------|-------------|-----------|
| **Simple Chatbot** | Q&A agent with conversational memory | Quick Start above |
| **Tool-Using Agent** | Agent that calls external tools (APIs, search) in a loop | `references/tool-agent-pattern.md` |
| **Structured Workflow** | Multi-step pipeline with conditional branches | `references/workflow-patterns.md` |
| **Long-Term Memory** | Persist across sessions, time-travel debugging | `references/persistence-memory.md` |
| **Human-in-the-Loop** | Pause for approval or correction mid-workflow | `references/hitl-patterns.md` |
| **Debugging/Monitoring** | Unit test nodes, visualize graphs, LangSmith tracing | `references/debugging-monitoring.md` |
| **Multi-Agent Systems** | Supervisor/swarm with handoff tools | `references/multi-agent-patterns.md` |
| **Production Deployment** | LangGraph Platform or custom infrastructure | `references/production-deployment.md` |

---

## Common Pitfalls

### 1. Forgetting `operator.add` on Lists
**Symptom:** Messages disappear, only last message retained.
```python
# ✗ Wrong: messages: list[AnyMessage]
# ✓ Fix: messages: Annotated[list[AnyMessage], operator.add]
```

### 2. Missing `thread_id` for Memory
**Symptom:** Agent forgets previous turns.
```python
# ✓ Fix: Always pass config with thread_id
chain.invoke(input, config={"configurable": {"thread_id": "unique-id"}})
```

### 3. Not Compiling Before Invoke
**Symptom:** AttributeError on graph object.
```python
# ✗ Wrong: graph.invoke(input)
# ✓ Fix: chain = graph.compile(); chain.invoke(input)
```

### 4. Non-Deterministic Nodes Without @task
**Symptom:** Different results on resume from checkpoint.
```python
from langgraph.func import task

@task  # Wrap for durable execution
def fetch_data(state):
    return {"data": requests.get(url).json()}
```

### 5. Circular Imports with Type Hints
```python
# ✓ Fix: Use string annotations
from __future__ import annotations
```

---

## Environment Setup

```bash
# Core
pip install -U langgraph

# LLM providers (pick one or more)
pip install langchain-openai
pip install langchain-anthropic

# Production persistence
pip install langgraph-checkpoint-postgres

# Observability
pip install langsmith
```

Environment variables:
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export LANGSMITH_API_KEY="ls-..."
export LANGSMITH_TRACING=true
```

---

## Quick Verification

### Before Building
- [ ] `python -c "import langgraph; print(langgraph.__version__)"` works
- [ ] LLM API key set (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`)
- [ ] Optional: `LANGSMITH_API_KEY` for tracing

### After Building
- [ ] Graph compiles without error: `chain = graph.compile()`
- [ ] Visualization renders: `print(chain.get_graph().draw_mermaid())`
- [ ] Invoke succeeds with sample input: `chain.invoke({...})`
- [ ] Lists accumulate correctly (verify `operator.add` annotations)
- [ ] Memory persists across invocations (test same `thread_id` twice)
- [ ] Conditional routing works as expected (test each branch)

---

## API Essentials

```python
# Imports
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict, Annotated
import operator

# State with append-mode list
class State(TypedDict):
    messages: Annotated[list, operator.add]

# Node signature
def node(state: State) -> dict:
    return {"messages": [new_message]}

# Graph construction
graph = StateGraph(State)
graph.add_node("name", node_fn)
graph.add_edge(START, "name")
graph.add_edge("name", END)

# Conditional routing
graph.add_conditional_edges(
    "from", router_fn,
    ["option1", "option2", END]
)

# Compile and run
chain = graph.compile(checkpointer=InMemorySaver())
result = chain.invoke(
    input,
    config={"configurable": {"thread_id": "id"}}
)

# Visualization
print(chain.get_graph().draw_mermaid())
```

---

## Reference Documents

Detailed reference guides are available in the `references/` directory:

| File | Covers |
|------|--------|
| `references/tool-agent-pattern.md` | Tool-using agent pattern, tool definition, error handling, advanced patterns |
| `references/workflow-patterns.md` | Multi-step pipelines, conditional branches, parallel execution, prompt chaining |
| `references/persistence-memory.md` | Long-term memory, time-travel debugging, crash recovery |
| `references/hitl-patterns.md` | Human approval, correction, interrupt patterns |
| `references/debugging-monitoring.md` | Unit testing, graph visualization, LangSmith tracing |
| `references/multi-agent-patterns.md` | Supervisor agents, swarm patterns, handoff tools |
| `references/production-deployment.md` | LangGraph Platform, self-hosted deployment, scaling |
| `references/core-api.md` | Core LangGraph API reference and deep dives |

---

## When to Use

- User mentions or implies: langgraph agent
- User mentions or implies: tool-using agent
- User mentions or implies: agent workflow with branching
- User mentions or implies: conversational memory
- User mentions or implies: human approval flow
- User mentions or implies: multi-agent system
- User mentions or implies: production agent deployment

## Related Skills

Works well with: `langgraph` (core patterns), `langfuse` (observability), `structured-output` (structured responses), `agent-evaluation` (testing)

## Limitations

- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
