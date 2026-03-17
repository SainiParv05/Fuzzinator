"""
config_loader.py
Fuzzinator — Configuration Management

Loads and validates configuration from YAML files.
"""

import os
import yaml
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for Fuzzinator."""

    def __init__(self, config_dict: Dict[str, Any], project_root: str):
        """
        Initialize configuration from a dictionary.

        Args:
            config_dict: Configuration dictionary loaded from YAML
            project_root: Root directory of the project
        """
        self._config = config_dict
        self._project_root = project_root
        self._validate()

    def _validate(self):
        """Validate configuration values."""
        # Check required sections
        required_sections = ["agent", "environment", "fuzzing", "paths", "logging"]
        for section in required_sections:
            if section not in self._config:
                raise ValueError(f"Missing required config section: {section}")

        # Validate agent settings
        agent_cfg = self._config.get("agent", {})
        if agent_cfg.get("learning_rate", 0) <= 0:
            raise ValueError("agent.learning_rate must be positive")

        # Validate environment settings
        env_cfg = self._config.get("environment", {})
        if env_cfg.get("timeout_ms", 0) <= 0:
            raise ValueError("environment.timeout_ms must be positive")
        if env_cfg.get("max_input_size", 0) <= 0:
            raise ValueError("environment.max_input_size must be positive")
        if env_cfg.get("max_steps", 0) <= 0:
            raise ValueError("environment.max_steps must be positive")

        # Validate fuzzing settings
        fuzz_cfg = self._config.get("fuzzing", {})
        if fuzz_cfg.get("buffer_size", 0) <= 0:
            raise ValueError("fuzzing.buffer_size must be positive")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'agent.learning_rate')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default

        return value

    def resolve_path(self, path_key: str) -> str:
        """
        Resolve a path configuration key relative to project root.

        Args:
            path_key: Path key (e.g., 'checkpoint_dir', 'crash_dir')

        Returns:
            Absolute path
        """
        relative_path = self.get(f"paths.{path_key}")
        if relative_path is None:
            raise ValueError(f"Path configuration '{path_key}' not found")

        if os.path.isabs(relative_path):
            return relative_path

        return os.path.join(self._project_root, relative_path)

    def __str__(self) -> str:
        """Return a readable configuration summary."""
        lines = ["Configuration:"]
        for section, values in self._config.items():
            lines.append(f"  [{section}]")
            if isinstance(values, dict):
                for key, value in values.items():
                    lines.append(f"    {key}: {value}")
        return "\n".join(lines)


def load_config(config_path: Optional[str] = None,
                project_root: Optional[str] = None) -> Config:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to config YAML file. If None, uses config/default.yaml
        project_root: Project root directory. If None, uses CWD

    Returns:
        Config object

    Raises:
        FileNotFoundError: If config file not found
        yaml.YAMLError: If config file is invalid
        ValueError: If configuration validation fails
    """
    if project_root is None:
        project_root = os.getcwd()

    if config_path is None:
        config_path = os.path.join(project_root, "config", "default.yaml")

    if not os.path.isfile(config_path):
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    try:
        with open(config_path, "r") as f:
            config_dict = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config file: {e}")

    if not isinstance(config_dict, dict):
        raise ValueError("Configuration file must contain a YAML dictionary")

    return Config(config_dict, project_root)
