"""
Evaluation metrics module for the Multi-Agent Workout System.
Implements comprehensive metrics for response quality, agent coordination, and system performance.
"""

import time
import json
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime
import statistics
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class EvaluationResult:
    """Container for evaluation results."""
    query: str
    response: str
    timestamp: str
    
    # Response Quality Metrics
    response_length: int
    readability_score: float
    completeness_score: float
    relevance_score: float
    actionability_score: float
    
    # Agent Coordination Metrics
    agent_coordination_score: float
    workflow_efficiency: float
    tool_usage_effectiveness: float
    
    # Performance Metrics
    total_response_time: float
    agent_response_times: Dict[str, float]
    memory_usage_score: float
    
    # Overall Scores
    overall_quality_score: float
    system_efficiency_score: float
    final_score: float


class ResponseQualityEvaluator:
    """Evaluates the quality of responses using multiple metrics."""
    
    def __init__(self):
        self.fitness_keywords = [
            'exercise', 'workout', 'fitness', 'strength', 'cardio', 'nutrition', 
            'diet', 'protein', 'calories', 'muscle', 'training', 'recovery',
            'sets', 'reps', 'intensity', 'form', 'technique', 'safety'
        ]
        
        self.action_words = [
            'start', 'begin', 'perform', 'do', 'try', 'practice', 'follow',
            'avoid', 'include', 'focus', 'aim', 'target', 'maintain', 'increase'
        ]
    
    def evaluate_response_length(self, response: str) -> int:
        """Evaluate response length."""
        return len(response.split())
    
    def evaluate_readability(self, response: str) -> float:
        """
        Simplified readability score based on sentence structure.
        Scale: 0-1 (higher is better).
        """
        sentences = re.split(r'[.!?]+', response)
        if not sentences:
            return 0.0
        
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
        
        # Optimal sentence length is around 15-20 words
        if 10 <= avg_sentence_length <= 25:
            readability = 1.0 - abs(avg_sentence_length - 17.5) / 17.5
        else:
            readability = max(0.0, 1.0 - abs(avg_sentence_length - 17.5) / 30)
        
        return min(1.0, readability)
    
    def evaluate_completeness(self, response: str, query: str) -> float:
        """
        Evaluate how complete the response is relative to the query.
        Scale: 0-1 (higher is better).
        """
        # Check if response addresses key aspects
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())
        
        # Coverage of query terms
        coverage = len(query_words.intersection(response_words)) / len(query_words) if query_words else 0
        
        # Check for fitness domain completeness
        fitness_coverage = sum(1 for keyword in self.fitness_keywords if keyword in response.lower())
        fitness_score = min(1.0, fitness_coverage / 5)  # Normalize by expected keyword count
        
        # Structure completeness (sections, lists, etc.)
        structure_score = 0.0
        if '**' in response or '*' in response:  # Has formatting
            structure_score += 0.3
        if any(marker in response for marker in ['1.', '2.', 'a)', 'b)']):  # Has lists
            structure_score += 0.3
        if len(response.split('\n')) > 3:  # Has multiple sections
            structure_score += 0.4
        
        return (coverage * 0.4 + fitness_score * 0.3 + structure_score * 0.3)
    
    def evaluate_relevance(self, response: str, query: str) -> float:
        """
        Evaluate how relevant the response is to the query.
        Scale: 0-1 (higher is better).
        """
        query_lower = query.lower()
        response_lower = response.lower()
        
        # Direct keyword matching
        query_keywords = set(re.findall(r'\b\w+\b', query_lower))
        response_keywords = set(re.findall(r'\b\w+\b', response_lower))
        
        keyword_overlap = len(query_keywords.intersection(response_keywords))
        keyword_score = keyword_overlap / len(query_keywords) if query_keywords else 0
        
        # Fitness domain relevance
        fitness_relevance = sum(1 for keyword in self.fitness_keywords if keyword in response_lower)
        fitness_score = min(1.0, fitness_relevance / 3)
        
        # Context relevance (check if response stays on topic)
        context_score = 1.0
        if 'fitness' in query_lower or 'workout' in query_lower:
            if not any(word in response_lower for word in ['exercise', 'workout', 'fitness', 'training']):
                context_score = 0.5
        
        return (keyword_score * 0.4 + fitness_score * 0.4 + context_score * 0.2)
    
    def evaluate_actionability(self, response: str) -> float:
        """
        Evaluate how actionable the response is (contains specific steps/advice).
        Scale: 0-1 (higher is better).
        """
        # Check for action words
        action_count = sum(1 for word in self.action_words if word in response.lower())
        action_score = min(1.0, action_count / 5)
        
        # Check for specific instructions
        instruction_patterns = [
            r'\d+\s*(sets?|reps?|repetitions?|minutes?|times?)',
            r'(start|begin)\s+with',
            r'(aim|target)\s+for',
            r'\d+[-–]\d+\s*(minutes?|hours?|times?)',
        ]
        
        instruction_count = sum(1 for pattern in instruction_patterns 
                              if re.search(pattern, response.lower()))
        instruction_score = min(1.0, instruction_count / 3)
        
        # Check for structured advice (steps, lists)
        structure_indicators = ['step', 'first', 'second', 'then', 'next', 'finally']
        structure_count = sum(1 for indicator in structure_indicators 
                            if indicator in response.lower())
        structure_score = min(1.0, structure_count / 4)
        
        return (action_score * 0.4 + instruction_score * 0.4 + structure_score * 0.2)


