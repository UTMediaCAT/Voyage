
import os
import subprocess

def install():
    """ (None) -> None
    Gives installation shell script permission and executes
    """
    os.chmod('./src/InstallScript.sh', 0700)
    subprocess.call(['./src/InstallScript.sh'])

if __name__ == '__main__':
    install()