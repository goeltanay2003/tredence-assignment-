"""
API Test Guide - How to Test All Endpoints

This script demonstrates how to test all the workflow engine APIs.
Run the FastAPI server first, then use these examples.
"""

# ============================================================================
# Step 1: Start the FastAPI Server
# ============================================================================

# In a terminal, run:
# cd workflow-engine
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# The server will start at: http://localhost:8000

# ============================================================================
# Step 2: Test Health Check
# ============================================================================

# Using curl:
# curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","service":"Workflow Engine"}


# ============================================================================
# Step 3: Get API Info
# ============================================================================

# Using curl:
# curl http://localhost:8000/

# Expected response shows all available endpoints


# ============================================================================
# Step 4: View Code Review Workflow Schema
# ============================================================================

# Using curl:
# curl http://localhost:8000/graph/demo/code-review

# This shows the structure of the Code Review workflow


# ============================================================================
# Step 5: Create a Graph
# ============================================================================

# Using Python requests library:
"""
import requests
import json

url = "http://localhost:8000/graph/create"

payload = {
    "name": "My Test Workflow",
    "description": "A test workflow",
    "nodes": [
        {
            "name": "step1",
            "node_type": "standard",
            "tool_name": None,
            "metadata": {}
        },
        {
            "name": "step2",
            "node_type": "standard",
            "tool_name": None,
            "metadata": {}
        }
    ],
    "edges": [
        {
            "from_node": "step1",
            "to_node": "step2",
            "condition": None
        }
    ],
    "entry_point": "step1",
    "exit_point": "step2"
}

response = requests.post(url, json=payload)
graph_data = response.json()
print(f"Graph ID: {graph_data['graph_id']}")
"""

# Or using curl with a JSON file:
# curl -X POST http://localhost:8000/graph/create \
#   -H "Content-Type: application/json" \
#   -d @graph_request.json


# ============================================================================
# Step 6: Run a Graph
# ============================================================================

# Using Python:
"""
import requests

url = "http://localhost:8000/graph/run"

# Use the graph_id from Step 5
payload = {
    "graph_id": "your-graph-id-here",
    "initial_state": {
        "data": "test"
    }
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Run ID: {result['run_id']}")
print(f"Status: {result['status']}")
print(f"Final State: {result['final_state']}")
print(f"Execution Logs: {result['execution_logs']}")
"""


# ============================================================================
# Step 7: Get Run State
# ============================================================================

# Using curl:
# curl http://localhost:8000/graph/state/{run_id}

# Where {run_id} is the run_id from Step 6


# ============================================================================
# Complete Python Example
# ============================================================================

"""
import requests
import json

# Workflow 1: Create a simple graph
graph_payload = {
    "name": "Simple Workflow",
    "description": "A simple test workflow",
    "nodes": [
        {
            "name": "start",
            "node_type": "standard",
            "tool_name": None,
            "metadata": {"description": "Start node"}
        },
        {
            "name": "end",
            "node_type": "standard",
            "tool_name": None,
            "metadata": {"description": "End node"}
        }
    ],
    "edges": [
        {
            "from_node": "start",
            "to_node": "end",
            "condition": None
        }
    ],
    "entry_point": "start",
    "exit_point": "end"
}

# Create the graph
print("Creating graph...")
response = requests.post("http://localhost:8000/graph/create", json=graph_payload)
graph_result = response.json()
graph_id = graph_result['graph_id']
print(f"✓ Graph created: {graph_id}")

# Run the graph
print("\nRunning graph...")
run_payload = {
    "graph_id": graph_id,
    "initial_state": {
        "test": "data"
    }
}

response = requests.post("http://localhost:8000/graph/run", json=run_payload)
run_result = response.json()
run_id = run_result['run_id']
print(f"✓ Run completed: {run_id}")
print(f"  Status: {run_result['status']}")
print(f"  Final State: {run_result['final_state']}")

# Get run state
print(f"\nFetching run state...")
response = requests.get(f"http://localhost:8000/graph/state/{run_id}")
state_result = response.json()
print(f"✓ Run state retrieved")
print(f"  Graph ID: {state_result['graph_id']}")
print(f"  Status: {state_result['status']}")
print(f"  Steps: {state_result['execution_steps']}")
"""


# ============================================================================
# Interactive Testing Using Swagger UI
# ============================================================================

# The easiest way to test all endpoints!
# 1. Start the server: uvicorn app.main:app --reload
# 2. Open browser: http://localhost:8000/docs
# 3. Try all endpoints in the interactive Swagger UI
# 4. Test with sample JSON payloads


# ============================================================================
# Complete curl Examples
# ============================================================================

"""
# Health check
curl http://localhost:8000/health

# Get API info
curl http://localhost:8000/

# View Code Review workflow
curl http://localhost:8000/graph/demo/code-review

# Create a graph (save as graph_create.json first)
curl -X POST http://localhost:8000/graph/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Workflow",
    "description": "Testing",
    "nodes": [
      {
        "name": "step1",
        "node_type": "standard",
        "tool_name": null,
        "metadata": {}
      }
    ],
    "edges": [],
    "entry_point": "step1",
    "exit_point": "step1"
  }'

# Run a graph
curl -X POST http://localhost:8000/graph/run \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "YOUR_GRAPH_ID",
    "initial_state": {"key": "value"}
  }'

# Get run state
curl http://localhost:8000/graph/state/YOUR_RUN_ID
"""
