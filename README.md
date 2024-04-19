# Fastapi Essential Modules
Essential modules for developing applications with FastAPI.
This project uses [Python](https://www.python.org/) 3.10 as the environment and [Poetry](https://python-poetry.org/) as the package manager.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M0U28LL)

## Table of Contents
1. [Quickstart](#quickstart)
2. [Migration](#migration)
3. [Logging](#logging)
4. [Caching](#caching)

## Quickstart
1. Open Terminal in this directory.

2. Initialize the virtual environment by command:

    ```bash
    python -m venv venv  # py -m venv venv
    ```

3. Use virtual environment by the activation command:

    ```bash
    venv\Scripts\activate # For Mac user: source bin/activate
    ```

4. Install Poetry and update required packages:

    ```bash
    pip install poetry

    poetry update
    ```

5. Run the application

    ```bash
    uvicorn app.main:app --reload
    ```

## Migration

To add or initialize a module, you can use the following commands:

```bash
poetry add alembic  # pip install alembic

alembic init migrations
```

To create a new revision:
```bash
alembic revision --autogenerate -m "message"
```

To migrate:
```bash
alembic upgrade head
```

To undo the latest migration:
```bash
alembic downgrade -1
```

To roll back to a specific revision:
```bash
alembic downgrade <<revision_id>>
```

## Logging

Everything is wrapped up in a function (`app/core/logger.py`) and it's just a matter of calling the function when initializing the application.

```python
from app.core.logger import setup as setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start up
    setup_logging()
    yield
    # shut down
    pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)
```

See the example in `app/api/utils.py`.

Test with [curl](https://curl.se/).
```bash
curl --request POST \
  --url 'http://localhost:8000/api/v1/utils/logs?text=This%20is%20log'
```

## Caching

Install the [Redis](https://github.com/redis/redis-py) package.

```bash
poetry add redis   # pip install redis
```

Adapter for Redis: `app\core\redis.py`. To manage connections and disconnections to Redis

```python
from app.core.redis import redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start up
    await redis_client.connect(str(settings.REDIS_URL))
    yield
    # shut down
    await redis_client.disconnect()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)
```

Caching module: `app\core\cache.py`

See the example in `app\api\user.py`

Test with [curl](https://curl.se/).

```bash
# Insert 20000 users
curl --request POST \
  --url http://localhost:8000/api/v1/users/bulk/20000

# Get 20000 users
curl --request GET \
  --url 'http://localhost:8000/api/v1/users?limit=20000&skip=0'
```
