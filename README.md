<p align="center">
    <img src="images/icon.png" alt="Project icon"/>
</p>

<h1 align="center">Xythrion</h1>
<h3 align="center">Discord graphing bot</h3>

# Requirements
- Python 3.10
- [`python-poetry`](https://github.com/python-poetry/poetry)

## Optional Requirements
- [`docker`](https://github.com/docker/cli) and [`docker-compose`](https://github.com/docker/compose)
- [`podman`](https://github.com/containers/podman) and [`podman-compose`](https://github.com/containers/podman-compose)

# Setup

## Local Installation
1. Place your key in `BOT_TOKEN` in the `.env` file.
2. (For development) Install pre-commit hooks using `poetry run task precommit`.
3. Run `poetry run task start`.

## Docker/Podman Installation
1. Place your key in `BOT_TOKEN` in the `.env` file.
2. Run `docker-compose up bot` or `podman-compose up bot`.
