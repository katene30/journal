# Hauora Journal

A personal wellbeing tracker built around Te Whare Tapa Whā and Te Pae Mahutonga — Māori models of health and wellbeing.

## Important links

| Important links           |
|---------------------------------- |
| Documentation in [`docs/`](docs/) |
|[Live site](https://journal-452552708454.australia-southeast1.run.app/app/)|
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
- Google Cloud Run (one Docker container: Django serves API + built frontend)
- Neon Postgres

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

On Cloud Run this is a Cloud Run Job (see below).

Environment variables:

| Variable | Required | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | yes | long random string |
| `DATABASE_URL` | yes | `postgresql://user:pass@host/db?sslmode=require` |
| `ALLOWED_HOSTS` | yes | `journal-abc123.a.run.app` (comma-separated) |
| `CSRF_TRUSTED_ORIGINS` | yes | `https://journal-abc123.a.run.app` (comma-separated, with scheme) |
| `DEBUG` | no | `false` (default) |

With `DEBUG` off, session and CSRF cookies are `Secure` (HTTPS only).

### Google Cloud Run + Neon

The app runs on Cloud Run and the database is Neon's free Postgres. Both have free allowances that easily cover a personal app.

#### One-time setup (in the browser)

1. **Neon:** create a project at [neon.tech](https://neon.tech). Pick the AWS Sydney region (closest to NZ) and copy the **direct** connection string, not the pooled one; Django keeps its own connections open. It looks like `postgresql://user:pass@ep-xxx.ap-southeast-2.aws.neon.tech/neondb?sslmode=require`.
2. **Google Cloud:** create a project and attach a billing account (a card is required even for the free allowance).
3. **Budget alert:** in the Cloud Console go to *Billing → Budgets & alerts* and create a budget of about $5 with email alerts. This is your safety net against surprise charges.
4. Install the [gcloud CLI](https://cloud.google.com/sdk/docs/install).

#### One-time setup (terminal)

```bash
PROJECT_ID=your-gcp-project-id
REGION=australia-southeast1                        # Sydney
IMAGE=$REGION-docker.pkg.dev/$PROJECT_ID/journal/app

gcloud auth login
gcloud config set project $PROJECT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  cloudbuild.googleapis.com secretmanager.googleapis.com

# Where the Docker images are stored
gcloud artifacts repositories create journal --repository-format=docker --location=$REGION

# Secrets (never put these in env vars on the command line or in git)
python3 -c 'import secrets; print(secrets.token_urlsafe(50), end="")' \
  | gcloud secrets create django-secret-key --data-file=-
printf '%s' 'postgresql://…your Neon direct connection string…' \
  | gcloud secrets create database-url --data-file=-

# Let Cloud Run read the secrets
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
for s in django-secret-key database-url; do
  gcloud secrets add-iam-policy-binding $s \
    --member=serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor
done
```

#### First deploy

```bash
# 1. Build the image on Google's servers (`.gcloudignore` keeps .env etc. out of the upload). Cloud Run needs linux/amd64; a local
#    build on an Apple Silicon Mac would produce arm64.
gcloud builds submit --region $REGION --tag $IMAGE

# 2. Create and run the migration job
gcloud run jobs create migrate --image $IMAGE --region $REGION \
  --set-secrets DJANGO_SECRET_KEY=django-secret-key:latest,DATABASE_URL=database-url:latest \
  --command python --args manage.py,migrate
gcloud run jobs execute migrate --region $REGION --wait

# 3. Deploy the web service. max-instances caps how far it can scale (and cost).
gcloud run deploy journal --image $IMAGE --region $REGION \
  --allow-unauthenticated \
  --max-instances 2 \
  --set-secrets DJANGO_SECRET_KEY=django-secret-key:latest,DATABASE_URL=database-url:latest

# 4. Tell Django its public hostnames. Cloud Run serves the app on two URLs (shown
#    in the deploy output and in `describe`); allow both. The ^@^ prefix makes @
#    the separator between variables so the values can contain commas.
gcloud run services describe journal --region $REGION --format='value(status.url,metadata.annotations."run.googleapis.com/urls")'
H1=journal-<project-number>.$REGION.run.app
H2=journal-<hash>.a.run.app
gcloud run services update journal --region $REGION \
  --update-env-vars "^@^ALLOWED_HOSTS=$H1,$H2@CSRF_TRUSTED_ORIGINS=https://$H1,https://$H2"
```

To create an admin user, run this locally against the Neon database:

```bash
cd journal
DATABASE_URL='postgresql://…neon…' DJANGO_SECRET_KEY=anything python manage.py createsuperuser
```

#### Every deploy after that

```bash
gcloud builds submit --region $REGION --tag $IMAGE
gcloud run jobs update migrate --image $IMAGE --region $REGION
gcloud run jobs execute migrate --region $REGION --wait
gcloud run deploy journal --image $IMAGE --region $REGION
```

## License

MIT