class AgentCoordinationEvaluator:
    """Evaluates agent coordination and workflow efficiency."""
    
    def evaluate_coordination_score(self, agent_outputs: Dict[str, List]) -> float:
        """
        Evaluate how well agents coordinated with each other.
        Scale: 0-1 (higher is better).
        """
        if not agent_outputs:
            return 0.0
        
        # Check if all expected agents participated
        expected_agents = {'planner', 'research', 'writer'}
        present_agents = set(agent_outputs.keys())
        participation_score = len(present_agents.intersection(expected_agents)) / len(expected_agents)
        
        # Check for information flow between agents
        info_flow_score = 0.0
        if 'planner' in agent_outputs and 'research' in agent_outputs:
            # Research should build on planner's output
            planner_output = ' '.join([out['output'] for out in agent_outputs['planner']])
            research_output = ' '.join([out['output'] for out in agent_outputs['research']])
            
            if any(word in research_output.lower() for word in planner_output.lower().split()[:10]):
                info_flow_score += 0.5
        
        if 'research' in agent_outputs and 'writer' in agent_outputs:
            # Writer should incorporate research findings
            research_output = ' '.join([out['output'] for out in agent_outputs['research']])
            writer_output = ' '.join([out['output'] for out in agent_outputs['writer']])
            
            research_keywords = set(research_output.lower().split()[:20])
            writer_keywords = set(writer_output.lower().split())
            
            overlap = len(research_keywords.intersection(writer_keywords))
            if overlap > 3:  # Reasonable overlap indicating information transfer
                info_flow_score += 0.5
        
        return (participation_score * 0.6 + info_flow_score * 0.4)
    
    def evaluate_workflow_efficiency(self, agent_response_times: Dict[str, float]) -> float:
        """
        Evaluate the efficiency of the workflow execution.
        Scale: 0-1 (higher is better).
        """
        if not agent_response_times:
            return 0.0
        
        total_time = sum(agent_response_times.values())
        
        # Expected reasonable response times (in seconds)
        expected_times = {'planner': 3.0, 'research': 5.0, 'writer': 4.0}
        
        efficiency_scores = []
        for agent, actual_time in agent_response_times.items():
            expected = expected_times.get(agent, 5.0)
            if actual_time <= expected:
                efficiency_scores.append(1.0)
            else:
                # Penalize excessive time
                efficiency_scores.append(max(0.0, 1.0 - (actual_time - expected) / expected))
        
        return statistics.mean(efficiency_scores) if efficiency_scores else 0.0
    
    def evaluate_tool_usage(self, agent_outputs: Dict[str, List]) -> float:
        """
        Evaluate how effectively tools were used by agents.
        Scale: 0-1 (higher is better).
        """
        if 'research' not in agent_outputs:
            return 0.0
        
        research_outputs = agent_outputs['research']
        tool_usage_indicators = [
            'CALCULATOR TOOL USED',
            'WEB SEARCH TOOL USED',
            'FITNESS RESEARCH TOOL USED'
        ]
        
        tools_used = 0
        for output in research_outputs:
            output_text = output['output']
            for indicator in tool_usage_indicators:
                if indicator in output_text:
                    tools_used += 1
                    break  # Count each tool only once per output
        
        # Research agent should use multiple tools
        expected_tools = 3
        tool_score = min(1.0, tools_used / expected_tools)
        
        # Check for meaningful tool results
        meaningful_usage = 0.0
        for output in research_outputs:
            output_text = output['output']
            if 'TOOL USED' in output_text and len(output_text) > 100:
                meaningful_usage = 1.0
                break
        
        return (tool_score * 0.7 + meaningful_usage * 0.3)


