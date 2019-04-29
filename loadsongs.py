import os

games = ['Pump it Up']

def load_song_lists():
    songlist = []
    numlists = 0
    numsongs = 0
    for file in os.listdir("app/gamelists/Pump it Up"):
        numlists += 1
        with open('app/gamelists/Pump it Up/{}'.format(file), 'r') as f:
            listadd = f.read()
            listadd = listadd.split('\n')
            for song in listadd:
                songlist.append(song)
                numsongs += 1
            del songlist[-1]
            print(f'Loaded {file}')
    songlist.sort()
    songlist_pairs = list(zip(songlist, songlist))
    print('{} List(s)'.format(numlists))
    print('{} Song(s)'.format(numsongs))
    return(songlist_pairs)
