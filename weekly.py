from loadsongs import load_song_lists
import random
import os
import json
import datetime
import schedule
import time
from threading import Thread

def get_current_weekly():
    with open('weekly.json', 'r') as f:
        weeklylist = json.load(f)
    return weeklylist['song']

def randomize_weekly():
    songs = load_song_lists()
    with open('weekly.json', 'r') as f:
        weeklyjson = json.load(f)
    weeklyjson['song'] =  random.choice(load_song_lists())[0]
    print(weeklyjson)
    with open('weekly.json', 'w') as f:
        json.dump(weeklyjson, f, indent=2)

schedule.every().friday.at("13:51").do(randomize_weekly)

class isitfridayyet(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon=True
        self.start()
    def run(self):
        while True:
            schedule.run_pending()

#isitfridayyet()
