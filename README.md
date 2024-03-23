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

# Installation

## Requirements

### Docker installation

- [`docker`](https://github.com/docker/cli) and [`docker-compose`](https://github.com/docker/compose)

### Local installation

- Postgres
- Python 3.11
- [`python-pdm`](https://github.com/pdm-project/pdm)

## Bringing up of [infra.xithrius.cloud](https://github.com/Xithrius/infra.xithrius.cloud)

1. Cloning

```bash
git clone https://github.com/Xithrius/infra.xithrius.cloud
```

2. Environment variables

```bash
cp .env.sample .env
```

Put a password into `POSTGRES_PASSWORD` and `"infra"` into `POSTGRES_USER`

> [!IMPORTANT]
> If you're setting up for production, you can place a discord webhook into `WATCHTOWER_NOTIFICATION_URL` if you plan to use watchtower.

3. Creating the Postgres container

```bash
cd infra.xithrius.cloud/scripts
./create-networks.sh
./setup-postgres.sh infra xythrion xythrion xythrion
```

## Bringing up of this repo

1. Copy the `.env.sample` file to `.env`

```bash
cp .env.sample .env
```

2. Place your key in `BOT_TOKEN` in the `.env` file, and whatever prefix you'd like (such as `";"`) into `BOT_PREFIX`

### Local Installation

1. (For development) Install pre-commit hooks using `pdm precommit`
2. (first time installation) run `pdm upgrade` to run database migrations
3. Run the API via `pdm api`
4. Finally get the bot up by `pdm bot`

### Docker/Podman Installation

1. Run `docker compose up -d`
2. (If in a production environment) run `loginctl enable-linger` such that detached containers don't exit when you logout
3. (Optional) run all the Grafana/Prometheus/Tempo/Loki containers from [infra.xithrius.cloud](https://github.com/Xithrius/infra.xithrius.cloud) to get realtime metrics.
