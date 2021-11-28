## Local Run

```
$ docker compose build

$ docker compose run --entrypoint "poetry install" app

# start FastAPI server on http://localhost:8000/
$ docker compose up

# DB Migration
$ docker compose exec app poetry run python -m src.migrate_db
```

## API Document

access to http://localhost:8000/docs
