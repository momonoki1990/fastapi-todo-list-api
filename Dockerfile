FROM python:3.10-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY src ./src

RUN poetry config virtualenvs.in-project true

RUN poetry install

ENTRYPOINT ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "src.main:app", "--reload"]