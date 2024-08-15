# TELETWEET
A telegram bot that uses twitter API to create tweets

## setting telegram webhook

You'll need to tell your telegram bot to call the appropriate URL when sending an update as a POST request. To do this, use the following command:

```bash
curl https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={url_to_send_updates_to}
```
Alternatively, if you don't want to use a webhook, you can use de `no-webhook` branch.

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
