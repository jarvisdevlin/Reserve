# re:serve
Allows Geometry Dash to function offline via caching along with editing responses to make the game more fun to mess with.
## Setup
Patch your game to use `http://127.0.0.1:19997////database` instead of `https://www.boomlings.com/database` for the Geometry Dash servers so that Reserve can be used instead. (CREATE A BACKUP OF YOUR EXE/APK)
```
pip install aiohttp      // To install aiohttp
python reserve.py        // To start Reserve
```
