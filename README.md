## :no_entry: [DEPRECATED] Active at https://github.com/UTMediaCAT/mediacat-domain-crawler
MediaCAT is open-source web-based application, with a curated search engine. It crawls designated news websites and twitter accounts for citations of or hyperlinks to a list of source sites. MediaCAT then archives all referring stories and source stories, in preparation for an advanced analysis of the relations across the digital news-scape.

#### [Home page](http://mediacat.utsc.utoronto.ca/)

Voyage currently has 2 components:
* __Web Server__ is capable of editing and displaying all the stored data as well as scopes you will provide to _Explorer_, through your favorite browser.
* __Explorer__ searches the web using scopes given through to the _Web Server_ and goes for exploring for you. It will automatically store all relevant informations found on the way, so that you can show all the loot through _Web Server_.


## Requirements
Before installation, verify you meet the following requirements

##### [Python 2.7.9+](https://www.python.org/downloads/release/python-279/)
The required version should be installed on Debian Jessie (and up), as well as Ubuntu 14.04 LTS (and up).
You can check your current version by `python --version`

Note: The project as of right now is supported up to Python 3.5.2. on Ubuntu 16.0.4. It is currently in the works to make the project compatible with Python 3.6.9. on Ubuntu 18.0.4.

If your Python version differs from Python 3.5, we highly recommend using virtual environment tools (such as pyenv) to help manage multiple Python versions. 

Typically, to use Python 2 use `python`. 
To use Python 3 use `python3`. 
To use whatever python version is set in your python virtual environment, use `python`.

##### [Wget 1.14+](http://www.gnu.org/software/wget/)
You can check your current version by `wget --version`

## Installation
* Clone the repo
* Go to the main folder
* Run the install script:
```
sudo -i
sudo ./InstallScript.sh
```

## Set Up Database
#### Log into admin account
In order to use Postgres, we'll need to log into that account. You can do that by typing:
```
sudo -i -u postgres
```
You will be asked for your normal user password and then will be given a shell prompt for the postgres user.
#### Get a Postgres Prompt
You can get a Postgres prompt immediately by typing:
```
psql
```
#### Add a password for the user:
By default, when you create a PostgreSQL cluster, password authentication for the database superuser (“postgres”) is disabled. In
order to make Django have access to this user, you will need to add password savely for this user.

In the Postgres prompt:
```
postgres=# \password
Enter new password: password
Enter it again:password
```
#### Create Database
In the Postgres prompt:
```
postgres=# create database mediacat;
postgres=# create database crawler;
```
You may exit out of postgres now

#### To integrate this database with Django:
Plase configure the databse setting in  `Frontend/Frontend/settings.py`. 
For example:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mediacat',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```


## Configuration
You can edit the config.yaml file for personal settings

:bangbang: IMPORTANT :bangbang: 

For production instances, be sure to use a new randomized SECRET_KEY in `Frontend/Frontend/settings.py`. 
A new SECRET key can be generate with the following python script:
```
import random
''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for _ in range(50))
```

#### Twitter Crawler
Please configure twitter credentials in config.yaml before using twitter crawler. You can get twitter credentials from <https://apps.twitter.com/>.

