# FastAPI application notes

FastAPI uses Python type hints to define API request and response shapes. Pydantic validates input data and provides clear errors for malformed requests. A path operation connects a URL and an HTTP method to a Python function.

When an application starts, it can initialise local resources such as a SQLite database. For a production deployment, use a separate database migration process and configure authentication, HTTPS, logging and backups.
