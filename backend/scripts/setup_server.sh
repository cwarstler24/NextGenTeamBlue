if [ -e ./scripts/setup_server.sh ]; then
    cd ./scripts
fi

if [ -f ../venv/bin/activate ]; then
    echo "virtualenv already created"
else
    echo "Creating virtualenv..."
    python3 -m venv ../venv
fi

if [ $? -eq 0 ]; then
    echo "virtualenv created"
else
    echo "virtualenv failed to create"
    exit 1
fi

source ../venv/bin/activate
pip install -r ../requirements.txt
