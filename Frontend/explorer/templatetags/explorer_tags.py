from django import template
from subprocess import Popen, PIPE

register = template.Library()

@register.simple_tag
def get_article_run_status():
    ps_process = Popen(["ps", "aux"], stdout=PIPE)
    ps_output = ps_process.communicate()[0]

    status = "OFF"
    if "python article_explorer.py" in ps_output:
	status = "ON"
    return status


