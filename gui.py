
import os
import subprocess
from Tkinter import *
from tkMessageBox import *
import webbrowser
import setup
import server

#+=========GUI===========GUI============GUI===========+
#---Window---#
#make window
window = Tk()
#change title
window.title("Voyage Exceute")
#change size
window.geometry("200x200")

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
    config = server.configuration()['server']
    server.run_server(config['ip_address'], config['port'])
    showinfo("Notice", "Server on!")

def close():
    '''
    ()-->None
    allow using python connect to CMD and run the sh script to close the django server
    '''
    config = server.configuration()['server']
    server.stop_server(config['port'])
    showinfo("Notice", "Server off!")

def open_web():
    '''
    ()-->None
    open the django web UI
    '''
    webbrowser.open('http://127.0.0.1:8000/admin')

def quit_app():
    window.destroy()

#---Widgets---#
#buttons
Button(window, text="Install", command = install_api).pack()
Button(window, text="Run Server", command = run).pack()
Button(window, text="Close Server", command = close).pack()
Button(window, text="Open Web", command = open_web).pack()
Button(text='Quit', command=quit_app).pack()

#+===================GUI END=====================+
window.mainloop()
