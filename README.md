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

2. Create `./.env`:

```bash
CLIENT_ID=<Client ID here>
CLIENT_SECRET=<Client Secret here>
OKTA_DOMAIN=<Your Okta Domain here>
```

3. Edit `kubernetes/secrets/oidc.yml`:

```yaml
CLIENT_ID: <Base64 Encoding of Client ID here>
CLIENT_SECRET: <Base64 Encoding of Client Secret here>
OKTA_DOMAIN: <Base64 Encoding of Your Okta Domain here>
```

## How to Set Up Development Environment (`localhost`)

```bash
$ docker compose up -d
$ docker exec -it app bash
$ python manage.py migrate
```

URLs:

- `http://localhost:8000/oidc`
- `http://localhost:8000/admin`
- `http://localhost:8000/swagger`

## How to Set Up Production Environment (`minikube`)

1. Start `minikube`:

```bash
$ sudo sh -c 'cat /dev/null > /var/db/dhcpd_leases'
$ minikube start --memory=6g --cpus=4 --disk-size=50g --addons=ingress
```

2. Build and Publish Image:

```bash
$ eval $(minikube -p minikube docker-env)
$ docker build -t app .
```

3. Deploy to Production Environment:

```bash
$ kubectl apply -R -f kubernetes
```

4. Create Tables and Superuser:

```bash
$ kubectl exec -it $(kubectl get pod --selector=app=app -o name) -- bash
$ python manage.py migrate
$ python manage.py collectstatic --noinput
```

URLs:

- `http://192.168.64.2/oidc`
- `http://192.168.64.2/admin`
- `http://192.168.64.2/swagger`
