# Workflow Engine - LangGraph-Inspired Backend System

A minimal, clean, and well-structured Python backend for defining and executing workflow graphs. Similar to LangGraph but designed for simplicity and learning.

## Features

✓ **Node-based Workflow Engine**: Define steps as nodes with tools  
✓ **Shared State Management**: State flows from node to node  
✓ **Conditional Branching**: Route execution based on state values  
✓ **Looping Support**: Run nodes repeatedly until conditions are met  
✓ **Tool Registry**: Pre-register Python functions for nodes to call  
✓ **FastAPI Integration**: Easy HTTP API for remote execution  
✓ **Execution Logging**: Track each node execution with timing  
✓ **Code Review Example**: Built-in mini-agent workflow  

## Project Structure

```
workflow-engine/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── core/
│   │   ├── __init__.py
│   │   ├── engine.py          # Core workflow engine (Node, Graph, Runner)
│   │   └── tools.py           # Tool registry system
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # FastAPI endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py         # Pydantic models
│   │   └── state.py           # WorkflowState class
│   └── workflows/
│       ├── __init__.py
│       └── code_review.py     # Example: Code Review workflow
├── demo.py                     # Standalone demo script (no FastAPI needed)
├── requirements.txt            # Python dependencies
└── README.md
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone or download the project
cd workflow-engine

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Option 1: Run Demo (No Server Required)

```bash
python demo.py
```

This runs 4 demonstrations:
1. **Basic Workflow**: Simple sequential execution
2. **Conditional Branching**: Routes based on state values
3. **Looping**: Repeats nodes until conditions are met
4. **Code Review Mini-Agent**: Full example workflow

### Option 2: Run FastAPI Server

```bash
# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server starts at `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
GET /health
```

#### Get API Info
```bash
GET /
```

#### Create a Graph
```bash
POST /graph/create

Request:
{
  "name": "My Workflow",
  "description": "A sample workflow",
  "nodes": [
    {
      "name": "step1",
      "node_type": "standard",
      "tool_name": "my_tool",
      "metadata": {}
    }
  ],
  "edges": [
    {
      "from_node": "step1",
      "to_node": "step2",
      "condition": null
    }
  ],
  "entry_point": "step1",
  "exit_point": "step2"
}

Response:
{
  "graph_id": "uuid-here",
  "name": "My Workflow",
  "message": "Graph created successfully"
}
```

#### Run a Graph
```bash
POST /graph/run

Request:
{
  "graph_id": "uuid-here",
  "initial_state": {
    "code": "def hello(): pass"
  }
}

Response:
{
  "run_id": "uuid-here",
  "graph_id": "uuid-here",
  "status": "completed",
  "final_state": {...},
  "execution_logs": [...],
  "total_duration_ms": 123.45
}
```

#### Get Run State
```bash
GET /graph/state/{run_id}
```

#### View Code Review Workflow Schema
```bash
GET /graph/demo/code-review
```

## Core Concepts

### 1. WorkflowState

Shared state dictionary that flows through the workflow:

```python
from app.models import WorkflowState

state = WorkflowState({"key": "value"})
state.set("new_key", "new_value")
state.get("key")  # "value"
state.to_dict()   # {"key": "value", "new_key": "new_value"}
```

### 2. Node

A single step in the workflow that executes a tool:

```python
from app.core import Node

node = Node(
    name="process",
    node_type="standard",
    tool_name="my_tool",
    metadata={"description": "Process data"}
)
```

### 3. Graph

Defines nodes and edges with conditional routing:

```python
from app.core import Graph
from app.models import GraphSchema, NodeSchema, EdgeSchema

schema = GraphSchema(
    name="My Workflow",
    nodes=[...],
    edges=[...],
    entry_point="start",
    exit_point="end"
)
graph = Graph(schema)
```

### 4. WorkflowRunner

Executes a graph with initial state:

```python
from app.core import WorkflowRunner

runner = WorkflowRunner(graph)
result = runner.run({"initial": "state"})

# Access results
result["final_state"]      # Final state dictionary
result["execution_logs"]   # List of ExecutionLog objects
```

### 5. Tool Registry

Register Python functions that nodes can call:

```python
from app.core.tools import get_registry

registry = get_registry()

def my_tool(state):
    # state is a WorkflowState object
    state.set("processed", True)
    return state

registry.register("my_tool", my_tool)
```

## Example: Code Review Workflow

The built-in Code Review workflow demonstrates:
- Multiple sequential nodes
- Conditional branching (quality_score >= 80)
- Looping (until quality threshold is met)
- State flow between nodes

### Workflow Steps:
1. **extract_functions**: Parse Python code and extract function names
2. **check_complexity**: Analyze code complexity metrics
3. **detect_issues**: Find common issues (TODOs, unsafe functions, etc.)
4. **suggest_improvements**: Generate suggestions and quality score
5. **Loop or Exit**: Based on quality_score >= 80

### Run Code Review Example:

```python
from app.workflows.code_review import setup_code_review_tools, create_code_review_workflow
from app.core import Graph, WorkflowRunner

