import os
from config import load_config
from context_mgr import truncate_context
from ai_client import AIAssistant
from file_mgr import process_files_in_text
from commands import get_initial_messages, process_chat_streaming, handle_file_chunk_mode


def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def print_welcome() -> None:
    print('=== The AI-assistant is running ===')
    print('Available commands: \\q (exit), /reset (reset dialog), /file_chunk (chunk mode)')


def main() -> None:
    config = load_config()

    ai = AIAssistant(
        api_host=config['api_host'],
        api_key=config['api_key'],
        model=config['model'],
        temperature=config['temperature'],
    )

    messages = get_initial_messages(config)
    print_welcome()

    while True:
        user_input = input('>>> ').strip()

        if not user_input:
            continue

        if user_input == '\\q':
            print('Program exit...')
            break

        elif user_input == '/reset':
            messages = get_initial_messages(config)
            clear_console()
            print('=== The dialog has been reset. New chat started ===')
            print_welcome()
            continue

        elif user_input.startswith('/file_chunk'):
            handle_file_chunk_mode(ai, user_input, config)
            print('\nReturning to the main chat.')
            continue

        processed_input, error_msg = process_files_in_text(user_input)

        if error_msg:
            print(f'[Error]: {error_msg}')
            print('Please, check the path and try one more time')
            continue

        messages.append({'role': 'user', 'content': processed_input})
        messages = truncate_context(messages, config['limit_message'], config['limit_chars'])

        try:
            assistant_reply = process_chat_streaming(ai, messages)
        except KeyboardInterrupt as e:
            assistant_reply = str(e) if e.args else ''

        if assistant_reply is not None:
            if assistant_reply:
                messages.append({'role': 'assistant', 'content': assistant_reply})
        else:
            messages.pop()


if __name__ == '__main__':
    main()
