# Django

Some django projects that I wrote.

## Dependencies

- Docker
- `kubectl`
- `minikube`
- Okta Developer Account (Free)

## Technologies

- Python 3
- Django
- PostgreSQL
- Memcached
- Redis
- RabbitMQ
- Open ID Connect
- Logstash

## Preliminaries

1. Create an OIDC application (see [instructions](https://help.okta.com/en-us/Content/Topics/Apps/Apps_App_Integration_Wizard_OIDC.htm)).

2. Edit `.env`:

```bash
CLIENT_ID=<Client ID here>
CLIENT_SECRET=<Client Secret here>
OKTA_DOMAIN=<Your Okta Domain here>
```

3. Edit 

## How to Set Up Development Environment (`localhost`)

```bash
$ docker compose up -d
$ docker exec -it app bash
$ python manage.py migrate
$ python manage.py createsuperuser
```

## How to Set Up Production Environment (`minikube`)

1. Start `minikube`:

```bash
$ minikube start --addons=ingress
```

2. Build and Publish Image:

```bash
$ eval $(minikube -p minikube docker-env)
$ docker build -t app .
```

3. Deploy to Production Environment:

```bash
$ kubectl apply -f kubernetes
```

4. Create Tables and Superuser:

```bash
$ kubectl exec -it <App Pod name here> -- bash
$ python manage.py migrate
$ python manage.py createsuperuser
```
