from typing import Any
from file_mgr import chunk_file_generator
from ai_client import AIAssistant


def get_initial_messages(config: dict[str, Any]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    if config['system_prompt']:
        messages.append({'role': 'system', 'content': config['system_prompt']})
    return messages


def process_chat_streaming(ai: AIAssistant, messages: list[dict[str, str]]) -> str | None:
    assistant_reply = ''
    print('Assistant: ', end='', flush=True)

    try:
        response_generator = ai.generate_streaming_response(messages)
        for chunk in response_generator:
            text_chunk = chunk.choices[0].delta.content
            if text_chunk is not None:
                print(text_chunk, end='', flush=True)
                assistant_reply += text_chunk
        print()
        return assistant_reply

    except KeyboardInterrupt:
        print('\n[The generation was interrupted by the user]')
        raise KeyboardInterrupt(assistant_reply)

    except Exception as e:
        print(f'\nError accessing the API: {e}')
        return None


def handle_file_chunk_mode(ai: AIAssistant, user_input: str, config: dict[str, Any]) -> None:
    parts = user_input.split()
    chunk_type = 'paragraph'
    chunk_size = 1
    auto_yes = '-y' in parts

    for part in parts:
        if part.startswith('paragraph='):
            chunk_type = 'paragraph'
            chunk_size = int(part.split('=')[1])
        elif part.startswith('len='):
            chunk_type = 'len'
            chunk_size = int(part.split('=')[1])

    filepath = input('Enter the path to file\n>>> ').strip()

    print('Accepted. What should I do for each fragment (User Prompt)?')
    prompt = input('>>> ').strip()

    print('Accepted. Processing is started...')

    try:
        chunks = chunk_file_generator(filepath, chunk_type, chunk_size)

        for i, chunk_text in enumerate(chunks, 1):
            print(f'\n--- Processing the chunk #{i} ---')

            chunk_messages = get_initial_messages(config)

            full_prompt = f'{prompt}\n\nFragment text:\n{chunk_text}'
            chunk_messages.append({'role': 'user', 'content': full_prompt})

            try:
                process_chat_streaming(ai, chunk_messages)
            except KeyboardInterrupt:
                print('\n[Chunk processing aborted by user]')
                break

            if not auto_yes:
                try:
                    action = input('<Press Enter for the next chunk or enter \\q for exit>')
                    if action.strip() == '\\q':
                        print('Exit from /file_chunk mode.')
                        break
                except KeyboardInterrupt:
                    print('\nExit from /file_chunk mode.')
                    break

        print('\nProcessing is ended.')

    except FileNotFoundError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'An unexpected error has occurred: {e}')
