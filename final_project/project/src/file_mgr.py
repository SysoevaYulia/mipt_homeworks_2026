import os
import re
from typing import Generator

MAX_FILE_SIZE = 5 * 1024 * 1024


def process_files_in_text(text: str) -> tuple[str, str | None]:
    pattern = r'@::(.*?)::'
    matches = re.findall(pattern, text)

    if not matches:
        return text, None

    processed_text = text

    for filepath in matches:
        clean_path = filepath.strip()

        if not os.path.exists(clean_path):
            return text, f'The file was not found: {clean_path}'

        if not os.path.isfile(clean_path):
            return text, f'This path is not a file: {clean_path}'

        if os.path.getsize(clean_path) > MAX_FILE_SIZE:
            return text, f'The file is too large (bigger than 5 MB): {clean_path}'

        try:
            with open(clean_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            tag = f'@::{filepath}::'
            replacement = f'\n{file_content}\n'
            processed_text = processed_text.replace(tag, replacement, 1)

        except UnicodeDecodeError:
            return text, f'Decode error or there is not a text file: {clean_path}'
        except Exception as e:
            return text, f'An error has occured while reading the file {clean_path}: {e}'

    return processed_text, None


def chunk_file_generator(
    filepath: str, chunk_type: str = 'paragraph', chunk_size: int = 1
) -> Generator[str, None, None]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'the file was not found: {filepath}')

    with open(filepath, 'r', encoding='utf-8') as f:
        if chunk_type == 'len':
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

        elif chunk_type == 'paragraph':
            content = f.read()
            paragraphs = []
            raw_chunks = re.split(r'\n', content)
            for paragraph in raw_chunks:
                clean_paragraph = paragraph.strip()
                if clean_paragraph != '':
                    paragraphs.append(clean_paragraph)

            for i in range(0, len(paragraphs), chunk_size):
                yield '\n'.join(paragraphs[i : i + chunk_size])
