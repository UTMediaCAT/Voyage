
import os
import subprocess
from Tkinter import *
from tkMessageBox import *
import webbrowser
import setup
#+=========GUI===========GUI============GUI===========+
#---Window---#
#make window
window = Tk()
#change title
window.title("Voyage Exceute")
#change size
window.geometry("200x220")

#---Commands---#
#Install API command
def install_api():
    '''
    ()-->None
    allow using python connect to CMD and run the sh script to install all api using pip
    '''
    setup.install()
    showinfo("congratulation", "All Api sucessfully install")

def run():
    '''
    ()-->None
    allow using python connect to CMD and run the sh script to open the django server
    '''
    os.chmod('./src/RunServer.sh', 0700)
    subprocess.Popen(['./src/RunServer.sh'], shell=True, stdout=subprocess.PIPE)
    showinfo("Notice", "Server on!")

def close():
    '''
    ()-->None
    allow using python connect to CMD and run the sh script to close the django server
    '''
    os.chmod('./src/CloseServer.sh', 0700)
    subprocess.Popen(['./src/CloseServer.sh'], shell=True, stdout=subprocess.PIPE)
    showinfo("Notice", "Server off!")

def open_web():
    '''
    ()-->None
    open the django web UI
    '''
    webbrowser.open('http://127.0.0.1:7999/admin')

def run_proxy():
    '''
    ()-->None
    allow using python connect to CMD and run the sh script to run the warc proxy
    '''
    #os.chmod('./src/RunProxy.sh', 0700)
    subprocess.Popen(['./src/RunProxy.sh'], shell=True, stdout=subprocess.PIPE)
    showinfo("Notice", "Server on!")

def close_proxy():
    '''
    ()-->None
    allow using python connect to CMD and run the sh script to close the warc proxy
    '''
    #os.chmod('./src/CloseProxy.sh', 0700)
    subprocess.Popen(['./src/CloseProxy.sh'], shell=True, stdout=subprocess.PIPE)
    showinfo("Notice", "Server off!")

def open_proxy():
    '''
    ()-->None
    open the warc proxy on web to view the warc
    '''
    webbrowser.open('http://127.0.0.1:8000')

def quit_app():
    window.destroy()

#---Widgets---#
#buttons
Button(window, text="Install", command = install_api).pack()
Button(window, text="Run Server", command = run).pack()
Button(window, text="Close Server", command = close).pack()
Button(window, text="Open Web", command = open_web).pack()
Button(window, text="Run Proxy", command = run_proxy).pack()
Button(window, text="Close Proxy", command = close_proxy).pack()
Button(window, text="Open Proxy Web", command = open_proxy).pack()
Button(text='Quit', command=quit_app).pack()

#+===================GUI END=====================+
window.mainloop()
