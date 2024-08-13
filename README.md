# TELETWEET
A telegram bot that uses twitter API to create tweets

## setting up env variables
```
cp .env.example .env
```

## running locally with poetry
requirements:
    - poetry

run 
```
poetry install
poetry run flask --app app.py run
```

## running with docker
requirements:
    - docker

```
docker build -t teletweet .
docker run -it -p 8000:5000 teletweet

```

