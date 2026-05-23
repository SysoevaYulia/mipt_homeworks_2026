from src.context_mgr import truncate_context  # type: ignore


def test_truncate_by_message_count() -> None:
    messages = [
        {'role': 'system', 'content': 'You are a bot'},
        {'role': 'user', 'content': 'msg1'},
        {'role': 'assistant', 'content': 'msg2'},
        {'role': 'user', 'content': 'msg3'},
    ]

    result = truncate_context(messages, limit_message=2, limit_chars=1000)

    assert len(result) == 3
    assert result[0]['role'] == 'system'
    assert result[1]['content'] == 'msg2'
    assert result[2]['content'] == 'msg3'


def test_truncate_by_char_count_remove_full_message() -> None:
    messages = [
        {'role': 'user', 'content': '1234567890'},
        {'role': 'assistant', 'content': '12345'},
    ]

    result = truncate_context(messages, limit_message=10, limit_chars=4)

    assert len(result) == 1
    assert result[0]['content'] == '2345'


def test_truncate_by_char_count_partial_trim() -> None:
    messages = [
        {'role': 'user', 'content': 'Hello world'},
    ]

    result = truncate_context(messages, limit_message=10, limit_chars=5)

    assert len(result) == 1
    assert result[0]['content'] == 'world'


def test_truncate_empty_messages() -> None:
    result = truncate_context([], limit_message=10, limit_chars=100)
    assert result == []


def test_truncate_only_system_prompt() -> None:
    messages = [{'role': 'system', 'content': 'Very long system prompt ' * 100}]
    result = truncate_context(messages, limit_message=0, limit_chars=10)

    assert len(result) == 1
    assert result[0]['role'] == 'system'


def test_truncate_exact_limit() -> None:
    messages = [{'role': 'user', 'content': '12345'}]
    result = truncate_context(messages, limit_message=10, limit_chars=5)

    assert len(result) == 1
    assert result[0]['content'] == '12345'
