From python:3.9.5 AS builder

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv lock -r -d > requirements.txt


FROM python:3.9.5-slim

WORKDIR /app

COPY --from=builder /app/requirements.txt .

RUN pip install -r requirements.txt && \
    pip install 'python-language-server[all]'

ENTRYPOINT ["pyls"]
CMD ["--host", "0.0.0.0", "--port", "2087", "--tcp", "-v"]
