"""
Memory management system for the multi-agent system.
Implements shared state and per-agent memory using LangChain's memory components.
"""

from typing import Dict, List, Any, Optional
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage, HumanMessage, AIMessage
import json
from datetime import datetime


class SharedState:
    """
    Shared state accessible to all agents.
    Stores common information and coordination data between agents.
    """
    
    def __init__(self):
        self.data = {}
        self.conversation_history = []
        self.current_task = None
        self.task_status = "idle"  # idle, planning, researching, writing, completed
        self.agent_outputs = {}
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
    
    def set_task(self, task: str):
        """Set the current task being processed."""
        self.current_task = task
        self.task_status = "planning"
        self.last_updated = datetime.now()
    
    def update_status(self, status: str):
        """Update the current task status."""
        self.task_status = status
        self.last_updated = datetime.now()
    
    def add_agent_output(self, agent_name: str, output: str, step: str = None):
        """Add output from an agent."""
        if agent_name not in self.agent_outputs:
            self.agent_outputs[agent_name] = []
        
        self.agent_outputs[agent_name].append({
            "output": output,
            "step": step,
            "timestamp": datetime.now().isoformat()
        })
        self.last_updated = datetime.now()
    
    def get_agent_outputs(self, agent_name: str) -> List[Dict]:
        """Get outputs from a specific agent."""
        return self.agent_outputs.get(agent_name, [])
    
    def get_all_outputs(self) -> Dict:
        """Get all agent outputs."""
        return self.agent_outputs
    
    def add_to_history(self, message: str, sender: str = "user"):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            "message": message,
            "sender": sender,
            "timestamp": datetime.now().isoformat()
        })
        self.last_updated = datetime.now()
    
    def get_history(self) -> List[Dict]:
        """Get the conversation history."""
        return self.conversation_history
    
    def set_data(self, key: str, value: Any):
        """Set data in shared state."""
        self.data[key] = value
        self.last_updated = datetime.now()
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """Get data from shared state."""
        return self.data.get(key, default)
    
    def clear(self):
        """Clear all data and reset state."""
        self.data = {}
        self.conversation_history = []
        self.current_task = None
        self.task_status = "idle"
        self.agent_outputs = {}
        self.last_updated = datetime.now()


class AgentMemory:
    """
    Memory management for individual agents.
    Each agent has its own ConversationBufferMemory and context.
    """
    
    def __init__(self, agent_name: str, max_token_limit: int = 2000):
        self.agent_name = agent_name
        self.memory = ConversationBufferMemory(
            max_token_limit=max_token_limit,
            return_messages=True
        )
        self.context = {}
        self.interaction_count = 0
        self.created_at = datetime.now()
        self.last_interaction = None
    
    def add_message(self, message: str, is_human: bool = True):
        """Add a message to the agent's memory."""
        if is_human:
            self.memory.chat_memory.add_user_message(message)
        else:
            self.memory.chat_memory.add_ai_message(message)
        
        self.interaction_count += 1
        self.last_interaction = datetime.now()
    
    def get_memory_variables(self) -> Dict:
        """Get memory variables for the agent."""
        return self.memory.load_memory_variables({})
    
    def get_messages(self) -> List[BaseMessage]:
        """Get all messages from memory."""
        return self.memory.chat_memory.messages
    
    def set_context(self, key: str, value: Any):
        """Set context data for the agent."""
        self.context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context data for the agent."""
        return self.context.get(key, default)
    
    def clear_memory(self):
        """Clear the agent's memory."""
        self.memory.clear()
        self.interaction_count = 0
    
    def get_recent_messages(self, count: int = 5) -> List[BaseMessage]:
        """Get the most recent messages."""
        messages = self.get_messages()
        return messages[-count:] if len(messages) > count else messages
    
    def get_summary(self) -> str:
        """Get a summary of the agent's memory state."""
        messages = self.get_messages()
        return f"Agent: {self.agent_name}, Messages: {len(messages)}, Interactions: {self.interaction_count}, Last: {self.last_interaction}"


class MemoryManager:
    """
    Central memory manager that coordinates shared state and individual agent memories.
    """
    
    def __init__(self):
        self.shared_state = SharedState()
        self.agent_memories: Dict[str, AgentMemory] = {}
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def get_or_create_agent_memory(self, agent_name: str) -> AgentMemory:
        """Get existing agent memory or create a new one."""
        if agent_name not in self.agent_memories:
            self.agent_memories[agent_name] = AgentMemory(agent_name)
        return self.agent_memories[agent_name]
    
    def add_user_message(self, message: str):
        """Add a user message to shared state and all agent memories."""
        self.shared_state.add_to_history(message, "user")
        
        # Add to all agent memories
        for agent_memory in self.agent_memories.values():
            agent_memory.add_message(message, is_human=True)
    
    def add_agent_response(self, agent_name: str, response: str, step: str = None):
        """Add an agent response to shared state and the agent's memory."""
        self.shared_state.add_agent_output(agent_name, response, step)
        self.shared_state.add_to_history(response, agent_name)
        
        agent_memory = self.get_or_create_agent_memory(agent_name)
        agent_memory.add_message(response, is_human=False)
    
    def get_context_for_agent(self, agent_name: str) -> Dict:
        """Get relevant context for a specific agent."""
        agent_memory = self.get_or_create_agent_memory(agent_name)
        
        context = {
            "agent_name": agent_name,
            "current_task": self.shared_state.current_task,
            "task_status": self.shared_state.task_status,
            "shared_data": self.shared_state.data,
            "recent_messages": [msg.content for msg in agent_memory.get_recent_messages()],
            "agent_context": agent_memory.context,
            "other_agent_outputs": {
                name: outputs for name, outputs in self.shared_state.agent_outputs.items() 
                if name != agent_name
            }
        }
        
        return context
    
    def set_task(self, task: str):
        """Set the current task across the system."""
        self.shared_state.set_task(task)
    
    def update_task_status(self, status: str):
        """Update the task status."""
        self.shared_state.update_status(status)
    
    def get_all_outputs(self) -> Dict:
        """Get all agent outputs."""
        return self.shared_state.get_all_outputs()
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the full conversation history."""
        return self.shared_state.get_history()
    
    def clear_all_memory(self):
        """Clear all memory and reset the system."""
        self.shared_state.clear()
        for agent_memory in self.agent_memories.values():
            agent_memory.clear_memory()
    
    def get_memory_summary(self) -> str:
        """Get a summary of the memory state."""
        summary = f"Memory Manager Summary (Session: {self.session_id})\n"
        summary += f"Current Task: {self.shared_state.current_task}\n"
        summary += f"Task Status: {self.shared_state.task_status}\n"
        summary += f"Conversation History: {len(self.shared_state.conversation_history)} messages\n"
        summary += f"Agent Memories: {len(self.agent_memories)} agents\n"
        
        for name, memory in self.agent_memories.items():
            summary += f"  - {memory.get_summary()}\n"
        
        return summary


# Global memory manager instance
memory_manager = MemoryManager()


def get_memory_manager() -> MemoryManager:
    """Get the global memory manager instance."""
    return memory_manager


def reset_memory():
    """Reset all memory in the system."""
    global memory_manager
    memory_manager.clear_all_memory()


def get_agent_context(agent_name: str) -> Dict:
    """Get context for a specific agent."""
    return memory_manager.get_context_for_agent(agent_name)
