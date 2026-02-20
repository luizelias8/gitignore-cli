import os
import pytest

from gitignore_cli.cli import build_parser, main
from gitignore_cli.exceptions import GitignoreAPIError


# --- Parser ---

def test_parser_technologies_posicional():
    args = build_parser().parse_args(['python', 'node'])
    assert args.technologies == ['python', 'node']


def test_parser_flag_list():
    args = build_parser().parse_args(['--list'])
    assert args.list is True


def test_parser_flag_output():
    args = build_parser().parse_args(['python', '-o', '.gitignore'])
    assert args.output == '.gitignore'


def test_parser_flag_append():
    args = build_parser().parse_args(['python', '--append'])
    assert args.append is True


def test_parser_sem_argumentos():
    args = build_parser().parse_args([])
    assert args.technologies == []
    assert args.list is False


# --- main() com --list ---

def test_main_list_imprime_technologies(capsys, monkeypatch):
    def fetch_list_mock():
        return ['node', 'python']

    def format_list_mock(technologies):
        return 'node  python'

    monkeypatch.setattr('gitignore_cli.cli.fetch_list', fetch_list_mock)
    monkeypatch.setattr('gitignore_cli.cli.format_list', format_list_mock)

    main(['--list'])

    assert 'node  python' in capsys.readouterr().out


def test_main_list_erro_de_api(capsys, monkeypatch):
    def fetch_list_erro():
        raise GitignoreAPIError('sem conexão')

    monkeypatch.setattr('gitignore_cli.cli.fetch_list', fetch_list_erro)

    with pytest.raises(SystemExit) as exc_info:
        main(['--list'])

    assert exc_info.value.code == 1
    assert 'sem conexão' in capsys.readouterr().err


# --- main() com technologies ---

def test_main_gera_gitignore_para_stdout(tmp_path, monkeypatch, mock_gitignore_content, capsys):
    # Mock da função fetch_gitignore
    def fetch_gitignore_mock(technologies):
        return mock_gitignore_content

    monkeypatch.setattr('gitignore_cli.cli.fetch_gitignore', fetch_gitignore_mock)

    # Muda o diretório de trabalho para um diretório temporário
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        main(['python'])
        # Verifica se o arquivo foi criado e tem o conteúdo esperado
        arquivo = tmp_path / '.gitignore'
        assert arquivo.exists()
        assert arquivo.read_text() == mock_gitignore_content

        # Verifica se a mensagem impressa contém o caminho do arquivo
        out = capsys.readouterr().out
        assert 'Arquivo gerado:' in out
        assert str(arquivo) in out
    finally:
        os.chdir(old_cwd)


def test_main_gera_gitignore_para_arquivo(tmp_path, monkeypatch, mock_gitignore_content):
    output_file = tmp_path / '.gitignore'

    def fetch_gitignore_mock(technologies):
        return mock_gitignore_content

    monkeypatch.setattr('gitignore_cli.cli.fetch_gitignore', fetch_gitignore_mock)

    main(['python', '-o', str(output_file)])

    assert output_file.read_text() == mock_gitignore_content


def test_main_append_concatena_ao_arquivo_existente(tmp_path, monkeypatch, mock_gitignore_content):
    output_file = tmp_path / '.gitignore'
    output_file.write_text('# conteúdo anterior\n')

    def fetch_gitignore_mock(technologies):
        return mock_gitignore_content

    monkeypatch.setattr('gitignore_cli.cli.fetch_gitignore', fetch_gitignore_mock)

    main(['python', '-o', str(output_file), '--append'])

    content = output_file.read_text()
    assert '# conteúdo anterior' in content
    assert mock_gitignore_content in content


def test_main_sem_technologies_sai_com_erro():
    with pytest.raises(SystemExit) as exc_info:
        main([])

    assert exc_info.value.code == 1


def test_main_erro_de_api_ao_gerar(capsys, monkeypatch):
    def fetch_gitignore_erro(technologies):
        raise GitignoreAPIError('timeout')

    monkeypatch.setattr('gitignore_cli.cli.fetch_gitignore', fetch_gitignore_erro)

    with pytest.raises(SystemExit) as exc_info:
        main(['python'])

    assert exc_info.value.code == 1
    assert 'timeout' in capsys.readouterr().err
