import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath('src'))

from main import get_initial_messages, clear_console, print_welcome  # type: ignore


def test_get_initial_messages() -> None:
    config_with_sys = {'system_prompt': 'You are helpful'}
    msgs = get_initial_messages(config_with_sys)
    assert len(msgs) == 1
    assert msgs[0]['role'] == 'system'

    config_without_sys = {'system_prompt': ''}
    msgs = get_initial_messages(config_without_sys)
    assert len(msgs) == 0


@patch('os.system')
def test_clear_console(mock_system: MagicMock) -> None:
    clear_console()
    mock_system.assert_called_once()


@patch('builtins.print')
def test_print_welcome(mock_print: MagicMock) -> None:
    print_welcome()
    assert mock_print.call_count == 2
