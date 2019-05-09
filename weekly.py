from loadsongs import load_song_lists
import random
import os
import json
import datetime

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