setup_code_review_tools()
schema = create_code_review_workflow()
graph = Graph(schema)

runner = WorkflowRunner(graph)
result = runner.run({
    "code": "def hello(): pass"
})

print(result["final_state"])  # See quality_score, issues, etc.
```

## Features Explained

### Conditional Branching

Routes execution based on state values:

```python
EdgeSchema(
    from_node="check",
    to_node="high_quality",
    condition="quality_score >= 80"
)
```

Supported operators: `>`, `<`, `>=`, `<=`, `==`, `!=`

### Looping

Nodes can route back to themselves or earlier nodes:

```python
EdgeSchema(from_node="process", to_node="check"),
EdgeSchema(from_node="check", to_node="process", condition="counter < 5"),
EdgeSchema(from_node="check", to_node="end", condition="counter >= 5"),
```

### Custom Handlers

Nodes can use custom Python functions instead of registered tools:

```python
def custom_handler(state):
    state.set("key", "value")
    return state

node = graph.nodes["my_node"]
node.set_handler(custom_handler)
```

## How to Extend

### Add a New Tool

```python
from app.core.tools import get_registry

def my_custom_tool(state):
    # Read from state
    data = state.get("input_data")
    
    # Process
    result = process(data)
    
    # Update state
    state.set("output", result)
    return state

registry = get_registry()
registry.register("my_custom_tool", my_custom_tool)
```

### Create a New Workflow

```python
from app.models import GraphSchema, NodeSchema, EdgeSchema

nodes = [
    NodeSchema(name="step1", node_type="standard", tool_name="tool1"),
    NodeSchema(name="step2", node_type="standard", tool_name="tool2"),
]

edges = [
    EdgeSchema(from_node="step1", to_node="step2"),
]

schema = GraphSchema(
    name="My Workflow",
    nodes=nodes,
    edges=edges,
    entry_point="step1",
    exit_point="step2"
)

graph = Graph(schema)
runner = WorkflowRunner(graph)
result = runner.run({"initial": "data"})
```

## Architecture Decisions

### Why This Structure?

1. **Separation of Concerns**: Core engine, tools, and API are independent
2. **Testability**: Each component can be tested in isolation
3. **Extensibility**: Easy to add new node types, tools, and workflows
4. **Clarity**: Code is readable and follows Python best practices
5. **Minimal Dependencies**: Only FastAPI (and Pydantic) for validation

### State as Dictionary

- Simple and Pythonic
- Easy to serialize to JSON
- Flexible for any data type
- Natural state progression

### Tool Registry Pattern

- Runtime registration of tools
- Decouples nodes from tool implementation
- Allows dynamic tool loading
- Easy to test in isolation

## What Could Be Improved (With More Time)

1. **Database Persistence**: Store graphs and runs in PostgreSQL instead of memory
2. **WebSocket Support**: Stream execution logs in real-time
3. **Async Execution**: Support long-running tasks with `asyncio`
4. **Graph Visualization**: Generate visual graphs of workflows
5. **Error Handling**: More granular error recovery and retry logic
6. **Validation**: More robust schema validation and error messages
7. **Performance**: Caching, batch execution, parallel node execution
8. **Security**: Authentication, authorization, rate limiting
9. **Monitoring**: Logging, metrics, tracing with OpenTelemetry
10. **Type Hints**: Full type annotations for better IDE support

## Testing

Run the demo to see all features in action:

```bash
python demo.py
```

Expected output:
- 4 successful workflow demonstrations
- Each demo shows different features
- Final summary confirms all tests passed

## API Documentation

Once the server is running, visit:
```
http://localhost:8000/docs
```

This opens the interactive Swagger UI with all endpoints documented.

## Code Review Mini-Agent Example

The workflow engine includes a complete Code Review agent that:

1. Extracts function definitions from Python code
2. Analyzes complexity metrics
3. Detects code issues (TODOs, unsafe functions, etc.)
4. Suggests improvements
5. Loops until quality score >= 80

This is a practical example of:
- Sequential execution
- Branching logic
- Looping until condition
- State modification and flow
- Tool integration

## Author Notes

This implementation prioritizes:
- **Clarity** over features
- **Correctness** over complexity
- **Extensibility** over flexibility
- **Testability** over performance

The goal is to demonstrate solid backend engineering principles while keeping the code simple and understandable.

## License

MIT License - Feel free to use and modify

---

Built with ❤️ for the Tredence AI Engineering Internship
