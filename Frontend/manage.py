#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # To force local copy of Django
    if os.name != 'nt':
    	sys.path.insert(0, os.path.join(os.environ['HOME'], '.local/lib/python2.7/site-packages'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
