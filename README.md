# Hauora Journal

A personal wellbeing tracker built around Te Whare Tapa Whā and Te Pae Mahutonga — Māori models of health and wellbeing.

## Important links

| Important links           |
|---------------------------------- |
| Documentation in [`docs/`](docs/) |
|[Live site](https://journal-9hww.onrender.com)|
|[Dev site FE](http://localhost:5173/)|
|[Dev site BE](http://localhost:8000)|
|[Django admin](http://localhost:8000/admin)|

## Overview

Hauora Journal helps you track daily wellbeing holistically, not just physical or mental health in isolation. The app is structured around seven pillars:

### Te Whare Tapa Whā (The Four Walls)

| Pillar | Icon | What it tracks |
|--------|------|----------------|
| **Hinengaro** | 🧠 | Mind — mood, anxiety, stress |
| **Tinana** | 💪 | Body — sleep, energy, exercise, diet |
| **Whānau** | 💛 | Relationships — connection, interaction quality |
| **Wairua** | 🌿 | Spirit — sense of meaning and purpose |

### Te Pae Mahutonga (The Southern Cross)

| Pillar | Icon | What it tracks |
|--------|------|----------------|
| **Mauriora** | 🪞 | Identity — feeling like yourself |
| **Waiora** | 🏡 | Environment — is your space supportive? |

### Reflection

| Pillar | Icon | What it tracks |
|--------|------|----------------|
| **Reflection** | 📝 | Overall day rating, journal, highlights |

## Features

- **Semantic scales** — Bipolar scales (e.g., "Calm ↔ Anxious") instead of numeric ratings
- **Bilingual prompts** — Questions in Te Reo Māori and English
- **Mauri indicators** — Show engagement level per pillar (○ ◔ ◕ ●), not completion pressure
- **One entry per day** — Edit throughout the day, each date has its own entry
- **Date picker** — Review and edit past entries
- **PWA Support** — Install on your phone's home screen

## Tech Stack

**Backend:**
- Django 5 + Django REST Framework
- PostgreSQL (production) / SQLite (development)

**Frontend:**
- SvelteKit + TypeScript
- SCSS (custom design tokens, no Bootstrap)
- Vite

**Deployment:**
- Render (Django serves API + built frontend)

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 20+
- pip

### Setup

```bash
# Clone the repo
git clone https://github.com/katene30/journal.git
cd journal

# Backend setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp example.env .env
# Edit .env and set DJANGO_SECRET_KEY

cd journal
python manage.py migrate
python manage.py createsuperuser
cd ..

# Frontend setup
cd frontend
npm install
cd ..
```

### Running locally

You need two terminals:

**Terminal 1 — Django API:**
```bash
cd journal
source ../venv/bin/activate
python manage.py runserver
```

**Terminal 2 — SvelteKit frontend:**
```bash
cd frontend
npm run dev
```

Visit:
- Frontend (dev): `http://localhost:5173/`
- Django admin: `http://localhost:8000/admin/`

Log in via Django first (`http://localhost:8000/login/`), then use the frontend.

**Production URLs:**
- `/app` — SvelteKit entry form (requires login)
- `/` — Django templates (legacy, gradual migration)
- `/api/` — REST API

## Project Structure

```
journal/
├── frontend/           # SvelteKit app
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/   # SemanticScale, PillarNav
│   │   │   ├── config/       # Pillar definitions
│   │   │   ├── stores/       # Entry state, mauri calculation
│   │   │   ├── api/          # API client
│   │   │   └── scss/         # Design tokens, mixins
│   │   └── routes/           # Pages
│   └── vite.config.ts
├── journal/            # Django project
│   ├── journal/        # Settings
│   └── entries/        # App (models, views, API)
├── docs/
│   ├── PILLARS.md      # Pillar documentation
│   └── FRONTEND_NOTES.md
└── requirements.txt
```

## Deployment

### Docker (any container host, e.g. Google Cloud Run)

The `Dockerfile` builds the Svelte frontend and the Django app into one image that listens on `$PORT` (default 8080).

```bash
docker build -t hauora-journal .
```

**Migrations are a separate step, not part of the build or startup.** Run them once per deploy, before the new version takes traffic, with the same image:

```bash
docker run --rm --env-file prod.env hauora-journal python manage.py migrate
```

On Cloud Run, do this as a Cloud Run Job that uses the same image, with the command `python manage.py migrate`.

Environment variables:

| Variable | Required | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | yes | long random string |
| `DATABASE_URL` | yes | `postgresql://user:pass@host/db?sslmode=require` |
| `ALLOWED_HOSTS` | yes | `journal-abc123.a.run.app` (comma-separated) |
| `CSRF_TRUSTED_ORIGINS` | yes | `https://journal-abc123.a.run.app` (comma-separated, with scheme) |
| `DEBUG` | no | `false` (default) |

With `DEBUG` off, session and CSRF cookies are `Secure` (HTTPS only).

### Render (legacy)

- `render.yaml` — Blueprint for web service + database
- `build.sh` — Builds frontend, collects static files, runs migrations (Render's free plan has no pre-deploy step)
- `DATABASE_URL` is auto-set by Render; the Render hostname is added to `ALLOWED_HOSTS` automatically

## License

MIT
