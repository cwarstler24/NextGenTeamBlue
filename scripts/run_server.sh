#!/bin/bash

function source_venv {
    if [ -e ../venv/bin/activate ]; then
        cd ../
    fi

    if [ ! -e ./venv/bin/activate ]; then
        echo "Error: venv not found\n Please run setup_server.sh first"
        exit 1
    fi

    source ./venv/bin/activate
}

while getopts "dkh" opt; do
      case $opt in
        d)
            echo "Starting in debug mode..."
            source_venv
            uvicorn src.test:app --reload
            exit 0
            ;;
        k)
            echo "Killing all uvicorn processes..."
            ./kill_server.sh
            exit 0
            ;;
        h)
            echo "Usage: ./run_server.sh [options]"
            echo "Options:"
            echo "  -d,      Start server in debug mode"
            echo "  -k,      Kill all uvicorn processes"
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
nohup uvicorn src.test:app --reload &
