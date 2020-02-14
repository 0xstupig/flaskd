#!/usr/bin/env bash


source venv/bin/activate
export FLASK_APP=cli:app

source seed/scripts/1_init_role_and_permission.sh
flask seed host_admin -e "$1"

deactivate
