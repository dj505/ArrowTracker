from flask import url_for
import datetime
from dhooks import Webhook, Embed
from configparser import ConfigParser

parser = ConfigParser()
parser.read('settings.ini')
url = parser.get('webhooks', 'url')

hook = Webhook(url)

def notify(updatedata, length):
    embed = Embed(
        title="Weekly Challenge Update",
        description=f"New song is \"{updatedata}\" ({length})",
        color=0x99beea,
        timestamp='now'
    )
    embed.set_author(name="Arrow Tracker", icon_url="https://arrowtracker.duckdns.org/static/newlogo-arrow-smaller.png")
    hook.send(embed=embed)
