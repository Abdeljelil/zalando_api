#!/bin/bash

# Start the first process
service postgresql start
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start postgresql: $status"
  exit $status
fi

make test
make populate

# Start the second process

python3.6 zalando_api/server.py 0.0.0.0:8080 &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start restful_api: $status"
  exit $status
fi

while /bin/true; do
  ps aux |grep '/usr/lib/postgresql/9.6/bin/postgres' |grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux |grep 'python3.6 zalando_api/server.py' |grep -q -v grep
  PROCESS_2_STATUS=$?
  # If the greps above find anything, they will exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit -1
  fi
  sleep 1
done