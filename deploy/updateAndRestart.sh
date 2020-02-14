#!/bin/bash

set -e

cd backend

echo "Update code"
git pull

echo "Running dependency install"
source venv/bin/activate
pip install -r requirements.txt

echo "Stop the previous instance"
kill $(lsof -i:5000)

echo "Running migration jobs"
export FLASK_APP=manage:app
flask db upgrade
source seed/scripts/seeder.sh

echo "Deploy"
sudo supervisorctl reload

echo "Finish"
