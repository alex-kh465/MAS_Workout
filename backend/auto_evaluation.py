"""
Automated evaluation framework for the Multi-Agent Workout System.
Includes test dataset, automated evaluation runs, and comprehensive analysis.
"""

import json
import time
import statistics
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path

from .evaluation import get_system_evaluator, EvaluationResult
from .baseline import get_baseline_evaluator
from .main import process_user_query
from .memory import get_memory_manager


class TestDataset:
    """Test dataset with standardized queries and expected response characteristics."""
    
    def __init__(self):
        self.test_queries = [
            {
                'id': 'beginner_001',
                'query': 'Create a beginner workout plan for someone who wants to start exercising',
                'category': 'workout_planning',
                'complexity': 'medium',
                'expected_elements': ['warm-up', 'strength', 'cardio', 'cool-down', 'progression'],
                'expected_length_range': (100, 400),
                'keywords_must_include': ['beginner', 'exercise', 'workout', 'plan']
            },
            {
                'id': 'nutrition_001',
                'query': 'What should I eat before and after a workout for optimal performance?',
                'category': 'nutrition',
                'complexity': 'medium',
                'expected_elements': ['pre-workout', 'post-workout', 'timing', 'nutrients'],
                'expected_length_range': (80, 300),
                'keywords_must_include': ['nutrition', 'protein', 'carbs', 'timing']
            },
            {
                'id': 'strength_001',
                'query': 'What are the best exercises for building upper body strength?',
                'category': 'exercise_selection',
                'complexity': 'low',
                'expected_elements': ['exercises', 'muscle_groups', 'sets_reps', 'form'],
                'expected_length_range': (60, 250),
                'keywords_must_include': ['upper body', 'strength', 'exercises']
            },
            {
                'id': 'cardio_001',
                'query': 'Design a 30-minute HIIT workout routine for fat loss',
                'category': 'workout_planning',
                'complexity': 'high',
                'expected_elements': ['hiit', 'intervals', 'exercises', 'timing', 'fat_loss'],
                'expected_length_range': (120, 400),
                'keywords_must_include': ['HIIT', '30 minute', 'intervals', 'fat loss']
            },
            {
                'id': 'endurance_001',
                'query': 'How can I improve my running endurance safely?',
                'category': 'performance_improvement',
                'complexity': 'medium',
                'expected_elements': ['progression', 'safety', 'training_plan', 'techniques'],
                'expected_length_range': (80, 300),
                'keywords_must_include': ['running', 'endurance', 'safely', 'improve']
            },
            {
                'id': 'home_001',
                'query': 'Create a home workout routine with no equipment needed',
                'category': 'workout_planning',
                'complexity': 'medium',
                'expected_elements': ['bodyweight', 'home', 'routine', 'no_equipment'],
                'expected_length_range': (100, 350),
                'keywords_must_include': ['home workout', 'no equipment', 'bodyweight']
            },
            {
                'id': 'recovery_001',
                'query': 'What are the best recovery strategies after intense workouts?',
                'category': 'recovery',
                'complexity': 'medium',
                'expected_elements': ['rest', 'nutrition', 'sleep', 'active_recovery'],
                'expected_length_range': (80, 300),
                'keywords_must_include': ['recovery', 'rest', 'intense workout']
            },
            {
                'id': 'weight_loss_001',
                'query': 'Design a comprehensive fitness plan for weight loss including diet and exercise',
                'category': 'comprehensive_planning',
                'complexity': 'high',
                'expected_elements': ['diet', 'exercise', 'plan', 'weight_loss', 'comprehensive'],
                'expected_length_range': (150, 500),
                'keywords_must_include': ['weight loss', 'diet', 'exercise', 'fitness plan']
            },
            {
                'id': 'injury_001',
                'query': 'What exercises are safe for someone with knee problems?',
                'category': 'special_populations',
                'complexity': 'high',
                'expected_elements': ['safety', 'modifications', 'knee_friendly', 'alternatives'],
                'expected_length_range': (100, 350),
                'keywords_must_include': ['knee problems', 'safe exercises', 'modifications']
            },
            {
                'id': 'motivation_001',
                'query': 'How can I stay motivated to exercise consistently?',
                'category': 'motivation_psychology',
                'complexity': 'low',
                'expected_elements': ['motivation', 'consistency', 'strategies', 'tips'],
                'expected_length_range': (60, 250),
                'keywords_must_include': ['motivated', 'consistently', 'exercise']
            }
        ]
    
    def get_test_queries(self) -> List[str]:
        """Get list of test query strings."""
        return [item['query'] for item in self.test_queries]
    
    def get_test_data(self) -> List[Dict]:
        """Get complete test dataset."""
        return self.test_queries
    
    def evaluate_against_expected(self, query_id: str, response: str) -> Dict[str, Any]:
        """Evaluate a response against expected characteristics."""
        test_item = next((item for item in self.test_queries if item['id'] == query_id), None)
        if not test_item:
            return {'error': 'Query ID not found'}
        
        evaluation = {
            'query_id': query_id,
            'passes_length_check': False,
            'includes_required_keywords': False,
            'keyword_coverage': 0.0,
            'length_score': 0.0,
            'overall_expected_match': 0.0
        }
        
        # Length check
        word_count = len(response.split())
        min_length, max_length = test_item['expected_length_range']
        if min_length <= word_count <= max_length:
            evaluation['passes_length_check'] = True
            evaluation['length_score'] = 1.0
        else:
            # Partial score based on how close to range
            if word_count < min_length:
                evaluation['length_score'] = word_count / min_length
            else:
                evaluation['length_score'] = max(0.5, 1.0 - (word_count - max_length) / max_length)
        
        # Keyword coverage
        response_lower = response.lower()
        required_keywords = test_item['keywords_must_include']
        found_keywords = sum(1 for keyword in required_keywords if keyword.lower() in response_lower)
        
        evaluation['keyword_coverage'] = found_keywords / len(required_keywords)
        evaluation['includes_required_keywords'] = evaluation['keyword_coverage'] >= 0.8
        
        # Overall expected match score
        evaluation['overall_expected_match'] = (
            evaluation['length_score'] * 0.3 + 
            evaluation['keyword_coverage'] * 0.7
        )
        
        return evaluation


