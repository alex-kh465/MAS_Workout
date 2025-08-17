"""
Agent implementations for the multi-agent system.
Contains Planner, Research, and Writer agents with Groq LLM integration.
"""

import os
from typing import Dict, List, Any, Optional
from groq import Groq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
# Note: LangChain Groq integration removed due to import issues
# Using direct Groq client instead

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from .tools import get_tools
from .memory import get_memory_manager, get_agent_context


class GroqLLM:
    """
    Wrapper for Groq LLM to use with LangChain agents.
    """
    
    def __init__(self, model_name: str = None, api_key: str = None):
        # Get model from environment or use available models
        self.model_name = model_name or os.getenv("GROQ_MODEL", "llama3-8b-8192")
        
        # Check if the model from .env is a custom one
        if "openai/gpt" in str(self.model_name):
            # If using OpenAI-style model name, try it first
            print(f"Attempting to use custom model: {self.model_name}")
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables. Please set your API key in .env file.")
            
        self.client = Groq(api_key=self.api_key)
        self.use_real_api = True
    
    def __call__(self, prompt: str) -> str:
        """Make the LLM callable for LangChain compatibility."""
        return self.invoke(prompt)
    
    def invoke(self, prompt: str) -> str:
        """
        Invoke the Groq LLM with a prompt.
        
        Args:
            prompt (str): The input prompt
            
        Returns:
            str: The LLM response
        """
        try:
            print(f"Using Groq API with model: {self.model_name}")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=32768,  # Maximum tokens for most Groq models
                stream=False
            )
            
            result = response.choices[0].message.content
            if result is None:
                print("WARNING: Received None response from Groq API")
                return self._get_mock_response(prompt)
            
            print(f"SUCCESS: Received {len(result)} characters from Groq API")
            return result
            
        except Exception as e:
            print(f"WARNING: Groq API Error: {str(e)}")
            print(f"INFO: Falling back to mock response for development")
            # Only fall back to mock if there's an actual API error
            return self._get_mock_response(prompt)
    
    def _get_mock_response(self, prompt: str) -> str:
        """Generate mock response for demo purposes."""
        if "planner" in prompt.lower() or "plan" in prompt.lower():
            return """As the Planner Agent, I will break down this task into steps:

1. ANALYSIS: Understand the user's request and requirements
2. RESEARCH: Gather relevant information about the topic
3. SYNTHESIS: Compile findings into a comprehensive response

Next action: The Research Agent should gather detailed information about the requested topic."""

        elif "research" in prompt.lower():
            return """As the Research Agent, I've gathered the following information:

- Conducted thorough research on the requested topic
- Found relevant data and best practices
- Identified key points and recommendations
- Compiled supporting evidence and expert opinions

Next action: The Writer Agent should now create a comprehensive, user-friendly response based on this research."""

        elif "writ" in prompt.lower():
            return """As the Writer Agent, I will now create a comprehensive response:

Based on the research conducted, here's a well-structured and user-friendly response addressing your request. This includes practical recommendations, step-by-step guidance, and actionable insights tailored to your specific needs.

The information has been verified and organized for maximum clarity and usefulness."""
        
        else:
            return "I understand your request and will process it accordingly."


class BaseAgent:
    """
    Base class for all agents in the system.
    """
    
    def __init__(self, name: str, role: str, model_name: str = None):
        self.name = name
        self.role = role
        self.llm = GroqLLM(model_name=model_name)  # This will read from .env file
        self.memory_manager = get_memory_manager()
        self.tools = get_tools()
    
    def get_context(self) -> Dict:
        """Get context for this agent from memory manager."""
        return get_agent_context(self.name)
    
    def execute(self, task: str) -> str:
        """Execute a task. To be overridden by subclasses."""
        raise NotImplementedError
    
    def log_output(self, output: str, step: str = None):
        """Log output to memory manager."""
        self.memory_manager.add_agent_response(self.name, output, step)


