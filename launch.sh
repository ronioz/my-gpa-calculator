#!/bin/zsh

# Function to kill the server when the script exits
cleanup() {
    echo "Shutting down..."
    kill $SERVER_PID
    exit
}

# Trap the exit signal (when you close the window)
trap cleanup EXIT

cd /Users/roniosipov/Documents/python/my-gpa-portal

# Launch the server in the background and capture its PID
/Users/roniosipov/Documents/python/my-gpa-portal/.venv/bin/python -m uvicorn src.app:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

# Wait forever so the script doesn't exit
wait $SERVER_PID