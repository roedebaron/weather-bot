# weather-bot

Discord bot that keeps you updated when it is going to rain 🌧

<img src="rainy_forecast_message.png" width=40%>

Weather forecasts are fetched from the [YR API](https://developer.yr.no/).

Features:

- Get notified about the weather forecast for today or tomorrow at a custom time every day
- Ask for the current weather

## Local setup

Create environment

```
conda create --name weatherbot --file requirements.txt python=3.10
conda activate weatherbot
```

Set up environment config

- Insert Discord bot token and a default lat/lon into `example.env` (see [Using a database](using-a-database-not-implemented) for using a database to store a default coordinate for each guild)
- Rename the file to `.env`
  - Or a use a custom name (e.g. `dev.env` or `prod.env`). For a custom named and/or located .env file, the path should be given as argument when running the bot using the `-e` option e.g. `-e dev.env`

Run

```
python main.py
```

Run with a custom named environment file called `dev.env`

```
python main.py -e dev.env
```

### Running with docker

The environment file should be placed on host and is mounted into the container. Please modify the path specified under `volumes` in the docker-compose files. You should modify the image name in `docker-compose.yml` such that it links to your own Docker Hub repository.

The following assumes your are in the `docker` folder

#### dev

Modify local path of .env file under `volumes` in `docker-compose.override.yml`, then run

```
docker-compose up --build
```

#### prod

Modify local path of .env file under `volumes` in `docker-compose.prod.yml`. When using the docker-compose file for production, the environemnt path can also be specified by setting $ENV_PATH environment variable. Then run:

```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

### Running the CICD pipeline

The CICD pipeline will deploy the bot on your server. Please inspect `.github/workflows/deploy.yaml` for the required environment variables that should be set up in your Github repository as well as the assumptions made about the file structure of the repo and server.

### Using a database (NOT IMPLEMENTED)

Instead of using static coordinates, it is possible to store a default location for each guild in a database. Add the database credentials in the `.env` file and remember to set `DB_ENABLED=TRUE`.

## Remarks

- All requests to the YR API are cached with respect to their individual `Expire` response header to comply with the YR TOS. As such, muliple forecast requests for the same coordinate will only result in a single http request until the response expires (typically 0.5 hour it seems). The cache will be stored as a sqlite db and placed in the root folder.