class PerformanceEvaluator:
    """Evaluates system performance metrics."""
    
    def evaluate_response_time(self, total_time: float) -> float:
        """
        Evaluate response time performance.
        Scale: 0-1 (higher is better).
        """
        # Expected reasonable total response time
        target_time = 12.0  # seconds
        excellent_time = 8.0  # seconds
        
        if total_time <= excellent_time:
            return 1.0
        elif total_time <= target_time:
            return 1.0 - (total_time - excellent_time) / (target_time - excellent_time) * 0.3
        else:
            # Penalize longer times
            return max(0.0, 0.7 - (total_time - target_time) / target_time)
    
    def evaluate_memory_usage(self, memory_manager) -> float:
        """
        Evaluate memory usage efficiency.
        Scale: 0-1 (higher is better).
        """
        try:
            all_outputs = memory_manager.get_all_outputs()
            
            # Check memory organization
            organization_score = 0.0
            if all_outputs:
                # Good if outputs are properly categorized by agent
                if len(all_outputs.keys()) >= 2:
                    organization_score += 0.5
                
                # Check if outputs have proper structure
                for agent_outputs in all_outputs.values():
                    if isinstance(agent_outputs, list) and agent_outputs:
                        if all('output' in item for item in agent_outputs):
                            organization_score += 0.5
                            break
            
            # Memory persistence score
            persistence_score = 1.0 if hasattr(memory_manager, 'shared_state') else 0.5
            
            return (organization_score * 0.6 + persistence_score * 0.4)
        except Exception:
            return 0.5  # Default score if memory evaluation fails


