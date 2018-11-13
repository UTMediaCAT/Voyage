from django import template
from subprocess import Popen, PIPE

register = template.Library()

@register.simple_tag
def get_article_run_status():
   return is_process_running("article_explorer.py")


@register.simple_tag
def get_twitter_run_status():
    return is_process_running("twitter_crawler.py")


def is_process_running(program_name):
    # get all running process by 'ps aux'
    ps_process = Popen(["ps", "aux"], stdout=PIPE)
    ps_output = ps_process.communicate()[0]

    status = "OFF"

    a = "python " + program_name
    conv_bytes = bytes(a, "ascii")
    if (conv_bytes) in ps_output:
        status = "ON"
    return status


