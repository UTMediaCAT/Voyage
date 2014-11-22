from django import template
from subprocess import Popen, PIPE
import time
import sys
import os

register = template.Library()
path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../../', 'src'))
sys.path.append(path)

import executer

@register.simple_tag
def get_article_run_status():
    os.chdir(path)
    return executer.status_output("article")

@register.simple_tag
def stop_button_article_explorer():
    if "Waiting" in get_article_run_status():
        return "Force Stop"
    else:
        return "Stop"

@register.simple_tag
def get_twitter_run_status():
    os.chdir(path)
    return executer.status_output("twitter")

@register.simple_tag
def stop_button_twitter_explorer():
    if "Waiting" in get_twitter_run_status():
        return "Force Stop"
    else:
        return "Stop"