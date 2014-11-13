
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
    webbrowser.open('http://127.0.0.1:8000/admin')

def quit_app():
    window.destroy()

#---Widgets---#
#buttons
Button(window, text="Install Api", command = install_api).pack()
Button(window, text="Runing Server", command = tun).pack()
Button(window, text="Close Server", command = vlose).pack()
Button(window, text="Open Web", command = open_web).pack()
Button(text='Quit', command=quit_app).pack()

#+===================GUI END=====================+
window.mainloop()
