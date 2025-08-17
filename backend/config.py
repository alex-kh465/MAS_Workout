"""
Configuration management for the Multi-Agent Workout System.
Loads settings from TOML configuration file.
"""

import os
import toml
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """
    Configuration manager that loads settings from TOML file.
    """
    
    def __init__(self, config_file: str = "config.toml"):
        """
        Initialize configuration loader.
        
        Args:
            config_file (str): Path to the TOML configuration file
        """
        self.config_file = config_file
        self.config_path = self._find_config_file()
        self._config_data = self._load_config()
    
    def _find_config_file(self) -> Path:
        """
        Find the configuration file in the project directory.
        
        Returns:
            Path: Path to the configuration file
        """
        # Start from the backend directory and look for config file
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
        
        config_path = project_root / self.config_file
        
        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file '{self.config_file}' not found at {config_path}. "
                f"Please ensure the config file exists in the project root."
            )
        
        return config_path
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from TOML file.
        
        Returns:
            Dict[str, Any]: Configuration data
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_data = toml.load(file)
            return config_data
        except Exception as e:
            raise RuntimeError(f"Error loading configuration from {self.config_path}: {str(e)}")
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section (str): Configuration section
            key (str): Configuration key
            default (Any): Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        return self._config_data.get(section, {}).get(key, default)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get an entire configuration section.
        
        Args:
            section (str): Configuration section name
            
        Returns:
            Dict[str, Any]: Configuration section data
        """
        return self._config_data.get(section, {})
    
    def has_section(self, section: str) -> bool:
        """
        Check if a configuration section exists.
        
        Args:
            section (str): Configuration section name
            
        Returns:
            bool: True if section exists
        """
        return section in self._config_data
    
    def has_key(self, section: str, key: str) -> bool:
        """
        Check if a configuration key exists in a section.
        
        Args:
            section (str): Configuration section
            key (str): Configuration key
            
        Returns:
            bool: True if key exists
        """
        return section in self._config_data and key in self._config_data[section]
    
    def reload(self):
        """
        Reload configuration from file.
        """
        self._config_data = self._load_config()
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration data.
        
        Returns:
            Dict[str, Any]: All configuration data
        """
        return self._config_data.copy()
    
    # Convenience methods for common configuration values
    
    @property
    def groq_api_key(self) -> str:
        """Get Groq API key."""
        api_key = self.get('api', 'groq_api_key')
        if not api_key or api_key == 'your_groq_api_key_here':
            raise ValueError(
                "Groq API key not configured. Please set 'groq_api_key' in the [api] section of config.toml"
            )
        return api_key
    
    @property
    def groq_model(self) -> str:
        """Get Groq model name."""
        return self.get('api', 'groq_model', 'llama3-8b-8192')
    
    @property
    def max_tokens(self) -> int:
        """Get maximum tokens for agent responses."""
        return self.get('agents', 'max_tokens', 32768)
    
    @property
    def temperature(self) -> float:
        """Get temperature for LLM responses."""
        return self.get('agents', 'temperature', 0.7)
    
    @property
    def debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get('system', 'debug', False)
    
    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.get('system', 'log_level', 'INFO')


# Global configuration instance
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config: Configuration instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


def reload_config():
    """
    Reload the global configuration.
    """
    global _config_instance
    if _config_instance is not None:
        _config_instance.reload()
    else:
        _config_instance = Config()


# Convenience functions for quick access
def get_groq_api_key() -> str:
    """Get Groq API key from configuration."""
    return get_config().groq_api_key


def get_groq_model() -> str:
    """Get Groq model name from configuration."""
    return get_config().groq_model


def get_max_tokens() -> int:
    """Get max tokens from configuration."""
    return get_config().max_tokens


def get_temperature() -> float:
    """Get temperature from configuration."""
    return get_config().temperature


def is_debug_mode() -> bool:
    """Check if debug mode is enabled."""
    return get_config().debug_mode
