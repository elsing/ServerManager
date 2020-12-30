##import threading
##import time
##
##
##class ThreadingExample(object):
##    """ Threading example class
##    The run() method will be started and it will run in the background
##    until the application exits.
##    """
##
##    def __init__(self, interval=1):
##        """ Constructor
##        :type interval: int
##        :param interval: Check interval, in seconds
##        """
##        self.interval = interval
##
##        thread = threading.Thread(target=self.run, args=())
##        thread.daemon = True                            # Daemonize thread
##        thread.start()                                  # Start the execution
##
##    def run(self):
##        """ Method that runs forever """
##        while True:
##            # Do something
##            print('Doing something imporant in the background')
##
##            time.sleep(self.interval)
##
##example = ThreadingExample()
##time.sleep(3)
##print('Checkpoint')
##time.sleep(2)
##print('Bye')

#import urllib2

##from multiprocessing.dummy import Pool as ThreadPool
##import subprocess
##import os
##
##urls = [
##  'http://www.python.org', 
##  'http://www.python.org/about/',
##  'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
##  'http://www.python.org/doc/',
##  'http://www.python.org/download/',
##  'http://www.python.org/getit/',
##  'http://www.python.org/community/',
##  'https://wiki.python.org/moin/',
##]

##def ping(host):
##    reply = subprocess.call(['ping', '-n', '4', '-w', '32', host], stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
##    print(reply)
##    if reply == 0:
##        return("Up")
##    else:
##        return("Down")
##
##ips = [
##    '192.168.1.5',
##    "162.168.1.4",
##    '162.168.1.4',
##    '162.168.1.250',
##    '162.168.1.10',
##]
### make the Pool of workers
##pool = ThreadPool(5) 
##
### open the urls in their own threads
### and return the results
##results = pool.map(ping, ips)
##
### close the pool and wait for the work to finish 
##pool.close() 
##pool.join()
##
##print(results)

import random

randID = ""
results = []
for i in range( 9):
    #code+=chr(random.randint(65,90))
    randID+=(str(random.randint(0,9)))
print(randID)


##results = []
##
##
##for i in range(0,4):
##    results.append(["1","2","3"])
##
##print(results)











