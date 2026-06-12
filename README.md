# Hauora Journal

A personal wellbeing tracker built around Te Whare Tapa Whā and Te Pae Mahutonga - Māori models of health and wellbeing.

## Overview

Hauora Journal helps you track daily wellbeing across multiple dimensions, not just physical or mental health in isolation. The app is structured around the four walls of Te Whare Tapa Whā:

- **Taha Hinengaro** (Mind) - Mood, anxiety, stress levels
- **Taha Tinana** (Body) - Sleep, exercise, diet, energy
- **Taha Whānau** (Family/Belonging) - Social connection and interaction quality
- **Taha Wairua** (Spirit) - Sense of meaning and purpose

Plus elements from Te Pae Mahutonga:
- **Mauriora** (Identity) - Feeling like yourself
- **Waiora** (Environment) - Quality of your physical environment

## Features

- **Daily Entries** - Track wellbeing metrics with simple 1-10 sliders
- **Reflection** - Record best/hardest moments and journal thoughts
- **Summary Charts** - Visualize trends over time for any metric
- **Per-Entry Charts** - See your hauora balance for each day
- **PWA Support** - Install on your phone's home screen for app-like access
- **Multi-user** - Each user sees only their own entries

## Tech Stack

- Django 5
- Bootstrap 5
- Chart.js
- PostgreSQL (production) / SQLite (development)
- Deployed on Render

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
# Clone the repo
git clone https://github.com/katene30/journal.git
cd journal

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp example.env .env
# Edit .env and set DJANGO_SECRET_KEY

# Run migrations
cd journal
python manage.py migrate

# Create a user
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## Deployment

The app is configured for Render deployment with:
- `render.yaml` - Blueprint for web service and database
- `build.sh` - Build script that runs migrations and collectstatic

Environment variables needed:
- `DJANGO_SECRET_KEY` - Secret key for Django
- `DATABASE_URL` - PostgreSQL connection string (auto-set by Render)
- `DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD` - For creating admin user on deploy

## License

MIT
