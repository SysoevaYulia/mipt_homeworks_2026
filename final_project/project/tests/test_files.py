from pathlib import Path
from unittest.mock import patch, MagicMock
from src.file_mgr import process_files_in_text, chunk_file_generator  # type: ignore


def test_process_files_success(tmp_path: Path) -> None:
    test_file = tmp_path / 'test.txt'
    test_file.write_text('Secret Data', encoding='utf-8')

    input_text = f'Read this: @::{test_file}::'

    processed_text, error = process_files_in_text(input_text)

    assert error is None
    assert 'Secret Data' in processed_text
    assert '@::' not in processed_text


def test_process_files_not_found() -> None:
    input_text = 'Read this: @::/fake/path/to/nothing.txt::'

    processed_text, error = process_files_in_text(input_text)

    assert processed_text == input_text
    assert error is not None
    assert 'The file was not found' in error


def test_chunk_file_generator_by_len(tmp_path: Path) -> None:
    test_file = tmp_path / 'book.txt'
    test_file.write_text('1234567890', encoding='utf-8')

    chunks = list(chunk_file_generator(str(test_file), chunk_type='len', chunk_size=3))

    assert len(chunks) == 4
    assert chunks[0] == '123'
    assert chunks[1] == '456'
    assert chunks[2] == '789'
    assert chunks[3] == '0'


@patch('os.path.exists')
@patch('os.path.isfile')
@patch('os.path.getsize')
def test_process_files_too_large(
    mock_getsize: MagicMock, mock_isfile: MagicMock, mock_exists: MagicMock
) -> None:
    mock_exists.return_value = True
    mock_isfile.return_value = True
    mock_getsize.return_value = 6 * 1024 * 1024

    input_text = 'Check this big file @::huge.txt::'
    processed_text, error = process_files_in_text(input_text)

    assert error is not None
    assert 'The file is too large' in error


@patch('os.path.exists')
@patch('os.path.isfile')
def test_process_files_is_directory(mock_isfile: MagicMock, mock_exists: MagicMock) -> None:
    mock_exists.return_value = True
    mock_isfile.return_value = False

    input_text = 'Check this dir @::/my/folder::'
    processed_text, error = process_files_in_text(input_text)

    assert error is not None
    assert 'This path is not a file' in error


def test_chunk_file_generator_by_paragraph(tmp_path: Path) -> None:
    test_file = tmp_path / 'book.txt'
    content = 'Абзац 1\nАбзац 2\nАбзац 3'
    test_file.write_text(content, encoding='utf-8')

    chunks = list(chunk_file_generator(str(test_file), chunk_type='paragraph', chunk_size=2))

    assert len(chunks) == 2
    assert chunks[0] == 'Абзац 1\nАбзац 2'
    assert chunks[1] == 'Абзац 3'


@patch('os.path.exists', return_value=True)
@patch('os.path.isfile', return_value=True)
@patch('os.path.getsize', return_value=100)
@patch('builtins.open')
def test_process_files_unicode_error(
    mock_open: MagicMock, mock_getsize: MagicMock, mock_isfile: MagicMock, mock_exists: MagicMock
) -> None:
    mock_open.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, 'reason')

    processed_text, error = process_files_in_text('Check @::image.png::')

    assert error is not None
    assert 'Decode error' in error


@patch('os.path.exists', return_value=True)
@patch('os.path.isfile', return_value=True)
@patch('os.path.getsize', return_value=100)
@patch('builtins.open')
def test_process_files_generic_error(
    mock_open: MagicMock, mock_getsize: MagicMock, mock_isfile: MagicMock, mock_exists: MagicMock
) -> None:
    mock_open.side_effect = Exception('Disk failure')

    processed_text, error = process_files_in_text('Check @::file.txt::')

    assert error is not None
    assert 'An error has occured' in error
