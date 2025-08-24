import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Ensure matplotlib backend works properly
plt.style.use('default')

# Agent performance data
agents = ['Planner Agent', 'Research Agent', 'Writer Agent']
agent_colors = ['#1976d2', '#388e3c', '#f57c00']

# Metrics for each agent (converted to 0-1 scale)
planner_metrics = {
    'Task Analysis\nAccuracy': 0.942,
    'Workflow\nOptimization': 0.891,
    'Resource\nAllocation': 0.918
}

research_metrics = {
    'Tool Usage\nRate': 0.983,
    'Information\nQuality': 0.876,
    'Synthesis\nEffectiveness': 0.854
}

writer_metrics = {
    'Response\nStructure': 0.921,
    'Actionability': 0.847,
    'User\nAccessibility': 0.889
}

all_metrics = [planner_metrics, research_metrics, writer_metrics]

# Create figure with subplots for individual radar charts
fig, axes = plt.subplots(figsize=(15, 5), nrows=1, ncols=3, subplot_kw=dict(projection='polar'))
fig.suptitle('Individual Agent Performance Metrics', fontsize=16, fontweight='bold', y=1.02)

# Function to create individual radar chart
def create_radar_chart(ax, metrics_dict, agent_name, color):
    # Get metrics
    categories = list(metrics_dict.keys())
    values = list(metrics_dict.values())
    
    # Calculate angles for each metric
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Complete the circle
    
    # Add values to complete the circle
    values += values[:1]
    
    # Plot
    ax.plot(angles, values, 'o-', linewidth=2, label=agent_name, color=color)
    ax.fill(angles, values, alpha=0.25, color=color)
    
    # Add labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # Add value labels
    for angle, value, category in zip(angles[:-1], values[:-1], categories):
        ax.annotate(f'{value:.3f}', xy=(angle, value), xytext=(5, 5),
                   textcoords='offset points', ha='left', va='bottom',
                   fontsize=9, fontweight='bold', color=color)
    
    # Title
    ax.set_title(agent_name, fontsize=12, fontweight='bold', pad=20)

# Create individual radar charts
for i, (metrics_dict, agent_name, color) in enumerate(zip(all_metrics, agents, agent_colors)):
    create_radar_chart(axes[i], metrics_dict, agent_name, color)

plt.tight_layout()
plt.savefig('diagrams/agent_performance_individual.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('diagrams/agent_performance_individual.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.show()

# Create combined radar chart
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

# Combine all metrics for comparison
all_categories = []
all_values = []
for metrics_dict in all_metrics:
    all_categories.extend(list(metrics_dict.keys()))
    all_values.extend(list(metrics_dict.values()))

# Create angles for all metrics
N_total = len(all_categories)
angles = [n / float(N_total) * 2 * pi for n in range(N_total)]
angles += angles[:1]
all_values += all_values[:1]

# Plot combined radar
ax.plot(angles, all_values, 'o-', linewidth=2, color='#424242', alpha=0.8)
ax.fill(angles, all_values, alpha=0.1, color='#424242')

# Color code sections by agent
section_colors = ['#1976d2', '#1976d2', '#1976d2',  # Planner
                 '#388e3c', '#388e3c', '#388e3c',  # Research  
                 '#f57c00', '#f57c00', '#f57c00']  # Writer

for i, (angle, value, color) in enumerate(zip(angles[:-1], all_values[:-1], section_colors)):
    ax.scatter(angle, value, color=color, s=100, alpha=0.8, edgecolor='black')
    ax.annotate(f'{value:.3f}', xy=(angle, value), xytext=(8, 8),
               textcoords='offset points', ha='left', va='bottom',
               fontsize=8, fontweight='bold', color=color)

# Customize combined chart
ax.set_xticks(angles[:-1])
ax.set_xticklabels(all_categories, fontsize=9)
ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_title('Combined Agent Performance Metrics', fontsize=14, fontweight='bold', pad=30)

# Add agent section labels
agent_positions = [1, 4, 7]  # Positions for agent labels
for pos, agent, color in zip(agent_positions, agents, agent_colors):
    angle = angles[pos]
    ax.annotate(agent, xy=(angle, 1.1), ha='center', va='center',
               fontsize=11, fontweight='bold', color=color,
               bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.2))

plt.tight_layout()
plt.savefig('diagrams/agent_performance_combined.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('diagrams/agent_performance_combined.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.show()

print("\nAgent Performance Radar Charts generated successfully!")
print("Files saved:")
print("- diagrams/agent_performance_individual.png (300 DPI)")
print("- diagrams/agent_performance_individual.pdf (vector format)")
print("- diagrams/agent_performance_combined.png (300 DPI)")
print("- diagrams/agent_performance_combined.pdf (vector format)")
