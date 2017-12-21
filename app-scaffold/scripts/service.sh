#!/bin/bash

case "$1" in
start)
   gunicorn -c ./scripts/gunicorn.conf --log-config ./scripts/logging.conf  wsgi:app  --chdir ./src --daemon
   ;;
debug)
   gunicorn -c ./scripts/gunicorn.conf --log-config ./scripts/logging.conf  wsgi:app  --chdir ./src
   ;;
stop)
   kill `cat ./logs/{app_name}.pid`
   rm ./logs/{app_name}.pid
   ;;
restart)
   $0 stop
   $0 start
   ;;
status)
   if [ -e ./logs/{app_name}.pid ]; then
      echo {app_name} is running, pid=`cat ./logs/{app_name}.pid`
   else
      echo {app_name} is NOT running
      exit 1
   fi
   ;;
*)
   echo "Usage: $0 {start|stop|debug|status|restart}"
esac

exit 0