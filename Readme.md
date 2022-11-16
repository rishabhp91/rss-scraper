# RSS Scraper

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is RSS scraper project for managing RSS Feeds. It's built using [cookiecutter-django-rest](https://github.com/agconti/cookiecutter-django-rest).

## Highlights

- Modern Python development with Python 3.8+
- Bleeding edge Django 3.1+
- Fully dockerized, local development via docker-compose.
- PostgreSQL
- Few test coverage
- Celery tasks

### Features built-in

- JSON Web Token authentication using [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- API Throttling enabled
- Swagger API docs out-of-the-box
- Code formatter [black](https://black.readthedocs.io/en/stable/)
- Tests (with mocking)

## API Docs

API documentation is automatically generated using Swagger. You can view documention by visiting this [link](http://localhost:8080/openapi?format=openapi-json).

## Prerequisites

If you are familiar with Docker, then you just need [Docker](https://docs.docker.com/docker-for-mac/install/). If you don't want to use Docker, then you just need Python3 and Postgres installed.

## Local Development with Docker

Start the dev server for local development:

```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

### Run migration

```bash
docker-compose run --rm web python manage.py migrate
```

### Create superuser

If you want, you can create initial super-user with next commad:

```bash
docker-compose run --rm web python manage.py createsuperuser
```
```
Username (leave blank to use 'root'): admin
Email address: example@sendcloud.com
Password: 
Password (again): 
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

### Running Tests

To run all tests with code-coverate report, simple run:

```bash
docker-compose run --rm web ./manage.py test
```

## Curl commands to try:
##### Get Token

```
curl -XPOST http://0.0.0.0:8080/login -d 'username=admin&password=pass'
```

##### Token Auth
```
curl -XPOST http://0.0.0.0:8080/v1/feeds -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"name": "Feed1", "url":"http://www.nu.nl/rss/Algemeen"}'
```

##### Basic Auth

```
curl --user "admin:pass" -XPOST http://0.0.0.0:8080/v1/feeds  -d '{"name": "Feed1", "url":"http://www.nu.nl/rss/Algemeen"}'
```

##### Add RSS feed
```
curl -XPOST http://0.0.0.0:8080/v1/feeds -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"name": "Feed1", "url":"http://www.nu.nl/rss/Algemeen"}'
```

##### List all RSS feeds
```
curl -XGET http://0.0.0.0:8080/v1/feeds -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc'
```

##### List my RSS feeds
```
curl -XGET http://0.0.0.0:8080/v1/feeds?owned=1 -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc'
```

##### List a RSS feed
```
curl -XGET http://0.0.0.0:8080/v1/feeds/${FEED_UUID} -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc'
```

##### Update a RSS feed
```
curl -XPUT http://0.0.0.0:8080/v1/feeds/${FEED_UUID} -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"name": "SendCloud - Test", "is_active": false}'
```

##### Delete a RSS feed
```
curl -XDELETE http://0.0.0.0:8080/v1/feeds/${FEED_UUID_TO_DELETE} -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc'
```

##### Filter read/unread feed items globally (order by date)
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/filters -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"is_read": true}'
```
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/filters -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"is_read": false}'
```
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/filters -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{}'
```

##### Filter read/unread feed items from specific feed (order by date)
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/filters -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"is_read": true}'
```
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/filters -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"is_read": false}'
```
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/filters -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{}'
```

##### Get a feed item
```
curl -XGET http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/items/10 -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc'
```

##### Mark feed item as read/unread
```
curl -XPUT http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/items/10/actions -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"is_read": true}'
```
```
curl -XPUT http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/items/10/actions -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"is_read": false}'
```
```
curl -XPUT http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/items/10/actions -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{}'
```

##### Follow / Unfollow / Force Update RSS
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/actions -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"is_followed": true}'
```
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/actions -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"is_followed": false}'
```
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/actions -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"force_extract": true}'
```
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/actions -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"force_extract": false}'
```
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/actions -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{}'
```

##### Filter read/unread feed items from specific feed (order by date)
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/filters -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"is_read": true}'
```
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/filters -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{"is_read": false}'
```
```
curl -XPOST http://0.0.0.0:8080/v1/feeds/${FEED_UUID}/filters -H 'Authorization: Token c028e484e879c23493cf9028093fee857e0c59bc' -d '{}'
```