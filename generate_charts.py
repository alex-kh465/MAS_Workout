#!/usr/bin/env python3
"""
Chart Generation Script for Multi-Agent Workout System Report
Generates publication-quality charts for the markdown document
"""

import matplotlib.pyplot as plt
import numpy as np
from math import pi
import seaborn as sns
import os

# Set style for publication-quality plots
plt.style.use('default')
sns.set_style("whitegrid")
sns.set_palette("husl")

# Create diagrams directory
os.makedirs('diagrams', exist_ok=True)

def generate_quality_comparison_chart():
    """Generate the response quality comparison bar chart"""
    print("Generating Response Quality Comparison Chart...")
    
    # Data
    metrics = ['Readability', 'Completeness', 'Relevance', 'Actionability', 'Overall Quality']
    multi_agent_scores = [0.823, 0.856, 0.892, 0.817, 0.847]
    baseline_scores = [0.667, 0.634, 0.723, 0.598, 0.656]
    improvements = [23.4, 35.0, 23.4, 36.6, 29.1]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Position settings
    x = np.arange(len(metrics))
    width = 0.35
    
    # Create bars
    bars1 = ax.bar(x - width/2, multi_agent_scores, width, 
                   label='Multi-Agent System', color='#1976d2', alpha=0.8)
    bars2 = ax.bar(x + width/2, baseline_scores, width,
                   label='Single-Agent Baseline', color='#ff8f00', alpha=0.8)
    
    # Add improvement percentages above multi-agent bars
    for i, (improvement, ma_score) in enumerate(zip(improvements, multi_agent_scores)):
        ax.annotate(f'+{improvement}%', 
                    xy=(x[i] - width/2, ma_score), 
                    xytext=(0, 5), textcoords='offset points',
                    ha='center', va='bottom', fontweight='bold',
                    color='#1976d2', fontsize=10)
    
    # Add value labels on bars
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        # Multi-agent values
        height1 = bar1.get_height()
        ax.annotate(f'{height1:.3f}',
                    xy=(bar1.get_x() + bar1.get_width() / 2, height1),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)
        
        # Baseline values
        height2 = bar2.get_height()
        ax.annotate(f'{height2:.3f}',
                    xy=(bar2.get_x() + bar2.get_width() / 2, height2),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)
    
    # Customize chart
    ax.set_xlabel('Evaluation Metrics', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score (0-1 Scale)', fontsize=12, fontweight='bold')
    ax.set_title('Response Quality Comparison: Multi-Agent vs Single-Agent Baseline', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11)
    ax.legend(fontsize=11, loc='upper left')
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Save chart
    plt.tight_layout()
    plt.savefig('diagrams/quality_comparison.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Quality comparison chart saved: diagrams/quality_comparison.png")

def generate_coordination_metrics_chart():
    """Generate coordination metrics visualization"""
    print("Generating Coordination Metrics Chart...")
    
    # Data
    metrics = ['Agent\nParticipation', 'Information\nFlow Quality', 
               'Tool Usage\nCoordination', 'Workflow\nEfficiency']
    scores = [1.00, 0.872, 0.915, 0.834]
    colors = ['#4caf50', '#2196f3', '#ff9800', '#9c27b0']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bars
    bars = ax.bar(metrics, scores, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Add value labels
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.annotate(f'{score:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Add target line at 0.8
    ax.axhline(y=0.8, color='red', linestyle='--', alpha=0.7, label='Excellence Threshold (0.8)')
    
    # Customize chart
    ax.set_ylabel('Coordination Score (0-1 Scale)', fontsize=12, fontweight='bold')
    ax.set_title('Agent Coordination Effectiveness Metrics', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=10)
    
    # Save chart
    plt.tight_layout()
    plt.savefig('diagrams/coordination_metrics.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Coordination metrics chart saved: diagrams/coordination_metrics.png")

def generate_performance_comparison():
    """Generate performance comparison visualization"""
    print("Generating Performance Comparison Chart...")
    
    # Data
    metrics = ['Response Time\n(seconds)', 'Response Length\n(words)', 'Success Rate\n(%)', 'User Satisfaction\n(0-1)']
    multi_agent = [8.42, 247, 100, 0.863]
    baseline = [6.18, 156, 95, 0.634]
    
    # Normalize data for visualization (different scales)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Response Time
    ax1.bar(['Multi-Agent', 'Baseline'], [8.42, 6.18], color=['#1976d2', '#ff8f00'], alpha=0.8)
    ax1.set_title('Response Time Comparison', fontweight='bold')
    ax1.set_ylabel('Seconds')
    ax1.annotate('+36.2%', xy=(0, 8.42), xytext=(0, 10), ha='center', fontweight='bold', color='red')
    
    # Response Length
    ax2.bar(['Multi-Agent', 'Baseline'], [247, 156], color=['#1976d2', '#ff8f00'], alpha=0.8)
    ax2.set_title('Response Comprehensiveness', fontweight='bold')
    ax2.set_ylabel('Word Count')
    ax2.annotate('+58.3%', xy=(0, 247), xytext=(0, 260), ha='center', fontweight='bold', color='green')
    
    # Success Rate
    ax3.bar(['Multi-Agent', 'Baseline'], [100, 95], color=['#1976d2', '#ff8f00'], alpha=0.8)
    ax3.set_title('System Reliability', fontweight='bold')
    ax3.set_ylabel('Success Rate (%)')
    ax3.set_ylim(90, 101)
    ax3.annotate('+5.3%', xy=(0, 100), xytext=(0, 100.5), ha='center', fontweight='bold', color='green')
    
    # User Satisfaction
    ax4.bar(['Multi-Agent', 'Baseline'], [0.863, 0.634], color=['#1976d2', '#ff8f00'], alpha=0.8)
    ax4.set_title('User Satisfaction Score', fontweight='bold')
    ax4.set_ylabel('Satisfaction (0-1)')
    ax4.set_ylim(0, 1)
    ax4.annotate('+36.1%', xy=(0, 0.863), xytext=(0, 0.9), ha='center', fontweight='bold', color='green')
    
    # Add value labels
    for ax, ma_val, base_val in zip([ax1, ax2, ax3, ax4], 
                                   [8.42, 247, 100, 0.863], 
                                   [6.18, 156, 95, 0.634]):
        bars = ax.patches
        ax.annotate(f'{ma_val}', xy=(bars[0].get_x() + bars[0].get_width()/2, bars[0].get_height()),
                   xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold')
        ax.annotate(f'{base_val}', xy=(bars[1].get_x() + bars[1].get_width()/2, bars[1].get_height()),
                   xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold')
    
    plt.suptitle('System Performance Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('diagrams/performance_comparison.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Performance comparison chart saved: diagrams/performance_comparison.png")

def generate_agent_radar_chart():
    """Generate individual agent performance radar chart"""
    print("Generating Agent Performance Radar Chart...")
    
    # Agent data
    agents = ['Planner Agent', 'Research Agent', 'Writer Agent']
    colors = ['#1976d2', '#388e3c', '#f57c00']
    
    # Metrics for each agent
    planner_metrics = ['Task Analysis\nAccuracy', 'Workflow\nOptimization', 'Resource\nAllocation']
    planner_values = [0.942, 0.891, 0.918]
    
    research_metrics = ['Tool Usage\nRate', 'Information\nQuality', 'Synthesis\nEffectiveness']
    research_values = [0.983, 0.876, 0.854]
    
    writer_metrics = ['Response\nStructure', 'Actionability', 'User\nAccessibility']
    writer_values = [0.921, 0.847, 0.889]
    
    all_data = [
        (planner_metrics, planner_values, 'Planner Agent', colors[0]),
        (research_metrics, research_values, 'Research Agent', colors[1]),
        (writer_metrics, writer_values, 'Writer Agent', colors[2])
    ]
    
    # Create subplots
    fig, axes = plt.subplots(figsize=(15, 5), nrows=1, ncols=3, subplot_kw=dict(projection='polar'))
    fig.suptitle('Individual Agent Performance Metrics', fontsize=16, fontweight='bold', y=0.98)
    
    for ax, (metrics, values, agent_name, color) in zip(axes, all_data):
        # Calculate angles
        N = len(metrics)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        values_circle = values + [values[0]]  # Complete the circle
        
        # Plot
        ax.plot(angles, values_circle, 'o-', linewidth=2, color=color, markersize=8)
        ax.fill(angles, values_circle, alpha=0.25, color=color)
        
        # Add labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, fontsize=10)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # Add value labels
        for angle, value in zip(angles[:-1], values):
            ax.annotate(f'{value:.3f}', xy=(angle, value), xytext=(8, 8),
                       textcoords='offset points', ha='left', va='bottom',
                       fontsize=9, fontweight='bold', color=color)
        
        # Title
        ax.set_title(agent_name, fontsize=12, fontweight='bold', pad=20, color=color)
    
    plt.tight_layout()
    plt.savefig('diagrams/agent_performance_radar.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Agent performance radar chart saved: diagrams/agent_performance_radar.png")

def generate_benefits_summary_chart():
    """Generate benefits summary visualization"""
    print("Generating Benefits Summary Chart...")
    
    # Data
    benefits = ['Response\nComprehensiveness', 'User\nSatisfaction', 'System\nReliability', 'Processing\nOverhead']
    values = [58.3, 36.1, 5.3, 36.2]
    colors = ['#4caf50', '#4caf50', '#4caf50', '#f44336']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create horizontal bars
    bars = ax.barh(benefits, values, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Add value labels
    for bar, value in zip(bars, values):
        width = bar.get_width()
        ax.annotate(f'+{value}%' if value > 0 else f'{value}%',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=11, fontweight='bold')
    
    # Add vertical line at 0
    ax.axvline(x=0, color='black', linewidth=1)
    
    # Customize chart
    ax.set_xlabel('Percentage Change (%)', fontsize=12, fontweight='bold')
    ax.set_title('Performance Trade-off Analysis', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#4caf50', alpha=0.8, label='Benefits'),
                      Patch(facecolor='#f44336', alpha=0.8, label='Overhead')]
    ax.legend(handles=legend_elements, fontsize=11, loc='lower right')
    
    plt.tight_layout()
    plt.savefig('diagrams/benefits_summary.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Benefits summary chart saved: diagrams/benefits_summary.png")

def generate_system_comparison_heatmap():
    """Generate system comparison heatmap"""
    print("Generating System Comparison Heatmap...")
    
    # Data
    metrics = ['Readability', 'Completeness', 'Relevance', 'Actionability', 'Overall']
    systems = ['Multi-Agent', 'Baseline']
    
    data = np.array([
        [0.823, 0.856, 0.892, 0.817, 0.847],  # Multi-Agent
        [0.667, 0.634, 0.723, 0.598, 0.656]   # Baseline
    ])
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 4))
    
    im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0.5, vmax=0.9)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(metrics)))
    ax.set_yticks(np.arange(len(systems)))
    ax.set_xticklabels(metrics)
    ax.set_yticklabels(systems)
    
    # Add text annotations
    for i in range(len(systems)):
        for j in range(len(metrics)):
            text = ax.text(j, i, f'{data[i, j]:.3f}',
                          ha="center", va="center", color="black", fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Score (0-1 Scale)', fontsize=11, fontweight='bold')
    
    ax.set_title('Response Quality Heatmap Comparison', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('diagrams/system_comparison_heatmap.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ System comparison heatmap saved: diagrams/system_comparison_heatmap.png")

def generate_improvement_summary():
    """Generate improvement summary chart"""
    print("Generating Improvement Summary Chart...")
    
    # Data
    categories = ['Response Quality', 'Agent Coordination', 'System Performance']
    subcategories = [
        ['Readability', 'Completeness', 'Relevance', 'Actionability'],
        ['Participation', 'Information Flow', 'Tool Usage', 'Workflow'],
        ['Comprehensiveness', 'Satisfaction', 'Reliability']
    ]
    improvements = [
        [23.4, 35.0, 23.4, 36.6],
        [0, 87.2, 91.5, 83.4],  # Coordination scores (not improvements)
        [58.3, 36.1, 5.3]
    ]
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    colors = [['#1976d2', '#1976d2', '#1976d2', '#1976d2'],
              ['#388e3c', '#388e3c', '#388e3c', '#388e3c'],
              ['#f57c00', '#f57c00', '#f57c00']]
    
    for ax, category, subcat, impr, color_list in zip(axes, categories, subcategories, improvements, colors):
        bars = ax.bar(range(len(subcat)), impr, color=color_list, alpha=0.8, edgecolor='black', linewidth=0.5)
        
        # Add value labels
        for bar, value in zip(bars, impr):
            height = bar.get_height()
            if category == 'Agent Coordination':
                label = f'{value:.1f}%' if value < 1 else f'{value:.1f}'
            else:
                label = f'+{value:.1f}%'
            ax.annotate(label,
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_title(category, fontsize=12, fontweight='bold')
        ax.set_xticks(range(len(subcat)))
        ax.set_xticklabels(subcat, fontsize=9, rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Multi-Agent System Improvements Across All Categories', 
                 fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('diagrams/improvement_summary.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Improvement summary chart saved: diagrams/improvement_summary.png")

def main():
    """Generate all charts"""
    print("=== Multi-Agent Workout System Chart Generator ===\n")
    
    try:
        generate_quality_comparison_chart()
        generate_coordination_metrics_chart()
        generate_performance_comparison()
        generate_agent_radar_chart()
        generate_benefits_summary_chart()
        generate_system_comparison_heatmap()
        
        print("\n🎉 All charts generated successfully!")
        print("\nGenerated files:")
        print("- diagrams/quality_comparison.png")
        print("- diagrams/coordination_metrics.png") 
        print("- diagrams/performance_comparison.png")
        print("- diagrams/agent_performance_radar.png")
        print("- diagrams/benefits_summary.png")
        print("- diagrams/system_comparison_heatmap.png")
        
        print("\n📋 Next steps:")
        print("1. View generated charts in the diagrams/ folder")
        print("2. Include charts in your markdown document")
        print("3. Use charts for presentations and reports")
        
    except Exception as e:
        print(f"❌ Error generating charts: {e}")
        print("Make sure matplotlib and seaborn are installed:")
        print("pip install matplotlib seaborn numpy")

if __name__ == "__main__":
    main()
