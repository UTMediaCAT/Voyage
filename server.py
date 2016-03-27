
import sys
import subprocess
import time
import os

# To load configurations
import yaml



class InputError(Exception):
    """ (None) -> None
    Custom Exception to raise when input is wrong
    """
    pass


def raise_input_error():
    """ (None) -> None
    Raise InputError wtih the proper usage of this script
    """
    raise InputError("Usage: python server.py [run|stop]")


def configuration():
    """ (None) -> dict
    Returns a dictionary containing the micro settings from the
    config.yaml file located in the directory containing this file
    """
    config_yaml = open("config.yaml", 'r')
    config = yaml.load(config_yaml)
    config_yaml.close()
    return config


def check_command(arg1):
    if arg1.lower() == "run":
        return "run"
    elif arg1.lower() == "stop":
        return "stop"
    raise_input_error()

def run_server(ip_address, port):
    """ (None) -> None
    Gives installation shell script permission and executes
    """
    os.chmod('./src/RunServer.sh', 0700)
    subprocess.call(['./src/RunServer.sh', 
                     format('%s:%i' % (ip_address, port))])
    os.chmod('./src/RunSchedule.sh', 0700)
    subprocess.call(['./src/RunSchedule.sh'])


def stop_server(port):
    """ (None) -> None
    Gives installation shell script permission and executes
    """
    config = configuration()['server']
    os.chmod('./src/StopServer.sh', 0700)
    subprocess.call(['./src/StopServer.sh', format('%i' % port)])
    os.chmod('./src/StopSchedule.sh', 0700)
    subprocess.call(['./src/StopSchedule.sh'])


if __name__ == "__main__":
    # Change current working directory to project root folder
    old_path  = os.getcwd()
    path = os.path.abspath(os.path.dirname(__file__))
    try:
        os.chdir(path)
        if not len(sys.argv) == 2:
            raise_input_error()
        else:
            command = check_command(sys.argv[1])
            config = configuration()['server']
            if command == "run":
                run_server(config['ip_address'], config['port'])
                print 'Server Running'
            else:
                stop_server(config['port'])
                print 'Server Stopped'
    finally:
        os.chdir(old_path)
