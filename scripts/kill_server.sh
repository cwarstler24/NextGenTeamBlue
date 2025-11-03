#!/bin/bash

ps -e | grep "uvicorn" | grep -v grep | awk '{print $1}' | xargs kill
if [ $? -eq 0 ]; then
    echo "All uvicorn processes killed"
else
    echo "Failed to kill all uvicorn processes"
fi
