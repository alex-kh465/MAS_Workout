#!/usr/bin/env python3
"""
Command-line evaluation script for the Multi-Agent Workout System.
Runs comprehensive evaluation and generates detailed reports.
"""

import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from backend.auto_evaluation import get_evaluation_framework, run_quick_evaluation, run_full_evaluation
from backend.evaluation import get_system_evaluator
from backend.baseline import get_baseline_evaluator


def run_evaluation_suite(evaluation_type: str = "quick", output_dir: str = None):
    """
    Run evaluation suite and generate reports.
    
    Args:
        evaluation_type: "quick" for 5 queries, "full" for all 10 queries
        output_dir: Directory to save reports (default: current directory)
    """
    print("🚀 Multi-Agent Workout System Evaluation Suite")
    print("=" * 60)
    print(f"Evaluation Type: {evaluation_type.title()}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Set output directory
    if not output_dir:
        output_dir = os.getcwd()
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Run evaluation
    if evaluation_type == "quick":
        print("Running quick evaluation (5 queries)...")
        results = run_quick_evaluation(5)
    else:
        print("Running full evaluation (10 queries)...")
        results = run_full_evaluation()
    
    print("✅ Evaluation completed!")
    print()
    
    # Generate reports
    print("📄 Generating reports...")
    
    # 1. JSON Report
    json_filename = f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    json_filepath = output_path / json_filename
    
    with open(json_filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"✓ JSON report saved: {json_filepath}")
    
    # 2. Markdown Report
    evaluation_framework = get_evaluation_framework()
    evaluation_framework.evaluation_results = results
    
    markdown_report = evaluation_framework.generate_markdown_report()
    
    md_filename = f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    md_filepath = output_path / md_filename
    
    with open(md_filepath, 'w') as f:
        f.write(markdown_report)
    
    print(f"✓ Markdown report saved: {md_filepath}")
    
    # 3. Summary Statistics
    summary_stats = results.get('summary_statistics', {})
    performance_highlights = summary_stats.get('performance_highlights', {})
    
    print()
    print("📊 Summary Statistics:")
    print("-" * 30)
    print(f"• Average Quality Score: {performance_highlights.get('avg_response_quality', 0):.3f}")
    print(f"• Average Efficiency Score: {performance_highlights.get('avg_system_efficiency', 0):.3f}")
    print(f"• Average Response Time: {performance_highlights.get('avg_response_time', 0):.2f}s")
    print(f"• Total Evaluations: {performance_highlights.get('total_evaluations', 0)}")
    
    # 4. Key Findings
    key_findings = results.get('comparison_analysis', {}).get('key_findings', [])
    if key_findings:
        print()
        print("🔍 Key Findings:")
        print("-" * 30)
        for finding in key_findings:
            print(f"• {finding}")
    
    # 5. Recommendation
    recommendation = (results.get('comparison_analysis', {})
                     .get('system_comparison', {})
                     .get('qualitative_analysis', {})
                     .get('recommendation', ''))
    
    if recommendation:
        print()
        print("🎯 Recommendation:")
        print("-" * 30)
        print(f"• {recommendation}")
    
    print()
    print("🎉 Evaluation suite completed successfully!")
    print(f"📁 Reports saved to: {output_path}")
    
    return results


def display_help():
    """Display help information."""
    help_text = """
🏋️‍♂️ Multi-Agent Workout System - Evaluation Suite

USAGE:
    python run_evaluation.py [OPTIONS]

OPTIONS:
    -t, --type TYPE        Evaluation type: "quick" (5 queries) or "full" (10 queries)
                          Default: quick
    
    -o, --output DIR       Output directory for reports
                          Default: current directory
    
    -h, --help            Show this help message

EXAMPLES:
    # Run quick evaluation
    python run_evaluation.py
    
    # Run full evaluation
    python run_evaluation.py --type full
    
    # Save reports to specific directory
    python run_evaluation.py --type full --output ./evaluation_reports

EVALUATION METRICS:
    • Response Quality (readability, completeness, relevance, actionability)
    • Agent Coordination (workflow efficiency, tool usage)
    • Performance (response time, memory usage)
    • Comparative Analysis (multi-agent vs single-agent baseline)

OUTPUT FILES:
    • evaluation_results_[timestamp].json  - Complete evaluation data
    • evaluation_report_[timestamp].md     - Human-readable markdown report
"""
    print(help_text)


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent Workout System Evaluation Suite",
        add_help=False  # We'll handle help manually
    )
    
    parser.add_argument(
        "-t", "--type",
        choices=["quick", "full"],
        default="quick",
        help="Evaluation type: quick (5 queries) or full (10 queries)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output directory for reports"
    )
    
    parser.add_argument(
        "-h", "--help",
        action="store_true",
        help="Show help message"
    )
    
    args = parser.parse_args()
    
    if args.help:
        display_help()
        return
    
    try:
        # Run evaluation
        results = run_evaluation_suite(
            evaluation_type=args.type,
            output_dir=args.output
        )
        
        # Exit successfully
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n❌ Evaluation interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Evaluation failed: {str(e)}")
        print("\nFor help, run: python run_evaluation.py --help")
        sys.exit(1)


if __name__ == "__main__":
    main()
