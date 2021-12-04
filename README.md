## Local Run

```
$ docker compose build

$ docker compose run --entrypoint "poetry install" app

# start FastAPI server on http://localhost:8000/
$ docker compose up

# DB Migration
$ docker compose exec app poetry run python -m src.migrate_db

# test
$ docker compose exec app poetry run tox
```

## API Document

access to http://localhost:8000/docs and try http request via "Try it out" button on the document.
