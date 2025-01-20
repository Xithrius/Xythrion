# Xythrion

Archived in favor of splitting up the repository and including it in [infra.xithrius.cloud](https://github.com/Xithrius/infra.xithrius.cloud).

API: https://github.com/Xithrius/xythrion-api

Bot: https://github.com/Xithrius/xythrion-bot

</div>

# Installation

## Requirements

### Docker installation

- [`docker`](https://github.com/docker/cli) and [`docker-compose`](https://github.com/docker/compose)

### Local installation

- Postgres
- Python 3.12
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

2. Place your key in `XYTHRION_BOT_TOKEN` in the `.env` file, and whatever prefix you'd like (such as `";"`) into `XYTHRION_BOT_PREFIX`

### Local Installation

1. (For development) Install pre-commit hooks using `pdm precommit`
2. (first time installation) run `pdm upgrade` to run database migrations
3. Run the API via `pdm api`
4. Finally get the bot up by `pdm bot`

### Docker/Podman Installation

1. Run `docker compose up -d`
2. (If in a production environment) run `loginctl enable-linger` such that detached containers don't exit when you logout
3. (Optional) run all the Grafana/Prometheus/Tempo/Loki containers from [infra.xithrius.cloud](https://github.com/Xithrius/infra.xithrius.cloud) to get realtime metrics.
