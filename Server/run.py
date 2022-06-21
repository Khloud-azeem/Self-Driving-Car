import subprocess
import sched, time
import requests

s = sched.scheduler(time.time, time.sleep)
# url = 'http://192.168.1.14/GetLetter/'
def do_something(sc): 
    subprocess.Popen(['python', 'laneDetection.py', '-m'])
    s.enter(3, 1, do_something, (sc,))
s.enter(3, 1, do_something, (s,))
s.run()