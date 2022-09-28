#!/bin/bash
export FLASK_APP=run.py;
export FLASK_ENV=development;
flask db migrate;
flask db upgrade;
flask run;