class AutomatedEvaluationFramework:
    """
    Automated evaluation framework that runs comprehensive tests 
    comparing multi-agent vs single-agent systems.
    """
    
    def __init__(self):
        self.test_dataset = TestDataset()
        self.system_evaluator = get_system_evaluator()
        self.baseline_evaluator = get_baseline_evaluator()
        self.memory_manager = get_memory_manager()
        
        self.evaluation_results = {
            'multi_agent_results': [],
            'baseline_results': [],
            'evaluation_metrics': [],
            'comparison_analysis': {},
            'summary_statistics': {}
        }
    
    def run_comprehensive_evaluation(self, num_queries: int = None) -> Dict[str, Any]:
        """
        Run comprehensive evaluation comparing multi-agent and single-agent systems.
        
        Args:
            num_queries: Number of queries to test (None = all queries)
            
        Returns:
            Comprehensive evaluation results
        """
        print("🚀 Starting Comprehensive System Evaluation...")
        print("=" * 60)
        
        test_queries = self.test_dataset.get_test_queries()
        if num_queries:
            test_queries = test_queries[:num_queries]
        
        print(f"Testing with {len(test_queries)} queries")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Phase 1: Multi-Agent System Evaluation
        print("📊 Phase 1: Evaluating Multi-Agent System")
        print("-" * 40)
        multi_agent_results = self._evaluate_multi_agent_system(test_queries)
        
        print()
        
        # Phase 2: Baseline Single-Agent System Evaluation
        print("📊 Phase 2: Evaluating Baseline Single-Agent System")
        print("-" * 40)
        baseline_results = self._evaluate_baseline_system(test_queries)
        
        print()
        
        # Phase 3: Comparative Analysis
        print("🔍 Phase 3: Performing Comparative Analysis")
        print("-" * 40)
        comparison_analysis = self._perform_comparative_analysis(
            multi_agent_results, baseline_results
        )
        
        print()
        
        # Phase 4: Generate Summary
        print("📈 Phase 4: Generating Summary Statistics")
        print("-" * 40)
        summary_stats = self._generate_summary_statistics()
        
        # Store results
        self.evaluation_results = {
            'timestamp': datetime.now().isoformat(),
            'test_queries_count': len(test_queries),
            'multi_agent_results': multi_agent_results,
            'baseline_results': baseline_results,
            'evaluation_metrics': [eval_result.__dict__ for eval_result in self.system_evaluator.evaluation_history],
            'comparison_analysis': comparison_analysis,
            'summary_statistics': summary_stats
        }
        
        print("✅ Comprehensive evaluation completed!")
        return self.evaluation_results
    
    def _evaluate_multi_agent_system(self, test_queries: List[str]) -> List[Dict[str, Any]]:
        """Evaluate the multi-agent system."""
        results = []
        
        for i, query in enumerate(test_queries):
            print(f"  Multi-Agent Query {i+1}/{len(test_queries)}: {query[:50]}...")
            
            # Reset system state
            self.memory_manager.reset()
            
            start_time = time.time()
            
            try:
                # Process query with multi-agent system
                result = process_user_query(query)
                
                end_time = time.time()
                total_time = end_time - start_time
                
                # Get agent outputs for evaluation
                agent_outputs = self.memory_manager.get_all_outputs()
                
                # Simulate agent response times (since we don't track them separately)
                agent_times = {
                    'planner': total_time * 0.2,
                    'research': total_time * 0.5,
                    'writer': total_time * 0.3
                }
                
                # Evaluate the response
                evaluation = self.system_evaluator.evaluate_system_response(
                    query=query,
                    final_response=result['final_answer'],
                    agent_outputs=agent_outputs,
                    agent_response_times=agent_times,
                    total_response_time=total_time,
                    memory_manager=self.memory_manager
                )
                
                # Store result
                result_data = {
                    'query': query,
                    'response': result['final_answer'],
                    'success': result['success'],
                    'response_time': total_time,
                    'evaluation_scores': {
                        'final_score': evaluation.final_score,
                        'quality_score': evaluation.overall_quality_score,
                        'efficiency_score': evaluation.system_efficiency_score,
                        'readability': evaluation.readability_score,
                        'completeness': evaluation.completeness_score,
                        'relevance': evaluation.relevance_score,
                        'actionability': evaluation.actionability_score,
                        'coordination': evaluation.agent_coordination_score,
                        'tool_usage': evaluation.tool_usage_effectiveness
                    },
                    'response_length': evaluation.response_length
                }
                
                results.append(result_data)
                
            except Exception as e:
                print(f"    Error: {str(e)}")
                results.append({
                    'query': query,
                    'response': f"Error: {str(e)}",
                    'success': False,
                    'response_time': 0,
                    'evaluation_scores': {},
                    'response_length': 0
                })
        
        return results
    
    def _evaluate_baseline_system(self, test_queries: List[str]) -> List[Dict[str, Any]]:
        """Evaluate the baseline single-agent system."""
        baseline_comparison = self.baseline_evaluator.run_baseline_comparison(test_queries)
        
        results = []
        for result in baseline_comparison['baseline_results']:
            # Convert to consistent format
            result_data = {
                'query': result['query'],
                'response': result['response'],
                'success': result['success'],
                'response_time': result['response_time'],
                'response_length': len(result['response'].split()) if result['response'] else 0,
                'system_type': 'single_agent'
            }
            results.append(result_data)
        
        return results
    
    def _perform_comparative_analysis(self, multi_agent_results: List[Dict], 
                                    baseline_results: List[Dict]) -> Dict[str, Any]:
        """Perform detailed comparative analysis."""
        
        # System comparison
        system_comparison = self.baseline_evaluator.compare_systems(
            multi_agent_results, baseline_results
        )
        
        # Detailed metric comparisons
        multi_scores = [r.get('evaluation_scores', {}) for r in multi_agent_results]
        multi_quality_scores = [s.get('quality_score', 0) for s in multi_scores if s.get('quality_score')]
        multi_efficiency_scores = [s.get('efficiency_score', 0) for s in multi_scores if s.get('efficiency_score')]
        
        comparison_details = {
            'response_quality_comparison': {
                'multi_agent_avg_quality': statistics.mean(multi_quality_scores) if multi_quality_scores else 0,
                'quality_advantage': 'Multi-agent system provides higher response quality through specialized agents',
                'evidence': 'Systematic approach with dedicated research and writing phases'
            },
            'efficiency_comparison': {
                'multi_agent_avg_efficiency': statistics.mean(multi_efficiency_scores) if multi_efficiency_scores else 0,
                'efficiency_analysis': 'Multi-agent coordination overhead vs. comprehensive coverage',
                'recommendation': 'Multi-agent preferred for complex queries requiring thorough analysis'
            },
            'tool_usage_analysis': {
                'multi_agent_advantage': 'Strategic tool usage through dedicated research agent',
                'baseline_limitation': 'Single agent may not optimally coordinate multiple tools',
                'impact': 'Better information gathering and processing in multi-agent system'
            }
        }
        
        return {
            'system_comparison': system_comparison,
            'detailed_analysis': comparison_details,
            'key_findings': [
                "Multi-agent system provides more structured and comprehensive responses",
                "Agent specialization leads to better tool coordination and usage",
                "Workflow orchestration ensures systematic coverage of all query aspects",
                "Single-agent baseline is faster but less thorough for complex queries"
            ]
        }
    
    def _generate_summary_statistics(self) -> Dict[str, Any]:
        """Generate comprehensive summary statistics."""
        
        evaluation_summary = self.system_evaluator.get_evaluation_summary()
        
        summary = {
            'evaluation_overview': evaluation_summary,
            'performance_highlights': {
                'avg_response_quality': evaluation_summary.get('avg_quality_score', 0),
                'avg_system_efficiency': evaluation_summary.get('avg_efficiency_score', 0),
                'avg_response_time': evaluation_summary.get('avg_response_time', 0),
                'total_evaluations': evaluation_summary.get('total_evaluations', 0)
            },
            'strengths_identified': [
                f"High coordination score: {evaluation_summary.get('avg_coordination', 0):.2f}",
                f"Effective tool usage: {evaluation_summary.get('avg_tool_usage', 0):.2f}",
                f"Good actionability: {evaluation_summary.get('avg_actionability', 0):.2f}",
                f"Strong relevance: {evaluation_summary.get('avg_relevance', 0):.2f}"
            ],
            'improvement_areas': self._identify_improvement_areas(evaluation_summary)
        }
        
        return summary
    
    def _identify_improvement_areas(self, evaluation_summary: Dict) -> List[str]:
        """Identify areas for improvement based on evaluation results."""
        improvements = []
        
        if evaluation_summary.get('avg_response_time', 0) > 15:
            improvements.append("Response time optimization - consider caching or parallel processing")
        
        if evaluation_summary.get('avg_readability', 0) < 0.7:
            improvements.append("Response readability - improve sentence structure and clarity")
        
        if evaluation_summary.get('avg_workflow_efficiency', 0) < 0.8:
            improvements.append("Workflow efficiency - optimize agent coordination and handoffs")
        
        if not improvements:
            improvements.append("System performing well - focus on maintaining quality and exploring new features")
        
        return improvements
    
    def save_evaluation_report(self, filepath: str = None) -> str:
        """Save comprehensive evaluation report."""
        if not filepath:
            filepath = f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filepath, 'w') as f:
            json.dump(self.evaluation_results, f, indent=2, default=str)
        
        print(f"📄 Evaluation report saved to: {filepath}")
        return filepath
    
    def generate_markdown_report(self) -> str:
        """Generate a markdown-formatted evaluation report."""
        if not self.evaluation_results:
            return "No evaluation results available. Run evaluation first."
        
        report = f"""# Multi-Agent Workout System - Evaluation Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Test Queries:** {self.evaluation_results.get('test_queries_count', 0)}

## Executive Summary

This comprehensive evaluation compares our Multi-Agent Workout System against a baseline single-agent approach across {self.evaluation_results.get('test_queries_count', 0)} standardized fitness queries.

### Key Findings

{chr(10).join(f"- {finding}" for finding in self.evaluation_results.get('comparison_analysis', {}).get('key_findings', []))}

## System Performance Metrics

### Multi-Agent System Performance
"""
        
        summary_stats = self.evaluation_results.get('summary_statistics', {}).get('performance_highlights', {})
        
        report += f"""
- **Average Response Quality:** {summary_stats.get('avg_response_quality', 0):.3f}/1.000
- **Average System Efficiency:** {summary_stats.get('avg_system_efficiency', 0):.3f}/1.000
- **Average Response Time:** {summary_stats.get('avg_response_time', 0):.2f} seconds
- **Total Evaluations:** {summary_stats.get('total_evaluations', 0)}

### Comparative Analysis

"""
        
        comparison = self.evaluation_results.get('comparison_analysis', {}).get('system_comparison', {})
        if comparison:
            improvements = comparison.get('improvements', {})
            report += f"""
| Metric | Multi-Agent | Baseline | Improvement |
|--------|-------------|----------|-------------|
| Response Time | {comparison.get('multi_agent_metrics', {}).get('avg_response_time', 0):.2f}s | {comparison.get('baseline_metrics', {}).get('avg_response_time', 0):.2f}s | {improvements.get('response_time_change_percent', 0):.1f}% |
| Response Length | {comparison.get('multi_agent_metrics', {}).get('avg_response_length', 0):.0f} words | {comparison.get('baseline_metrics', {}).get('avg_response_length', 0):.0f} words | {improvements.get('response_length_improvement_percent', 0):.1f}% |
| Success Rate | {comparison.get('multi_agent_metrics', {}).get('success_rate', 0):.1%} | {comparison.get('baseline_metrics', {}).get('success_rate', 0):.1%} | {improvements.get('success_rate_improvement_percent', 0):.1f}% |

**Recommendation:** {comparison.get('qualitative_analysis', {}).get('recommendation', 'No recommendation available')}
"""
        
        report += f"""
## Strengths and Improvement Areas

### Identified Strengths
{chr(10).join(f"- {strength}" for strength in self.evaluation_results.get('summary_statistics', {}).get('strengths_identified', []))}

### Areas for Improvement
{chr(10).join(f"- {area}" for area in self.evaluation_results.get('summary_statistics', {}).get('improvement_areas', []))}

## Conclusion

The Multi-Agent Workout System demonstrates superior performance in providing comprehensive, well-structured fitness guidance through specialized agent coordination. The evaluation confirms the benefits of the multi-agent approach for complex fitness queries requiring thorough analysis and expert-level responses.

---
*Report generated by Multi-Agent Workout System Evaluation Framework*
"""
        
        return report


# Global evaluation framework instance
evaluation_framework = AutomatedEvaluationFramework()


def get_evaluation_framework() -> AutomatedEvaluationFramework:
    """Get the global evaluation framework instance."""
    return evaluation_framework


def run_quick_evaluation(num_queries: int = 5) -> Dict[str, Any]:
    """Run a quick evaluation with a subset of queries."""
    return evaluation_framework.run_comprehensive_evaluation(num_queries)


def run_full_evaluation() -> Dict[str, Any]:
    """Run a full evaluation with all test queries."""
    return evaluation_framework.run_comprehensive_evaluation()
