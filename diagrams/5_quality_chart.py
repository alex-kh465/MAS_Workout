import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# Data from evaluation results
metrics = ['Readability\nScore', 'Completeness\nScore', 'Relevance\nScore', 
           'Actionability\nScore', 'Overall\nQuality']
multi_agent_scores = [0.823, 0.856, 0.892, 0.817, 0.847]
baseline_scores = [0.667, 0.634, 0.723, 0.598, 0.656]
improvements = [23.4, 35.0, 23.4, 36.6, 29.1]

# Set up the figure
fig, ax = plt.subplots(figsize=(12, 8))

# Position settings
x = np.arange(len(metrics))
width = 0.35

# Create bars
bars1 = ax.bar(x - width/2, multi_agent_scores, width, 
               label='Multi-Agent System', color='#1976d2', alpha=0.8,
               edgecolor='black', linewidth=0.5)
bars2 = ax.bar(x + width/2, baseline_scores, width,
               label='Single-Agent Baseline', color='#ff8f00', alpha=0.8,
               edgecolor='black', linewidth=0.5)

# Add improvement percentages above bars
for i, (improvement, ma_score) in enumerate(zip(improvements, multi_agent_scores)):
    ax.annotate(f'+{improvement}%', 
                xy=(x[i] - width/2, ma_score), 
                xytext=(0, 5), textcoords='offset points',
                ha='center', va='bottom', fontweight='bold',
                color='#1976d2', fontsize=10)

# Customize the chart
ax.set_xlabel('Evaluation Metrics', fontsize=12, fontweight='bold')
ax.set_ylabel('Score (0-1 Scale)', fontsize=12, fontweight='bold')
ax.set_title('Response Quality Comparison: Multi-Agent vs Single-Agent Baseline', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=10)
ax.legend(fontsize=11, loc='upper left')

# Add grid for better readability
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 1.0)

# Add value labels on bars
for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    # Multi-agent values
    height1 = bar1.get_height()
    ax.annotate(f'{height1:.3f}',
                xy=(bar1.get_x() + bar1.get_width() / 2, height1),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Baseline values
    height2 = bar2.get_height()
    ax.annotate(f'{height2:.3f}',
                xy=(bar2.get_x() + bar2.get_width() / 2, height2),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

# Add a subtle background
ax.set_facecolor('#fafafa')

# Add statistical significance indicators
for i, improvement in enumerate(improvements):
    if improvement > 30:  # Highly significant improvements
        ax.add_patch(Rectangle((x[i] - width/2 - 0.1, -0.05), 
                              width + 0.2, 0.03, 
                              facecolor='green', alpha=0.3))

# Tight layout and save
plt.tight_layout()
plt.savefig('diagrams/quality_comparison_chart.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('diagrams/quality_comparison_chart.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')

# Display the plot
plt.show()

print("Response Quality Comparison Chart generated successfully!")
print("Files saved:")
print("- diagrams/quality_comparison_chart.png (300 DPI)")
print("- diagrams/quality_comparison_chart.pdf (vector format)")
