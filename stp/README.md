# СТП, семестр 7

🔑 Современные технологии программирования

University project "Babushka" - social network for publishing photos, inspired by Instagram.

<hr>

## Installation

Run docker compose:

```bash
docker compose up -d --build
```

After a successful installation, your application will be available at following addresses:
- Backend: http://0.0.0.0:8000
- Frontend: http://0.0.0.0:3000

<hr>

## Backend

<div style="display: flex">
  <img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" height="50" alt="Django">
  <img src="https://upload.wikimedia.org/wikipedia/commons/2/29/Postgresql_elephant.svg" height="50" alt="PostgreSQL">
</div>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Source code - [backend/](backend/)

### Configuration

To override environment variables use `.env` file in the backend root directory ([backend/](backend/)):

```bash
cp .env.template .env
```

### Contributing

<details>
<summary>List of used linters and hooks</summary>

- [black](https://github.com/psf/black)
- [isort](https://github.com/PyCQA/isort)
- [flake8](https://github.com/pycqa/flake8)
- [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
  - check-added-large-files
  - check-json
  - check-toml
  - check-xml
</details>

To install pre-commit hooks run:

```bash
pre-commit install
```

You can manually run the pre-commit hooks on all files before committing:

```bash
pre-commit run --all-files
```

<hr>

## Frontend

<div style="display: flex">
  <img src="https://www.svgrepo.com/show/452092/react.svg" height="50" alt="React">
</div>

<hr>

## CI/CD

<div style="display: flex">
  <img src="https://www.svgrepo.com/show/475654/github-color.svg" height="50" alt="GitHub">
  <img src="https://icon.icepanel.io/Technology/svg/GitHub-Actions.svg" height="50" alt="GitHub Actions">
</div>

GitHub Actions workflows:
- [Backend CI](.github/workflows/backend-ci.yaml)
- [Backend Deployment](.github/workflows/backend-deployment.yaml)

<hr>

## Deployment

<div style="display: flex">
  <img src="https://www.svgrepo.com/show/448221/docker.svg" height="50" alt="Docker">
  <img src="https://www.svgrepo.com/show/376331/kubernetes.svg" height="50" alt="Kubernetes">
  <img src="https://www.svgrepo.com/show/374122/terraform.svg" height="50" alt="Terraform">
  <img src="https://www.svgrepo.com/show/349337/digitalocean.svg" height="50" alt="DigitalOcean">
</div>

### Cloud infrastructure

The general idea here - to use cloud resources for all the required services. The following services are used:
- DigitalOcean Kubernetes
- DigitalOcean Container Registry
- DigitalOcean Managed PostgreSQL

You can manage the infrastructure manually or using Terraform. The configuration is located in the [terraform](terraform/) directory.

Generate API access tokens for DigitalOcean account. You can use the following names:

- `stpbabushka-terraform-digitaloceanaccess-token` - Access token to use in Terraform
- `stpbabushka-githubactions-digitaloceanaccess-token` - Access token to use in GitHub Actions
- `stpbabushka-terraform-digitaloceanspaces-key` - Spaces access key to use in Terraform
- `stpbabushka-backend-digitaloceanspaces-key` - Spaces access key to use in backend

### a. Terraform cloud infrastructure management (recommended)

1. Set up a Terraform [backend](terraform/main.tf):
  - remote
  - local

This project uses a remote backend with Terraform Cloud. Learn more about connecting to the Terraform Cloud [here](https://developer.hashicorp.com/terraform/cli/cloud/settings).

2. Initialize a project and create a new production workspace:

```bash
cd terraform/
terraform init
```

If you are using a remote backend, you need to log in to Terraform Cloud using `terraform login` and set up the workspace in the web interface instead of running the following commands.

```bash
terraform workspace new prod
terraform workspace select prod
```

3. Configure variables for production workspace. If you are using a remote backend, you can set them in the web interface and skip the following commands. If you are using a local backend, create a new file `prod.tfvars`:

```bash
cp terraform.tfvars.template prod.tfvars
nano prod.tfvars
```

4. Apply the configuration. If you are using remote backend workspace variables, bypass `-var-file` argument.

```bash
terraform apply -var-file=prod.tfvars
```

To get exported values, run:

```bash
terraform output database_user_backend_password
terraform output database_user_localmanagement_password
```

5. `[Optional]` Get the kubeconfig file. Log in to a DigitalOcean web interface and download the kubeconfig file for the new cluster.

6. `[Optional]` Change environment variables `S3_ENDPOINT_URL` and `S3_BUCKET_NAME` in the backend `.env` file to the corresponding generated keys especially for backend. By default, Terraform set these variables to values provided for Terraform.

### b. Manual cloud infrastructure management 

1. Create a new Kubernetes cluster on DigitalOcean. Configure it in web interface or using `doctl` CLI tool. Download the configuration file and apply it locally.
2. Create a new Managed PostgreSQL database on DigitalOcean. Create a new user and database for this project. Copy the generated password.
3. Create a new Container Registry on DigitalOcean.

#### Set up PostgreSQL

Create new user and database for this project. You can use following names:
- Database name: `stpbabushka-prod-postgresql-db`
- Database user for Django application: `stpbabushka-prod-backend-postgresql-user`
- Database user for local management: `stpbabushka-prod-localmanagement-postgresql-user`

Connect to default database with admin user and run following command:

```psql
\connect "your-database-name"
ALTER SCHEMA public OWNER TO "your user";
GRANT ALL ON ALL TABLES IN SCHEMA "public" TO "user-name"
exit
```

#### Set up Kubernetes cluster

1. Create new namespace

```bash
kubectl create namespace stpbabushka-prod
```

2. Create secrets for backend

```bash
kubectl create secret \
    generic backend-secrets -n stpbabushka-prod \
    --from-literal=ENV=prod \
    --from-literal=SECRET_KEY=value \
    --from-literal=FRONTEND_URL="value" \
    --from-literal=BACKEND_URL="value" \
    --from-literal=DATABASE_HOSTNAME=value \
    --from-literal=DATABASE_PORT=value \
    --from-literal=DATABASE_NAME=value \
    --from-literal=DATABASE_USERNAME=value \
    --from-literal=DATABASE_PASSWORD=value
```

3. Install ingress-nginx and cert-manager

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.0-beta.0/deploy/static/provider/do/deploy.yaml
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.1/cert-manager.yaml
```

4. `[Optional]` Set context to new namespace for convenience

```bash
kubectl config set-context stpbabushka-prod \
    --namespace stpbabushka-prod \
    --cluster value \
    --user value
```

where:
- cluster `value` is the corresponding name of your cluster,
- user `value` is the corresponding name of your user.
