"""
Evaluation Dashboard for the Multi-Agent Workout System.
Provides comprehensive evaluation metrics, comparison analysis, and automated testing.
"""

import streamlit as st
import time
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any

# Import backend modules
import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.auto_evaluation import get_evaluation_framework, run_quick_evaluation, run_full_evaluation
from backend.evaluation import get_system_evaluator
from backend.baseline import get_baseline_evaluator
from backend.main import get_system_info

# Page configuration
st.set_page_config(
    page_title="Multi-Agent System Evaluation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for evaluation dashboard
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E88E5;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 0.5rem;
    }
    
    .evaluation-header {
        background: linear-gradient(90deg, #1E88E5, #1976D2);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .comparison-box {
        border: 2px solid #28a745;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f8fff9;
    }
    
    .score-excellent { color: #28a745; font-weight: bold; }
    .score-good { color: #17a2b8; font-weight: bold; }
    .score-fair { color: #ffc107; font-weight: bold; }
    .score-poor { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


def get_score_class(score: float) -> str:
    """Get CSS class based on score value."""
    if score >= 0.8:
        return "score-excellent"
    elif score >= 0.6:
        return "score-good"
    elif score >= 0.4:
        return "score-fair"
    else:
        return "score-poor"


def get_score_label(score: float) -> str:
    """Get human-readable label for score."""
    if score >= 0.8:
        return "Excellent"
    elif score >= 0.6:
        return "Good"
    elif score >= 0.4:
        return "Fair"
    else:
        return "Needs Improvement"


def display_metric_card(title: str, value: float, format_str: str = ":.3f"):
    """Display a metric card with score styling."""
    score_class = get_score_class(value)
    formatted_value = f"{value:{format_str}}"
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value {score_class}">{formatted_value}</div>
        <div class="metric-label">{title}</div>
        <div class="metric-label">{get_score_label(value)}</div>
    </div>
    """, unsafe_allow_html=True)


def display_evaluation_header():
    """Display the evaluation dashboard header."""
    st.markdown("""
    <div class="evaluation-header">
        <h1>📊 Multi-Agent System Evaluation Dashboard</h1>
        <p>Comprehensive analysis and comparison of system performance metrics</p>
    </div>
    """, unsafe_allow_html=True)


def display_current_system_metrics():
    """Display current system performance metrics."""
    st.header("📈 Current System Performance")
    
    # Get system evaluator
    system_evaluator = get_system_evaluator()
    evaluation_summary = system_evaluator.get_evaluation_summary()
    
    if evaluation_summary:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_metric_card(
                "Overall Quality Score",
                evaluation_summary.get('avg_quality_score', 0)
            )
        
        with col2:
            display_metric_card(
                "System Efficiency",
                evaluation_summary.get('avg_efficiency_score', 0)
            )
        
        with col3:
            display_metric_card(
                "Response Time (s)",
                evaluation_summary.get('avg_response_time', 0),
                ":.2f"
            )
        
        with col4:
            display_metric_card(
                "Total Evaluations",
                evaluation_summary.get('total_evaluations', 0),
                ":.0f"
            )
        
        # Detailed metrics
        st.subheader("Detailed Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Response Quality Metrics**")
            display_metric_card(
                "Readability",
                evaluation_summary.get('avg_readability', 0)
            )
            display_metric_card(
                "Completeness",
                evaluation_summary.get('avg_completeness', 0)
            )
        
        with col2:
            st.write("**Content Quality Metrics**")
            display_metric_card(
                "Relevance",
                evaluation_summary.get('avg_relevance', 0)
            )
            display_metric_card(
                "Actionability",
                evaluation_summary.get('avg_actionability', 0)
            )
        
        with col3:
            st.write("**System Coordination Metrics**")
            display_metric_card(
                "Agent Coordination",
                evaluation_summary.get('avg_coordination', 0)
            )
            display_metric_card(
                "Tool Usage Effectiveness",
                evaluation_summary.get('avg_tool_usage', 0)
            )
    
    else:
        st.info("No evaluation data available. Run some queries in the main interface or use automated evaluation below.")


def display_automated_evaluation_section():
    """Display automated evaluation controls and results."""
    st.header("🤖 Automated System Evaluation")
    
    st.write("""
    Run comprehensive automated evaluations to compare the multi-agent system 
    against a single-agent baseline across standardized test queries.
    """)
    
    # Evaluation controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quick Evaluation")
        st.write("Test 5 representative queries (faster)")
        
        if st.button("🚀 Run Quick Evaluation", type="secondary"):
            with st.spinner("Running quick evaluation..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Run evaluation with progress updates
                status_text.text("Initializing evaluation framework...")
                progress_bar.progress(10)
                
                status_text.text("Testing multi-agent system...")
                progress_bar.progress(30)
                
                results = run_quick_evaluation(5)
                
                status_text.text("Testing baseline system...")
                progress_bar.progress(60)
                
                status_text.text("Generating analysis...")
                progress_bar.progress(90)
                
                progress_bar.progress(100)
                status_text.text("Evaluation complete!")
                
                # Store results in session state
                st.session_state.evaluation_results = results
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                st.success("Quick evaluation completed! See results below.")
                st.rerun()
    
    with col2:
        st.subheader("Full Evaluation")
        st.write("Test all 10 standardized queries (comprehensive)")
        
        if st.button("📊 Run Full Evaluation", type="primary"):
            with st.spinner("Running comprehensive evaluation..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Run evaluation with progress updates
                status_text.text("Initializing comprehensive evaluation...")
                progress_bar.progress(5)
                
                status_text.text("Testing multi-agent system (10 queries)...")
                progress_bar.progress(25)
                
                results = run_full_evaluation()
                
                status_text.text("Testing baseline system...")
                progress_bar.progress(60)
                
                status_text.text("Performing comparative analysis...")
                progress_bar.progress(80)
                
                status_text.text("Generating detailed report...")
                progress_bar.progress(95)
                
                progress_bar.progress(100)
                status_text.text("Comprehensive evaluation complete!")
                
                # Store results in session state
                st.session_state.evaluation_results = results
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                st.success("Full evaluation completed! See detailed results below.")
                st.rerun()


def display_evaluation_results():
    """Display evaluation results if available."""
    if 'evaluation_results' not in st.session_state:
        return
    
    results = st.session_state.evaluation_results
    
    st.header("📋 Evaluation Results")
    
    # Summary statistics
    summary_stats = results.get('summary_statistics', {}).get('performance_highlights', {})
    if summary_stats:
        st.subheader("📊 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_metric_card(
                "Average Quality Score",
                summary_stats.get('avg_response_quality', 0)
            )
        
        with col2:
            display_metric_card(
                "Average Efficiency",
                summary_stats.get('avg_system_efficiency', 0)
            )
        
        with col3:
            display_metric_card(
                "Average Response Time",
                summary_stats.get('avg_response_time', 0),
                ":.2f"
            )
        
        with col4:
            display_metric_card(
                "Queries Tested",
                summary_stats.get('total_evaluations', 0),
                ":.0f"
            )
    
    # Comparative analysis
    comparison = results.get('comparison_analysis', {}).get('system_comparison', {})
    if comparison:
        st.subheader("⚖️ Multi-Agent vs Baseline Comparison")
        
        # Create comparison table
        comparison_data = {
            'Metric': ['Response Time (s)', 'Response Length (words)', 'Success Rate (%)'],
            'Multi-Agent System': [
                f"{comparison.get('multi_agent_metrics', {}).get('avg_response_time', 0):.2f}",
                f"{comparison.get('multi_agent_metrics', {}).get('avg_response_length', 0):.0f}",
                f"{comparison.get('multi_agent_metrics', {}).get('success_rate', 0):.1%}"
            ],
            'Baseline System': [
                f"{comparison.get('baseline_metrics', {}).get('avg_response_time', 0):.2f}",
                f"{comparison.get('baseline_metrics', {}).get('avg_response_length', 0):.0f}",
                f"{comparison.get('baseline_metrics', {}).get('success_rate', 0):.1%}"
            ],
            'Improvement': [
                f"{comparison.get('improvements', {}).get('response_time_change_percent', 0):.1f}%",
                f"{comparison.get('improvements', {}).get('response_length_improvement_percent', 0):.1f}%",
                f"{comparison.get('improvements', {}).get('success_rate_improvement_percent', 0):.1f}%"
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.table(comparison_df)
        
        # Recommendation
        recommendation = comparison.get('qualitative_analysis', {}).get('recommendation', '')
        if recommendation:
            st.markdown(f"""
            <div class="comparison-box">
                <strong>🎯 Recommendation:</strong><br>
                {recommendation}
            </div>
            """, unsafe_allow_html=True)
    
    # Key findings
    key_findings = results.get('comparison_analysis', {}).get('key_findings', [])
    if key_findings:
        st.subheader("🔍 Key Findings")
        for finding in key_findings:
            st.write(f"• {finding}")
    
    # Individual query results
    multi_agent_results = results.get('multi_agent_results', [])
    if multi_agent_results:
        st.subheader("📝 Individual Query Results")
        
        for i, result in enumerate(multi_agent_results[:5]):  # Show first 5 results
            with st.expander(f"Query {i+1}: {result.get('query', 'Unknown')[:50]}..."):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Query:**")
                    st.write(result.get('query', 'N/A'))
                    
                    st.write("**Success:**")
                    st.write("✅ Yes" if result.get('success') else "❌ No")
                    
                    st.write("**Response Time:**")
                    st.write(f"{result.get('response_time', 0):.2f} seconds")
                
                with col2:
                    evaluation_scores = result.get('evaluation_scores', {})
                    if evaluation_scores:
                        st.write("**Evaluation Scores:**")
                        
                        metrics = [
                            ('Final Score', 'final_score'),
                            ('Quality', 'quality_score'),
                            ('Relevance', 'relevance'),
                            ('Actionability', 'actionability')
                        ]
                        
                        for metric_name, metric_key in metrics:
                            score = evaluation_scores.get(metric_key, 0)
                            score_class = get_score_class(score)
                            st.markdown(f"**{metric_name}:** <span class='{score_class}'>{score:.3f}</span>", 
                                      unsafe_allow_html=True)


def display_export_section():
    """Display evaluation export options."""
    if 'evaluation_results' not in st.session_state:
        return
    
    st.header("📤 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Download JSON Report"):
            results_json = json.dumps(st.session_state.evaluation_results, indent=2, default=str)
            st.download_button(
                label="Download evaluation_results.json",
                data=results_json,
                file_name=f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📄 Generate Markdown Report"):
            evaluation_framework = get_evaluation_framework()
            evaluation_framework.evaluation_results = st.session_state.evaluation_results
            
            markdown_report = evaluation_framework.generate_markdown_report()
            
            st.download_button(
                label="Download evaluation_report.md",
                data=markdown_report,
                file_name=f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )


def display_sidebar():
    """Display evaluation dashboard sidebar."""
    st.sidebar.header("📊 Evaluation Controls")
    
    # System info
    system_info = get_system_info()
    system_status = system_info.get("system_status", {})
    
    st.sidebar.subheader("System Status")
    st.sidebar.write(f"**Session ID:** {system_status.get('session_id', 'Unknown')}")
    st.sidebar.write(f"**Agents Available:** {system_status.get('agents_available', 0)}")
    st.sidebar.write(f"**Tools Available:** {system_status.get('tools_available', 0)}")
    
    st.sidebar.divider()
    
    # Clear results
    if st.sidebar.button("🗑️ Clear Evaluation Results"):
        if 'evaluation_results' in st.session_state:
            del st.session_state.evaluation_results
        st.sidebar.success("Results cleared!")
        st.rerun()
    
    st.sidebar.divider()
    
    # Navigation
    st.sidebar.subheader("Navigation")
    if st.sidebar.button("🏠 Back to Main App"):
        st.switch_page("app.py")
    
    # Information
    st.sidebar.subheader("About Evaluation")
    st.sidebar.info("""
    This dashboard provides comprehensive evaluation of the multi-agent system including:
    
    • Response quality metrics
    • Agent coordination analysis
    • Performance comparisons
    • Automated testing framework
    """)


def main():
    """Main evaluation dashboard function."""
    try:
        # Display header
        display_evaluation_header()
        
        # Display sidebar
        display_sidebar()
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["Current Performance", "Automated Evaluation", "Export Results"])
        
        with tab1:
            display_current_system_metrics()
        
        with tab2:
            display_automated_evaluation_section()
            display_evaluation_results()
        
        with tab3:
            display_export_section()
        
        # Footer
        st.divider()
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
            Multi-Agent System Evaluation Dashboard | Advanced Performance Analytics<br>
            Built with comprehensive metrics and automated testing framework
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Dashboard Error: {str(e)}")
        st.write("**Error Details:**")
        st.code(str(e))
        
        if st.button("🔄 Refresh Dashboard"):
            st.rerun()


if __name__ == "__main__":
    main()
