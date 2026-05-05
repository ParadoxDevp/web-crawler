import yaml
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
    
    def load(self, cli_overrides=None):
        """Load config from YAML and merge with CLI overrides."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in config file: {e}")
        
        if not config.get('seed_urls') or not isinstance(config['seed_urls'], list):
            raise ValueError("Config must contain 'seed_urls' as a non-empty list")
        
        if cli_overrides:
            config = self._deep_merge(config, cli_overrides)
        
        logger.info(f"Loaded configuration from {self.config_path}")
        return config
    
    def _deep_merge(self, base, override):
        """Deep merge override dict into base dict."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
