#!/bin/zsh

# Define paths
PROJECT_DIR="/Users/roniosipov/Documents/python/my-gpa-portal"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"

cd "$PROJECT_DIR"

# Cleanup function to ensure no zombie processes
cleanup() {
    pkill -f "uvicorn"
    exit
}

# Trap exit signals
trap cleanup EXIT SIGINT SIGTERM

# Launch
"$VENV_PYTHON" -m uvicorn src.app:app --host 127.0.0.1 --port 8000