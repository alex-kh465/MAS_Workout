"""
Streamlit frontend for the Multi-Agent Workout System.
Interactive UI with input, run button, and step-by-step output display.
"""

import streamlit as st
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add the backend to the Python path
sys.path.append(os.path.dirname(__file__))

from backend.main import process_user_query, reset_system, get_system_info

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Workout System",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
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
        tab1, tab2 = st.tabs(["Main Interface", "Conversation History"])
        
        with tab1:
            process_query_ui()
        
        with tab2:
            display_conversation_history()
        
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
