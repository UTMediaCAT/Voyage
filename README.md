##UTMediaCAT 
MediaCAT is open-source web-based application, with a curated search engine. It crawls designated news websites and twitter accounts for citations of or hyperlinks to a list of source sites. MediaCAT then archives all referring stories and source stories, in preparation for an advanced analysis of the relations across the digital news-scape.

####[Home page](https://mediacat.utsc.utoronto.ca/)

Voyage currently has 2 components:
* __Web Server__ is capable of editing and displaying all the stored data as well as scopes you will provide to _Explorer_, through your favorite browser. 
* __Explorer__ searches the web using scopes given through to the _Web Server_ and goes for exploring for you. It will automatically store all relevant informations found on the way, so that you can show all the loot through _Web Server_.

##Installation and requirements
See: INSTALL.md

##Usage: Web Server
####Through terminal
* To start `python server.py run`

By defualt, this Django app is set to listen on all public IPs.

You can now access the server through http://IP:PORT/admin

The default is [http://127.0.0.1/admin](http://127.0.0.1/admin)

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
