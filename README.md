# Fastapi Essential Modules
Essential modules for developing applications with FastAPI.
This project uses [Python](https://www.python.org/) 3.10 as the environment and [Poetry](https://python-poetry.org/) as the package manager.


## Table of Contents
1. [Quickstart](#quickstart)
2. [Migration](#migration)

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
