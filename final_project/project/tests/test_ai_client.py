from unittest.mock import patch, MagicMock
from src.ai_client import AIAssistant


@patch('src.ai_client.OpenAI')
def test_generate_streaming_response(mock_openai_class):
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client

    chunk1 = MagicMock()
    chunk1.choices[0].delta.content = 'Привет, '

    chunk2 = MagicMock()
    chunk2.choices[0].delta.content = 'мир!'

    mock_client.chat.completions.create.return_value = [chunk1, chunk2]

    ai = AIAssistant(
        api_host='http://fake-host', api_key='fake-key', model='fake-model', temperature=0.7
    )

    messages = [{'role': 'user', 'content': 'Скажи Привет мир'}]

    response_generator = ai.generate_streaming_response(messages)

    result_text = ''
    for chunk in response_generator:
        result_text += chunk.choices[0].delta.content

    assert result_text == 'Привет, мир!'

    mock_client.chat.completions.create.assert_called_once_with(
        model='fake-model', messages=messages, temperature=0.7, stream=True
    )
