import pytest
from pathlib import Path

from gitignore_cli.service import GitignoreService
from gitignore_cli.exceptions import InvalidTechnologyError


def test_generate_creates_file(tmp_path, monkeypatch):
    """
    Deve gerar arquivo corretamente quando tecnologias válidas são informadas.
    """
    service = GitignoreService()

    # Mock da função fetch_gitignore
    def mock_fetch_gitignore(technologies):
        return '# conteúdo fake'

    monkeypatch.setattr(
        'gitignore_cli.service.fetch_gitignore',
        mock_fetch_gitignore
    )

    output_file = tmp_path / 'test.gitignore'

    result_path = service.generate(
        technologies=['python'],
        output=str(output_file)
    )

    assert output_file.exists()
    assert output_file.read_text(encoding='utf-8') == '# conteúdo fake'
    assert isinstance(result_path, Path)

def test_generate_without_technologies_raises_error():
    """
    Deve lançar erro se nenhuma tecnologia for informada.
    """
    service = GitignoreService()

    with pytest.raises(InvalidTechnologyError):
        service.generate(technologies=[])

def test_list_supported(monkeypatch):
    """
    Deve retornar lista de tecnologias corretamente.
    """
    service = GitignoreService()

    def mock_list():
        return ['python', 'django']

    monkeypatch.setattr(
        'gitignore_cli.service.fetch_supported_technologies',
        mock_list
    )

    result = service.list_supported()

    assert 'python' in result
