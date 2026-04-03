#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_DIR="${DEPLOY_PATH:-/home/jaspesoft/coven_api_admin}"
VENV_DIR="${VENV_PATH:-/home/jaspesoft/VIRTUAL}"
BRANCH="${DEPLOY_BRANCH:-master}"
APP_SERVICE="${APP_SERVICE:-coven-web}"
CELERY_SERVICE="${CELERY_SERVICE:-coven-celery}"
CELERY_BEAT_SERVICE="${CELERY_BEAT_SERVICE:-coven-celery-beat}"
SYSTEMCTL_PREFIX="${SYSTEMCTL_PREFIX:-sudo}"

cd "$PROJECT_DIR"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Virtualenv not found at $VENV_DIR"
  exit 1
fi

if [[ -n "$SYSTEMCTL_PREFIX" ]]; then
  read -r -a SYSTEMCTL_CMD <<< "$SYSTEMCTL_PREFIX"
  SYSTEMCTL_CMD+=(systemctl)
else
  SYSTEMCTL_CMD=(systemctl)
fi

source "$VENV_DIR/bin/activate"

python --version
pip --version

pip install -r requirements.txt
pip install gunicorn

python manage.py migrate --noinput
python manage.py collectstatic --noinput

"${SYSTEMCTL_CMD[@]}" daemon-reload
"${SYSTEMCTL_CMD[@]}" restart "$APP_SERVICE"
"${SYSTEMCTL_CMD[@]}" restart "$CELERY_SERVICE"
"${SYSTEMCTL_CMD[@]}" restart "$CELERY_BEAT_SERVICE"

"${SYSTEMCTL_CMD[@]}" is-active "$APP_SERVICE"
"${SYSTEMCTL_CMD[@]}" is-active "$CELERY_SERVICE"
"${SYSTEMCTL_CMD[@]}" is-active "$CELERY_BEAT_SERVICE"

echo "Deploy finished successfully on branch $BRANCH"
