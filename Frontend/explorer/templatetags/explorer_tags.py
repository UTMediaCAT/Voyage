from django import template
from subprocess import Popen, PIPE
import time
import sys
import os

old_path = os.getcwd()
register = template.Library()
path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../../', 'src'))
sys.path.append(path)

import executer

@register.simple_tag
def get_article_run_status():
    try:
        os.chdir(path)
        result = executer.status_output("article")
    finally:
        os.chdir(old_path)
    return result

@register.simple_tag
def stop_button_article_explorer():
    if "Waiting" in get_article_run_status():
        return "[F]Stop"
    else:
        return "Stop"

@register.simple_tag
def get_twitter_run_status():
    try:
        os.chdir(path)
        result = executer.status_output("twitter")
    finally:
        os.chdir(old_path)
    return result

@register.simple_tag
def stop_button_twitter_explorer():
    if "Waiting" in get_twitter_run_status():
        return "[F]Stop"
    else:
        return "Stop"