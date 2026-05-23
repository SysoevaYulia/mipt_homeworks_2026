import pytest
from typing import Any
from unittest.mock import patch, MagicMock
from src.config import load_config  # type: ignore


@patch('os.environ.get')
@patch('os.path.exists')
def test_load_config_missing_everything(mock_exists: MagicMock, mock_env_get: MagicMock) -> None:
    mock_exists.return_value = False
    mock_env_get.return_value = None

    with pytest.raises(SystemExit) as exc_info:
        load_config()

    assert 'Error: there is not neither os.environ.get nor config.yaml' in str(exc_info.value)


@patch('os.environ.get')
@patch('os.path.exists')
def test_load_config_missing_required_param(
    mock_exists: MagicMock, mock_env_get: MagicMock
) -> None:
    mock_exists.return_value = False

    def fake_env_get(key: str, default: Any = None) -> Any:
        if key == 'API_KEY':
            return 'fake-key'
        return None

    mock_env_get.side_effect = fake_env_get

    with pytest.raises(SystemExit) as exc_info:
        load_config()

    assert 'Error: the required parameter' in str(exc_info.value)


@patch('os.path.exists')
@patch('os.environ.get')
def test_load_config_success(mock_env_get: MagicMock, mock_exists: MagicMock) -> None:
    mock_exists.return_value = False

    def fake_env_get(key: str, default: Any = None) -> Any:
        params = {
            'API_KEY': '123',
            'API_HOST': 'http://localhost',
            'LIMIT_MESSAGE': '10',
            'LIMIT_CHARS': '1000',
            'TEMPERATURE': '0.7',
            'MODEL': 'test-model',
        }
        return params.get(key, default)

    mock_env_get.side_effect = fake_env_get

    config = load_config()

    assert config['api_key'] == '123'
    assert config['limit_message'] == 10
    assert config['temperature'] == 0.7


@patch('os.path.exists')
@patch('builtins.open')
@patch('yaml.safe_load')
@patch('os.environ.get')
def test_load_config_with_yaml(
    mock_env_get: MagicMock, mock_yaml_load: MagicMock, mock_open: MagicMock, mock_exists: MagicMock
) -> None:
    mock_exists.return_value = True

    mock_yaml_load.return_value = {
        'api_key': 'yaml-key',
        'api_host': 'http://yaml-host',
        'limit_message': 15,
        'limit_chars': 1500,
        'temperature': 0.5,
        'model': 'yaml-model',
        'system_prompt': 'yaml-prompt',
    }

    mock_env_get.side_effect = lambda key, default=None: default

    config = load_config()

    assert config['api_key'] == 'yaml-key'
    assert config['limit_message'] == 15
    assert config['system_prompt'] == 'yaml-prompt'
