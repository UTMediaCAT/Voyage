from django import template
from subprocess import Popen, PIPE
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
def run_article_explorer():
    os.chdir(path)
    executer.run("article")

@register.simple_tag
def pause_article_explorer():
    os.chdir(path)
    executer.pause("article")

@register.simple_tag
def stop_article_explorer():
    os.chdir(path)
    executer.stop("article")

@register.simple_tag
def get_twitter_run_status():
    os.chdir(path)
    return executer.status_output("twitter")

@register.simple_tag
def run_twitter_explorer():
    os.chdir(path)
    executer.run("twitter")

@register.simple_tag
def pause_twitter_explorer():
    os.chdir(path)
    executer.pause("twitter")

@register.simple_tag
def stop_twitter_explorer():
    os.chdir(path)
    executer.stop("twitter")