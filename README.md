# 🏋️‍♂️ Multi-Agent Workout System

A complete multi-agent system built with **LangGraph**, **Groq API**, and **Streamlit** that provides personalized fitness guidance through coordinated AI agents.

## 🎯 System Overview

This system uses three specialized AI agents working together to provide comprehensive fitness advice:

- **🎯 Planner Agent**: Analyzes user requests and creates execution plans
- **🔍 Research Agent**: Gathers fitness information using available tools
- **✍️ Writer Agent**: Creates comprehensive, user-friendly responses

## 🏗️ Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Streamlit UI      │    │   Backend System    │    │   Groq API          │
│                     │    │                     │    │                     │
│ • Input Interface   │───▶│ • Agent Orchestr.   │───▶│ • LLM Processing    │
│ • Progress Display  │    │ • Memory Management │    │ • Response Gen.     │
│ • Results Viewer    │    │ • Tool Integration  │    │                     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

### Core Components

1. **Backend System** (`/backend/`)
   - `agents.py`: Three specialized AI agents with Groq integration
   - `tools.py`: Calculator, web search, and fitness research tools
   - `memory.py`: Shared state and per-agent memory management
   - `graph.py`: Simplified workflow orchestration
   - `main.py`: Main API and system coordination

2. **Frontend** (`app.py`)
   - Interactive Streamlit UI
   - Real-time workflow visualization
   - Conversation history management

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Git
- (Optional) Groq API key for enhanced LLM responses

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd workout_agent
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv workout_agent_env
   
   # Activate (Windows)
   workout_agent_env\Scripts\activate
   
   # Activate (macOS/Linux)
   source workout_agent_env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment (Optional):**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Groq API key
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```
   
   > **Note**: The system includes mock responses and will work without an API key for demonstration purposes.

### Running the Application

**Start the Streamlit application:**
```bash
streamlit run app.py
```

The application will be available at: `http://localhost:8501`

## 💡 Usage Examples

### Example Queries You Can Try:

1. **"Create a beginner workout plan for someone who wants to start exercising"**
2. **"What are the best exercises for building upper body strength?"**
3. **"Design a 30-minute HIIT workout routine"**
4. **"What should I eat before and after a workout?"**
5. **"How can I improve my running endurance?"**
6. **"Create a home workout routine with no equipment"**

### How It Works:

1. **Enter your fitness question** in the text area
2. **Click "🚀 Run Multi-Agent System"**
3. **Watch the progress** as each agent processes your request:
   - 🎯 Planner analyzes and creates a plan
   - 🔍 Research gathers relevant information
   - ✍️ Writer creates the final response
4. **View the comprehensive answer** with step-by-step agent outputs

## 🛠️ Features

### Multi-Agent Coordination
- **Sequential workflow**: Agents execute in logical order
- **Shared memory**: Context preserved between agents
- **Tool integration**: Agents can use calculators and research tools

### Interactive UI
- **Real-time progress**: Visual feedback during processing
- **Expandable steps**: View detailed agent outputs
- **Conversation history**: Track previous queries and responses
- **System controls**: Reset and monitor system status
- **Evaluation metrics**: Real-time quality assessment of responses

### Memory Management
- **Per-agent memory**: Individual conversation buffers
- **Shared state**: Global context and task coordination
- **Session persistence**: Maintain context across interactions

### 📊 Comprehensive Evaluation Framework
- **Response Quality Metrics**: Readability, completeness, relevance, actionability
- **Agent Coordination Analysis**: Workflow efficiency, tool usage effectiveness
- **Performance Benchmarking**: Response time, memory usage, success rates
- **Baseline Comparison**: Multi-agent vs single-agent system comparison
- **Automated Testing**: Standardized test dataset with 10 representative queries
- **Real-time Evaluation**: Quality scores displayed with each response
- **Comprehensive Reports**: JSON and Markdown evaluation reports

## 📁 Project Structure

```
workout_agent/
├── backend/
│   ├── __init__.py          # Backend module initialization
│   ├── agents.py            # AI agents with Groq integration
│   ├── graph.py             # Workflow orchestration
│   ├── main.py              # Main backend API
│   ├── memory.py            # Memory management system
│   └── tools.py             # Available tools and functions
├── app.py                   # Streamlit frontend application
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Optional: Model selection
GROQ_MODEL=mixtral-8x7b-32768
```

### Available Models
- `mixtral-8x7b-32768` (default)
- `llama2-70b-4096`
- `gemma-7b-it`

