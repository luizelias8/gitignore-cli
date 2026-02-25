import requests

from gitignore_cli.exceptions import GitignoreAPIError


BASE_URL = 'https://www.toptal.com/developers/gitignore/api'


def fetch_gitignore(technologies: list[str]) -> str:
    """Busca o conteúdo .gitignore para as tecnologias fornecidas."""
    url = f'{BASE_URL}/{','.join(technologies)}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise GitignoreAPIError('Não foi possível conectar à API. Verifique sua conexão.')
    except requests.exceptions.Timeout:
        raise GitignoreAPIError('A requisição excedeu o tempo limite.')
    except requests.exceptions.HTTPError as e:
        raise GitignoreAPIError(f'Erro HTTP: {e}')
    return response.text


def fetch_list() -> list[str]:
    """Retorna a lista de todas os tecnologias disponíveis."""
    url = f'{BASE_URL}/list'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise GitignoreAPIError('Não foi possível conectar à API. Verifique sua conexão.')
    except requests.exceptions.Timeout:
        raise GitignoreAPIError('A requisição excedeu o tempo limite.')
    except requests.exceptions.HTTPError as e:
        raise GitignoreAPIError(f'Erro HTTP: {e}')

    # A API retorna as tecnologias separados por vírgula e newline. Exemplo:
    # python,node,linux
    # windows,macos
    # vscode
    raw = response.text

    technologies = [t.strip() for line in raw.splitlines() for t in line.split(',') if t.strip()]
    return sorted(technologies)
