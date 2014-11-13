#!/usr/bin/python

import sys
from subprocess import Popen
import time
import os

# Comm file format: (Status)(Command)
# Status Type: (R)unning, (P)aused, (S)topped, (W)aiting
# Command Type: (R)esume, (P)ause, (S)top/exit

COMM_FILE = '_comm.stream'
RETRY_COUNT = 10
RETRY_DELTA = 1

class InputError(Exception):
    pass

def raise_input_error():
    raise InputError("Usage: python executer.py [article|twitter] [status|run|pause|stop]")

def comm_read(explorer):
    for i in range(RETRY_COUNT):
        try:
            comm = open(explorer + COMM_FILE, 'r')
            msg = comm.read()
            comm.close()
            return msg
        except:
            time.sleep(RETRY_DELTA)

def comm_write(explorer, text):
    for i in range(RETRY_COUNT):
        try:
            comm = open(explorer + COMM_FILE, 'w')
            comm.write(text)
            comm.close()
            return None
        except:
            time.sleep(RETRY_DELTA)

def get_status(explorer):
    return comm_read(explorer_format(explorer))[0]

def explorer_format(arg1):

    if arg1.lower() == 'article':
        return 'article'
    elif arg1.lower() == 'twitter':
        return 'twitter'
    return None

def command_format(arg2):

    if arg2.lower() == 'status':
        return 'status'
    elif arg2.lower() == 'run':
        return 'run'
    elif arg2.lower() == 'pause':
        return 'pause'
    elif arg2.lower() == 'stop':
        return 'stop'
    return None 

def status_format(status):
    if status == 'Waiting':
        return ('%s: %s - Last Command Not Processed Yet' % 
           (command[0].upper() + command[1:], name))
        sys.exit(0)
    elif status == 'R':
        return 'Running'
    elif status == 'P':
        return 'Paused'
    elif status == 'S':
        return 'Stopped'
    elif status == 'W':
        return 'Waiting'
    return None

def run(status, explorer, name):
    if status == 'Waiting':
        return ('%s - Last Command Not Processed Yet' % 
           (name))
        sys.exit(0)
    elif status == 'Paused':
        comm_write(explorer, 'WR')
        return format('Run: %s - Resuming' % name)
    elif status == 'Stopped':
        a = Popen(['python', os.path.abspath(os.path.dirname( __file__ )) + '/' + explorer.lower() + '_explorer.py'], 
            cwd=os.path.abspath(os.path.dirname( __file__ )))
        return format('Run: %s - Started Running' % name)
    elif status == 'Running':
        return format('Run: %s - Already Running' % name)

def pause(status, explorer, name):
    if status == 'Waiting':
        return ('%s - Last Command Not Processed Yet' % 
           (name))
        sys.exit(0)
    elif status == 'Paused':
        return format('Pause: %s - Already in Pause' % name)
    elif status == 'Stopped':
        return format('Pause: %s - Cannot pause non-Started Instance' % name)
    elif status == 'Running':
        comm_write(explorer, 'WP')
        return format('Pause: %s - Pausing' % name)

def stop(status, explorer, name):
    if status == 'Waiting':
        return ('%s - Last Command Not Processed Yet' % 
           (name))
        sys.exit(0)
    elif status == 'Paused':
        comm_write(explorer, 'WS')
        return format('Stop: %s - Stopping Paused Explorer' % name)
    elif status == 'Stopped':
        return format('Stop: %s - Cannot Stop non-Started Explorer' % name)
    elif status == 'Running':
        comm_write(explorer, 'WS')
        return format('Stop: %s - Stopping' % name)

def status_output(status, explorer, name):
    return format('%s - %s' % (name, status))

if __name__ == '__main__':
    if len(sys.argv) == 3:

        explorer = explorer_format(sys.argv[1])
        command = command_format(sys.argv[2])

        if not explorer or not command:
            raise_input_error()

        s = comm_read(explorer)
        name = explorer[0].upper() + explorer[1:] + ' Explorer'

        status = status_format(get_status(explorer))

        if not status:
            raise_input_error()

        if command == 'status':
            print status_output(status, explorer, name)

        elif command == 'run':
            print run(status, explorer, name)

        elif command == 'pause':
            print pause(status, explorer, name)

        elif command == 'stop':
            print stop(status, explorer, name)