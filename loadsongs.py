import os
import json

games = ['Pump it Up']

def load_song_lists():
    songlist = []
    numlists = 0
    numsongs = 0
    for file in os.listdir("app/gamelists/Pump it Up"):
        numlists += 1
        with open('app/gamelists/Pump it Up/{}'.format(file), 'r') as f:
            songfile = json.load(f)
            for song in songfile.keys():
                try:
                    songlist.append(song.encode('utf-8'))
                except:
                    print('error')
                numsongs += 1
            print(f'Loaded {file}')
    songlist.sort()
    songlist_pairs = list(zip(songlist, songlist))
    print('{} List(s)'.format(numlists))
    print('{} Song(s)'.format(numsongs))
    return(songlist_pairs)

print(load_song_lists())
