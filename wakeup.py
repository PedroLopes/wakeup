import shlex
import sys
import re
import random
from random import randint
import subprocess
import time
import threading


sleep_time = 1
sleep_start = 10
texts_dir="texts/"
wakeup_file="intro_"
morningplan_file="plan_"
file_extension=".txt"
vlc_location="/Applications/VLC.app/Contents/MacOS/"
music_location="/Users/pedro/Dropbox/12.senses/sound/wakeup/wakeset_"
music_extension=".mp3"
yoga_tutorial_location = "/Users/pedro/Dropbox/5.visuals/3.videos/yoga/"
yoga_tutorial_file = "a.mp4"

def play_background():
     subprocess.call(['mplayer', "/Users/pedro/Dropbox/12.senses/sound/QuietInletFood/01Tobiko.mp3"])
     #subprocess.call(['mplayer', music_location + str(random.randint(1,10)) + music_extension])
	#cinematic orchestra	1
	#fennesz		2
	#fennesz + sakamoto	3
	#godspeed		4
	#jagga jazzist		5
	#kashiwa		6
	#oren audience 1	7
	#quiet inlet		8
	#bad plus		9
	#reich 18 musicians    10


listen_thread = threading.Thread(target=play_background)
listen_thread.start()

time.sleep(sleep_start)

with open(texts_dir+wakeup_file+str(int(random.randint(1,2)))+file_extension) as f:
    wakeup_text = f.readlines()

for sentence in wakeup_text:
    if (sentence[0] != '-'):
    	subprocess.call(['say', str(sentence)])
    else:
	time.sleep(sleep_time)

with open(texts_dir+morningplan_file+str(int(random.randint(1,2)))+file_extension) as f:
    morningplan_text = f.readlines()

for sentence in morningplan_text:
    if (sentence[0] != '-'):
    	subprocess.call(['say', str(sentence)])
    else:
	time.sleep(sleep_time)

time.sleep(sleep_start)

#say time
if (time.localtime().tm_wday < 5):
    subprocess.call(['say', "Weekday"])
   #if so, we say we need to be in hpi at <> for <> (get from google)
else:    
    subprocess.call(['say', "Weekend"])
   #else we say our first thing if it is in less than 2h

time.sleep(sleep_start)

subprocess.call(['say', "Alright, let us start by"])
for sentence in morningplan_text:
    if (sentence[0] != '-'):
   	subprocess.call(['say', str(sentence)])
    	if (sentence[0] == 'y' and sentence[1] == 'o' and sentence[2] == 'g' and sentence[3] == 'a'): #seriously, this is what happens when you write code on train without internet
		subprocess.call([vlc_location+"VLC", "--no-audio", "--video-on-top", "-f", " --play-and-exit", yoga_tutorial_location+yoga_tutorial_file])
    	while True:
        	choice = raw_input("type will when you have done it.")
        	if choice == 'will':
        		break

#say goodbye (can we get next train time?)

listen_thread.join() #kill background process
sys.exit()
