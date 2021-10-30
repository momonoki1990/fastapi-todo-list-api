FROM python:3.10-buster

WORKDIR /usr/src/app

RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false
RUN if [ -f pyproject.toml ]; then poetry install; fi

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "src.main:app", "--reload"]