# Hauora Journal

A personal wellbeing tracker built around Te Whare Tapa Whā and Te Pae Mahutonga — Māori models of health and wellbeing.

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

Configured for Render with:
- `render.yaml` — Blueprint for web service + database
- `build.sh` — Builds frontend, collects static files, runs migrations

Environment variables:
- `DJANGO_SECRET_KEY`
- `DATABASE_URL` (auto-set by Render)
- `DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD`

## License

MIT