class SystemEvaluator:
    """Main evaluator that coordinates all evaluation components."""
    
    def __init__(self):
        self.quality_evaluator = ResponseQualityEvaluator()
        self.coordination_evaluator = AgentCoordinationEvaluator()
        self.performance_evaluator = PerformanceEvaluator()
        
        self.evaluation_history = []
    
    def evaluate_system_response(self, 
                                query: str, 
                                final_response: str, 
                                agent_outputs: Dict[str, List],
                                agent_response_times: Dict[str, float],
                                total_response_time: float,
                                memory_manager) -> EvaluationResult:
        """
        Comprehensive evaluation of a system response.
        
        Args:
            query: Original user query
            final_response: Final system response
            agent_outputs: Dictionary of agent outputs
            agent_response_times: Dictionary of agent response times
            total_response_time: Total time for complete response
            memory_manager: System memory manager
            
        Returns:
            EvaluationResult: Comprehensive evaluation results
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Response Quality Metrics
        response_length = self.quality_evaluator.evaluate_response_length(final_response)
        readability_score = self.quality_evaluator.evaluate_readability(final_response)
        completeness_score = self.quality_evaluator.evaluate_completeness(final_response, query)
        relevance_score = self.quality_evaluator.evaluate_relevance(final_response, query)
        actionability_score = self.quality_evaluator.evaluate_actionability(final_response)
        
        # Agent Coordination Metrics
        coordination_score = self.coordination_evaluator.evaluate_coordination_score(agent_outputs)
        workflow_efficiency = self.coordination_evaluator.evaluate_workflow_efficiency(agent_response_times)
        tool_usage_effectiveness = self.coordination_evaluator.evaluate_tool_usage(agent_outputs)
        
        # Performance Metrics
        response_time_score = self.performance_evaluator.evaluate_response_time(total_response_time)
        memory_usage_score = self.performance_evaluator.evaluate_memory_usage(memory_manager)
        
        # Calculate overall scores
        overall_quality_score = statistics.mean([
            readability_score, completeness_score, relevance_score, actionability_score
        ])
        
        system_efficiency_score = statistics.mean([
            coordination_score, workflow_efficiency, tool_usage_effectiveness, 
            response_time_score, memory_usage_score
        ])
        
        final_score = (overall_quality_score * 0.6 + system_efficiency_score * 0.4)
        
        # Create evaluation result
        result = EvaluationResult(
            query=query,
            response=final_response[:200] + "..." if len(final_response) > 200 else final_response,
            timestamp=timestamp,
            response_length=response_length,
            readability_score=readability_score,
            completeness_score=completeness_score,
            relevance_score=relevance_score,
            actionability_score=actionability_score,
            agent_coordination_score=coordination_score,
            workflow_efficiency=workflow_efficiency,
            tool_usage_effectiveness=tool_usage_effectiveness,
            total_response_time=total_response_time,
            agent_response_times=agent_response_times,
            memory_usage_score=memory_usage_score,
            overall_quality_score=overall_quality_score,
            system_efficiency_score=system_efficiency_score,
            final_score=final_score
        )
        
        self.evaluation_history.append(result)
        return result
    
    def get_evaluation_summary(self) -> Dict[str, Any]:
        """Get summary statistics of all evaluations."""
        if not self.evaluation_history:
            return {}
        
        metrics = {
            'total_evaluations': len(self.evaluation_history),
            'avg_final_score': statistics.mean([r.final_score for r in self.evaluation_history]),
            'avg_quality_score': statistics.mean([r.overall_quality_score for r in self.evaluation_history]),
            'avg_efficiency_score': statistics.mean([r.system_efficiency_score for r in self.evaluation_history]),
            'avg_response_time': statistics.mean([r.total_response_time for r in self.evaluation_history]),
            'avg_response_length': statistics.mean([r.response_length for r in self.evaluation_history]),
            
            # Individual metric averages
            'avg_readability': statistics.mean([r.readability_score for r in self.evaluation_history]),
            'avg_completeness': statistics.mean([r.completeness_score for r in self.evaluation_history]),
            'avg_relevance': statistics.mean([r.relevance_score for r in self.evaluation_history]),
            'avg_actionability': statistics.mean([r.actionability_score for r in self.evaluation_history]),
            'avg_coordination': statistics.mean([r.agent_coordination_score for r in self.evaluation_history]),
            'avg_workflow_efficiency': statistics.mean([r.workflow_efficiency for r in self.evaluation_history]),
            'avg_tool_usage': statistics.mean([r.tool_usage_effectiveness for r in self.evaluation_history]),
        }
        
        return metrics
    
    def save_evaluation_results(self, filepath: str = None):
        """Save evaluation results to JSON file."""
        if not filepath:
            filepath = f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results_data = {
            'summary': self.get_evaluation_summary(),
            'individual_results': [asdict(result) for result in self.evaluation_history]
        }
        
        with open(filepath, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        return filepath


# Global evaluator instance
system_evaluator = SystemEvaluator()


def get_system_evaluator() -> SystemEvaluator:
    """Get the global system evaluator instance."""
    return system_evaluator
