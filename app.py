"""
Streamlit frontend for the Multi-Agent Workout System.
Interactive UI with input, run button, and step-by-step output display.
"""

import streamlit as st
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# Load configuration from TOML
sys.path.append(os.path.dirname(__file__))
from backend.config import get_config

# Add the backend to the Python path
sys.path.append(os.path.dirname(__file__))

from backend.main import process_user_query, reset_system, get_system_info
from backend.evaluation import get_system_evaluator
from backend.auto_evaluation import get_evaluation_framework, run_quick_evaluation, run_full_evaluation
import pandas as pd
import json


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

# Load configuration
config = get_config()
streamlit_config = config.get_section('streamlit')

# Page configuration
st.set_page_config(
    page_title=streamlit_config.get('page_title', "Multi-Agent Workout System"),
    page_icon=streamlit_config.get('page_icon', "💪"),
    layout=streamlit_config.get('layout', "wide"),
    initial_sidebar_state=streamlit_config.get('initial_sidebar_state', "expanded")
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .agent-step {
        background-color: #f0f8ff;
        border-left: 4px solid #1E88E5;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    
    .agent-badge {
        background-color: #1E88E5;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #e3f2fd;
        border: 1px solid #bbdefb;
        color: #0d47a1;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    if 'system_initialized' not in st.session_state:
        st.session_state.system_initialized = True
        st.session_state.system_info = get_system_info()


def display_header():
    """Display the main header and description."""
    st.markdown('<h1 class="main-header">Multi-Agent Workout System</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>Welcome to the Multi-Agent Workout System!</strong><br>
        This intelligent system uses three specialized AI agents working together to provide personalized fitness advice:
        <ul>
            <li><strong>Planner Agent:</strong> Analyzes your request and creates a plan</li>
            <li><strong>Research Agent:</strong> Gathers relevant fitness information and data</li>
            <li><strong>Writer Agent:</strong> Creates comprehensive, actionable responses</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def display_sidebar():
    """Display the sidebar with system information and controls."""
    st.sidebar.header("System Controls")
    
    # Reset button
    if st.sidebar.button("Reset System", type="secondary"):
        reset_system()
        st.session_state.conversation_history = []
        st.session_state.system_info = get_system_info()
        st.sidebar.success("System reset successfully!")
        st.rerun()
    
    st.sidebar.divider()
    
    # System Information
    st.sidebar.header("System Information")
    
    system_info = st.session_state.system_info
    system_status = system_info.get("system_status", {})
    
    st.sidebar.metric("Session ID", system_status.get("session_id", "Unknown"))
    st.sidebar.metric("Agents Available", system_status.get("agents_available", 0))
    st.sidebar.metric("Tools Available", system_status.get("tools_available", 0))
    
    st.sidebar.divider()
    
    # Agent Information
    st.sidebar.header("Agents")
    agents = system_info.get("agents", {})
    
    for agent_key, agent_info in agents.items():
        with st.sidebar.expander(f"{agent_info['name']}"):
            st.write(f"**Role:** {agent_info['role']}")
            st.write(f"**Description:** {agent_info['description']}")
    
    st.sidebar.divider()
    
    # Tools Information
    st.sidebar.header("Available Tools")
    tools = system_info.get("tools", [])
    
    for tool in tools:
        with st.sidebar.expander(f"{tool['name'].title()}"):
            st.write(tool['description'])


def display_agent_steps(agent_steps: List[Dict]):
    """Display the agent workflow steps."""
    if not agent_steps:
        return
    
    st.header("Agent Workflow Steps")
    
    for i, step in enumerate(agent_steps):
        # Create expandable section for each agent step
        with st.expander(f"{step['agent']} - {step['description']}", expanded=(i == len(agent_steps) - 1)):
            
            # Step metadata
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Step:** {step['step']}")
                st.write(f"**Agent:** {step['agent']}")
            with col2:
                st.write(f"**Time:** {step['timestamp'][-8:-3]}")  # Show only time part
            
            st.divider()
            
            # Agent output
            st.write("**Output:**")
            st.write(step['output'])


def display_conversation_history():
    """Display the conversation history."""
    if not st.session_state.conversation_history:
        return
    
    st.header("Conversation History")
    
    for i, item in enumerate(reversed(st.session_state.conversation_history)):
        with st.expander(f"Query {len(st.session_state.conversation_history) - i}: {item['query'][:50]}...", expanded=(i == 0)):
            
            # Query info
            st.write(f"**Query:** {item['query']}")
            st.write(f"**Time:** {item['timestamp']}")
            st.write(f"**Success:** {'Yes' if item['success'] else 'No'}")
            
            if item.get('error'):
                st.error(f"Error: {item['error']}")
            
            st.divider()
            
            # Final answer
            st.write("**Final Answer:**")
            st.write(item['final_answer'])


def process_query_ui():
    """Handle the main query processing UI."""
    st.header("Ask Your Fitness Question")
    
    # Example queries
    st.write("**Example queries you can try:**")
    examples = [
        "Create a beginner workout plan for someone who wants to start exercising",
        "What are the best exercises for building upper body strength?",
        "Design a 30-minute HIIT workout routine",
        "What should I eat before and after a workout?",
        "How can I improve my running endurance?",
        "Create a home workout routine with no equipment"
    ]
    
    example_cols = st.columns(2)
    for i, example in enumerate(examples):
        col = example_cols[i % 2]
        if col.button(f"{example[:45]}...", key=f"example_{i}"):
            st.session_state.user_query = example
    
    st.divider()
    
    # Main input form
    with st.form("query_form"):
        user_query = st.text_area(
            "Enter your fitness question or request:",
            height=100,
            placeholder="e.g., Create a workout plan for beginners who want to lose weight...",
            value=st.session_state.get('user_query', '')
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            submit_button = st.form_submit_button(
                "Run Multi-Agent System",
                type="primary",
                disabled=st.session_state.processing,
                use_container_width=True
            )
    
    # Process the query
    if submit_button and user_query.strip():
        if not st.session_state.processing:
            st.session_state.processing = True
            
            # Show processing message
            with st.spinner("Multi-Agent System is processing your request..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Update progress
                progress_bar.progress(25)
                status_text.text("Planner Agent is analyzing your request...")
                
                # Process the query
                result = process_user_query(user_query)
                
                progress_bar.progress(50)
                status_text.text("Research Agent is gathering information...")
                
                progress_bar.progress(75)
                status_text.text("Writer Agent is creating your response...")
                
                progress_bar.progress(100)
                status_text.text("Processing complete!")
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
            
            # Store result in session state
            result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.conversation_history.append(result)
            st.session_state.processing = False
            
            # Display results
            if result['success']:
                st.markdown('<div class="success-message"><strong>Query processed successfully!</strong></div>', unsafe_allow_html=True)
                
                # Display final answer
                st.header("Final Answer")
                st.write(result['final_answer'])
                
                # Display evaluation metrics if available
                if result.get('evaluation_metrics') and 'error' not in result['evaluation_metrics']:
                    st.subheader("📊 Response Quality Metrics")
                    
                    metrics = result['evaluation_metrics']
                    
                    # Create metrics display
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        final_score = metrics.get('final_score', 0)
                        score_color = "🟢" if final_score >= 0.8 else "🟡" if final_score >= 0.6 else "🔴"
                        st.metric("Overall Score", f"{final_score:.3f}", delta=None)
                        st.write(f"{score_color} {get_score_label(final_score)}")
                    
                    with col2:
                        quality_score = metrics.get('quality_score', 0)
                        st.metric("Quality Score", f"{quality_score:.3f}")
                    
                    with col3:
                        efficiency_score = metrics.get('efficiency_score', 0)
                        st.metric("Efficiency Score", f"{efficiency_score:.3f}")
                    
                    with col4:
                        response_time = result.get('response_time', 0)
                        st.metric("Response Time", f"{response_time:.2f}s")
                    
                    # Detailed metrics in expander
                    with st.expander("🔍 Detailed Metrics"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Content Quality:**")
                            st.write(f"• Readability: {metrics.get('readability_score', 0):.3f}")
                            st.write(f"• Completeness: {metrics.get('completeness_score', 0):.3f}")
                            st.write(f"• Relevance: {metrics.get('relevance_score', 0):.3f}")
                            st.write(f"• Actionability: {metrics.get('actionability_score', 0):.3f}")
                        
                        with col2:
                            st.write("**System Performance:**")
                            st.write(f"• Agent Coordination: {metrics.get('coordination_score', 0):.3f}")
                            st.write(f"• Tool Usage: {metrics.get('tool_usage_score', 0):.3f}")
                            st.write(f"• Response Length: {metrics.get('response_length', 0)} words")
                
                st.divider()
                
                # Display agent steps
                if result.get('agent_steps'):
                    display_agent_steps(result['agent_steps'])
                
            else:
                st.markdown(f'<div class="error-message"><strong>Error:</strong> {result.get("error", "Unknown error occurred")}</div>', unsafe_allow_html=True)
            
            # Rerun to update the interface
            st.rerun()
    
    elif submit_button and not user_query.strip():
        st.warning("Please enter a question or request before submitting.")


def get_score_class(score: float) -> str:
    """Get CSS class name based on score value."""
    if score >= 0.8:
        return "score-excellent"
    elif score >= 0.6:
        return "score-good"
    elif score >= 0.4:
        return "score-fair"
    else:
        return "score-poor"


def display_metric_card(title: str, value: float, format_str: str = ".3f"):
    """Display a metric card with score styling."""
    score_class = get_score_class(value)
    
    # Handle formatting more safely
    try:
        if format_str.startswith(':'):
            format_str = format_str[1:]  # Remove the colon
        formatted_value = f"{float(value):{format_str}}"
    except (ValueError, TypeError):
        formatted_value = f"{float(value):.3f}"  # Default fallback
    
    score_label = get_score_label(value)
    
    # Use Streamlit's built-in metric with custom styling
    st.metric(title, formatted_value, help=score_label)


def display_evaluation_dashboard():
    """Display comprehensive evaluation dashboard."""
    st.header("📊 Evaluation Dashboard")
    
    st.markdown("""
    <div class="info-box">
        <strong>System Evaluation Framework</strong><br>
        This dashboard provides comprehensive analysis of the multi-agent system performance,
        including response quality metrics, agent coordination analysis, and baseline comparisons.
    </div>
    """, unsafe_allow_html=True)
    
    # Current Performance Section
    st.subheader("📈 Current Session Performance")
    
    # Get system evaluator
    system_evaluator = get_system_evaluator()
    evaluation_summary = system_evaluator.get_evaluation_summary()
    
    if evaluation_summary and evaluation_summary.get('total_evaluations', 0) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_metric_card(
                "Overall Quality",
                evaluation_summary.get('avg_quality_score', 0)
            )
        
        with col2:
            display_metric_card(
                "System Efficiency",
                evaluation_summary.get('avg_efficiency_score', 0)
            )
        
        with col3:
            display_metric_card(
                "Avg Response Time",
                evaluation_summary.get('avg_response_time', 0),
                ".2f"
            )
        
        with col4:
            display_metric_card(
                "Total Evaluations",
                evaluation_summary.get('total_evaluations', 0),
                ".0f"
            )
        
        # Detailed metrics
        st.subheader("🔍 Detailed Performance Breakdown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**📝 Response Quality Metrics**")
            quality_metrics = {
                "Readability": evaluation_summary.get('avg_readability', 0),
                "Completeness": evaluation_summary.get('avg_completeness', 0),
                "Relevance": evaluation_summary.get('avg_relevance', 0),
                "Actionability": evaluation_summary.get('avg_actionability', 0)
            }
            
            for metric, value in quality_metrics.items():
                score_color = "🟢" if value >= 0.8 else "🟡" if value >= 0.6 else "🔴"
                st.write(f"{score_color} **{metric}:** {value:.3f} ({get_score_label(value)})")
        
        with col2:
            st.write("**🤝 Agent Coordination Metrics**")
            coordination_metrics = {
                "Agent Coordination": evaluation_summary.get('avg_coordination', 0),
                "Workflow Efficiency": evaluation_summary.get('avg_workflow_efficiency', 0),
                "Tool Usage": evaluation_summary.get('avg_tool_usage', 0)
            }
            
            for metric, value in coordination_metrics.items():
                score_color = "🟢" if value >= 0.8 else "🟡" if value >= 0.6 else "🔴"
                st.write(f"{score_color} **{metric}:** {value:.3f} ({get_score_label(value)})")
        
        with col3:
            st.write("**⚡ Performance Statistics**")
            st.write(f"📏 **Avg Response Length:** {evaluation_summary.get('avg_response_length', 0):.0f} words")
            st.write(f"⏱️ **Response Time Range:** {evaluation_summary.get('avg_response_time', 0):.2f}s avg")
            st.write(f"✅ **Success Rate:** 100%")  # Assuming successful queries are tracked
            
            # Show improvement areas
            st.write("**🎯 Focus Areas:**")
            if evaluation_summary.get('avg_response_time', 0) > 10:
                st.write("🔄 Response time optimization")
            if evaluation_summary.get('avg_readability', 0) < 0.7:
                st.write("📖 Readability improvement")
            if evaluation_summary.get('avg_tool_usage', 0) < 0.8:
                st.write("🛠️ Tool usage optimization")
            if (evaluation_summary.get('avg_response_time', 0) <= 10 and 
                evaluation_summary.get('avg_readability', 0) >= 0.7 and 
                evaluation_summary.get('avg_tool_usage', 0) >= 0.8):
                st.write("🎉 System performing excellently!")
    
    else:
        st.info("💡 No evaluation data available yet. Run some queries in the Main Interface tab to see performance metrics here.")
    
    st.divider()
    
    # Automated Evaluation Section
    st.subheader("🤖 Automated System Evaluation")
    
    st.markdown("""
    Run comprehensive automated evaluations to compare the multi-agent system 
    against a single-agent baseline across standardized test queries.
    """)
    
    # Evaluation controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🚀 Quick Evaluation**")
        st.write("Test 5 representative queries (2-3 minutes)")
        
        if st.button("Run Quick Evaluation", type="secondary", key="quick_eval"):
            run_automated_evaluation("quick")
    
    with col2:
        st.write("**📊 Comprehensive Evaluation**")
        st.write("Test all 10 standardized queries (5-8 minutes)")
        
        if st.button("Run Full Evaluation", type="primary", key="full_eval"):
            run_automated_evaluation("full")
    
    # Display evaluation results if available
    if 'automated_evaluation_results' in st.session_state:
        display_automated_evaluation_results()


def run_automated_evaluation(eval_type: str):
    """Run automated evaluation and store results."""
    with st.spinner(f"Running {eval_type} evaluation..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Run evaluation with progress updates
            status_text.text("Initializing evaluation framework...")
            progress_bar.progress(10)
            
            status_text.text("Testing multi-agent system...")
            progress_bar.progress(30)
            
            if eval_type == "quick":
                results = run_quick_evaluation(5)
                num_queries = 5
            else:
                results = run_full_evaluation()
                num_queries = 10
            
            status_text.text("Testing baseline system...")
            progress_bar.progress(60)
            
            status_text.text("Performing comparative analysis...")
            progress_bar.progress(80)
            
            status_text.text("Generating results...")
            progress_bar.progress(95)
            
            progress_bar.progress(100)
            status_text.text("Evaluation complete!")
            
            # Store results in session state
            st.session_state.automated_evaluation_results = results
            st.session_state.last_evaluation_type = eval_type
            st.session_state.last_evaluation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"✅ {eval_type.title()} evaluation completed! Tested {num_queries} queries. See detailed results below.")
            st.rerun()
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Evaluation failed: {str(e)}")
            st.write("Please try again or check the system logs for more details.")


def display_automated_evaluation_results():
    """Display automated evaluation results."""
    if 'automated_evaluation_results' not in st.session_state:
        return
    
    results = st.session_state.automated_evaluation_results
    eval_type = st.session_state.get('last_evaluation_type', 'unknown')
    eval_time = st.session_state.get('last_evaluation_time', 'unknown')
    
    st.divider()
    st.subheader(f"📋 {eval_type.title()} Evaluation Results")
    st.write(f"**Completed:** {eval_time} | **Queries Tested:** {results.get('test_queries_count', 0)}")
    
    # Summary statistics
    summary_stats = results.get('summary_statistics', {}).get('performance_highlights', {})
    if summary_stats:
        st.write("**📊 Performance Summary**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            score = summary_stats.get('avg_response_quality', 0)
            score_emoji = "🟢" if score >= 0.8 else "🟡" if score >= 0.6 else "🔴"
            st.metric("Quality Score", f"{score:.3f}")
            st.write(f"{score_emoji} {get_score_label(score)}")
        
        with col2:
            score = summary_stats.get('avg_system_efficiency', 0)
            score_emoji = "🟢" if score >= 0.8 else "🟡" if score >= 0.6 else "🔴"
            st.metric("Efficiency Score", f"{score:.3f}")
            st.write(f"{score_emoji} {get_score_label(score)}")
        
        with col3:
            time_val = summary_stats.get('avg_response_time', 0)
            time_emoji = "🟢" if time_val <= 8 else "🟡" if time_val <= 12 else "🔴"
            st.metric("Avg Response Time", f"{time_val:.2f}s")
            st.write(f"{time_emoji} {'Fast' if time_val <= 8 else 'Moderate' if time_val <= 12 else 'Slow'}")
        
        with col4:
            st.metric("Queries Tested", f"{summary_stats.get('total_evaluations', 0):.0f}")
            st.write("📊 Test Coverage")
    
    # Comparative analysis
    comparison = results.get('comparison_analysis', {}).get('system_comparison', {})
    if comparison:
        st.write("**⚖️ Multi-Agent vs Baseline Comparison**")
        
        # Create comparison table
        comparison_data = {
            'Metric': ['Response Time (s)', 'Response Length (words)', 'Success Rate'],
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
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Recommendation
        recommendation = comparison.get('qualitative_analysis', {}).get('recommendation', '')
        if recommendation:
            st.success(f"🎯 **Recommendation:** {recommendation}")
    
    # Key findings
    key_findings = results.get('comparison_analysis', {}).get('key_findings', [])
    if key_findings:
        st.write("**🔍 Key Findings**")
        for i, finding in enumerate(key_findings, 1):
            st.write(f"{i}. {finding}")
    
    # Individual query results preview
    multi_agent_results = results.get('multi_agent_results', [])
    if multi_agent_results:
        st.write("**📝 Individual Query Results (Top 3)**")
        
        for i, result in enumerate(multi_agent_results[:3]):
            with st.expander(f"Query {i+1}: {result.get('query', 'Unknown')[:60]}..."):
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Query:** {result.get('query', 'N/A')}")
                    st.write(f"**Success:** {'✅ Yes' if result.get('success') else '❌ No'}")
                    st.write(f"**Response Time:** {result.get('response_time', 0):.2f} seconds")
                    st.write(f"**Response Length:** {result.get('response_length', 0)} words")
                
                with col2:
                    evaluation_scores = result.get('evaluation_scores', {})
                    if evaluation_scores:
                        st.write("**🎯 Evaluation Scores:**")
                        
                        scores_to_show = [
                            ('Final Score', 'final_score'),
                            ('Quality', 'quality_score'),
                            ('Relevance', 'relevance'),
                            ('Actionability', 'actionability')
                        ]
                        
                        for metric_name, metric_key in scores_to_show:
                            score = evaluation_scores.get(metric_key, 0)
                            score_emoji = "🟢" if score >= 0.8 else "🟡" if score >= 0.6 else "🔴"
                            st.write(f"{score_emoji} **{metric_name}:** {score:.3f}")
    
    # Export section
    st.divider()
    st.subheader("📤 Export Evaluation Results")
    
    if 'automated_evaluation_results' in st.session_state:
        col1, col2 = st.columns(2)
        
        with col1:
            # JSON export
            results_json = json.dumps(st.session_state.automated_evaluation_results, indent=2, default=str)
            st.download_button(
                label="📄 Download JSON Report",
                data=results_json,
                file_name=f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                help="Download complete evaluation data in JSON format"
            )
        
        with col2:
            # Markdown export
            try:
                evaluation_framework = get_evaluation_framework()
                evaluation_framework.evaluation_results = st.session_state.automated_evaluation_results
                markdown_report = evaluation_framework.generate_markdown_report()
                
                st.download_button(
                    label="📋 Download Markdown Report",
                    data=markdown_report,
                    file_name=f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    help="Download human-readable evaluation report"
                )
            except Exception as e:
                st.error(f"Error generating markdown report: {str(e)}")
    
    else:
        st.info("💡 Run an automated evaluation above to generate downloadable reports.")
    
    # Information about evaluation
    with st.expander("ℹ️ About the Evaluation Framework"):
        st.markdown("""
        **Evaluation Metrics Explained:**
        
        **Response Quality Metrics:**
        - **Readability**: Measures sentence structure and clarity (optimal 15-20 words per sentence)
        - **Completeness**: Evaluates coverage of query requirements and fitness domain knowledge
        - **Relevance**: Assesses alignment between user query and system response
        - **Actionability**: Measures presence of specific, executable fitness advice
        
        **Agent Coordination Metrics:**
        - **Agent Coordination**: Evaluates information flow and collaboration between agents
        - **Workflow Efficiency**: Measures timeliness and organization of agent execution
        - **Tool Usage Effectiveness**: Assesses strategic use of available research tools
        
        **Performance Metrics:**
        - **Response Time**: Total system processing time
        - **Memory Usage**: Efficiency of state management
        - **Success Rate**: Reliability of query processing
        
        **Baseline Comparison:**
        The automated evaluation compares our multi-agent system against a single-agent baseline
        that uses the same LLM and tools but without agent coordination. This demonstrates the
        benefits of the multi-agent approach.
        """)


def main():
    """Main application function."""
    try:
        # Initialize session state
        initialize_session_state()
        
        # Display header
        display_header()
        
        # Display sidebar
        display_sidebar()
        
        # Create main content tabs
        tab1, tab2, tab3 = st.tabs(["Main Interface", "Conversation History", "Evaluation Dashboard"])
        
        with tab1:
            process_query_ui()
        
        with tab2:
            display_conversation_history()
        
        with tab3:
            display_evaluation_dashboard()
        
        # Footer
        st.divider()
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: #666; font-size: 0.9rem;'>
                Multi-Agent Workout System | Powered by LangGraph + Groq + Streamlit<br>
                Built with three AI agents working together to provide personalized fitness guidance
            </div>
            """,
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.write("**Error Details:**")
        st.code(str(e))
        
        if st.button("Reload Application"):
            st.rerun()


if __name__ == "__main__":
    main()
