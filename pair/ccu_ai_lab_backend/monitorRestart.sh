#!/bin/bash
LABBACKEND=/home/esl/www/ccu_ai_lab_backend/
APPSETTING=run.py
ENVSETTING=production

ps -ef | grep "gunicorn" | grep -v "grep"
if [ "$?" -eq 1 ]
then
        cd $LABBACKEND
        source ../../bin/activate
        fuser -k 5000/tcp
        export FLASK_APP=$APPSETTING
        export FLASK_ENV=$ENVSETTING
        exec ../bin/gunicorn -D --certfile=/etc/letsencrypt/live/embedded.cs.ccu.edu.tw-0001/fullchain.pem --keyfile=/etc/letsencrypt/live/embedded.cs.ccu.edu.tw-0001/privkey.pem -b 0.0.0.0:5000 -w 4 run:app
	echo "process has been restarted!"
else
	echo "process already started!"
fi
