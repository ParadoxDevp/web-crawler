import pytest
import yaml
from webcrawler.config_loader import ConfigLoader

def test_load_config_from_yaml(tmp_path):
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text("""
seed_urls:
  - "http://example.com"
concurrent_requests: 3
download_delay: 1.0
""")
    
    loader = ConfigLoader(str(config_file))
    config = loader.load()
    
    assert config['seed_urls'] == ["http://example.com"]
    assert config['concurrent_requests'] == 3
    assert config['download_delay'] == 1.0

def test_file_not_found_error():
    loader = ConfigLoader('nonexistent.yaml')
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        loader.load()

def test_invalid_yaml_error(tmp_path):
    config_file = tmp_path / "invalid.yaml"
    config_file.write_text("invalid: yaml: content:")
    
    loader = ConfigLoader(str(config_file))
    with pytest.raises(yaml.YAMLError, match="Invalid YAML"):
        loader.load()

def test_missing_seed_urls(tmp_path):
    config_file = tmp_path / "no_seeds.yaml"
    config_file.write_text("concurrent_requests: 3")
    
    loader = ConfigLoader(str(config_file))
    with pytest.raises(ValueError, match="seed_urls"):
        loader.load()

def test_empty_seed_urls(tmp_path):
    config_file = tmp_path / "empty_seeds.yaml"
    config_file.write_text("seed_urls: []")
    
    loader = ConfigLoader(str(config_file))
    with pytest.raises(ValueError, match="non-empty list"):
        loader.load()

def test_cli_overrides_deep_merge(tmp_path):
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text("""
seed_urls:
  - "http://example.com"
settings:
  timeout: 30
  retries: 3
""")
    
    loader = ConfigLoader(str(config_file))
    config = loader.load(cli_overrides={'settings': {'timeout': 60}})
    
    assert config['settings']['timeout'] == 60
    assert config['settings']['retries'] == 3
