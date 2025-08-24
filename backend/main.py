"""
Main backend API for the multi-agent workout system.
Provides a clean interface for the Streamlit frontend.
"""

import os
import time
from typing import Dict, List, Any, Optional
import traceback
from datetime import datetime

from .graph import run_multi_agent_workflow, get_workflow_status, reset_workflow
from .memory import get_memory_manager
from .agents import get_all_agents
from .tools import get_tools
from .evaluation import get_system_evaluator


class WorkoutAgentSystem:
    """
    Main system class that orchestrates the multi-agent workflow.
    Provides a clean API for the frontend.
    """
    
    def __init__(self):
        self.memory_manager = get_memory_manager()
        self.agents = get_all_agents()
        self.tools = get_tools()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def process_query(self, query: str, enable_evaluation: bool = True) -> Dict[str, Any]:
        """
        Process a user query through the multi-agent workflow.
        
        Args:
            query (str): User's query or request
            enable_evaluation (bool): Whether to run evaluation metrics
            
        Returns:
            Dict[str, Any]: Complete workflow results and agent outputs
        """
        start_time = time.time()
        
        try:
            print(f"\n{'='*60}")
            print(f"Processing query: {query}")
            print(f"Session ID: {self.session_id}")
            print(f"{'='*60}")
            
            # Run the workflow
            workflow_result = run_multi_agent_workflow(query, use_simple=True)
            
            end_time = time.time()
            total_response_time = end_time - start_time
            
            # Get all agent outputs from memory
            all_outputs = self.memory_manager.get_all_outputs()
            
            # Prepare response
            response = {
                "success": workflow_result.get("success", True),
                "query": query,
                "session_id": self.session_id,
                "final_answer": workflow_result.get("final_output", ""),
                "agent_steps": self._format_agent_steps(all_outputs),
                "workflow_result": workflow_result,
                "timestamp": datetime.now().isoformat(),
                "response_time": total_response_time,
                "error": workflow_result.get("error", None)
            }
            
            # Add evaluation metrics if enabled
            if enable_evaluation and workflow_result.get("success", True):
                try:
                    system_evaluator = get_system_evaluator()
                    
                    # Simulate agent response times (proportional to total time)
                    agent_times = {
                        'planner': total_response_time * 0.2,
                        'research': total_response_time * 0.5,
                        'writer': total_response_time * 0.3
                    }
                    
                    evaluation_result = system_evaluator.evaluate_system_response(
                        query=query,
                        final_response=workflow_result.get("final_output", ""),
                        agent_outputs=all_outputs,
                        agent_response_times=agent_times,
                        total_response_time=total_response_time,
                        memory_manager=self.memory_manager
                    )
                    
                    response['evaluation_metrics'] = {
                        'final_score': evaluation_result.final_score,
                        'quality_score': evaluation_result.overall_quality_score,
                        'efficiency_score': evaluation_result.system_efficiency_score,
                        'response_length': evaluation_result.response_length,
                        'readability_score': evaluation_result.readability_score,
                        'completeness_score': evaluation_result.completeness_score,
                        'relevance_score': evaluation_result.relevance_score,
                        'actionability_score': evaluation_result.actionability_score,
                        'coordination_score': evaluation_result.agent_coordination_score,
                        'tool_usage_score': evaluation_result.tool_usage_effectiveness
                    }
                    
                    print(f"Evaluation Score: {evaluation_result.final_score:.3f}")
                    
                except Exception as eval_error:
                    print(f"Evaluation error: {str(eval_error)}")
                    response['evaluation_metrics'] = {'error': str(eval_error)}
            
            print(f"\nSUCCESS: Query processed successfully!")
            print(f"Final answer length: {len(response['final_answer'])} characters")
            print(f"Agent steps: {len(response['agent_steps'])}")
            
            return response
            
        except Exception as e:
            print(f"\nERROR: Error processing query: {str(e)}")
            traceback.print_exc()
            
            return {
                "success": False,
                "query": query,
                "session_id": self.session_id,
                "final_answer": f"Sorry, I encountered an error while processing your request: {str(e)}",
                "agent_steps": [],
                "workflow_result": {"error": str(e)},
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _format_agent_steps(self, all_outputs: Dict[str, List[Dict]]) -> List[Dict]:
        """
        Format agent outputs for display.
        
        Args:
            all_outputs (Dict): All agent outputs from memory
            
        Returns:
            List[Dict]: Formatted agent steps
        """
        steps = []
        
        # Define agent order and descriptions
        agent_info = {
            "planner": {"name": "Planner Agent", "description": "Analyzing task and creating plan"},
            "research": {"name": "Research Agent", "description": "Gathering information and conducting research"},  
            "writer": {"name": "Writer Agent", "description": "Creating comprehensive response"}
        }
        
        # Process outputs in order
        for agent_key in ["planner", "research", "writer"]:
            if agent_key in all_outputs:
                agent_outputs = all_outputs[agent_key]
                info = agent_info.get(agent_key, {"name": agent_key.title(), "description": "Processing"})
                
                for i, output in enumerate(agent_outputs):
                    steps.append({
                        "agent": info["name"],
                        "agent_key": agent_key,
                        "description": info["description"],
                        "output": output["output"],
                        "step": output.get("step", f"step_{i+1}"),
                        "timestamp": output["timestamp"]
                    })
        
        return steps
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status and statistics.
        
        Returns:
            Dict[str, Any]: System status information
        """
        workflow_status = get_workflow_status()
        
        return {
            "session_id": self.session_id,
            "agents_available": len(self.agents),
            "tools_available": len(self.tools),
            "memory_status": self.memory_manager.get_memory_summary(),
            "workflow_status": workflow_status,
            "system_ready": True
        }
    
    def reset_system(self):
        """
        Reset the entire system state.
        """
        print("INFO: Resetting system...")
        reset_workflow()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"SUCCESS: System reset complete. New session ID: {self.session_id}")
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Get the conversation history.
        
        Returns:
            List[Dict]: Conversation history
        """
        return self.memory_manager.get_conversation_history()
    
    def get_agent_info(self) -> Dict[str, Dict]:
        """
        Get information about available agents.
        
        Returns:
            Dict[str, Dict]: Agent information
        """
        return {
            "planner": {
                "name": "Planner Agent",
                "role": "Task Planner and Coordinator", 
                "description": "Analyzes tasks and coordinates workflow between other agents"
            },
            "research": {
                "name": "Research Agent",
                "role": "Information Researcher",
                "description": "Gathers information using available tools and conducts research"
            },
            "writer": {
                "name": "Writer Agent", 
                "role": "Content Writer and Response Generator",
                "description": "Creates comprehensive, user-friendly responses based on research"
            }
        }
    
    def get_tool_info(self) -> List[Dict]:
        """
        Get information about available tools.
        
        Returns:
            List[Dict]: Tool information
        """
        tools_info = []
        for tool in self.tools:
            tools_info.append({
                "name": tool.name,
                "description": tool.description,
                "type": "function"
            })
        
        return tools_info


# Global system instance
workout_system = WorkoutAgentSystem()


def get_workout_system() -> WorkoutAgentSystem:
    """
    Get the global workout agent system instance.
    
    Returns:
        WorkoutAgentSystem: The system instance
    """
    return workout_system


def process_user_query(query: str, enable_evaluation: bool = True) -> Dict[str, Any]:
    """
    Process a user query through the system.
    
    Args:
        query (str): User's query
        enable_evaluation (bool): Whether to run evaluation metrics
        
    Returns:
        Dict[str, Any]: Complete response
    """
    return workout_system.process_query(query, enable_evaluation)


def reset_system():
    """
    Reset the system state.
    """
    workout_system.reset_system()


def get_system_info() -> Dict[str, Any]:
    """
    Get comprehensive system information.
    
    Returns:
        Dict[str, Any]: System information
    """
    return {
        "system_status": workout_system.get_system_status(),
        "agents": workout_system.get_agent_info(),
        "tools": workout_system.get_tool_info(),
        "conversation_history": workout_system.get_conversation_history()
    }


if __name__ == "__main__":
    # Test the system
    print("Testing Workout Agent System")
    print("=" * 50)
    
    # Test query
    test_query = "Create a beginner workout plan for someone who wants to start exercising"
    result = process_user_query(test_query)
    
    print(f"\nTest Query: {test_query}")
    print(f"Success: {result['success']}")
    print(f"Agent Steps: {len(result['agent_steps'])}")
    print(f"Final Answer Preview: {result['final_answer'][:200]}...")
    
    print("\nSUCCESS: System test completed!")
