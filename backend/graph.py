"""
LangGraph workflow implementation for the multi-agent system.
Sets up nodes, edges, and routing logic for agent orchestration.
"""

from typing import Dict, List, Any, Optional, Union
# Note: LangGraph imports removed due to compatibility issues
# Using simplified workflow instead
from pydantic import BaseModel
import json

from .agents import get_agent, get_all_agents
from .memory import get_memory_manager


class AgentState(BaseModel):
    """
    State model for the agent workflow.
    Contains all the information that flows between agents.
    """
    
    # Core task information
    task: str
    current_agent: str = "planner"
    status: str = "idle"
    
    # Agent outputs
    planner_output: str = ""
    research_output: str = ""
    writer_output: str = ""
    
    # Workflow control
    next_agent: str = "planner"
    iteration_count: int = 0
    max_iterations: int = 10
    
    # Results
    final_output: str = ""
    completed: bool = False
    
    # Additional context
    context: Dict[str, Any] = {}


# WorkflowGraph class removed due to LangGraph compatibility issues
# Using SimpleWorkflow instead


class SimpleWorkflow:
    """
    Simplified workflow for cases where LangGraph might have issues.
    Sequential execution of agents with manual orchestration.
    """
    
    def __init__(self):
        self.memory_manager = get_memory_manager()
        self.agents = get_all_agents()
    
    def run_workflow(self, task: str) -> Dict[str, Any]:
        """
        Run a simplified sequential workflow.
        
        Args:
            task (str): The task to execute
            
        Returns:
            Dict[str, Any]: Final workflow results
        """
        print(f"Starting simplified workflow for task: {task}")
        print("=" * 60)
        
        # Add task to memory manager
        self.memory_manager.set_task(task)
        self.memory_manager.add_user_message(task)
        
        results = {
            "success": True,
            "planner_output": "",
            "research_output": "",
            "writer_output": "",
            "final_output": "",
            "iteration_count": 3
        }
        
        try:
            # Step 1: Planning
            print("Step 1: Planning...")
            planner = self.agents["planner"]
            planner_result = planner.execute(task)
            results["planner_output"] = planner_result
            print(f"   Planning completed: {len(planner_result)} characters")
            print()
            
            # Step 2: Research
            print("Step 2: Research...")
            researcher = self.agents["research"]
            research_result = researcher.execute(task)
            results["research_output"] = research_result
            print(f"   Research completed: {len(research_result)} characters")
            print()
            
            # Step 3: Writing
            print("Step 3: Writing...")
            writer = self.agents["writer"]
            writer_result = writer.execute(task)
            results["writer_output"] = writer_result
            results["final_output"] = writer_result
            print(f"   Writing completed: {len(writer_result)} characters")
            print()
            
            print("=" * 60)
            print("SUCCESS: Simplified workflow completed successfully!")
            
            return results
            
        except Exception as e:
            print(f"ERROR: Workflow failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "final_output": "Sorry, there was an error processing your request."
            }


# Global workflow instances
# workflow_graph = WorkflowGraph()  # Removed due to LangGraph compatibility issues
simple_workflow = SimpleWorkflow()


def run_multi_agent_workflow(task: str, use_simple: bool = True) -> Dict[str, Any]:
    """
    Run the multi-agent workflow.
    
    Args:
        task (str): The task to execute
        use_simple (bool): Whether to use the simplified workflow
        
    Returns:
        Dict[str, Any]: Workflow results
    """
    # Always use simplified workflow for now
    return simple_workflow.run_workflow(task)


def get_workflow_status() -> Dict[str, Any]:
    """
    Get the current workflow status.
    
    Returns:
        Dict[str, Any]: Current status information
    """
    memory_manager = get_memory_manager()
    
    return {
        "current_task": memory_manager.shared_state.current_task,
        "task_status": memory_manager.shared_state.task_status,
        "agent_outputs": memory_manager.get_all_outputs(),
        "conversation_history": memory_manager.get_conversation_history(),
        "memory_summary": memory_manager.get_memory_summary()
    }


def reset_workflow():
    """
    Reset the workflow state.
    """
    memory_manager = get_memory_manager()
    memory_manager.clear_all_memory()
    print("INFO: Workflow reset completed.")
