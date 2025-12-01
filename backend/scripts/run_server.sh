#!/bin/bash

function source_venv {
    if [ -e ../venv/bin/activate ]; then
        cd ../
    fi

    if [ ! -e ./venv/bin/activate ]; then
        echo "Error: venv not found\n Please run setup_server.sh first"
        exit 1
    fi

    if [ -e ../src/main.py ]; then
        echo "Remove the venv file in this directory and the parent directory and run setup_server.sh again"
        exit 1
    fi
    source ./venv/bin/activate
}

while getopts "dkhp" opt; do
      case $opt in
        d)
            echo "Starting in debug mode..."
            source_venv
            uvicorn src.main:app --reload
            exit 0
            ;;
        k)
            echo "Killing all uvicorn processes..."
            ./kill_server.sh
            exit 0
            ;;
        p)
            echo "Starting in production mode..."
            source_venv
            nohup uvicorn src.main:app --host 0.0.0.0 --port 8000 &
            exit 0
            ;;
        h)
            echo "Usage: ./run_server.sh [options]"
            echo "Options:"
            echo "  -d,      Start server in debug mode (default)"
            echo "  -k,      Kill all uvicorn processes"
            echo "  -p,      Start server in production mode"
            echo "  -h,      Show this help message"
            exit 0
          ;;
        \?)
          echo "Invalid option: -$OPTARG" >&2
          exit 1
          ;;
      esac
    done
    shift $((OPTIND-1))

source_venv
uvicorn src.main:app --reload
