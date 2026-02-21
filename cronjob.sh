#!/usr/bin/env bash

source /srv/scull_suite/venv/bin/activate

/srv/scull_suite/backend/manage.py create_accounts_summaries

exit