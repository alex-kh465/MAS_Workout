#!/usr/bin/env python3
"""
Complete diagram generation script for Multi-Agent Workout System Research Paper
Generates all required diagrams in both PNG and PDF formats
"""

import os
import subprocess
import sys
from pathlib import Path

def ensure_directory():
    """Ensure diagrams directory exists"""
    diagrams_dir = Path("diagrams")
    diagrams_dir.mkdir(exist_ok=True)
    return diagrams_dir

def install_requirements():
    """Install required packages for diagram generation"""
    packages = ['matplotlib', 'numpy', 'pillow']
    
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def generate_matplotlib_charts():
    """Generate matplotlib-based charts"""
    print("Generating matplotlib charts...")
    
    # Run the quality comparison chart
    exec(open('diagrams/5_quality_chart.py').read())
    
    # Run the agent performance radar charts
    exec(open('diagrams/6_agent_performance.py').read())

def convert_mermaid_to_image():
    """Instructions for converting Mermaid diagrams"""
    print("\n=== Mermaid Diagram Conversion Instructions ===")
    print("To convert Mermaid diagrams to images:")
    print("1. Install Mermaid CLI: npm install -g @mermaid-js/mermaid-cli")
    print("2. Convert diagrams:")
    print("   mmdc -i diagrams/1_architecture.mmd -o diagrams/architecture.png -t neutral -w 1200 -H 800")
    print("   mmdc -i diagrams/3_evaluation_framework.mmd -o diagrams/evaluation_framework.png -t neutral -w 1200 -H 800")
    print("\nAlternatively, use online tools:")
    print("- Mermaid Live Editor: https://mermaid.live/")
    print("- Copy diagram code and export as PNG/SVG")

def convert_plantuml_to_image():
    """Instructions for converting PlantUML diagrams"""
    print("\n=== PlantUML Diagram Conversion Instructions ===")
    print("To convert PlantUML diagrams to images:")
    print("1. Install PlantUML: Download plantuml.jar from http://plantuml.com/download")
    print("2. Convert diagram:")
    print("   java -jar plantuml.jar diagrams/2_workflow.puml")
    print("\nAlternatively, use online tools:")
    print("- PlantUML Online Server: http://www.plantuml.com/plantuml/uml/")
    print("- Copy diagram code and export as PNG/SVG")

def convert_graphviz_to_image():
    """Instructions for converting Graphviz diagrams"""
    print("\n=== Graphviz Diagram Conversion Instructions ===")
    print("To convert Graphviz diagrams to images:")
    print("1. Install Graphviz: https://graphviz.org/download/")
    print("2. Convert diagram:")
    print("   dot -Tpng diagrams/4_implementation_architecture.dot -o diagrams/implementation_architecture.png")
    print("   dot -Tpdf diagrams/4_implementation_architecture.dot -o diagrams/implementation_architecture.pdf")
    print("\nAlternatively, use online tools:")
    print("- Graphviz Online: https://dreampuf.github.io/GraphvizOnline/")
    print("- Copy diagram code and export as PNG/SVG")

def create_latex_include_file():
    """Create LaTeX file with proper figure includes"""
    latex_content = """% Replace diagram placeholders with these includes in your main paper

% Figure 1: System Architecture
\\begin{figure}[htbp]
\\centering
\\includegraphics[width=0.9\\textwidth]{diagrams/architecture.png}
\\caption{System Architecture Overview}
\\label{fig:architecture}
\\end{figure}

% Figure 2: Agent Coordination Workflow  
\\begin{figure}[htbp]
\\centering
\\includegraphics[width=0.9\\textwidth]{diagrams/workflow.png}
\\caption{Agent Coordination Workflow}
\\label{fig:workflow}
\\end{figure}

% Figure 3: Evaluation Framework
\\begin{figure}[htbp]
\\centering
\\includegraphics[width=0.9\\textwidth]{diagrams/evaluation_framework.png}
\\caption{Evaluation Framework Overview}
\\label{fig:evaluation_framework}
\\end{figure}

% Figure 4: Technical Implementation
\\begin{figure}[htbp]
\\centering
\\includegraphics[width=0.9\\textwidth]{diagrams/implementation_architecture.png}
\\caption{Technical Implementation Architecture}
\\label{fig:implementation_architecture}
\\end{figure}

% Figure 5: Quality Comparison Chart
\\begin{figure}[htbp]
\\centering
\\includegraphics[width=0.9\\textwidth]{diagrams/quality_comparison_chart.png}
\\caption{Response Quality Comparison Chart}
\\label{fig:quality_chart}
\\end{figure}

% Figure 6: Agent Performance Metrics
\\begin{figure}[htbp]
\\centering
\\includegraphics[width=0.9\\textwidth]{diagrams/agent_performance_individual.png}
\\caption{Individual Agent Performance Metrics}
\\label{fig:agent_performance}
\\end{figure}
"""
    
    with open('diagrams/latex_includes.tex', 'w') as f:
        f.write(latex_content)
    
    print("LaTeX include file created: diagrams/latex_includes.tex")

def main():
    """Main execution function"""
    print("=== Multi-Agent Workout System Diagram Generator ===\n")
    
    # Setup
    ensure_directory()
    install_requirements()
    
    # Generate matplotlib charts (these will work immediately)
    generate_matplotlib_charts()
    
    # Create LaTeX includes
    create_latex_include_file()
    
    # Provide conversion instructions for other formats
    convert_mermaid_to_image()
    convert_plantuml_to_image() 
    convert_graphviz_to_image()
    
    print("\n=== Summary ===")
    print("✅ Matplotlib charts generated automatically")
    print("📋 Conversion instructions provided for Mermaid, PlantUML, and Graphviz")
    print("📄 LaTeX include file created for easy integration")
    print("\nNext steps:")
    print("1. Convert Mermaid/PlantUML/Graphviz diagrams using provided instructions")
    print("2. Replace diagram placeholders in research_paper.tex with includes from latex_includes.tex")
    print("3. Compile LaTeX document for final paper")

if __name__ == "__main__":
    main()
