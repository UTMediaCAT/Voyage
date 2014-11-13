#!/usr/bin/python

import sys
from subprocess import Popen, PIPE, STDOUT
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
    if status == 'R':
        return 'Running'
    elif status == 'P':
        return 'Paused'
    elif status == 'S':
        return 'Stopped'
    elif status == 'W':
        return 'Waiting'
    return None

if __name__ == '__main__':
    if len(sys.argv) == 3:

        explorer = explorer_format(sys.argv[1])
        command = command_format(sys.argv[2])

        if not explorer or not command:
            raise_input_error()

        s = comm_read(explorer)
        name = explorer[0].upper() + explorer[1:]

        status = status_format(get_status(explorer))

        if not status:
            raise_input_error()

        if status == 'Waiting':
            print ('Run: %s - Last Command Not Processed Yet' % name)
            sys.exit()

        if command == 'status':
            print ('Status: %s - %s' % (name + ' Explorer', status))

        elif command == 'run':
            if status == 'Paused':
                comm_write(explorer, 'WR')
                print ('Run: %s - Resuming' % name)
            elif status == 'Stopped':
                a = Popen(['python', os.path.abspath(os.path.dirname( __file__ )) + '/' + explorer.lower() + '_explorer.py'], 
                    cwd=os.path.abspath(os.path.dirname( __file__ )))
                print ('Run: %s - Started Running' % name)
            elif status == 'Running':
                print ('Run: %s - Already Running' % name)

        elif command == 'pause':
            if status == 'Paused':
                print ('Run: %s - Already in Pause' % name)
            elif status == 'Stopped':
                print ('Run: %s - Cannot pause non-Started Instance' % name)
            elif status == 'Running':
                comm_write(explorer, 'WP')
                print ('Run: %s - Pausing' % name)

        elif command == 'stop':
            if status == 'Paused':
                comm_write(explorer, 'WS')
                print ('Run: %s - Stopping Paused Explorer' % name)
            elif status == 'Stopped':
                print ('Run: %s - Cannot Stop non-Started Explorer' % name)
            elif status == 'Running':
                comm_write(explorer, 'WS')
                print ('Run: %s - Stopping' % name)