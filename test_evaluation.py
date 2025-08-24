#!/usr/bin/env python3
"""
Test script to verify evaluation system integration.
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from backend.main import process_user_query
from backend.evaluation import get_system_evaluator
from backend.auto_evaluation import get_evaluation_framework
from backend.baseline import get_baseline_evaluator


def test_single_query_evaluation():
    """Test evaluation on a single query."""
    print("🧪 Testing Single Query Evaluation")
    print("=" * 50)
    
    test_query = "Create a beginner workout plan for someone who wants to start exercising"
    print(f"Test Query: {test_query}")
    print()
    
    # Process query with evaluation
    print("Processing query with multi-agent system...")
    result = process_user_query(test_query, enable_evaluation=True)
    
    if result['success']:
        print("✅ Query processed successfully!")
        print(f"Response length: {len(result['final_answer'])} characters")
        print(f"Response time: {result.get('response_time', 0):.2f} seconds")
        
        # Check evaluation metrics
        if 'evaluation_metrics' in result and 'error' not in result['evaluation_metrics']:
            metrics = result['evaluation_metrics']
            print()
            print("📊 Evaluation Metrics:")
            print(f"  • Final Score: {metrics.get('final_score', 0):.3f}")
            print(f"  • Quality Score: {metrics.get('quality_score', 0):.3f}")
            print(f"  • Efficiency Score: {metrics.get('efficiency_score', 0):.3f}")
            print(f"  • Readability: {metrics.get('readability_score', 0):.3f}")
            print(f"  • Completeness: {metrics.get('completeness_score', 0):.3f}")
            print(f"  • Relevance: {metrics.get('relevance_score', 0):.3f}")
            print(f"  • Actionability: {metrics.get('actionability_score', 0):.3f}")
        else:
            print("⚠️ No evaluation metrics available")
            if 'evaluation_metrics' in result:
                print(f"Error: {result['evaluation_metrics'].get('error', 'Unknown error')}")
    else:
        print("❌ Query processing failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    return result


def test_evaluation_system_components():
    """Test individual evaluation system components."""
    print("\n🔧 Testing Evaluation System Components")
    print("=" * 50)
    
    # Test system evaluator
    try:
        system_evaluator = get_system_evaluator()
        summary = system_evaluator.get_evaluation_summary()
        print(f"✅ System Evaluator: {type(system_evaluator).__name__}")
        print(f"   Evaluation history: {len(system_evaluator.evaluation_history)} entries")
        
        if summary:
            print(f"   Average final score: {summary.get('avg_final_score', 0):.3f}")
        else:
            print("   No evaluation history yet")
    except Exception as e:
        print(f"❌ System Evaluator Error: {str(e)}")
    
    # Test evaluation framework
    try:
        eval_framework = get_evaluation_framework()
        test_data = eval_framework.test_dataset.get_test_data()
        print(f"✅ Evaluation Framework: {type(eval_framework).__name__}")
        print(f"   Test dataset: {len(test_data)} queries available")
    except Exception as e:
        print(f"❌ Evaluation Framework Error: {str(e)}")
    
    # Test baseline evaluator
    try:
        baseline_evaluator = get_baseline_evaluator()
        print(f"✅ Baseline Evaluator: {type(baseline_evaluator).__name__}")
        print(f"   Single agent available: {type(baseline_evaluator.single_agent).__name__}")
    except Exception as e:
        print(f"❌ Baseline Evaluator Error: {str(e)}")


def main():
    """Main test function."""
    print("🏋️‍♂️ Multi-Agent Workout System - Evaluation System Test")
    print("=" * 70)
    print()
    
    # Test 1: Single query evaluation
    result = test_single_query_evaluation()
    
    # Test 2: System components
    test_evaluation_system_components()
    
    print()
    print("🎉 Evaluation system test completed!")
    print()
    print("💡 Next steps:")
    print("  1. Run 'streamlit run app.py' to use the interactive interface")
    print("  2. Check the 'Evaluation Dashboard' tab for metrics and automated testing")
    print("  3. Run 'python run_evaluation.py' for command-line evaluation")
    print()
    
    return result


if __name__ == "__main__":
    main()