## Usage: Web Server
#### If it is your FIRST time to run the server:
please make sure to apply migrations under [Frontend folder](https://github.com/UTMediaCAT/Voyage/tree/master/Frontend):
```
python manage.py makemigrations
python manage.py migrate
```
And create admin users
```
python manage.py createsuperuser
```

#### Otherwise start/stop the server:

* To start `python server.py run`

(note: if using port 80, then```sudo``` is needed to run/stop the server) 

By default, this Django app is set to listen on all public IPs (port 80).

You can now access the server through http://IP:PORT/admin

The default is [http://127.0.0.1/admin](http://127.0.0.1/admin)



# Tabs
#### Home
Here you can view your action history and quick navigations to the database
#### Scope
Here, you can view and edit 4 requirement to explore:
* __Referring Sites__: The sites in which explorer will look into. It will automatically get validated when adding.
* __Referring Twitter Accounts__: The twitter accounts which explorer will look into. It will automatically be validated when adding.
* __Source Sites__: The sites which explorer looks for in the articles/tweets if they are used as source.
* __Source Twitter Accounts__ : The twitter accounts which explorer will look for in articles/tweets if they are used as source.
* __Keywords__: The words which explorer look for in the articles/tweets if they are used.

#### Data
Here, you can view the collected data by the explorer. Furthermore, you can download the archived entry as __Web Archive__.
For demo, it is filled with pre-explored entries.
#### Downloads
Here, you can download all the data stored in the database as __Json__ format.
#### Statistics
Here, you can view the statistics among the collected entries.

For example, you can view how many articles got collected per day as a [Annotation Chart](https://developers.google.com/chart/interactive/docs/gallery/annotationchart)
#### Visualizations
Here, you can view the relations between each of the 4 scopes, based on the exploration.

#### Authorization
Here, you can manage the users and groups used for log in.
Furthermore, users can have different _permissions_.

## Exploring
Once your scope is ready, you may use the following explorers under [src](https://github.com/UTMediaCAT/Voyage/tree/master/src) folder to crawl news and Tweets:
* __Article Explorer__ will explore through the _Referring Sites_ for articles
* __Twitter Crawler__ will explore through _Referring Twitter Accounts's_ posts

### Article Explorer
The article explorer will explore each site under a given domain. After this crawler is finished crawling the entire domain the shallow crawler will activate. At this point, the article explorer will only go N `levels` down from the domain's homepage. A visual prompt indicating shallow crawling will be visible in the `Scope/Referring Sites` tab. The `level` value is set to a default of 3, but can be changed in the config.yaml file.

__:bangbang: NOTE__: The article crawler can be quite taxing in terms of resources used. On initial tests with the shallow crawler it was found that the article crawler would freeze after a certain amount of time (freezing occured on a server instace with the follwing specs: 1 vCPU, and 2GB RAM with the crawler having 77 domains in its referring scope). Once we began testing using a more powerful server instance (10 vCPU, and 32 GB RAM) the freezing issues stopped. If you do run into freezing issues, the `article_explorer_run.sh` found under the `src/` folder contains some lines of code that will automatically restart the crawler after a certain period of time.

#### Running the Explorer

To run the crawler you must first run the `warc_queue.py` so that the warc files will be created as the crawler runs. Note: We create a screen so that the warc queue can operate in the background.

```
screen -S warc
python src/warc_queue.py
```

(Ctrl+A followed by Ctrl+D to get back to the original screen)
After this, you must run the actual crawler. 

```
screen -S article
python src/article_explorer.py
```

### Twitter Crawler 
Twitter crawler has three modes of crawling: `timeline`, `streaming` and `history`, with `timeline` and `streaming` based on [twarc](https://github.com/DocNow/twarc) and `history` based on [GetOldTweets-python](https://github.com/Jefferson-Henrique/GetOldTweets-python). 
* `timeline` mode will crawl the timeline of _Referring Twitter Accounts_ with up to 3200 of a user's most recent Tweets (Twitter's API constraint). You can set the frequency of timeline re-crawling in [config.yaml](https://github.com/UTMediaCAT/Voyage/blob/master/config.yaml) (the default frequency is crawling timeline every 30 days).
```
python twitter_crawler.py timeline
```
* `streaming` mode will crawl Tweets of _Referring Twitter Accounts_ on a real-time basis.
```
python twitter_crawler.py streaming
```
* `history` mode will collect all Tweets posted by _Referring Twitter Accounts_.
```
python twitter_crawler.py history
```
Running twitter crawler with no parameter will run all three modes together by default.
```
python twitter_crawler.py
```

___

## UnitTest
Unit test files are located under `src/unit_tests`
