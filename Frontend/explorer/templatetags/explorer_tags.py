from django import template
from subprocess import Popen, PIPE
import time
import sys
import os

register = template.Library()

import executer

@register.simple_tag
def get_article_run_status():
    return "disabled"

@register.simple_tag
def stop_button_article_explorer():
    if "Waiting" in get_article_run_status():
        return "[F]Stop"
    else:
        return "Stop"

@register.simple_tag
def get_twitter_run_status():
    return "disabled"

@register.simple_tag
def stop_button_twitter_explorer():
    if "Waiting" in get_twitter_run_status():
        return "[F]Stop"
    else:
        return "Stop"