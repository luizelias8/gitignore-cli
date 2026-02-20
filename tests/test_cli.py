# tests/test_cli.py

import pytest
from gitignore_cli.cli import main


def test_cli_list(monkeypatch, capsys):
    """
    Deve imprimir lista quando --list for usado.
    """

    def mock_list(self):
        return ['python', 'django']

    monkeypatch.setattr(
        'gitignore_cli.service.GitignoreService.list_supported',
        mock_list
    )

    monkeypatch.setattr('sys.argv', ['gitignore', '--list'])

    main()

    captured = capsys.readouterr()

    assert 'python' in captured.out


def test_cli_generate(monkeypatch, tmp_path, capsys):
    """
    Deve gerar arquivo corretamente via CLI.
    """

    def mock_generate(self, technologies, output):
        file_path = tmp_path / '.gitignore'
        file_path.write_text('# fake')
        return file_path

    monkeypatch.setattr(
        'gitignore_cli.service.GitignoreService.generate',
        mock_generate
    )

    monkeypatch.setattr('sys.argv', ['gitignore', 'python'])

    main()

    captured = capsys.readouterr()

    assert 'gerado com sucesso' in captured.out