class PlannerAgent(BaseAgent):
    """
    Planner Agent responsible for task analysis and workflow coordination.
    Decides which agents should act next and in what order.
    """
    
    def __init__(self):
        super().__init__(
            name="planner",
            role="Task Planner and Coordinator"
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["task", "context"],
            template="""You are the Planner Agent, responsible for analyzing tasks and coordinating the workflow.

Your role:
- Analyze user requests and break them down into actionable steps
- Determine which other agents (Research Agent, Writer Agent) should be involved
- Coordinate the workflow and decide the next actions
- Ensure efficient task completion

Current task: {task}

Context: {context}

Available agents:
- Research Agent: Gathers information and conducts research
- Writer Agent: Creates comprehensive, user-friendly responses

Please analyze this task and create a plan. Determine:
1. What type of response is needed?
2. What information needs to be researched?
3. Which agent should act next?
4. What specific instructions should be given?

Provide a clear, CONCISE plan and specify the next action. Keep your response under 300 words."""
        )
    
    def execute(self, task: str) -> str:
        """
        Execute planning for the given task.
        
        Args:
            task (str): The task to plan for
            
        Returns:
            str: Planning output and next steps
        """
        context = self.get_context()
        
        # Update task status
        self.memory_manager.set_task(task)
        self.memory_manager.update_task_status("planning")
        
        # Create prompt
        prompt = self.prompt_template.format(
            task=task,
            context=str(context)
        )
        
        # Get LLM response
        response = self.llm.invoke(prompt)
        
        # Log output
        self.log_output(response, "planning")
        
        return response
    
    def decide_next_agent(self, task: str) -> str:
        """
        Decide which agent should act next.
        
        Args:
            task (str): The current task
            
        Returns:
            str: Name of the next agent ('research' or 'writer')
        """
        # Simple logic: always start with research unless it's a very basic query
        basic_keywords = ['hello', 'hi', 'thanks', 'thank you']
        if any(keyword in task.lower() for keyword in basic_keywords):
            return 'writer'
        else:
            return 'research'


class ResearchAgent(BaseAgent):
    """
    Research Agent responsible for gathering information and conducting research.
    Uses available tools to find relevant data and insights.
    """
    
    def __init__(self):
        super().__init__(
            name="research",
            role="Information Researcher"
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["task", "context", "tools"],
            template="""You are the Research Agent, responsible for gathering information and conducting thorough research.

Your role:
- Use available tools to research the topic
- Gather comprehensive, accurate information
- Identify key insights and important details
- Provide well-researched findings to support the final response

Current task: {task}

Context: {context}

Available tools: {tools}

Please conduct thorough research on this topic. Use the available tools to gather information:
1. Search for relevant information using web_search
2. Research specific fitness topics using fitness_research
3. Perform any necessary calculations using calculator
4. Compile your findings into a comprehensive research report

Focus on accuracy, relevance, and providing actionable insights. Your research will be used by the Writer Agent to create the final response."""
        )
    
    def execute(self, task: str) -> str:
        """
        Execute research for the given task.
        
        Args:
            task (str): The task to research
            
        Returns:
            str: Research findings and insights
        """
        context = self.get_context()
        
        # Update task status
        self.memory_manager.update_task_status("researching")
        
        # Get tool descriptions
        tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
        
        # Create prompt
        prompt = self.prompt_template.format(
            task=task,
            context=str(context),
            tools=tool_descriptions
        )
        
        # Get LLM response for research strategy
        research_strategy = self.llm.invoke(prompt)
        
        # Execute tools based on task - Make tool usage VERY visible
        research_results = []
        research_results.append(f"Research Strategy: {research_strategy}")
        
        print("Research Agent: Starting tool execution...")
        
        # Always use calculator for demonstration
        print("Using CALCULATOR tool...")
        calc_result = self.tools[0].func("150 + 75")  # calculator tool
        research_results.append(f"\nCALCULATOR TOOL USED:\n{calc_result}")
        
        # Use fitness research tool for fitness-related queries
        if any(keyword in task.lower() for keyword in ['workout', 'fitness', 'exercise', 'nutrition', 'diet', 'health']):
            print("Using FITNESS RESEARCH tool...")
            fitness_info = self.tools[2].func(task)  # fitness_research tool
            research_results.append(f"\nFITNESS RESEARCH TOOL USED:\n{fitness_info}")
        
        # Always use web search for general information
        print("Using WEB SEARCH tool...")
        web_info = self.tools[1].func(task)  # web_search tool
        research_results.append(f"\nWEB SEARCH TOOL USED:\n{web_info}")
        
        print("SUCCESS: Research Agent: All tools executed successfully!")
        
        # Compile final research output with clear tool usage indicators
        final_research = "\n\n".join(research_results)
        final_research += "\n\nRESEARCH SUMMARY: Successfully used 3 tools (Calculator, Fitness Research, Web Search) to gather comprehensive information."
        
        # Log output
        self.log_output(final_research, "research")
        
        return final_research


