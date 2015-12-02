#!/usr/bin/python
# Backend script to communicate with explorers.
# This script allows running, pausing, stopping
# explorers which are already running.
#
# Comm file format: (Status)(Command)
# Status Type: (R)unning, (P)aused, (S)topped, (W)aiting
# Command Type: (R)esume, (P)ause, (S)top
#
# This script also supports executing using arguments.
# Ex. 'python executer.py article status'

import sys
import subprocess
import time
import os
# To load configurations
import yaml

# Change current working directory to src/ folder
path = os.path.abspath(os.path.dirname(__file__))
os.chdir(path)

# Global variables for settings
COMM_FILE = '_comm.stream'


def configuration():
    """ (None) -> dict
    Returns a dictionary containing the micro settings from the
    config.yaml file located in the directory containing this file
    """
    config_yaml = open("../config.yaml", 'r')
    config = yaml.load(config_yaml)
    config_yaml.close()
    return config


class InputError(Exception):
    """ (None) -> None
    Custom Exception to raise when input is wrong
    """
    pass


class TimeoutError(Exception):
    """ (None) -> None
    Custom Exception to raise when timeout occurs
    when communicating with the stream.
    """
    pass


def raise_input_error():
    """ (None) -> None
    Raise InputError with the proper usage of this script
    """
    raise InputError("Usage: python executer.py [article|twitter] " +
                     "[status|run|pause|stop|fstop]")


def raise_timeout_error():
    """ (None) -> None
    Raise TimeoutError with message
    """
    raise TimeoutError("Could not access the communication stream file")


def comm_read(explorer):
    """ (Str) -> Str
    Open, read and return the content on the communication stream file
    Raise TimeoutError if reading was not accomplished within the time limit
    """
    for i in range(configuration()['communication']['retry_count']):
        try:
            comm = open(explorer + COMM_FILE, 'r')
            msg = comm.read()
            comm.close()
            return msg
        except:
            time.sleep(configuration()['communication']['retry_delta'])
    raise_timeout_error()


def comm_write(explorer, text):
    """ (Str, Str) -> None
    Open, read and write on the communication stream file
    Raise TimeoutError if writing was not accomplished within the time limit
    """
    for i in range(configuration()['communication']['retry_count']):
        try:
            comm = open(explorer + COMM_FILE, 'w')
            comm.write(text)
            comm.close()
            return None
        except:
            time.sleep(configuration()['communication']['retry_delta'])
    raise_timeout_error()


def get_status(explorer):
    """ (Str) -> Str
    Extract and return the status section of the communication stream
    """
    return comm_read(explorer_format(explorer))[0]


def explorer_format(arg1):
    """ (Str) -> Str
    Formats and checks the explorer input
    """

    if arg1.lower() == 'article':
        return 'article'
    elif arg1.lower() == 'twitter':
        return 'twitter'
    return None


def command_format(arg2):
    """ (Str) -> Str
    Formats and checks the command input
    """

    if arg2.lower() == 'status':
        return 'status'
    elif arg2.lower() == 'run':
        return 'run'
    elif arg2.lower() == 'pause':
        return 'pause'
    elif arg2.lower() == 'stop':
        return 'stop'
    elif arg2.lower() == 'fstop':
        return 'fstop'
    return None


def status_format(raw_status):
    """ (Str) -> Str
    Formats and checks the status output
    """

    if raw_status == 'R':
        return 'Running'
    elif raw_status == 'P':
        return 'Paused'
    elif raw_status == 'S':
        return 'Stopped'
    elif raw_status == 'W':
        return 'Waiting'
    return None


def input_format(arg1, arg2):
    """ (Str, Str) -> Str, Str
    Formats and checks the inputs
    """
    expl = explorer_format(arg1)
    comm = command_format(arg2)
    if not expl or not comm:
        raise_input_error()
    return expl, comm


def name_format(explorer):
    """ (Str) -> Str
    Formats and adds ' Explorer' after the explorer
    """
    return explorer[0].upper() + explorer[1:] + ' Explorer'


def run(explorer):
    """ (Str) -> Str
    Run explorer depending on the status and return it's status
    """

    status = status_format(get_status(explorer))
    pid = comm_read(explorer).split(' ')[1]
    name = name_format(explorer)

    if status == 'Waiting':
        return format('%s - Last Command Not Processed Yet' % name)
    elif status == 'Paused':
        comm_write(explorer, format('WR %s' % pid))
        return format('Run: %s - Resuming' % name)
    elif status == 'Stopped':
        subprocess.Popen(['python', explorer.lower() + '_explorer.py'])
        return format('Run: %s - Started Running' % name)
    elif status == 'Running':
        return format('Run: %s - Already Running' % name)


def pause(explorer):
    """ (Str) -> Str
    Pause explorer depending on the status and return it's status
    """

    status = status_format(get_status(explorer))
    pid = comm_read(explorer).split(' ')[1]
    name = name_format(explorer)

    if status == 'Waiting':
        return format('%s - Last Command Not Processed Yet' % name)
    elif status == 'Paused':
        return format('Pause: %s - Already in Pause' % name)
    elif status == 'Stopped':
        return format('Pause: %s - Cannot pause non-Started Instance' % name)
    elif status == 'Running':
        comm_write(explorer, format('WP %s' % pid))
        return format('Pause: %s - Pausing' % name)


def stop(explorer):
    """ (Str) -> Str
    Stop explorer depending on the status and return it's status
    """

    status = status_format(get_status(explorer))
    pid = comm_read(explorer).split(' ')[1]
    name = name_format(explorer)

    if status == 'Waiting':
        return format('%s - Last Command Not Processed Yet' % name)
    elif status == 'Paused':
        comm_write(explorer, format('WS %s' % pid))
        return format('Stop: %s - Stopping Paused Explorer' % name)
    elif status == 'Stopped':
        return format('Stop: %s - Cannot Stop non-Started Explorer' % name)
    elif status == 'Running':
        comm_write(explorer, format('WS %s' % pid))
        return format('Stop: %s - Stopping' % name)


def force_stop(explorer):
    """ (Str) -> Str
    Force stop the explorer using it's pid and unix kill command.
    Also, forces the comm file to be in stop state, allowing new explorer
    to start.
    """
    name = name_format(explorer)
    subprocess.call("kill -9 ps -aux | grep -v grep |grep "+ explorer +  " | awk '{ print $2 }'", shell=True)
    return format('Force Stop: %s' % (name))


def status_output(explorer):
    """ (Str, Str) -> Str
    Checks and returns explorer's status
    """
    tmp_exp = explorer_format(explorer)
    status = status_format(get_status(tmp_exp))
    name = name_format(tmp_exp)

    return format('%s - %s' % (name, status))


if __name__ == '__main__':

    # To be able to run the script with arguments
    if len(sys.argv) == 3:

        exp, com = input_format(sys.argv[1], sys.argv[2])

        if com == 'status':
            print status_output(exp)

        elif com == 'run':
            print run(exp)

        elif com == 'pause':
            print pause(exp)

        elif com == 'stop':
            print stop(exp)

        elif com == 'fstop':
            print force_stop(exp)
        else:
            raise_input_error()
    else:
        raise_input_error()
