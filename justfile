
setup-dev:
    pip install pip-tools
    pip-sync requirements.txt requirements-dev.txt
    pre-commit install

test:
    python -m pytest

run:
    uvicorn app.main:app
