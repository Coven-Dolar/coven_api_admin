# Deployment guide

This repository now includes a GitHub Actions workflow for SSH-based deployments.

## Required GitHub secrets

Create these repository secrets before enabling the workflow:

- `DEPLOY_HOST`: public IP or hostname of the server.
- `DEPLOY_USER`: SSH user used by GitHub Actions.
- `DEPLOY_SSH_KEY`: private SSH key matching the public key installed on the server.
- `DEPLOY_PORT`: optional SSH port. Defaults to `22`.
- `DEPLOY_PATH`: absolute path of the checked out project on the server. Example: `/home/jaspesoft/coven_api_admin`.
- `VENV_PATH`: absolute path of the Python virtualenv. Example: `/home/jaspesoft/VIRTUAL`.
- `DEPLOY_BRANCH`: optional branch to deploy. Defaults to `master`.
- `APP_SERVICE`: optional systemd service name. Defaults to `coven-web`.
- `CELERY_SERVICE`: optional systemd service name. Defaults to `coven-celery`.
- `CELERY_BEAT_SERVICE`: optional systemd service name. Defaults to `coven-celery-beat`.

## Server requirements

The server must already contain:

- the project cloned at `DEPLOY_PATH`
- a working virtualenv at `VENV_PATH`
- systemd services for the web app, celery worker and celery beat
- a valid `.env` file for Django production settings

## Important note about systemctl permissions

The deploy script restarts systemd services. If `DEPLOY_USER` is not `root`, that user must be allowed to run `systemctl daemon-reload`, `systemctl restart`, and `systemctl is-active` for the application services.

A common way is to add a sudoers rule like this:

```sudoers
jaspesoft ALL=(ALL) NOPASSWD:/bin/systemctl daemon-reload,/bin/systemctl restart coven-web,/bin/systemctl restart coven-celery,/bin/systemctl restart coven-celery-beat,/bin/systemctl is-active coven-web,/bin/systemctl is-active coven-celery,/bin/systemctl is-active coven-celery-beat
```

If you prefer, you can use a deploy user with enough permissions to restart those services directly.

## What the deploy script does

1. activates the virtualenv
2. installs Python dependencies
3. ensures `gunicorn` is installed
4. runs `python manage.py migrate --noinput`
5. runs `python manage.py collectstatic --noinput`
6. reloads systemd and restarts the application services

## Triggering a deployment

Deployments run automatically on pushes to `master` and can also be triggered manually from the Actions tab.
