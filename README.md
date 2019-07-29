# ArrowTracker

Arrow Tracker is a functional online leaderboard and score tracker built for Pump it Up XX, but supports older games. It's meant to be an external solution to the removal of the worldwide leaderboard in XX, aiming to recreate many of Prime 2's leaderboard features to the greatest possible extent without access to the game's servers and other data.

## Features

* Home page displaying latest scores in order of newest first.
* User dashboard allows players to update their information, profile picture, etc.
* Tournaments page allows members to organize online tournaments, with Challonge embed support.
* Individual song leaderboards with filtering allows users to track certain songs and help them set goals.
* Weekly Challenge - every Friday, the weekly challenge song changes and the leaderboard is saved and reset.
* Resources page including links to useful information and documents.
* Images can be uploaded alongside scores to "verify" the score, allowing it to be displayed on the leaderboard.
* Full mobile device support.

## Planned

* Mission tracking
* Personal score tracking
* Completionist-oriented page to show progress on songs cleared vs uncleared
* YouTube videos embedded on weekly challenge page
* Much more

## Installing/Running

1. Install requirements via `pip install -r requirements.txt`
2. Create the database (more on this soon)
3. Fill in the settings
4. Run `run.py` and connect to `localhost:5000`

## Credits

* Pump Out (Song database and thumbnail image source)
* Andamiro (Prime 2 profile images)
* [daneden's Animeate.css](https://github.com/daneden/animate.css)

## Find Arrow Tracker useful?

Consider supporting! Arrow Tracker is and will always be free, open source, and ad-free. Supporters will go in the site's list of supporters!

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y8106HR)

### DISCLAIMER

I do not own any of the Pump it Up Prime 2 profile images, song banners, or song thumbnails used in this project. All copyrights there go to their respective owners. The rest of the site (everything outside of the `default` profile images and the things in `app/static/songthumbs`) is owned by myself and the contributors of this repository.
