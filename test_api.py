"""
Live Demonstration of Workflow Engine API Usage
Shows how the API works with real examples
"""

import sys
sys.path.insert(0, '.')

from app.models import GraphSchema, NodeSchema, EdgeSchema
from app.core import Graph, WorkflowRunner

print("\n" + "="*70)
print("  WORKFLOW ENGINE - LIVE API DEMONSTRATION")
print("="*70 + "\n")

# ============================================================================
# EXAMPLE 1: Simple Data Processing Pipeline
# ============================================================================

print("EXAMPLE 1: Data Processing Pipeline")
print("-" * 70)

nodes = [
    NodeSchema(name="extract", node_type="standard", tool_name=None),
    NodeSchema(name="analyze", node_type="standard", tool_name=None),
    NodeSchema(name="report", node_type="standard", tool_name=None),
]

edges = [
    EdgeSchema(from_node="extract", to_node="analyze"),
    EdgeSchema(from_node="analyze", to_node="report"),
]

schema = GraphSchema(
    name="Data Processing Pipeline",
    description="Extract, Analyze, and Report data",
    nodes=nodes,
    edges=edges,
    entry_point="extract",
    exit_point="report"
)

graph = Graph(schema)

# Set handlers
def extract_handler(state):
    print("  → EXTRACT: Reading data...")
    state.set("raw_data", "Sample data from database")
    return state

def analyze_handler(state):
    print("  → ANALYZE: Processing data...")
    raw = state.get("raw_data")
    state.set("analysis", f"Processed: {raw}")
    return state

def report_handler(state):
    print("  → REPORT: Generating report...")
    analysis = state.get("analysis")
    state.set("report", f"Final Report - {analysis}")
    return state

graph.nodes["extract"].set_handler(extract_handler)
graph.nodes["analyze"].set_handler(analyze_handler)
graph.nodes["report"].set_handler(report_handler)

# Run workflow
print("\nExecuting workflow:\n")
runner = WorkflowRunner(graph)
result = runner.run({"source": "API"})

print("\n✓ Workflow Completed!\n")
print("Final State:")
for key, value in result["final_state"].items():
    print(f"  {key}: {value}")

print(f"\nExecution Trace:")
for log in result["execution_logs"]:
    print(f"  {log.node_name} → {log.status} ({log.duration_ms:.2f}ms)")

# ============================================================================
# EXAMPLE 2: Conditional Branching
# ============================================================================

print("\n\n" + "="*70)
print("EXAMPLE 2: Workflow with Conditional Branching")
print("-" * 70)

nodes = [
    NodeSchema(name="check_quality", node_type="conditional", tool_name=None),
    NodeSchema(name="approve", node_type="standard", tool_name=None),
    NodeSchema(name="reject", node_type="standard", tool_name=None),
    NodeSchema(name="done", node_type="standard", tool_name=None),
]

edges = [
    EdgeSchema(from_node="check_quality", to_node="approve", condition="quality_score >= 80"),
    EdgeSchema(from_node="check_quality", to_node="reject", condition="quality_score < 80"),
    EdgeSchema(from_node="approve", to_node="done"),
    EdgeSchema(from_node="reject", to_node="done"),
]

schema = GraphSchema(
    name="Quality Control Pipeline",
    description="Check quality and route accordingly",
    nodes=nodes,
    edges=edges,
    entry_point="check_quality",
    exit_point="done"
)

graph = Graph(schema)

def check_handler(state):
    print("  → CHECKING: Evaluating quality...")
    return state

def approve_handler(state):
    print("  ✓ APPROVED: Quality is acceptable!")
    state.set("status", "approved")
    return state

def reject_handler(state):
    print("  ✗ REJECTED: Quality needs improvement!")
    state.set("status", "rejected")
    return state

def done_handler(state):
    print("  → DONE: Process complete")
    return state

graph.nodes["check_quality"].set_handler(check_handler)
graph.nodes["approve"].set_handler(approve_handler)
graph.nodes["reject"].set_handler(reject_handler)
graph.nodes["done"].set_handler(done_handler)

# Test with high quality
print("\nTest Case 1: quality_score = 85\n")
runner = WorkflowRunner(graph)
result = runner.run({"quality_score": 85})
print(f"Result: {result['final_state'].get('status')}")

# Test with low quality
print("\nTest Case 2: quality_score = 65\n")
runner = WorkflowRunner(graph)
result = runner.run({"quality_score": 65})
print(f"Result: {result['final_state'].get('status')}")

# ============================================================================
# EXAMPLE 3: Looping Workflow
# ============================================================================

print("\n\n" + "="*70)
print("EXAMPLE 3: Workflow with Looping (Retry Until Success)")
print("-" * 70)

nodes = [
    NodeSchema(name="attempt", node_type="standard", tool_name=None),
    NodeSchema(name="check", node_type="conditional", tool_name=None),
    NodeSchema(name="success", node_type="standard", tool_name=None),
]

edges = [
    EdgeSchema(from_node="attempt", to_node="check"),
    EdgeSchema(from_node="check", to_node="attempt", condition="attempts < 3"),
    EdgeSchema(from_node="check", to_node="success", condition="attempts >= 3"),
]

schema = GraphSchema(
    name="Retry Logic",
    description="Retry operation until success",
    nodes=nodes,
    edges=edges,
    entry_point="attempt",
    exit_point="success"
)

graph = Graph(schema)

def attempt_handler(state):
    attempts = state.get("attempts", 0)
    attempts += 1
    state.set("attempts", attempts)
    print(f"  → ATTEMPT #{attempts}: Trying operation...")
    return state

def check_handler(state):
    attempts = state.get("attempts", 0)
    print(f"  → CHECK: Evaluated {attempts} attempts")
    return state

def success_handler(state):
    print(f"  ✓ SUCCESS: Operation completed after {state.get('attempts')} attempts!")
    return state

graph.nodes["attempt"].set_handler(attempt_handler)
graph.nodes["check"].set_handler(check_handler)
graph.nodes["success"].set_handler(success_handler)

print("\nExecuting retry workflow:\n")
runner = WorkflowRunner(graph)
result = runner.run({"attempts": 0})

print(f"\nFinal Result:")
print(f"  Total Attempts: {result['final_state'].get('attempts')}")
print(f"  Total Steps Executed: {len(result['execution_logs'])}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n\n" + "="*70)
print("  SUMMARY")
print("="*70)

print("""
✓ Demonstrated 3 core workflow patterns:
  1. Sequential Pipeline: data flows through nodes in sequence
  2. Conditional Branching: routes based on state values
  3. Looping: repeats nodes until conditions are met

✓ API Features Shown:
  • Graph creation with nodes and edges
  • Custom handler functions per node
  • State management across nodes
  • Execution logging with timing
  • Conditional routing based on state
  • Loop detection and execution

✓ Real-World Applications:
  • Data processing pipelines
  • Quality control workflows
  • Approval workflows
  • Retry logic
  • Agent-based systems

The workflow engine provides a flexible, production-ready system for
building complex workflows with clear state management and logging.
""")

print("="*70)
print("✓ All demonstrations completed successfully!")
print("="*70 + "\n")
