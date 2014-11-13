
import os
import subprocess
#+=========GUI===========GUI============GUI===========+

#import os
#sys=os.path.dirname(os.path.dirname(__file__))
#print(sys)
from Tkinter import *
from tkMessageBox import *
import webbrowser


#---Window---#
#make window
window = Tk()
#change title
window.title("Acme Exceute")
#change size
window.geometry("200x200")

#---Commands---#
#go


#---Widgets---#
#buttons

def InstallApi():
    os.chmod('./src/InstallScript.sh', 0700)
    subprocess.call(['./src/InstallScript.sh'])
    showinfo("congratulation", "All Api sucessfully install")
Button(window, text="Install Api", command = InstallApi).pack(padx=0)

def Run():
    os.chmod('./src/RunServer.sh', 0700)
    #subprocess.call(['./src/RunServer.sh'])
    subprocess.Popen(['./src/RunServer.sh'], shell=True, stdout=subprocess.PIPE)
    showinfo("Notice", "Server on!")
    #subprocess.Popen(['./src/RunServer.sh'], shell=True, stdout=subprocess.PIPE)
    
Button(window, text="Runing Server", command = Run).pack()

def Close():
    os.chmod('./src/CloseServer.sh', 0700)
    subprocess.Popen(['./src/CloseServer.sh'], shell=True, stdout=subprocess.PIPE)
    showinfo("Notice", "Server off!")
    
Button(window, text="Close Server", command = Close).pack()

def openweb():
    webbrowser.open('http://127.0.0.1:8000/admin')
Button(window, text="Open", command = openweb).pack()
#message


#quit
def quit_app():
    window.destroy()
Button(text='quit', command=quit_app).pack()
#+===================GUI END=====================+
window.mainloop()
