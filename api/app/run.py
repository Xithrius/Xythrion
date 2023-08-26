"""
Entrypoint when running as a module, useful for development.

It is recommended that if this is deployed in production to use the uvicorn
    commandline rather than running as a Python module.

https://www.uvicorn.org/deployment/
https://www.uvicorn.org/deployment/#gunicorn
"""
import uvicorn


def main() -> None:
    """Run server with hot reloading."""
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
