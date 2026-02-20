import argparse
import sys
from pathlib import Path

from gitignore_cli.exceptions import GitignoreAPIError
from gitignore_cli.api import fetch_gitignore, fetch_list
from gitignore_cli.formatter import format_list
from gitignore_cli import __version__


def build_parser() -> argparse.ArgumentParser:
    """
    Cria e configura o parser de argumentos do CLI.
    """
    parser = argparse.ArgumentParser(
        prog='gitignore',
        description='Gerador profissional de .gitignore via API do Toptal',
        epilog='Exemplo: gitignore python node vscode -o .gitignore'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    parser.add_argument(
        'technologies',
        nargs='*',
        metavar='TECH',
        help='Tecnologias desejadas (ex: python django linux)'
    )

    parser.add_argument(
        '-o',
        '--output',
        metavar='PATH',
        help='Arquivo de saída (padrão: .gitignore no diretório atual)'
    )

    parser.add_argument(
        '--append',
        action='store_true',
        help='Concatena ao arquivo existente em vez de sobrescrever'
    )

    parser.add_argument(
        '-l',
        '--list',
        action='store_true',
        help='Lista as tecnologias suportadas'
    )

    return parser

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv) # Se argv for None, parse_args() usa sys.argv automaticamente

    if args.list:
        try:
            technologies = fetch_list()
        except GitignoreAPIError as e:
            print(f'Erro: {e}', file=sys.stderr)
            sys.exit(1)
        print(format_list(technologies))
        return

    if not args.technologies:
        parser.print_help()
        sys.exit(1)

    try:
        content = fetch_gitignore(args.technologies)
    except GitignoreAPIError as e:
        print(f'Erro: {e}', file=sys.stderr)
        sys.exit(1)

    # Define o caminho do arquivo de saída
    # Caso o usuário não informe -o/--output,
    # o padrão será ".gitignore" no diretório atual
    path = Path(args.output) if args.output else Path.cwd() / '.gitignore'

    # Escreve no arquivo:
    # - Se --append estiver ativo e o arquivo já existir,
    #   concatena o conteúdo ao final
    # - Caso contrário, sobrescreve
    if args.append and path.exists():
        existing_content = path.read_text()
        path.write_text(existing_content + '\n' + content)
        action = 'Conteúdo adicionado em'
    else:
        path.write_text(content)
        action = 'Arquivo gerado:'

    print(f'{action} {path}')


if __name__ == '__main__':
    main()
