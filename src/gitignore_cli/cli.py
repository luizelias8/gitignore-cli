import argparse
import sys

from gitignore_cli.exceptions import GitignoreError
from gitignore_cli.service import GitignoreService


__version__ = '0.1.0'


def main() -> None:
    """
    Ponto de entrada do CLI.
    """
    parser = argparse.ArgumentParser(
        prog='gitignore',
        description='Gerador profissional de .gitignore via API do Toptal'
    )

    parser.add_argument(
        'technologies',
        nargs='*',
        metavar='TECH',
        help='Tecnologias desejadas (ex: python django linux)'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='Lista as tecnologias suportadas'
    )

    parser.add_argument(
        '-o', '--output',
        metavar='PATH',
        help='Arquivo de saída (padrão: .gitignore no diretório atual)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    args = parser.parse_args()

    service = GitignoreService()

    try:
        if args.list:
            technologies = service.list_supported()
            print('\n'.join(technologies))
            return

        output_path = service.generate(
            technologies=args.technologies,
            output=args.output
        )

        print(f'.gitignore gerado com sucesso em: {output_path}')

    except GitignoreError as exc:
        print(f'Erro: {exc}')
        sys.exit(1)


if __name__ == '__main__':
    main()
