# wakeup
======
**Wakeup script** that plays soothing music, reads out your day's agenda from google cal, plays your yoga tutorial video and has a nice chat with you. 

This uses google calendar API to connect to your google calendar and read out the first nice activity of the day. This requires a step of setup between your python API and Google API (more on that https://developers.google.com/google-apps/calendar/quickstart/python).

## notes
===
Was developed for very personal use, means that it does more than you might need. But then again it is open code that you can use for your own ideas. 

## installing it
===
This is python code. You need **python**.

simply: ``./install_deps.sh`` (install one dependency to which I could not find a pip install)
then: pip install -r requirements.txt
You should now have everything to run this.  

## testing it
``python wakeup.py``
