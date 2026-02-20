import pytest
import responses
import requests

from gitignore_cli.api import fetch_gitignore, fetch_list
from gitignore_cli.exceptions import GitignoreAPIError

BASE_URL = 'https://www.toptal.com/developers/gitignore/api'


@responses.activate
def test_fetch_gitignore_single_template(mock_gitignore_content):
    responses.add(responses.GET, f'{BASE_URL}/python', body=mock_gitignore_content, status=200)

    result = fetch_gitignore(['python'])

    assert result == mock_gitignore_content


@responses.activate
def test_fetch_gitignore_multiple_templates(mock_gitignore_content):
    responses.add(responses.GET, f'{BASE_URL}/python,node', body=mock_gitignore_content, status=200)

    result = fetch_gitignore(['python', 'node'])

    assert result == mock_gitignore_content


@responses.activate
def test_fetch_gitignore_http_error():
    responses.add(responses.GET, f'{BASE_URL}/invalid', status=500)

    with pytest.raises(GitignoreAPIError, match='Erro HTTP'):
        fetch_gitignore(['invalid'])


@responses.activate
def test_fetch_gitignore_connection_error():
    responses.add(responses.GET, f'{BASE_URL}/python', body=requests.exceptions.ConnectionError())

    with pytest.raises(GitignoreAPIError, match='conectar'):
        fetch_gitignore(['python'])


@responses.activate
def test_fetch_list_returns_sorted_list():
    responses.add(responses.GET, f'{BASE_URL}/list', body='node,python\nmacos,vscode', status=200)

    result = fetch_list()

    assert result == ['macos', 'node', 'python', 'vscode']
    assert result == sorted(result)


@responses.activate
def test_fetch_list_http_error():
    responses.add(responses.GET, f'{BASE_URL}/list', status=503)

    with pytest.raises(GitignoreAPIError, match='Erro HTTP'):
        fetch_list()
