#Profiling design decisions
* profiling is done with cprofile in addition to manual time.time() timers
* cprofile can't record the time taken for a specific call (all calls are lumped together), and only provides aggergate data, hence the need for manual time.time()
* time.time() is prone to errors in a multithreading environment if the program is preempted, causing the recorded time to take longer. this is worked around by allocating 1 core per running instance
* profiling results are recorded per crawl iteration and written to a .csv file for later analysis
* multiple sites (one foreign and one local) is used to ensure accuracy
