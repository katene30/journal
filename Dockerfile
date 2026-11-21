# --- Stage 1: build the SvelteKit frontend ---
FROM node:22-slim AS frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build


# --- Stage 2: Django app ---
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY journal/ ./journal/

# collectstatic needs a SECRET_KEY to import settings; this one is build-only and never used at runtime
RUN cd journal \
    && DJANGO_SECRET_KEY=build-only-not-secret python manage.py collectstatic --no-input

# The SPA is served by Django from STATIC_ROOT/frontend (see journal/urls.py, journal/views.py)
COPY --from=frontend /frontend/build/ ./journal/staticfiles/frontend/

RUN useradd --create-home appuser
USER appuser

WORKDIR /app/journal

# Migrations are NOT run here. Run them as a separate one-off step before deploying
# (see "Deployment" in README.md).
CMD exec gunicorn journal.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers 2 \
    --threads 4 \
    --timeout 60
