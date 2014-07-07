import shlex
import sys
import re
import random
from random import randint
import subprocess
import threading
import argparse
import httplib2
import os
import datetime
import time
import feed.date.rfc3339

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools
from rfc3339 import rfc3339
from dateutil.parser import parse 


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
yoga_tutorial_extension = ".mp4"
next_meeting_range_weekends = 3
secure_dir_no_git = "not-git-tracked-secure"
xrds_dir_no_git = "xrds-data"
newline = '\n'
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
today=time.localtime().tm_wday
day=time.localtime().tm_mday
hour=time.localtime().tm_hour
month=time.localtime().tm_mon
next_event_summary = None
next_event_time = None

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), secure_dir_no_git+'/client_secrets.json')
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))

with open(secure_dir_no_git+'/calendar_id.txt') as f:
    calendarID = f.readlines()
calendarID = str(calendarID[0]).replace('\n', "")               #ID of the google calendar to write the events to

storage = file.Storage(secure_dir_no_git+'/sample.dat')
credentials = storage.get()
if credentials is None or credentials.invalid:
  credentials = tools.run_flow(FLOW, storage, flags)
http = httplib2.Http()
http = credentials.authorize(http)
service = discovery.build('calendar', 'v3', http=http)

try:
  print("OK: Probing for google / internet . . . ")

  event_start_date = datetime.date(datetime.datetime.now().year,month,day)
  start_day_o = event_start_date.toordinal()

  event_start_time = datetime.time(int("03"), int("00"))
  event_start_date = datetime.date.fromordinal(start_day_o)
  event_start = datetime.datetime.combine(event_start_date, event_start_time)
  event_start = rfc3339(event_start)
  _timeMin = event_start
  event_start_time = datetime.time(int("23"), int("00"))
  event_start = datetime.datetime.combine(event_start_date, event_start_time)
  event_start = rfc3339(event_start)
  _timeMax = event_start 

  page_token = None
  events = service.events().list(calendarId=calendarID, maxResults=int(2), pageToken=page_token, singleEvents=True, orderBy="startTime", timeMax=_timeMax, timeMin=_timeMin).execute()
  next_event_summary = (events['items'])[0]['summary']
  next_event_time = (events['items'])[0]['start']
  timestamp = feed.date.rfc3339.tf_from_timestamp(next_event_time['dateTime'])
  next_event_time = datetime.datetime.fromtimestamp(timestamp)

except client.AccessTokenRefreshError:
  print ("SORRY: The credentials have been revoked or expired, please re-run"
    "the application to re-authorize // could be that we don't have internet access.")

def play_background():
     subprocess.call(['mplayer', music_location + str(random.randint(1,10)) + music_extension])

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

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
today=time.localtime().tm_wday
day=time.localtime().tm_mday
hour=time.localtime().tm_hour
month=time.localtime().tm_mon
subprocess.call(['say', "Today is "+ days[today] + " day " + str(day) + " of " + months[month-1]])
#TODO #if so, we say we need to be in hpi at <> for <> (get from google)

if next_event_summary is not None:
  subprocess.call(['say', "We have " + next_event_summary + " at " + str(next_event_time.hour)])
  time.sleep(sleep_start)

subprocess.call(['say', "Alright, let us start by"])
for sentence in morningplan_text:
    if (sentence[0] != '-'):
   	subprocess.call(['say', str(sentence)])
    	if (sentence[0] == 'y' and sentence[1] == 'o' and sentence[2] == 'g' and sentence[3] == 'a'): #seriously, this is what happens when you write code on train without internet
		subprocess.call([vlc_location+"VLC", "--no-audio", "--video-on-top", "-f", " --play-and-exit", yoga_tutorial_location+str(random.randint(1,3))+yoga_tutorial_extension])
    	while True:
        	choice = raw_input("type will when you have done it.")
        	if choice == 'will':
        		break

#say goodbye (can we get next train time?)
listen_thread.join() #kill background process
sys.exit()

####ideas for next versions
#cardinality = ["first", "second", "third", "forth", "fifth", "sixth", "seventh", "eight", "ninght", "tenth", "eleventh", "twelveth", "thirteenth", "fourtheenth", "fifthteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth", "th"]
#day_spoken = str(day) #this is code to get fancier speech output on days, quite irrelevant
#if (day < 20):
#	day_spoken = cardinality[day]
#elif (day >= 20 and day % 10 == 0):
#	day_spoken = cardinality[19]
