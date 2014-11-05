
import os
import subprocess

os.chmod('./src/InstallScript.sh', 0700)
subprocess.call(['./src/InstallScript.sh'])

