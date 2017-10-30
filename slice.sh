#!/bin/bash
#
# chkconfig: 35 90 12
# description: Slice Scanner Runner
#
# Get function from functions library
. /etc/init.d/functions

# Start
start() {
    if running $1;
    then
        echo "Slice Already Running"
        echo;
    else
        echo "Starting Slice Server..."
        sudo python /home/ec2-user/slice_scanner/app.py -c /home/ec2-user/slice_scanner/slice.json > /dev/null 2>&1 &
        ### Create the lock file ###
        touch /var/lock/subsys/slice
        echo "Slice Running"
        echo;
    fi
}

# Restart
stop() {
    if running $1;
    then
        echo "Stopping Slice Server..."
        ps -aef | grep "sudo python /home/ec2-user/slice_scanner/app.py" | awk '{print $2}' | xargs sudo kill > /dev/null 2>&1 &
        ### Remove the Lock File ###
        rm -f /var/lock/subsys/slice
        echo "Slice Stopped"
        echo;
    else
        echo "Slice Not Running"
        echo;
    fi
}

# Status
status() {
    if running $1;
    then
        echo "Slice Running"
        echo;
    else
        echo "Slice Not Running"
        echo;
    fi
}

running() {
    if [ -f "/var/lock/subsys/slice" ]
    then
        return 0
    else
        return 1
    fi
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  status)
    status
    ;;
  running)
    running
    ;;
  *)
    echo "Usage: $0 {start|stop|status}"
esac

### main logic ###
#slice 80L, 1484C
