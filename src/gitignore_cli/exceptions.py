class GitignoreError(Exception):
    """Erro base do domínio da aplicação."""
    pass


class APIRequestError(GitignoreError):
    """Erro ao comunicar com a API."""
    pass


class InvalidTechnologyError(GitignoreError):
    """Tecnologia inválida ou não encontrada."""
    pass
