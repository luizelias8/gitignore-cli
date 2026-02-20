import requests

from gitignore_cli.exceptions import APIRequestError


BASE_URL = 'https://www.toptal.com/developers/gitignore/api'


def fetch_gitignore(technologies: list[str]) -> str:
    """
    Realiza requisição à API para gerar o .gitignore.
    """
    tech_string = ','.join(technologies)
    url = f'{BASE_URL}/{tech_string}'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text

        return content

    except requests.RequestException as exc:
        # Utilizamos "raise ... from exc" para manter o encadeamento explícito
        # de exceções (exception chaining). Dessa forma, preservamos a exceção
        # original do requests como causa raiz (__cause__), mantendo o traceback
        # completo e facilitando debug e observabilidade.
        #
        # Sem o "from exc", perderíamos o erro original (timeout, DNS, conexão, etc.).
        raise APIRequestError(
            f'Falha ao comunicar com a API: {exc}'
        ) from exc


def fetch_supported_technologies() -> list[str]:
    """
    Obtém lista de tecnologias suportadas.
    """
    url = f'{BASE_URL}/list'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # A API retorna uma lista separada por quebras de linha
        technologies = response.text.splitlines()

        return sorted(technologies)

    except requests.RequestException as exc:
        # Encadeamento explícito da exceção para preservar a causa original.
        # Isso mantém o traceback completo (erro real de rede) enquanto
        # expomos um erro semântico da aplicação (APIRequestError).
        # Facilita debug, logs estruturados e testes.
        raise APIRequestError(
            f'Falha ao obter lista de tecnologias: {exc}'
        ) from exc
