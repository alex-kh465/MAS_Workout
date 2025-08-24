import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_system_architecture():
    """Generate System Architecture Overview diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Define colors
    agent_color = '#e3f2fd'
    tool_color = '#e8f5e8'
    ui_color = '#fff3e0'
    backend_color = '#f3e5f5'
    
    # User and UI Layer (Top)
    user_box = FancyBboxPatch((1, 8.5), 2, 1, boxstyle="round,pad=0.1", 
                              facecolor='#ffecb3', edgecolor='black', linewidth=2)
    ax.add_patch(user_box)
    ax.text(2, 9, '👤 User', ha='center', va='center', fontsize=12, fontweight='bold')
    
    ui_box = FancyBboxPatch((5, 8.5), 4, 1, boxstyle="round,pad=0.1",
                            facecolor=ui_color, edgecolor='black', linewidth=2)
    ax.add_patch(ui_box)
    ax.text(7, 9, '🖥️ Streamlit Interface\n• Query Input • Response Display\n• Evaluation Dashboard', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Multi-Agent System Core (Middle)
    # LangGraph State Management
    state_box = FancyBboxPatch((2, 6.5), 8, 1, boxstyle="round,pad=0.1",
                               facecolor='#e1f5fe', edgecolor='#01579b', linewidth=2)
    ax.add_patch(state_box)
    ax.text(6, 7, '📊 LangGraph State Management\n• Agent Coordination • Memory Buffers • Workflow Orchestration',
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Three Agents
    planner_box = FancyBboxPatch((1, 4.5), 3, 1.5, boxstyle="round,pad=0.1",
                                 facecolor=agent_color, edgecolor='#01579b', linewidth=2)
    ax.add_patch(planner_box)
    ax.text(2.5, 5.25, '🧠 Planner Agent\n• Query Analysis\n• Task Decomposition\n• Workflow Planning',
            ha='center', va='center', fontsize=9, fontweight='bold')
    
    research_box = FancyBboxPatch((4.5, 4.5), 3, 1.5, boxstyle="round,pad=0.1",
                                  facecolor=agent_color, edgecolor='#01579b', linewidth=2)
    ax.add_patch(research_box)
    ax.text(6, 5.25, '🔍 Research Agent\n• Tool Coordination\n• Information Synthesis\n• Data Validation',
            ha='center', va='center', fontsize=9, fontweight='bold')
    
    writer_box = FancyBboxPatch((8, 4.5), 3, 1.5, boxstyle="round,pad=0.1",
                                facecolor=agent_color, edgecolor='#01579b', linewidth=2)
    ax.add_patch(writer_box)
    ax.text(9.5, 5.25, '✍️ Writer Agent\n• Content Organization\n• Response Generation\n• User Adaptation',
            ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Tools Layer (Lower Middle)
    fitness_tool = FancyBboxPatch((1, 2.5), 3, 1.2, boxstyle="round,pad=0.1",
                                  facecolor=tool_color, edgecolor='#2e7d32', linewidth=2)
    ax.add_patch(fitness_tool)
    ax.text(2.5, 3.1, '🏋️ Fitness Research Tool\n• Exercise Database\n• Training Principles\n• Safety Guidelines',
            ha='center', va='center', fontsize=9, fontweight='bold')
    
    nutrition_tool = FancyBboxPatch((4.5, 2.5), 3, 1.2, boxstyle="round,pad=0.1",
                                    facecolor=tool_color, edgecolor='#2e7d32', linewidth=2)
    ax.add_patch(nutrition_tool)
    ax.text(6, 3.1, '🥗 Nutritional Calculator\n• Calorie Calculations\n• Macro Planning\n• Meal Timing',
            ha='center', va='center', fontsize=9, fontweight='bold')
    
    web_tool = FancyBboxPatch((8, 2.5), 3, 1.2, boxstyle="round,pad=0.1",
                              facecolor=tool_color, edgecolor='#2e7d32', linewidth=2)
    ax.add_patch(web_tool)
    ax.text(9.5, 3.1, '🌐 Web Search Tool\n• Current Research\n• Best Practices\n• Trend Analysis',
            ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Backend Services (Bottom)
    groq_box = FancyBboxPatch((2, 0.5), 4, 1.2, boxstyle="round,pad=0.1",
                              facecolor=backend_color, edgecolor='#6a1b9a', linewidth=2)
    ax.add_patch(groq_box)
    ax.text(4, 1.1, '⚡ Groq API\nMixtral-8x7b-32768\n• Fast Inference\n• Model Selection',
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    eval_box = FancyBboxPatch((7, 0.5), 4, 1.2, boxstyle="round,pad=0.1",
                              facecolor='#fce4ec', edgecolor='#c2185b', linewidth=2)
    ax.add_patch(eval_box)
    ax.text(9, 1.1, '📈 Evaluation Framework\n• Quality Metrics\n• Coordination Analysis\n• Performance Monitoring',
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Arrows - Data Flow
    # User to UI
    ax.arrow(3, 9, 1.8, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
    
    # UI to State Management
    ax.arrow(7, 8.5, 0, -0.8, head_width=0.1, head_length=0.1, fc='black', ec='black')
    
    # State to Agents
    ax.arrow(4.5, 6.5, -1.8, -0.8, head_width=0.1, head_length=0.1, fc='#01579b', ec='#01579b')
    ax.arrow(6, 6.5, 0, -0.8, head_width=0.1, head_length=0.1, fc='#01579b', ec='#01579b')
    ax.arrow(7.5, 6.5, 1.8, -0.8, head_width=0.1, head_length=0.1, fc='#01579b', ec='#01579b')
    
    # Agents to Tools
    ax.arrow(2.5, 4.5, 0, -0.6, head_width=0.1, head_length=0.1, fc='#2e7d32', ec='#2e7d32')
    ax.arrow(6, 4.5, 0, -0.6, head_width=0.1, head_length=0.1, fc='#2e7d32', ec='#2e7d32')
    ax.arrow(9.5, 4.5, 0, -0.6, head_width=0.1, head_length=0.1, fc='#2e7d32', ec='#2e7d32')
    
    # Agents to Backend (dashed lines)
    ax.plot([2.5, 4], [4.5, 1.7], '--', color='#6a1b9a', linewidth=2, alpha=0.7)
    ax.plot([6, 4], [4.5, 1.7], '--', color='#6a1b9a', linewidth=2, alpha=0.7)
    ax.plot([9.5, 4], [4.5, 1.7], '--', color='#6a1b9a', linewidth=2, alpha=0.7)
    
    # Agents to Evaluation (dashed lines)
    ax.plot([2.5, 9], [4.5, 1.7], '--', color='#c2185b', linewidth=2, alpha=0.7)
    ax.plot([6, 9], [4.5, 1.7], '--', color='#c2185b', linewidth=2, alpha=0.7)
    ax.plot([9.5, 9], [4.5, 1.7], '--', color='#c2185b', linewidth=2, alpha=0.7)
    
    # Set limits and remove axes
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Title
    plt.title('Multi-Agent Workout System - Architecture Overview', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Save
    plt.tight_layout()
    plt.savefig('diagrams/system_architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ System architecture diagram saved: diagrams/system_architecture.png")

def create_workflow_diagram():
    """Generate Agent Coordination Workflow diagram"""
    fig, ax = plt.subplots(figsize=(12, 14))
    
    # Define positions for workflow steps
    steps = [
        ("👤 User Query", 6, 13, '#ffecb3'),
        ("🖥️ Streamlit UI", 6, 12, '#fff3e0'),
        ("🧠 Planner Agent\nAnalysis", 6, 10.5, '#e3f2fd'),
        ("📊 LangGraph State\nUpdate", 6, 9, '#e1f5fe'),
        ("🔍 Research Agent\nCoordination", 6, 7.5, '#e3f2fd'),
        ("🛠️ Tool Execution\n(Parallel)", 6, 6, '#e8f5e8'),
        ("📊 Information\nSynthesis", 6, 4.5, '#e3f2fd'),
        ("✍️ Writer Agent\nGeneration", 6, 3, '#e3f2fd'),
        ("📈 Evaluation\nProcessing", 6, 1.5, '#fce4ec'),
        ("👤 Final Response", 6, 0, '#ffecb3')
    ]
    
    # Draw workflow steps
    for i, (label, x, y, color) in enumerate(steps):
        box = FancyBboxPatch((x-1.5, y-0.4), 3, 0.8, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Add arrows between steps
        if i < len(steps) - 1:
            ax.arrow(x, y-0.4, 0, -0.7, head_width=0.2, head_length=0.1, 
                     fc='black', ec='black', linewidth=2)
    
    # Add side processes
    # Tool details (right side)
    tools = [
        ("🏋️ Fitness Research", 10, 6.5, '#e8f5e8'),
        ("🥗 Nutrition Calculator", 10, 6, '#e8f5e8'),
        ("🌐 Web Search", 10, 5.5, '#e8f5e8')
    ]
    
    for tool, x, y, color in tools:
        tool_box = FancyBboxPatch((x-1, y-0.2), 2, 0.4, boxstyle="round,pad=0.05",
                                  facecolor=color, edgecolor='#2e7d32', linewidth=1)
        ax.add_patch(tool_box)
        ax.text(x, y, tool, ha='center', va='center', fontsize=9, fontweight='bold')
        
        # Connect to main workflow
        ax.arrow(7.5, 6, 1.3, y-6, head_width=0.1, head_length=0.05, 
                 fc='#2e7d32', ec='#2e7d32', linewidth=1, alpha=0.7)
    
    # Add decision points and feedback loops
    decision_points = [
        ("Query Analysis\nComplexity Check", 2, 10.5),
        ("Information\nSufficiency Check", 2, 4.5),
        ("Quality\nValidation", 10, 1.5)
    ]
    
    for label, x, y in decision_points:
        decision_box = FancyBboxPatch((x-0.8, y-0.3), 1.6, 0.6, boxstyle="round,pad=0.05",
                                      facecolor='#ffffcc', edgecolor='orange', linewidth=1)
        ax.add_patch(decision_box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Add feedback arrows
    ax.arrow(4.5, 4.5, -1.5, 0, head_width=0.1, head_length=0.1, 
             fc='orange', ec='orange', linewidth=1, alpha=0.7, linestyle='--')
    ax.arrow(8.5, 1.5, 1.3, 0, head_width=0.1, head_length=0.1, 
             fc='orange', ec='orange', linewidth=1, alpha=0.7, linestyle='--')
    
    # Set limits and formatting
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.5, 14)
    ax.axis('off')
    
    plt.title('Multi-Agent Workout System - Architecture Overview', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Save
    plt.tight_layout()
    plt.savefig('diagrams/system_architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ System architecture diagram saved")

def create_coordination_workflow():
    """Generate Agent Coordination Workflow diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create timeline with phases
    phases = [
        ("Query Processing", 0.5, 8.5, 2.5, '#e3f2fd'),
        ("Research & Tool Coordination", 3.5, 8.5, 4, '#e8f5e8'),
        ("Response Generation", 8, 8.5, 2.5, '#fff3e0'),
        ("Evaluation & Feedback", 11, 8.5, 2, '#fce4ec')
    ]
    
    for phase, x, y, width, color in phases:
        phase_box = FancyBboxPatch((x, y), width, 0.8, boxstyle="round,pad=0.1",
                                   facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(phase_box)
        ax.text(x + width/2, y + 0.4, phase, ha='center', va='center', 
                fontsize=11, fontweight='bold')
    
    # Detailed workflow steps
    workflow_steps = [
        ("1. User submits\nfitness query", 1.5, 7.5),
        ("2. Planner analyzes\nquery complexity", 1.5, 6.5),
        ("3. Research plan\ncreated", 1.5, 5.5),
        ("4. Tools coordinated\nin parallel", 5.5, 7),
        ("🏋️ Fitness DB", 4, 6),
        ("🥗 Nutrition Calc", 5.5, 6),
        ("🌐 Web Search", 7, 6),
        ("5. Information\nsynthesized", 5.5, 4.5),
        ("6. Writer organizes\ncontent", 9, 7),
        ("7. Response\ngenerated", 9, 5.5),
        ("8. Quality metrics\ncalculated", 12, 7),
        ("9. Final response\nwith evaluation", 12, 5.5)
    ]
    
    for i, (step, x, y) in enumerate(workflow_steps):
        if i < 3 or i == 7 or i == 8:  # Main workflow steps
            color = '#ffffff'
            edge_color = '#1976d2'
        elif 4 <= i <= 6:  # Tools
            color = '#e8f5e8'
            edge_color = '#2e7d32'
        else:  # Other steps
            color = '#f5f5f5'
            edge_color = '#666666'
            
        step_box = FancyBboxPatch((x-0.8, y-0.4), 1.6, 0.8, boxstyle="round,pad=0.05",
                                  facecolor=color, edgecolor=edge_color, linewidth=1)
        ax.add_patch(step_box)
        ax.text(x, y, step, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Add flow arrows
    flow_arrows = [
        (1.5, 7.1, 0, -0.4),  # 1 to 2
        (1.5, 6.1, 0, -0.4),  # 2 to 3
        (2.3, 5.5, 2.4, 1.3),  # 3 to 4
        (5.5, 6.6, 0, -1.7),   # 4 to 5
        (6.3, 4.5, 2, 2.3),    # 5 to 6
        (9, 6.6, 0, -0.7),     # 6 to 7
        (9.8, 5.5, 1.4, 1.3),  # 7 to 8
        (12, 6.6, 0, -0.7)     # 8 to 9
    ]
    
    for x, y, dx, dy in flow_arrows:
        ax.arrow(x, y, dx, dy, head_width=0.15, head_length=0.1, 
                 fc='#1976d2', ec='#1976d2', linewidth=2)
    
    # Tool coordination arrows
    for tool_x in [4, 5.5, 7]:
        ax.arrow(5.5, 6.6, tool_x-5.5, -0.4, head_width=0.1, head_length=0.05, 
                 fc='#2e7d32', ec='#2e7d32', linewidth=1.5)
        ax.arrow(tool_x, 5.6, 5.5-tool_x, -0.9, head_width=0.1, head_length=0.05, 
                 fc='#2e7d32', ec='#2e7d32', linewidth=1.5)
    
    # Set limits and formatting
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    plt.title('Agent Coordination Workflow', fontsize=16, fontweight='bold', pad=20)
    
    # Save
    plt.tight_layout()
    plt.savefig('diagrams/coordination_workflow.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Coordination workflow diagram saved")

def create_evaluation_framework():
    """Generate Evaluation Framework Overview diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Input layer
    dataset_box = FancyBboxPatch((5, 8.5), 4, 1, boxstyle="round,pad=0.1",
                                 facecolor='#e8f5e8', edgecolor='#2e7d32', linewidth=2)
    ax.add_patch(dataset_box)
    ax.text(7, 9, '📋 Test Dataset\n10 Standardized Fitness Queries', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Processing layer - parallel systems
    multi_agent_box = FancyBboxPatch((2, 6.5), 3.5, 1.5, boxstyle="round,pad=0.1",
                                     facecolor='#e3f2fd', edgecolor='#01579b', linewidth=2)
    ax.add_patch(multi_agent_box)
    ax.text(3.75, 7.25, '🤝 Multi-Agent System\n• Planner Agent\n• Research Agent\n• Writer Agent', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    baseline_box = FancyBboxPatch((8.5, 6.5), 3.5, 1.5, boxstyle="round,pad=0.1",
                                  facecolor='#fff3e0', edgecolor='#ef6c00', linewidth=2)
    ax.add_patch(baseline_box)
    ax.text(10.25, 7.25, '🔄 Single-Agent Baseline\n• Unified Prompt\n• Direct Tool Access\n• Single-stage Generation', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Evaluation components
    eval_components = [
        ("📊 Response Quality\nEvaluator", 2, 4.5, '#fff3e0'),
        ("🔗 Agent Coordination\nAnalyzer", 7, 4.5, '#fff3e0'),
        ("⚡ Performance\nMonitor", 12, 4.5, '#fff3e0')
    ]
    
    for label, x, y, color in eval_components:
        eval_box = FancyBboxPatch((x-1.2, y-0.6), 2.4, 1.2, boxstyle="round,pad=0.1",
                                  facecolor=color, edgecolor='#ef6c00', linewidth=2)
        ax.add_patch(eval_box)
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Analysis layer
    analysis_box = FancyBboxPatch((5, 2.5), 4, 1, boxstyle="round,pad=0.1",
                                  facecolor='#f3e5f5', edgecolor='#6a1b9a', linewidth=2)
    ax.add_patch(analysis_box)
    ax.text(7, 3, '📈 Comparative Analysis\n• Statistical Testing\n• Improvement Calculation', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Output layer
    outputs = [
        ("📄 JSON Reports", 2, 0.5, '#fce4ec'),
        ("📝 Markdown Reports", 7, 0.5, '#fce4ec'),
        ("🖥️ Dashboard Display", 12, 0.5, '#fce4ec')
    ]
    
    for label, x, y, color in outputs:
        output_box = FancyBboxPatch((x-1.2, y-0.3), 2.4, 0.6, boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor='#c2185b', linewidth=2)
        ax.add_patch(output_box)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Add flow arrows
    # Dataset to systems
    ax.arrow(6, 8.5, -2, -1.8, head_width=0.2, head_length=0.1, fc='black', ec='black', linewidth=2)
    ax.arrow(8, 8.5, 2, -1.8, head_width=0.2, head_length=0.1, fc='black', ec='black', linewidth=2)
    
    # Systems to evaluation
    ax.arrow(3.75, 6.5, -1.5, -1.7, head_width=0.15, head_length=0.1, fc='#ef6c00', ec='#ef6c00', linewidth=1.5)
    ax.arrow(5.5, 6.5, 1.3, -1.7, head_width=0.15, head_length=0.1, fc='#ef6c00', ec='#ef6c00', linewidth=1.5)
    ax.arrow(10.25, 6.5, 1.5, -1.7, head_width=0.15, head_length=0.1, fc='#ef6c00', ec='#ef6c00', linewidth=1.5)
    
    # Evaluation to analysis
    ax.arrow(2, 3.9, 2.8, -1.2, head_width=0.15, head_length=0.1, fc='#6a1b9a', ec='#6a1b9a', linewidth=1.5)
    ax.arrow(7, 3.9, 0, -0.6, head_width=0.15, head_length=0.1, fc='#6a1b9a', ec='#6a1b9a', linewidth=1.5)
    ax.arrow(12, 3.9, -2.8, -1.2, head_width=0.15, head_length=0.1, fc='#6a1b9a', ec='#6a1b9a', linewidth=1.5)
    
    # Analysis to outputs
    ax.arrow(5.5, 2.5, -3.2, -1.8, head_width=0.15, head_length=0.1, fc='#c2185b', ec='#c2185b', linewidth=1.5)
    ax.arrow(7, 2.5, 0, -1.8, head_width=0.15, head_length=0.1, fc='#c2185b', ec='#c2185b', linewidth=1.5)
    ax.arrow(8.5, 2.5, 3.2, -1.8, head_width=0.15, head_length=0.1, fc='#c2185b', ec='#c2185b', linewidth=1.5)
    
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    plt.title('Evaluation Framework Overview', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('diagrams/evaluation_framework.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Evaluation framework diagram saved")

def create_technical_implementation():
    """Generate Technical Implementation Architecture diagram"""
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Layer definitions
    layers = [
        ("Frontend Layer", 1, 10, 12, 1.5, '#e3f2fd'),
        ("Application Layer", 1, 7.5, 12, 2, '#e8f5e8'),
        ("Integration Layer", 1, 5, 12, 1.5, '#fff3e0'),
        ("Backend Services", 1, 2, 12, 2.5, '#f3e5f5')
    ]
    
    for layer_name, x, y, width, height, color in layers:
        layer_box = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.1",
                                   facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.3)
        ax.add_patch(layer_box)
        ax.text(x + 0.5, y + height - 0.3, layer_name, ha='left', va='top', 
                fontsize=12, fontweight='bold')
    
    # Frontend components
    frontend_components = [
        ("🖥️ Streamlit UI", 2, 10.7, 3),
        ("📊 Dashboard", 6, 10.7, 2.5),
        ("📈 Live Metrics", 9.5, 10.7, 2.5)
    ]
    
    for comp, x, y, width in frontend_components:
        comp_box = FancyBboxPatch((x, y), width, 0.6, boxstyle="round,pad=0.05",
                                  facecolor='#bbdefb', edgecolor='#1976d2', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x + width/2, y + 0.3, comp, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Application components
    app_components = [
        ("🧠 Planner", 2, 8.7, 2),
        ("🔍 Research", 4.5, 8.7, 2),
        ("✍️ Writer", 7, 8.7, 2),
        ("📊 LangGraph", 9.5, 8.7, 2.5),
        ("💾 Memory Mgmt", 2, 8, 3),
        ("📈 Evaluation", 6, 8, 3),
        ("🔧 Config", 10, 8, 2)
    ]
    
    for comp, x, y, width in app_components:
        comp_box = FancyBboxPatch((x, y), width, 0.6, boxstyle="round,pad=0.05",
                                  facecolor='#c8e6c8', edgecolor='#388e3c', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x + width/2, y + 0.3, comp, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Integration components
    integration_components = [
        ("🔗 LangChain Tools", 2, 5.7, 3),
        ("🌐 API Connectors", 6, 5.7, 3),
        ("📊 State Management", 10, 5.7, 2.5)
    ]
    
    for comp, x, y, width in integration_components:
        comp_box = FancyBboxPatch((x, y), width, 0.6, boxstyle="round,pad=0.05",
                                  facecolor='#ffcc02', edgecolor='#f57c00', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x + width/2, y + 0.3, comp, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Backend components
    backend_components = [
        ("⚡ Groq API\nMixtral-8x7b", 2, 3.5, 3),
        ("🏋️ Fitness Tool", 6, 3.5, 2),
        ("🥗 Nutrition Tool", 8.5, 3.5, 2),
        ("🌐 Web Search", 11, 3.5, 1.5),
        ("💾 Data Storage", 2, 2.5, 3),
        ("🔧 Configuration", 6, 2.5, 3),
        ("📝 Logging", 10, 2.5, 2.5)
    ]
    
    for comp, x, y, width in backend_components:
        comp_box = FancyBboxPatch((x, y), width, 0.8, boxstyle="round,pad=0.05",
                                  facecolor='#ce93d8', edgecolor='#6a1b9a', linewidth=1)
        ax.add_patch(comp_box)
        ax.text(x + width/2, y + 0.4, comp, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Add connection arrows between layers
    connection_points = [
        (3.5, 10.7, 3.5, 9.3),  # Frontend to Application
        (7.5, 10.7, 7.5, 9.3),
        (3.5, 8, 3.5, 6.3),     # Application to Integration
        (7.5, 8, 7.5, 6.3),
        (3.5, 5.7, 3.5, 4.3),   # Integration to Backend
        (7.5, 5.7, 7.5, 4.3)
    ]
    
    for x1, y1, x2, y2 in connection_points:
        ax.arrow(x1, y1, x2-x1, y2-y1, head_width=0.15, head_length=0.1, 
                 fc='gray', ec='gray', linewidth=1.5, alpha=0.6)
    
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    plt.title('Technical Implementation Architecture', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('diagrams/technical_implementation.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Technical implementation diagram saved")

if __name__ == "__main__":
    print("=== Generating Proper Architecture Diagrams ===\n")
    
    # Ensure diagrams directory exists
    import os
    os.makedirs('diagrams', exist_ok=True)
    
    # Generate all diagrams
    create_system_architecture()
    create_coordination_workflow()
    create_evaluation_framework()
    create_technical_implementation()
    
    print("\n🎉 All architecture diagrams generated successfully!")
    print("\nGenerated files:")
    print("- diagrams/system_architecture.png")
    print("- diagrams/coordination_workflow.png")
    print("- diagrams/evaluation_framework.png")
    print("- diagrams/technical_implementation.png")
