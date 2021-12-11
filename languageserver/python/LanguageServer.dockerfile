From python:3.9.5

ARG dir="/app"
WORKDIR $dir

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv lock -r -d > requirements.txt && \
    pip install -r requirements.txt && \
    pip install 'python-lsp-server[all]' pyls-flake8 pylsp-mypy

ENTRYPOINT ["pylsp"]
CMD ["--host", "0.0.0.0", "--port", "2087", "--tcp", "-v"]
