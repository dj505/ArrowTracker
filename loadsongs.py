import os
import json

games = ['Pump it Up']
with open('app/static/gamelists/Pump it Up/complete.json', 'r') as f:
    raw_songdata = json.load(f)

def load_song_lists():
    songlist = []
    lengthtypes = []
    numlists = 0
    numsongs = 0
    numlengths = 0
    numdiffs = 0
    for file in os.listdir("app/static/gamelists/Pump it Up"):
        numlists += 1
        with open('app/static/gamelists/Pump it Up/{}'.format(file), 'r') as f:
            songfile = json.load(f)
            for song in songfile.keys():
                try:
                    songlist.append(song.encode('utf-8'))
                except:
                    print('error')
                numsongs += 1
            for k, v in songfile.items():
                for key, value in v.items():
                    if key == 'length' and value not in lengthtypes:
                        lengthtypes.append(value)
                        numlengths += 1
            print(f'Loaded {file}')
    songlist.sort()
    lengthtypes.sort()
    songlist_pairs = list(zip(songlist, songlist))
    lengthtype_pairs = list(zip(lengthtypes, lengthtypes))
    print(f'{numlists} List(s)')
    print(f'{numsongs} Song(s)')
    print(f'{numlengths} Length(s)')
    return(songlist_pairs, lengthtype_pairs)
