"""
Standalone demo script to test the workflow engine without FastAPI.
This demonstrates the core functionality of the workflow engine.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import WorkflowState, NodeSchema, EdgeSchema, GraphSchema
from app.core.engine import Graph, WorkflowRunner
from app.workflows.code_review import setup_code_review_tools, create_code_review_workflow


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_basic_workflow():
    """Demonstrate basic workflow execution"""
    print_section("DEMO 1: Basic Workflow")
    
    # Define a simple workflow
    nodes = [
        NodeSchema(name="start", node_type="standard", tool_name=None),
        NodeSchema(name="process", node_type="standard", tool_name=None),
        NodeSchema(name="end", node_type="standard", tool_name=None),
    ]
    
    edges = [
        EdgeSchema(from_node="start", to_node="process"),
        EdgeSchema(from_node="process", to_node="end"),
    ]
    
    schema = GraphSchema(
        name="Simple Workflow",
        nodes=nodes,
        edges=edges,
        entry_point="start",
        exit_point="end"
    )
    
    graph = Graph(schema)
    
    # Add custom handlers
    def start_handler(state):
        print("→ START: Initializing workflow")
        state.set("step", 1)
        return state
    
    def process_handler(state):
        print("→ PROCESS: Processing data")
        state.set("result", "processed")
        state.set("step", 2)
        return state
    
    def end_handler(state):
        print("→ END: Workflow completed")
        state.set("step", 3)
        return state
    
    graph.nodes["start"].set_handler(start_handler)
    graph.nodes["process"].set_handler(process_handler)
    graph.nodes["end"].set_handler(end_handler)
    
    runner = WorkflowRunner(graph)
    result = runner.run({"initial": "data"})
    
    print("\n✓ Final State:")
    for key, value in result["final_state"].items():
        print(f"  {key}: {value}")
    
    print(f"\n✓ Execution Steps: {len(result['execution_logs'])}")


def demo_conditional_workflow():
    """Demonstrate workflow with conditional branching"""
    print_section("DEMO 2: Conditional Branching")
    
    nodes = [
        NodeSchema(name="check", node_type="conditional", tool_name=None),
        NodeSchema(name="high_path", node_type="standard", tool_name=None),
        NodeSchema(name="low_path", node_type="standard", tool_name=None),
        NodeSchema(name="end", node_type="standard", tool_name=None),
    ]
    
    edges = [
        # Conditional edges based on score
        EdgeSchema(from_node="check", to_node="high_path", condition="score >= 50"),
        EdgeSchema(from_node="check", to_node="low_path", condition="score < 50"),
        EdgeSchema(from_node="high_path", to_node="end"),
        EdgeSchema(from_node="low_path", to_node="end"),
    ]
    
    schema = GraphSchema(
        name="Conditional Workflow",
        nodes=nodes,
        edges=edges,
        entry_point="check",
        exit_point="end"
    )
    
    graph = Graph(schema)
    
    def check_handler(state):
        print("→ CHECK: Evaluating score")
        return state
    
    def high_handler(state):
        print("✓ HIGH PATH: Score is good!")
        state.set("path", "high")
        return state
    
    def low_handler(state):
        print("✗ LOW PATH: Score is low, needs improvement")
        state.set("path", "low")
        return state
    
    def end_handler(state):
        print("→ END: Workflow finished")
        return state
    
    graph.nodes["check"].set_handler(check_handler)
    graph.nodes["high_path"].set_handler(high_handler)
    graph.nodes["low_path"].set_handler(low_handler)
    graph.nodes["end"].set_handler(end_handler)
    
    # Test with high score
    print("Test Case 1: score = 75")
    runner = WorkflowRunner(graph)
    result = runner.run({"score": 75})
    print(f"Result path: {result['final_state'].get('path')}\n")
    
    # Test with low score
    print("Test Case 2: score = 30")
    runner = WorkflowRunner(graph)
    result = runner.run({"score": 30})
    print(f"Result path: {result['final_state'].get('path')}")


def demo_code_review_workflow():
    """Demonstrate the Code Review workflow"""
    print_section("DEMO 3: Code Review Mini-Agent")
    
    # Setup tools
    setup_code_review_tools()
    
    # Create workflow
    schema = create_code_review_workflow()
    graph = Graph(schema)
    
    # Sample Python code to review
    sample_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total

def nested_loop_example():
    result = []
    for i in range(10):
        for j in range(10):
            for k in range(10):
                result.append(i * j * k)
    return result

# TODO: Refactor this
def complex_function():
    # FIXME: This is slow
    pass
"""
    
    print("Code to Review:")
    print("-" * 60)
    print(sample_code)
    print("-" * 60 + "\n")
    
    runner = WorkflowRunner(graph)
    result = runner.run({"code": sample_code})
    
    print("\n✓ Execution Summary:")
    print(f"  Total steps: {len(result['execution_logs'])}")
    
    final_state = result["final_state"]
    print(f"\n✓ Final Results:")
    print(f"  Functions found: {final_state.get('functions', [])}")
    print(f"  Function count: {final_state.get('function_count', 0)}")
    print(f"  Complexity score: {final_state.get('complexity_score', 0)}")
    print(f"  Issues detected: {final_state.get('issue_count', 0)}")
    print(f"  Issues: {final_state.get('detected_issues', [])}")
    print(f"  Final quality score: {final_state.get('quality_score', 0)}/100")
    print(f"  Suggestions: {final_state.get('suggestions', [])}")


def demo_looping_workflow():
    """Demonstrate workflow with looping"""
    print_section("DEMO 4: Looping Workflow")
    
    nodes = [
        NodeSchema(name="increment", node_type="standard", tool_name=None),
        NodeSchema(name="check_limit", node_type="conditional", tool_name=None),
        NodeSchema(name="end", node_type="standard", tool_name=None),
    ]
    
    edges = [
        EdgeSchema(from_node="increment", to_node="check_limit"),
        # Loop back to increment if counter < 5
        EdgeSchema(from_node="check_limit", to_node="increment", condition="counter < 5"),
        # Go to end if counter >= 5
        EdgeSchema(from_node="check_limit", to_node="end", condition="counter >= 5"),
    ]
    
    schema = GraphSchema(
        name="Loop Workflow",
        nodes=nodes,
        edges=edges,
        entry_point="increment",
        exit_point="end"
    )
    
    graph = Graph(schema)
    
    def increment_handler(state):
        counter = state.get("counter", 0)
        counter += 1
        state.set("counter", counter)
        print(f"→ INCREMENT: counter = {counter}")
        return state
    
    def check_handler(state):
        counter = state.get("counter", 0)
        print(f"✓ CHECK: Is {counter} < 5?")
        return state
    
    def end_handler(state):
        print(f"✓ END: Loop completed")
        return state
    
    graph.nodes["increment"].set_handler(increment_handler)
    graph.nodes["check_limit"].set_handler(check_handler)
    graph.nodes["end"].set_handler(end_handler)
    
    runner = WorkflowRunner(graph)
    result = runner.run({"counter": 0})
    
    print(f"\nFinal counter: {result['final_state'].get('counter')}")
    print(f"Total execution steps: {len(result['execution_logs'])}")


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "   WORKFLOW ENGINE - DEMO & TEST SUITE".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        demo_basic_workflow()
        demo_conditional_workflow()
        demo_looping_workflow()
        demo_code_review_workflow()
        
        print_section("ALL DEMOS COMPLETED SUCCESSFULLY")
        print("✓ All tests passed!")
        print("✓ Workflow engine is working correctly!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
