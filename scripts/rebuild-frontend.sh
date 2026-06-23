#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

echo "Building frontend..."
cd frontend
npm run build

echo "Copying to Django static..."
cd ..
cp -r frontend/build/* journal/staticfiles/frontend/

echo "Done! Restart Django server to see changes."
