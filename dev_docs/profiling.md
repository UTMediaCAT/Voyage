#Profiling design decisions
* profiling is done with cprofile in addition to manual time.time() timers
* cprofile can't record the time taken for a specific call (all calls are lumped together), and only provides aggergate data, hence the need for manual time.time()
* time.time() is prone to errors in a multithreading environment if the program is preempted, causing the recorded time to take longer. this is worked around by allocating 1 core per running instance
* profiling results are recorded per crawl iteration and written to a .csv file for later analysis
* multiple sites (one foreign and one local) is used to ensure accuracy

#Profiling results
###Table of time taken to do each operation (in seconds, averaged across iterations)

|  | in-memory | database |
|---|---|---|
| total | 0.812163224 | 1.103184348 |
| total_unaccounted | 0.284702686 | 0.407231798 |
| crawler_total | 0.391773038 | 0.614576046 |
| crawler_unaccounted | 9.77159E-05 | 7.95276E-05 |
| preliminary_parse_total | 0.132138106 | 0.077791874 |
| explorer_article_total | 0.000480708 | 0.000412674 |
| get_keywords_total | 0.001989078 | 0.002126981 |
| get_sources_sites_total | 0.000758123 | 0.00067787 |
| get_sources_twitter_total | 0.000321485 | 0.000367104 |
| tovisit_pop_total | 0.006414753 | 0.001922648 |
| article_download_total | 0.318082063 | 0.569303254 |
| get_links_total | 0.00867734 | 0.005932315 |
| process_links_total | 0.058501166 | 0.037338301 |

On the surface, storing the visited set in memory appears to be faster than in database. However, if we only look at process_links_total, which is the portion of code that changes if we switch between memory and database, we see that the database is in fact *1.57x faster* than memory. Even if we take into account that (for whatever reason) the memory crawling instance processed more links per iteration, the database approach is still *1.12x faster*. Multiple reasons have been proposed for the discrepencies between the benchmarked time and the overall time. William thinks that the difference in overall crawling time is solely attributed to differences in network speed (the tests were conducted on seperate VMs, but in the same datacenter region), whereas Anya thinks the difference in time is caused by background database operations. More testing is needed to thoroughly study this issue.

#Future profiling methodology
To eliminate as many variables as possible, two approaches are purposed to fix the shortcomings with the previous benchmarking trial.

##Proposal \#1: cache pages to be visited on
On the first run, the crawler will save each page it encounters to disk. This run will not be used for profiling. Subsequent runs will use a modified crawler that get the page directly from disk rather than over the network.

Pros:
* Most accurate simulation of crawler operation (everything in a normal crawl loop is done)

Cons:
* Includes operations that are unchanged between database/memory implementation (and thus shouldn't be included as they should run in the same time)

##Proposal \#2: log and replay operations done to the ADT
On the first run, the crawler will log each call it makes to the visited ADT (whether it be set or database). This log will then be saved to disk. Profiling data will be obtained by "replaying" the log file on the two ADTs (basically making the same calls again) and see which can complete all the operations the fastest.

Pros:
* Only profiles parts of the code that have changed
* Disk latency less of an issue (compared to #1), because there is less to fetch from disk

Cons:
* Doesn't simulate a complete crawl loop
