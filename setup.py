
import os
import subprocess
from Tkinter import *
from tkMessageBox import *
import webbrowser
#+=========GUI===========GUI============GUI===========+
#---Window---#
#make window
window = Tk()
#change title
window.title("Acme Exceute")
#change size
window.geometry("200x200")

#---Commands---#
#Install API command
def InstallApi():
    '''
    ()-->None
    allow using python connect to CMD and run the sh script to install all api using pip
    '''
    os.chmod('./src/InstallScript.sh', 0700)
    subprocess.call(['./src/InstallScript.sh'])
    showinfo("congratulation", "All Api sucessfully install")

def Run():
     '''
    ()-->None
    allow using python connect to CMD and run the sh script to open the django server
    '''
     os.chmod('./src/RunServer.sh', 0700)
    subprocess.Popen(['./src/RunServer.sh'], shell=True, stdout=subprocess.PIPE)
    showinfo("Notice", "Server on!")

def Close():
     '''
    ()-->None
    allow using python connect to CMD and run the sh script to close the django server
    '''
    os.chmod('./src/CloseServer.sh', 0700)
    subprocess.Popen(['./src/CloseServer.sh'], shell=True, stdout=subprocess.PIPE)
    showinfo("Notice", "Server off!")

def openweb():
     '''
    ()-->None
    open the django web UI
    '''
    webbrowser.open('http://127.0.0.1:8000/admin')

def quit_app():
    window.destroy()

#---Widgets---#
#buttons
Button(window, text="Install Api", command = InstallApi).pack()
Button(window, text="Runing Server", command = Run).pack()
Button(window, text="Close Server", command = Close).pack()
Button(window, text="Open", command = openweb).pack()
Button(text='quit', command=quit_app).pack()

#+===================GUI END=====================+
window.mainloop()
