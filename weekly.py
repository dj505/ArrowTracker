from loadsongs import load_song_lists
from app.models import WeeklyPost
from app import db, current_app, raw_songdata
import datetime
import random
import json
import app
import os
import send_webhook

songpairs, songtypes = load_song_lists()

def get_current_weekly():
    with open('weekly.json', 'r') as f:
        weeklylist = json.load(f)
    return [weeklylist['song'], weeklylist['length']]

def create_json(item):
    scoredict = {
        item.id: {
            'song': item.song,
            'difficulty': item.difficulty,
            'lettergrade': item.lettergrade,
            'score': item.score,
            'stagepass': item.stagepass,
            'platform': item.platform,
            'ranked': item.ranked,
            'author': item.author.username
        }
    }
    rootdir = os.path.join(current_app.root_path, f'static/archived_weekly')
    datedir = os.path.join(current_app.root_path, f'static/archived_weekly', datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    if not os.path.exists(datedir):
        os.makedirs(datedir)
    jsonfile = os.path.join(rootdir, datedir, f'{item.id}.json')
    with open(jsonfile, 'w+') as f:
        json.dump(scoredict, f, indent=2)

def randomize_weekly(app):
    songs = load_song_lists()
    with open('weekly.json', 'r') as f:
        weeklyjson = json.load(f)
    newsong = random.choice(songpairs)[0]
    weeklyjson['song'] = newsong.decode('utf-8')
    weeklyjson['length'] = raw_songdata[newsong.decode('utf-8')]['length']
    weeklyjson['diffs'] = raw_songdata[newsong.decode('utf-8')]['difficulties']
    with open('weekly.json', 'w') as f:
        json.dump(weeklyjson, f, indent=2)
    with app.app_context():
        posts = db.session.query(WeeklyPost).all()
        for item in posts:
            create_json(item)
        db.session.query(WeeklyPost).delete()
        db.session.commit()
    send_webhook.notify(newsong.decode('utf-8'), raw_songdata[newsong.decode('utf-8')]['length'])