## 🧪 Testing

**Test the backend system:**
```bash
python -m backend.main
```

This will run a test query and verify all components are working.

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the virtual environment
   pip install -r requirements.txt --upgrade
   ```

2. **Streamlit Not Starting**
   ```bash
   # Check if Streamlit is installed
   pip show streamlit
   
   # Reinstall if necessary
   pip install streamlit --upgrade
   ```

3. **LangGraph Compatibility**
   - The system uses a simplified workflow due to LangGraph version compatibility
   - All functionality is preserved through the `SimpleWorkflow` class

4. **Memory Warnings**
   - LangChain memory deprecation warnings can be ignored
   - The system functions normally despite these warnings

### System Requirements
- **RAM**: Minimum 4GB, 8GB recommended
- **Storage**: ~2GB for dependencies
- **Network**: Internet connection for API calls (if using real Groq API)

## 🚀 Advanced Usage

### Running Without Groq API
The system includes comprehensive mock responses for all agents, allowing full functionality without API keys.

### Customizing Agents
Modify agent prompts and behavior in `backend/agents.py`:

```python
# Example: Customize the Planner Agent
self.prompt_template = PromptTemplate(
    input_variables=["task", "context"],
    template="""Your custom prompt here..."""
)
```

### Adding New Tools
Extend functionality by adding tools in `backend/tools.py`:

```python
def your_custom_tool(input_data: str) -> str:
    # Your tool implementation
    return "Tool result"

custom_tool = Tool(
    name="custom_tool",
    description="Your tool description",
    func=your_custom_tool
)
```

## 📊 System Monitoring

The Streamlit UI provides real-time monitoring:

- **System Status**: Session ID, available agents, and tools
- **Memory Usage**: Current task status and agent outputs  
- **Conversation History**: Full history with timestamps
- **Agent Performance**: Processing time and output length
- **Quality Metrics**: Real-time evaluation scores for each response

## 🔬 Evaluation Framework

### Comprehensive Evaluation System
The system includes a complete evaluation framework for academic assessment and performance analysis:

#### Automated Evaluation
```bash
# Run quick evaluation (5 test queries)
python run_evaluation.py

# Run comprehensive evaluation (10 test queries)
python run_evaluation.py --type full

# Save reports to specific directory
python run_evaluation.py --type full --output ./evaluation_reports
```

#### Evaluation Dashboard
```bash
# Launch evaluation dashboard
streamlit run evaluation_dashboard.py
```

#### Key Evaluation Metrics

**Response Quality Metrics:**
- **Readability Score**: Sentence structure and clarity assessment
- **Completeness Score**: Coverage of query requirements and domain knowledge
- **Relevance Score**: Alignment between query and response content
- **Actionability Score**: Presence of specific, executable advice

**Agent Coordination Metrics:**
- **Coordination Score**: Effectiveness of inter-agent communication
- **Workflow Efficiency**: Timeliness and organization of execution
- **Tool Usage Effectiveness**: Strategic use of available research tools

**Performance Metrics:**
- **Response Time**: Total system processing time
- **Memory Usage**: Efficiency of state management
- **Success Rate**: Reliability of query processing

#### Baseline Comparison
The evaluation includes comparison against a single-agent baseline to demonstrate multi-agent benefits:

- **Single-Agent Baseline**: Same LLM and tools but no agent coordination
- **Comparative Analysis**: Statistical comparison across all metrics
- **Improvement Quantification**: Percentage improvements in key areas
- **Qualitative Assessment**: Analysis of coordination benefits

#### Academic Report Generation
Automatically generates comprehensive academic reports:

- **JSON Reports**: Complete evaluation data in machine-readable format
- **Markdown Reports**: Human-readable analysis with tables and visualizations
- **Statistical Analysis**: Detailed performance comparisons and recommendations
- **Academic Format**: Structured for academic submission and peer review

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain**: For the agent framework and memory management
- **LangGraph**: For workflow orchestration concepts
- **Groq**: For fast LLM inference
- **Streamlit**: For the interactive web interface

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Verify Python version compatibility (3.8+)
4. Check that the virtual environment is activated

## 🔄 Updates

The system is designed to be extensible and maintainable:
- Add new agents by extending the `BaseAgent` class
- Integrate new tools by following the LangChain Tool pattern
- Customize the UI by modifying `app.py`
- Enhance memory management in `memory.py`

---

**Built with ❤️ using LangGraph + Groq + Streamlit**

*A complete multi-agent system for personalized fitness guidance*
