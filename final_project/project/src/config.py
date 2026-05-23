import os
import sys
from typing import Any
import yaml  # type: ignore


def load_config() -> dict[str, Any]:
    config: dict[str, Any] = {}

    if os.path.exists('config.yaml'):
        try:
            with open('config.yaml', 'r', encoding='utf-8') as file:
                yaml_data = yaml.safe_load(file)
                if yaml_data:
                    config.update(yaml_data)
        except Exception as e:
            print(f'An error has occured while reading config.yaml: {e}')

    if not config and not os.environ.get('API_KEY'):
        sys.exit('Error: there is not neither os.environ.get nor config.yaml.')

    def get_required(env_name: str, yaml_name: str, cast_type: type = str) -> Any:
        val = os.environ.get(env_name, config.get(yaml_name))
        if val is None:
            sys.exit(f"Error: the required parameter '{yaml_name}' is not set!")
        return cast_type(val)

    final_config: dict[str, Any] = {
        'api_key': get_required('API_KEY', 'api_key'),
        'api_host': get_required('API_HOST', 'api_host'),
        'limit_message': get_required('LIMIT_MESSAGE', 'limit_message', int),
        'limit_chars': get_required('LIMIT_CHARS', 'limit_chars', int),
        'temperature': get_required('TEMPERATURE', 'temperature', float),
        'system_prompt': config.get('system_prompt', ''),
        'model': get_required('MODEL', 'model'),
    }

    return final_config
