#!/usr/bin/env bash

flask seed roles -s ./seed/data/roles.csv
flask seed permissions -s ./seed/data/permissions.csv
flask seed role_permissions -s ./seed/data/role_permissions.csv

