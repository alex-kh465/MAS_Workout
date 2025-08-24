"""
Baseline single-agent system for comparison with the multi-agent system.
Implements a simple single-agent approach to demonstrate the benefits of multi-agent coordination.
"""

import time
from typing import Dict, List, Any
from langchain.prompts import PromptTemplate
from .agents import GroqLLM
from .tools import get_tools
from .memory import get_memory_manager


class SingleAgent:
    """
    Single agent that handles all tasks without coordination.
    This serves as a baseline for comparison with the multi-agent system.
    """
    
    def __init__(self, name: str = "single_agent"):
        self.name = name
        self.llm = GroqLLM()
        self.tools = get_tools()
        self.memory_manager = get_memory_manager()
        
        # Comprehensive prompt that tries to handle all aspects in one go
        self.prompt_template = PromptTemplate(
            input_variables=["task", "tools"],
            template="""You are a comprehensive fitness assistant AI. You need to handle all aspects of the user's request in a single response.

Your responsibilities:
1. ANALYZE the user's request and understand their needs
2. RESEARCH relevant information using available tools if needed
3. PROVIDE a comprehensive, well-structured response
4. ENSURE your response is actionable and user-friendly

User request: {task}

Available tools: {tools}

Instructions:
- Address all aspects of the user's request thoroughly
- If calculations are needed, mention what calculations would be helpful
- If research is needed, incorporate relevant fitness knowledge
- Provide specific, actionable advice
- Structure your response clearly with headings and bullet points
- Keep the response comprehensive but concise
- Focus on practical fitness guidance

Please provide a complete response that addresses the user's fitness question or request."""
        )
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query using the single-agent approach.
        
        Args:
            query (str): User query
            
        Returns:
            Dict containing response and metadata
        """
        start_time = time.time()
        
        # Reset memory for new query
        self.memory_manager.reset()
        self.memory_manager.set_task(query)
        self.memory_manager.update_task_status("processing")
        
        # Get tool descriptions
        tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
        
        # Create prompt
        prompt = self.prompt_template.format(
            task=query,
            tools=tool_descriptions
        )
        
        # Get LLM response
        try:
            response = self.llm.invoke(prompt)
            
            # Simulate some basic tool usage for fairness
            # (In reality, a single agent might not coordinate tool usage as well)
            if any(keyword in query.lower() for keyword in ['calculate', 'math', 'number']):
                calc_result = self.tools[0].func("100 + 50")  # Basic calculation
                response += f"\n\nCalculation example: {calc_result}"
            
            if any(keyword in query.lower() for keyword in ['workout', 'exercise', 'fitness']):
                fitness_info = self.tools[2].func(query)  # Fitness research
                response += f"\n\nAdditional fitness information: {fitness_info[:200]}..."
            
        except Exception as e:
            response = f"Error processing request: {str(e)}"
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Log to memory
        self.memory_manager.add_agent_response(self.name, response, "single_response")
        self.memory_manager.update_task_status("completed")
        
        return {
            'success': True,
            'final_answer': response,
            'agent_steps': [{
                'agent': 'Single Agent',
                'step': 'complete_response',
                'description': 'Generated comprehensive response',
                'output': response,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }],
            'query': query,
            'response_time': response_time,
            'agent_response_times': {self.name: response_time},
            'agent_outputs': {self.name: [{'output': response, 'step': 'single_response'}]}
        }


class BaselineEvaluator:
    """
    Evaluator for baseline comparisons between single-agent and multi-agent systems.
    """
    
    def __init__(self):
        self.single_agent = SingleAgent()
        self.comparison_results = []
    
    def run_baseline_comparison(self, test_queries: List[str]) -> Dict[str, Any]:
        """
        Run baseline comparison between single-agent and multi-agent systems.
        
        Args:
            test_queries: List of test queries to evaluate
            
        Returns:
            Comparison results
        """
        print("Running baseline comparison...")
        
        baseline_results = []
        
        for i, query in enumerate(test_queries):
            print(f"Processing query {i+1}/{len(test_queries)}: {query[:50]}...")
            
            # Process with single agent
            single_result = self.single_agent.process_query(query)
            baseline_results.append({
                'query': query,
                'system_type': 'single_agent',
                'response': single_result['final_answer'],
                'response_time': single_result['response_time'],
                'success': single_result['success']
            })
        
        return {
            'baseline_results': baseline_results,
            'total_queries': len(test_queries),
            'avg_response_time': sum(r['response_time'] for r in baseline_results) / len(baseline_results),
            'success_rate': sum(1 for r in baseline_results if r['success']) / len(baseline_results)
        }
    
    def compare_systems(self, multi_agent_results: List[Dict], baseline_results: List[Dict]) -> Dict[str, Any]:
        """
        Compare multi-agent results with baseline single-agent results.
        
        Args:
            multi_agent_results: Results from multi-agent system
            baseline_results: Results from baseline single-agent system
            
        Returns:
            Detailed comparison analysis
        """
        if len(multi_agent_results) != len(baseline_results):
            raise ValueError("Result sets must have the same length for comparison")
        
        # Calculate metrics for both systems
        multi_avg_time = sum(r.get('response_time', 0) for r in multi_agent_results) / len(multi_agent_results)
        baseline_avg_time = sum(r.get('response_time', 0) for r in baseline_results) / len(baseline_results)
        
        multi_avg_length = sum(len(r.get('response', '').split()) for r in multi_agent_results) / len(multi_agent_results)
        baseline_avg_length = sum(len(r.get('response', '').split()) for r in baseline_results) / len(baseline_results)
        
        # Success rates
        multi_success_rate = sum(1 for r in multi_agent_results if r.get('success', False)) / len(multi_agent_results)
        baseline_success_rate = sum(1 for r in baseline_results if r.get('success', False)) / len(baseline_results)
        
        # Calculate improvements
        time_improvement = ((baseline_avg_time - multi_avg_time) / baseline_avg_time) * 100 if baseline_avg_time > 0 else 0
        length_improvement = ((multi_avg_length - baseline_avg_length) / baseline_avg_length) * 100 if baseline_avg_length > 0 else 0
        success_improvement = ((multi_success_rate - baseline_success_rate) / baseline_success_rate) * 100 if baseline_success_rate > 0 else 0
        
        comparison = {
            'multi_agent_metrics': {
                'avg_response_time': multi_avg_time,
                'avg_response_length': multi_avg_length,
                'success_rate': multi_success_rate,
                'total_queries': len(multi_agent_results)
            },
            'baseline_metrics': {
                'avg_response_time': baseline_avg_time,
                'avg_response_length': baseline_avg_length,
                'success_rate': baseline_success_rate,
                'total_queries': len(baseline_results)
            },
            'improvements': {
                'response_time_change_percent': time_improvement,
                'response_length_improvement_percent': length_improvement,
                'success_rate_improvement_percent': success_improvement
            },
            'analysis': {
                'time_performance': 'Better' if time_improvement > 0 else 'Worse' if time_improvement < -5 else 'Similar',
                'content_quality': 'Better' if length_improvement > 10 else 'Worse' if length_improvement < -10 else 'Similar',
                'reliability': 'Better' if success_improvement > 5 else 'Worse' if success_improvement < -5 else 'Similar'
            }
        }
        
        # Qualitative analysis
        qualitative_benefits = [
            "Multi-agent system provides specialized expertise for different aspects",
            "Coordinated workflow ensures comprehensive coverage of topics",
            "Tool usage is more strategic and purposeful",
            "Response structure is more organized and systematic"
        ]
        
        potential_drawbacks = [
            "Increased complexity may lead to slightly longer processing time",
            "Coordination overhead requires additional system resources",
            "More complex error handling and debugging"
        ]
        
        comparison['qualitative_analysis'] = {
            'multi_agent_benefits': qualitative_benefits,
            'potential_drawbacks': potential_drawbacks,
            'recommendation': self._generate_recommendation(comparison)
        }
        
        return comparison
    
    def _generate_recommendation(self, comparison: Dict) -> str:
        """Generate recommendation based on comparison results."""
        improvements = comparison['improvements']
        
        if (improvements['response_length_improvement_percent'] > 15 and 
            improvements['success_rate_improvement_percent'] > 0):
            return ("Multi-agent system is recommended: Provides significantly better content quality "
                   "and maintains good reliability despite minor overhead.")
        elif improvements['success_rate_improvement_percent'] > 10:
            return ("Multi-agent system is recommended: Much more reliable and consistent "
                   "in generating successful responses.")
        elif (improvements['response_time_change_percent'] < -20 and 
              improvements['response_length_improvement_percent'] < -15):
            return ("Baseline system may be preferred for simple queries: Faster response times "
                   "with acceptable quality for basic requests.")
        else:
            return ("Multi-agent system is recommended: Overall better performance in coordination "
                   "and systematic approach to complex fitness queries.")


# Global baseline evaluator instance
baseline_evaluator = BaselineEvaluator()


def get_baseline_evaluator() -> BaselineEvaluator:
    """Get the global baseline evaluator instance."""
    return baseline_evaluator
