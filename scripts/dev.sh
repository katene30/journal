#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting development servers...${NC}"

# Function to cleanup background processes on exit
cleanup() {
    echo -e "\n${RED}Shutting down servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${GREEN}Starting Django backend on http://localhost:8000${NC}"
source venv/bin/activate
cd journal
python manage.py runserver &
BACKEND_PID=$!
cd ..

# Give backend a moment to start
sleep 2

# Start frontend
echo -e "${GREEN}Starting SvelteKit frontend on http://localhost:5173${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "\n${BLUE}Both servers running:${NC}"
echo -e "  Frontend: ${GREEN}http://localhost:5173${NC}"
echo -e "  Backend:  ${GREEN}http://localhost:8000${NC}"
echo -e "  Admin:    ${GREEN}http://localhost:8000/admin${NC}"
echo -e "\nPress Ctrl+C to stop both servers.\n"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
