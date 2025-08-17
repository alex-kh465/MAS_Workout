#!/usr/bin/env python3
"""Test configuration system for deployment compatibility."""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_config():
    """Test the configuration system."""
    try:
        from backend.config import get_config
        print("✅ Configuration module imported successfully")
        
        config = get_config()
        print(f"✅ Configuration loaded: Streamlit Cloud = {config.is_streamlit_cloud}")
        
        # Test basic config values
        api_key_present = bool(config.get('api', 'groq_api_key'))
        model_name = config.get('api', 'groq_model')
        max_tokens = config.get('agents', 'max_tokens')
        
        print(f"✅ API key configured: {api_key_present}")
        print(f"✅ Model name: {model_name}")
        print(f"✅ Max tokens: {max_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """Test all required imports."""
    try:
        import streamlit
        print("✅ Streamlit imported")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import toml
        print("✅ TOML imported")
    except ImportError as e:
        print(f"❌ TOML import failed: {e}")
        return False
    
    try:
        import groq
        print("✅ Groq imported")
    except ImportError as e:
        print(f"❌ Groq import failed: {e}")
        return False
    
    try:
        import langchain
        print("✅ LangChain imported")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    return True

def test_backend_imports():
    """Test backend module imports."""
    try:
        from backend import agents, tools, memory, graph, config
        print("✅ All backend modules imported")
        return True
    except Exception as e:
        print(f"❌ Backend import failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Multi-Agent Workout System Deployment Compatibility")
    print("=" * 60)
    
    print("\n📦 Testing Imports...")
    imports_ok = test_imports()
    
    print("\n🔧 Testing Backend Modules...")
    backend_ok = test_backend_imports()
    
    print("\n⚙️ Testing Configuration System...")
    config_ok = test_config()
    
    print("\n" + "=" * 60)
    if imports_ok and backend_ok and config_ok:
        print("🎉 ALL TESTS PASSED - Ready for Streamlit Cloud deployment!")
    else:
        print("❌ TESTS FAILED - Fix issues before deploying")
    
    print("=" * 60)
