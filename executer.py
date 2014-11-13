#!/usr/bin/python

import sys
from subprocess import Popen
import time

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

    if explorer == 'art' or explorer == 'twe':
        for i in range(RETRY_COUNT):
            try:
                comm = open(explorer + COMM_FILE, 'r')
                msg = comm.read()
                comm.close()
                return msg
            except:
                time.sleep(RETRY_DELTA)

def comm_write(explorer, text):

    if explorer == 'art' or explorer == 'twe':
        for i in range(RETRY_COUNT):
            try:
                comm = open(explorer + COMM_FILE, 'w')
                comm.write(text)
                comm.close()
                return None
            except:
                time.sleep(RETRY_DELTA)

def get_status(explorer):
    return comm_read(explorer)[0]

def check_explorer_format(arg1):

    if arg1.lower() == 'article':
        return 'article'
    elif arg1.lower() == 'twitter':
        return 'twitter'
    return None

def check_command_format(arg2):

    if sys.argv[2] == 'Status':
        return 'status'
    elif sys.argv[2] == 'Run':
        return 'resume'
    elif sys.argv[2] == 'Pause':
        return 'pause'
    elif sys.argv[2] == 'Rtop':
        return 'stop'
    return None 

def check_status_format(status):
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
    if len(sys.argv) == 2:

        explorer = check_explorer_format(sys.argv[1])
        command = check_command_format(sys.argv[2])

        if not explorer or not command:
            raise_input_error()

        s = comm_read(explorer)
        name = explorer[0].upper() + explorer[1:]

        status = status_format(get_status(explorer))

        if not status:
            raise_input_error()

        if status == 'Waiting':
            return ('Run: %s - Last Command Not Processed Yet' % name)

        if command == 'Status':
            return ('Status: %s - %s' % (name + ' Explorer', status))

        elif command == 'Run':
            if status == 'Paused':
                comm_write('WR')
                return ('Run: %s - Resuming' % name)
            elif status == 'Stopped':
                # Popen
                return ('Run: %s - Started Running' % name)
            elif status == 'Running':
                return ('Run: %s - Already Running' % name)

        elif command == 'Pause':
            if status == 'Paused':
                return ('Run: %s - Already in Pause' % name)
            elif status == 'Stopped':
                # Popen
                return ('Run: %s - Cannot pause non-Started Instance' % name)
            elif status == 'Running':
                comm_write('WP')
                return ('Run: %s - Pausing' % name)

        elif command == 'Stop':
            if status == 'Paused':
                comm_write('WS')
                return ('Run: %s - Stopping Paused Explorer' % name)
            elif status == 'Stopped':
                return ('Run: %s - Cannot Stop non-Started Explorer' % name)
            elif status == 'Running':
                comm_write('WS')
                return ('Run: %s - Stopping' % name)