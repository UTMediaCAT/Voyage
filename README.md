##UTMediaCAT 
MediaCAT is open-source web-based application, with a curated search engine. It crawls designated news websites and twitter accounts for citations of or hyperlinks to a list of source sites. MediaCAT then archives all referring stories and source stories, in preparation for an advanced analysis of the relations across the digital news-scape.

######[Home page](https://mediacat.utsc.utoronto.ca/)

Voyage currently has 2 components:
* __Web Server__ is capable of editing and displaying all the stored data as well as scopes you will provide to _Explorer_, through your favorite browser. 
* __Explorer__ searches the web using scopes given through to the _Web Server_ and goes for exploring for you. It will automatically store all relevant informations found on the way, so that you can show all the loot through _Web Server_.

##Requirements
Before installation, verify you meet the following requirements
#####[Python 2.7.10+](https://www.python.org/downloads/release/python-2710/)
The required version should be installed on Debian Jessie (and up), as well as Ubuntu 16.04 LTS (and up). You can check your current version by `python --version`

If the version available through your package mananger is not 2.7.10 or above, you will need to manually build and install 2.7.10. Luckily, there is a tool for doing that.

	curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
	sudo apt-get build-dep python2.7
	pyenv install 2.7.10
	pyenv global 2.7.10
	pip install -U pip

#####[Wget 1.14+](http://www.gnu.org/software/wget/)
You can check your current version by `wget --version`

##Installation
####Option 1: Default Install
* Clone the repo
* Go to the main folder
* Run DefaultInstall script
```
sudo ./DefaultInstall.sh 
```

####Option 2: Custom Install
You can modify the steps below based on your own development enviroment.
* To swtich the root user: 
```
sudo -i
```
* Install apt dependencies: 
```
apt-get update && apt-get install -y python-pip python-dev libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev python3-pip  libmysqlclient-dev phantomjs postgresql postgresql-contrib
```
PhantomJS should be available on Ubuntu. If it's not available in your distribution, you may install it manually by downloading the [prebuilt version](http://phantomjs.org/download.html) and extracting the contents of bin `/usr/local/bin`.

* Clone the repo

* Install python dependencies:

from the root of the repo:
```
pip install -r requirements.txt
pip3 install wpull
```

* Run the install script:
```
./InstallScript.sh
```


##Configuration
You can edit the config.yaml file for personal settings

:bangbang: IMPORTANT :bangbang: For production instances, be sure to use a new randomized SECRET_KEY in `Frontend/Frontend/settings.py`. A new SECRET key can be generate with the following python script:
```
import random
''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for _ in range(50))
```

##Usage: Web Server
####Before starting the web server, please run the following to apply migrations:
```
python Frontend/manage.py makemigrations
python Frontend/manage.py migrate
```
####Then you can strat/stop the server
* To start `sudo python server.py run`
* To stop `sudo python server.py stop`

By defualt, this Django app is set to listen on all public IPs.

You can now access the server through http://IP:PORT/admin

The default is [http://127.0.0.1/admin](http://127.0.0.1/admin)


__Default Login Credentials:__
* User: admin
* Password: admin

#Tabs
####Home
Here you can view your action history and quick navigations to the database
####Scope
Here, you can view and edit 4 requirement to explore:
* __Referring Sites__: The sites in which explorer will look into. It will automatically get validated when adding.
* __Twitter Accounts__: The twitter accounts which explorer will look into. It will automatically be validated when adding.
* __Source Sites__: The sites which explorer looks for in the articles/tweets if they are used as source.
* __Keywords__: The words which explorer look for in the articles/tweets if they are used.

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
* __Article Explorer__ will explore through the _Referring Sites_ for articles
* __Twitter Explorer__ will explore through _Twitter_ for _Twitter Accounts's_ posts

___
___

##UnitTest
Unit test files are located under `src/unit_tests`
