import pytest


MOCK_GITIGNORE_CONTENT = """\
# Created by https://www.toptal.com/developers/gitignore/api/python
# Edit at https://www.toptal.com/developers/gitignore?templates=python

### Python ###
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
"""


@pytest.fixture
def mock_gitignore_content():
    return MOCK_GITIGNORE_CONTENT
