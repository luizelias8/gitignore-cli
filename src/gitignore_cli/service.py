from pathlib import Path

from gitignore_cli.api import fetch_gitignore, fetch_supported_technologies
from gitignore_cli.exceptions import InvalidTechnologyError


class GitignoreService:
    """
    Camada de serviço responsável pelas regras de negócio.
    """

    def generate(self, technologies: list[str], output: str | None = None) -> Path:
        """
        Gera o .gitignore e salva no arquivo de saída.
        """
        if not technologies:
            raise InvalidTechnologyError('Nenhuma tecnologia foi informada.')

        content = fetch_gitignore(technologies)

        output_path = Path(output) if output else Path.cwd() / '.gitignore'

        output_path.write_text(content, encoding='utf-8')

        return output_path.resolve()

    def list_supported(self) -> list[str]:
        """
        Retorna lista de tecnologias suportadas.
        """
        return fetch_supported_technologies()
