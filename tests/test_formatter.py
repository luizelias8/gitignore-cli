import os
from gitignore_cli.formatter import format_list


def test_format_list_empty():
    assert format_list([]) == ''


def test_format_list_single_item():
    result = format_list(['python'])
    assert 'python' in result


def test_format_list_multiple_items():
    technologies = ['python', 'node', 'vscode', 'macos']
    result = format_list(technologies)
    for t in technologies:
        assert t in result


def test_format_list_terminal_estreito(monkeypatch):
    technologies = ['python', 'node', 'vscode', 'macos', 'linux', 'windows']

    def terminal_estreito(fallback=None):
        return os.terminal_size((20, 24))

    monkeypatch.setattr('shutil.get_terminal_size', terminal_estreito)

    result = format_list(technologies)

    assert len(result.splitlines()) >= 2


def test_format_list_terminal_largo(monkeypatch):
    technologies = ['python', 'node', 'vscode', 'macos', 'linux', 'windows']

    def terminal_largo(fallback=None):
        return os.terminal_size((200, 24))

    monkeypatch.setattr('shutil.get_terminal_size', terminal_largo)

    result = format_list(technologies)

    assert len(result.splitlines()) <= len(technologies)


def test_format_list_all_technologies_present():
    technologies = ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
    result = format_list(technologies)
    for t in technologies:
        assert t in result
