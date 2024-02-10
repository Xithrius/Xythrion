<div align="center">

<img src="images/icon.png" width=256/>

# Xythrion

A graphing bot built with [`discord.py`](https://github.com/Rapptz/discord.py).

[![MIT][s1]][l1] [![CI][s2]][l2] [![pre-commit.ci status][s3]][l3] [![codecov][s4]][l4]

[s1]: https://img.shields.io/badge/License-MIT-blue.svg
[l1]: https://opensource.org/licenses/MIT
[s2]: https://github.com/Xithrius/Xythrion/actions/workflows/ci.yml/badge.svg
[l2]: https://github.com/Xithrius/Xythrion/actions/workflows/ci.yml
[s3]: https://results.pre-commit.ci/badge/github/Xithrius/Xythrion/main.svg
[l3]: https://results.pre-commit.ci/latest/github/Xithrius/Xythrion/main
[s4]: https://codecov.io/gh/Xithrius/Xythrion/graph/badge.svg?token=J03UIHW314
[l4]: https://codecov.io/gh/Xithrius/Xythrion

</div>

## Requirements

- Python 3.11
- [`python-pdm`](https://github.com/pdm-project/pdm)

### Optional Requirements

- [`docker`](https://github.com/docker/cli) and [`docker-compose`](https://github.com/docker/compose)
- [`podman`](https://github.com/containers/podman) and [`podman-compose`](https://github.com/containers/podman-compose)

## Setup

### Local Installation

1. Place your key in `BOT_TOKEN` in the `.env` file.
2. (For development) Install pre-commit hooks using `pdm precommit`.
3. Run `pdm api` to start the api, and `pdm bot` to run the bot.

### Docker/Podman Installation

1. Place your key in `BOT_TOKEN` in the `.env` file.
2. Run `docker-compose up bot` or `podman-compose up bot`.