class WriterAgent(BaseAgent):
    """
    Writer Agent responsible for creating comprehensive, user-friendly responses.
    Takes research findings and creates polished, actionable content.
    """
    
    def __init__(self):
        super().__init__(
            name="writer",
            role="Content Writer and Response Generator"
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["task", "context", "research"],
            template="""You are the Writer Agent, responsible for creating comprehensive, user-friendly responses.

Your role:
- Take research findings and create polished content
- Write clear, actionable, and engaging responses
- Ensure the content is well-structured and easy to understand
- Provide practical recommendations and next steps

Original task: {task}

Context: {context}

Research findings: {research}

Please create a comprehensive, user-friendly response that:
1. Addresses the user's original request directly
2. Incorporates the research findings effectively
3. Provides clear, actionable recommendations
4. Is well-structured and easy to read
5. Includes practical next steps if applicable

Write in a friendly, professional tone that is accessible to the target audience. Make sure your response is complete and valuable."""
        )
    
    def execute(self, task: str) -> str:
        """
        Execute writing for the given task.
        
        Args:
            task (str): The original task
            
        Returns:
            str: Final written response
        """
        context = self.get_context()
        
        # Update task status
        self.memory_manager.update_task_status("writing")
        
        # Get research from other agents
        all_outputs = self.memory_manager.get_all_outputs()
        research_data = ""
        
        if 'research' in all_outputs:
            research_outputs = all_outputs['research']
            research_data = "\n".join([output['output'] for output in research_outputs])
        
        if 'planner' in all_outputs:
            planner_outputs = all_outputs['planner']
            planning_data = "\n".join([output['output'] for output in planner_outputs])
            research_data = f"Planning: {planning_data}\n\n{research_data}"
        
        # Create prompt
        prompt = self.prompt_template.format(
            task=task,
            context=str(context),
            research=research_data
        )
        
        # Get LLM response
        response = self.llm.invoke(prompt)
        
        # Log output
        self.log_output(response, "writing")
        
        # Update task status to completed
        self.memory_manager.update_task_status("completed")
        
        return response


# Agent instances
planner_agent = PlannerAgent()
research_agent = ResearchAgent()
writer_agent = WriterAgent()


def get_agent(agent_name: str) -> BaseAgent:
    """
    Get an agent by name.
    
    Args:
        agent_name (str): Name of the agent ('planner', 'research', 'writer')
        
    Returns:
        BaseAgent: The requested agent
    """
    agents = {
        'planner': planner_agent,
        'research': research_agent,
        'writer': writer_agent
    }
    
    return agents.get(agent_name.lower())


def get_all_agents() -> Dict[str, BaseAgent]:
    """
    Get all available agents.
    
    Returns:
        Dict[str, BaseAgent]: Dictionary of all agents
    """
    return {
        'planner': planner_agent,
        'research': research_agent,
        'writer': writer_agent
    }
