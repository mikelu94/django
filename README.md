# Django

Some django projects that I wrote.

## Dependencies

- Docker
- Kubernetes

## Technologies

- Python 3
- Django
- PostgreSQL
- Memcached

## How to Set Up Development Environment (localhost)

```bash
$ docker-compose up -d
$ docker exec -it django bash
$ python manage.py migrate
$ python manage.py createsuperuser
```

## How to Build and Publish Image

```bash
$ docker build -t [dockerhub-username]/[image-name]:[tag] .
$ docker push [dockerhub-username]/[image-name]:[tag]
```

## How to Deploy to Production Environment (Kubernetes)

`kubectl`.