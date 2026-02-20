# gitignore-cli

CLI para gerar arquivos `.gitignore` a partir da API do [gitignore.io](https://www.toptal.com/developers/gitignore).

## Requisitos

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Instalação

```bash
git clone https://github.com/luizelias8/gitignore-cli.git
cd gitignore-cli
uv sync
```

## Uso

**Gerar e imprimir no terminal:**
```bash
gitignore python node vscode
```

**Salvar direto em arquivo:**
```bash
gitignore python node vscode -o .gitignore
```

**Adicionar tecnologias a um `.gitignore` existente:**
```bash
gitignore macos -o .gitignore --append
```

**Listar todos as tecnologias disponíveis:**
```bash
gitignore --list
```

**Ver a versão instalada:**
```bash
gitignore --version
```

## Opções

| Opção | Descrição |
|---|---|
| `TEMPLATE ...` | Um ou mais templates a incluir |
| `-o, --output ARQUIVO` | Arquivo de destino (padrão: stdout) |
| `--append` | Concatena ao arquivo existente em vez de sobrescrever |
| `-l, --list` | Lista todos os templates disponíveis |
| `--version` | Exibe a versão instalada |

## Desenvolvimento

Instalar dependências incluindo as de desenvolvimento:

```bash
uv sync
```

Rodar os testes:

```bash
uv run pytest
```

Rodar os testes com output detalhado:

```bash
uv run pytest -v
```

## Estrutura do projeto

```
gitignore-cli/
├── src/
│   └── gitignore_cli/
│       ├── __init__.py      # versão do pacote
│       ├── cli.py           # argparse e orquestração
│       ├── api.py           # comunicação com a API
│       └── formatter.py     # formatação do output
├── tests/
│   ├── conftest.py
│   ├── test_cli.py
│   ├── test_api.py
│   └── test_formatter.py
├── pyproject.toml
└── README.md
```
