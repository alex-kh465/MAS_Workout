"""
Tools module for the multi-agent system.
Contains calculator and web search tools wrapped as LangChain Tool objects.
"""

import re
import json
import requests
from typing import Union
from langchain.tools import Tool


def calculator_tool(expression: str) -> str:
    """
    Evaluates mathematical expressions safely.
    
    Args:
        expression (str): Mathematical expression to evaluate
        
    Returns:
        str: Result of the calculation or error message
    """
    try:
        # Basic safety check - only allow numbers, operators, and parentheses
        if not re.match(r'^[0-9+\-*/()\s.]+$', expression):
            return "Error: Invalid characters in expression. Only numbers and basic operators (+, -, *, /, (), .) are allowed."
        
        # Evaluate the expression
        result = eval(expression)
        return f"The result of {expression} is {result}"
        
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: Could not evaluate expression '{expression}'. {str(e)}"


def web_search_tool(query: str) -> str:
    """
    Mock web search tool that simulates web search functionality.
    In a real implementation, this would use a search API like Google, Bing, or DuckDuckGo.
    
    Args:
        query (str): Search query
        
    Returns:
        str: Mock search results formatted as text
    """
    # Mock search results based on common fitness queries
    mock_results = {
        "workout": "Workout plans should include cardiovascular exercise, strength training, and flexibility work. Beginners should start with 3 days per week, 30-45 minutes per session.",
        "beginner": "Beginner workouts should focus on bodyweight exercises like push-ups, squats, lunges, and planks. Start with 2-3 sets of 8-12 repetitions.",
        "fitness": "A balanced fitness routine includes cardio (150 minutes moderate intensity per week), strength training (2-3 times per week), and flexibility exercises.",
        "exercise": "Regular exercise provides numerous health benefits including improved cardiovascular health, stronger muscles and bones, better mental health, and weight management.",
        "nutrition": "Proper nutrition for fitness includes adequate protein (0.8-1.2g per kg body weight), complex carbohydrates, healthy fats, and plenty of water.",
        "diet": "A balanced diet should include lean proteins, whole grains, fruits, vegetables, and healthy fats. Avoid processed foods and excessive sugar.",
        "cardio": "Cardio exercises include walking, running, cycling, swimming, and dancing. Aim for 150 minutes of moderate intensity or 75 minutes of vigorous intensity per week.",
        "strength": "Strength training should target all major muscle groups at least 2 days per week. Use progressive overload to continuously challenge muscles.",
        "yoga": "Yoga combines physical postures, breathing exercises, and meditation. It improves flexibility, strength, balance, and mental well-being.",
        "running": "Running is an excellent cardiovascular exercise. Beginners should start with a walk-run program and gradually increase duration and intensity."
    }
    
    # Find relevant results based on query keywords
    query_lower = query.lower()
    results = []
    
    for keyword, info in mock_results.items():
        if keyword in query_lower:
            results.append(f"**{keyword.title()} Information**: {info}")
    
    if not results:
        results.append("**General Fitness Information**: Regular exercise and proper nutrition are key to maintaining good health. Consult with a healthcare provider before starting any new fitness program.")
    
    return "\n\n".join(results)


def research_fitness_topic(topic: str) -> str:
    """
    Research fitness-related topics with more detailed mock information.
    
    Args:
        topic (str): Fitness topic to research
        
    Returns:
        str: Detailed research information
    """
    topic_lower = topic.lower()
    
    fitness_database = {
        "beginner workout": {
            "overview": "A beginner workout plan should be simple, progressive, and sustainable.",
            "components": [
                "Warm-up: 5-10 minutes of light cardio",
                "Strength training: 2-3 times per week, focusing on major muscle groups",
                "Cardio: 150 minutes of moderate intensity per week",
                "Cool-down: 5-10 minutes of stretching"
            ],
            "exercises": [
                "Bodyweight squats: 2-3 sets of 8-12 reps",
                "Push-ups (modified if needed): 2-3 sets of 5-10 reps",
                "Plank: 2-3 sets of 15-30 seconds",
                "Walking lunges: 2-3 sets of 8-12 reps per leg",
                "Glute bridges: 2-3 sets of 10-15 reps"
            ],
            "progression": "Increase reps, sets, or duration by 10% each week",
            "rest": "Take at least one full rest day between strength training sessions"
        },
        "nutrition": {
            "overview": "Proper nutrition supports fitness goals and overall health.",
            "macronutrients": [
                "Protein: 0.8-1.2g per kg body weight for muscle maintenance",
                "Carbohydrates: 45-65% of total calories for energy",
                "Fats: 20-35% of total calories for hormone production"
            ],
            "timing": [
                "Pre-workout: Light carbs and protein 1-2 hours before",
                "Post-workout: Protein and carbs within 30 minutes",
                "Hydration: 8-10 glasses of water daily, more during exercise"
            ],
            "foods": [
                "Lean proteins: chicken, fish, eggs, beans",
                "Complex carbs: oats, quinoa, sweet potatoes",
                "Healthy fats: avocados, nuts, olive oil",
                "Fruits and vegetables: variety of colors for nutrients"
            ]
        }
    }
    
    # Search for relevant topics
    for key, data in fitness_database.items():
        if key in topic_lower or any(word in topic_lower for word in key.split()):
            result = f"**{key.title()} Research**\n\n"
            result += f"**Overview**: {data['overview']}\n\n"
            
            for section, items in data.items():
                if section != 'overview':
                    result += f"**{section.title()}**:\n"
                    if isinstance(items, list):
                        for item in items:
                            result += f"• {item}\n"
                    else:
                        result += f"• {items}\n"
                    result += "\n"
            
            return result
    
    return f"Research on '{topic}': This is a fitness-related topic that would benefit from professional guidance. Consider consulting with a certified personal trainer or nutritionist for personalized advice."


# Create LangChain Tool objects
calculator = Tool(
    name="calculator",
    description="Use this tool to perform mathematical calculations. Input should be a valid mathematical expression using numbers and basic operators (+, -, *, /, (), .).",
    func=calculator_tool
)

web_search = Tool(
    name="web_search",
    description="Use this tool to search for information on the internet. Input should be a search query string. This tool provides fitness and health-related information.",
    func=web_search_tool
)

fitness_research = Tool(
    name="fitness_research",
    description="Use this tool to research detailed fitness topics like workout plans, nutrition, exercise techniques. Input should be a fitness-related topic or question.",
    func=research_fitness_topic
)

# List of all available tools
AVAILABLE_TOOLS = [calculator, web_search, fitness_research]


def get_tools():
    """
    Returns a list of all available tools.
    
    Returns:
        list: List of LangChain Tool objects
    """
    return AVAILABLE_TOOLS


def get_tool_descriptions():
    """
    Returns descriptions of all available tools.
    
    Returns:
        str: Formatted string with tool descriptions
    """
    descriptions = []
    for tool in AVAILABLE_TOOLS:
        descriptions.append(f"- {tool.name}: {tool.description}")
    
    return "\n".join(descriptions)
