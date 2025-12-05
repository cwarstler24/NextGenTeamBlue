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

source_venv
source ./venv/bin/activate
python -m log.security_reader
