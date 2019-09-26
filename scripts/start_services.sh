#!/usr/bin/env bash
### This script is triggered from within docker contrainer
### to start multiple processes in the same container.
### This script is defined in the CMD option in Dockerfile

# Start actions server in background
python3.6 -m rasa_core_sdk.endpoint --actions app.actions.actions& 


# Running date validation script
python3.6 -m /app/validatedate.py

# Start rasa core server with nlu model
python3.6 -m rasa_core.run  --enable_api --core /app/models/rasa_core -u /app/models/nlu/default/model_20190905-183519  --endpoints /app/config/endpoints.yml --credentials /app/config/credentials.yml -d /app/models/dialogue
