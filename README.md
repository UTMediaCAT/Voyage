##Team ACME

Username  |Name | Email
--------------|-------------------|--------------------------
sunakujira1 | Yuya Iwabuchi | yuya.iwabuchi@gmail.com
sughandj | Jai Sughand | jaisughand@gmail.com
wangx173 | Xiang Wang | rogerxiang.wang@gmail.com
kbridge | Kyle Bridgemohansingh | bsingh.kyle@gmail.com
ryanbelt | Ryan Pan | ryanbelt1993129@hotmail.com

##Installation

Install Python and PIP

* [Python 2.7.x](https://www.python.org/downloads/release/python-278/) 
* [pip](https://pip.pypa.io/en/latest/installing.html)


Install all of the following api's on terminal

* PyMongo 2.7.2 :` pip install pymongo==2.7.2`
* Django 1.7 : 	`pip install Django==1.7`
* Newspaper 0.0.8: [click this](https://github.com/codelucas/newspaper/archive/3573217c7468a23a2690aa9c3930e3f3990cb382.zip) to download, extract then run commands:`pip install -r requirements.txt` then `python setup.py install`
* dateutil 1.5: [Click this](https://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz) to download, extract and then `python setup.py install`
* Tweepy : 	`pip install tweepy`

If any problem occurs, please contact one of us on the email address listed above.

##Usage

Create a new script and import executer.py by `import src/executer`


Use one of the functions we have:
```
add_monitor_site(url, name, influence)
add_foreign_site(url, name, influence)
get_sites_by_value(field, value)
get_all_sites()
get_monitor_sites()
get_foreign_sites()
set_site_by_value(url, field, new_value)
del_site(url)
del_sites(urls=None)
add_keyword(keyword)
get_all_keywords()
del_keyword(keyword)
del_all_keywords()
```
After configuration and modification, start exploring by:
```
run_article_explorer()
run_twitter_explorer() (coming soon)

```
Exploring articles may take a lot of time and resource depending on the site of the populated site.
For testing purpose, keep only 1 monitoring site with size < 500

For more information, view `src/execute.py`

##Task Board

Our Task Board and Assignment progress is on [Trello](https://trello.com/b/Y08lMCXy/cscc01-acme)

USER: **acmeteam4@gmail.com** Password: **acmeteam4**

In My Boards click **CSCC01-ACME** to see the progress

##Database 

All our articles and tweets are stored on [MongoDB](https://mongolab.com)

USER: **acmeteam4** Password: **acmeteam4**

click **CSCC01-ACME** to access the database

##Website

Our website is located at team04-Project\Website\index.html

It is organized with all the work in the every Phase so far
