##Voyage
Voyage currently has 2 components:
* __Web Server__ is capable of editing and displaying all the stored data as well as scopes you will provide to _Explorer_, through your favorite browser. 
* __Explorer__ searches the web using scopes given through to the _Web Server_ and goes for exploring for you. It will automatically store all relevant informations found on the way, so that you can show all the loot through _Web Server_.

##Team ACME

Username  |Name | Email
--------------|-------------------|--------------------------
sunakujira1 | Yuya Iwabuchi | yuya.iwabuchi@gmail.com
sughandj | Jai Sughand | jaisughand@gmail.com
wangx173 | Xiang Wang | rogerxiang.wang@gmail.com
kbridge | Kyle Bridgemohansingh | bsingh.kyle@gmail.com
ryanbelt | Ryan Pan | ryanbelt1993129@hotmail.com

##Requirement

* [Python 2.7.x](https://www.python.org/downloads/release/python-278/) 
* [Wget 1.14+](http://www.gnu.org/software/wget/)

##Installation
####Method 1: Through tkinter
* Download, extract the __master__ then execute on terminal `python gui.py`
* click `Install` in the pop up GUI.
* Done!

####Method 2: Through terminal
* Download, extract the __master__ then execute on terminal `python setup.py` 
* Done!

If any problem occurs, please contact one of us on the email address listed above.

##Usage: Web Server
####Method 1: Through tkinter
* To start `python gui.py` then click _Run Server_
* To stop click _Stop Server_

####Method 2: Through terminal
* To start `python server.py run`
* To stop `python server.py stop`

You can now access the server through http://IP:PORT/admin
The default is [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)


__Default Login Credentials:__
* User: acme
* Password: cscc01

#Tabs
####Home
Here you can view your action history and quick navigations to the database
####Scope
Here, you can view and edit 4 requirement to explore:
* __Monitoring Sites__: The site in which explorer will look into. It will automatically get validated when adding.
* __Twitter Accounts__: The twitter accounts which explorer will look into. It will automatically be validated when adding.
* __Foreign Sites__: The site in which explorer checks if it used as source.
* __Keywords__: The words in which the explorer will see if it is used.

####Data
Here, you can view the collected data by the explorer. Furthermore, you can download the archived entry as __Web Archive__.
For demo, it is filled with pre-explored entries.
####Downloads
Here, you can download all the data stored in the database as __Json__ format.
####Statistics
Here, you can view the statistics among the collected entries.

For example, you can view how many articles got collected per day as a [Annotation Chart](https://developers.google.com/chart/interactive/docs/gallery/annotationchart)
####Visualizations
Here, you can view the relations between each of the 4 scopes, based on the exploration.

####Authorization
Here, you can manage the users and groups used for log in.
Furthermore, users can have different _permissions_.

## Exploring
Once your scope is ready, you may start exploring by clicking __Run__ on the status bar.
* __Article Explorer__ will explore through the _Monitoring Sites_ for articles
* __Twitter Explorer__ will explore through _Twitter_ for _Twitter Accounts's_ posts

___
___
##Task Board
Our Task Board and Assignment progress is on [Trello](https://trello.com/b/Y08lMCXy/cscc01-acme)

USER: **acmeteam4@gmail.com** Password: **acmeteam4**

In My Boards click **CSCC01-ACME** to see the progress

##Website

Our website is located at team04-Project\Website\index.html

It is organized with all the work in the every Phase so far
