
"""
Downloading albums into the current working directory (./) by importing the module as: 

from khinsider import Scraper
"""


from ..khinsider import Scraper
links = """https://downloads.khinsider.com/game-soundtracks/album/88-games-arcade https://downloads.khinsider.com/game-soundtracks/album/007-nightfire-2002-gc 
https://downloads.khinsider.com/game-soundtracks/album/0x10c-2014 https://downloads.khinsider.com/game-soundtracks/album/1000-cooking-recipes-from-elle-a-table-2010-nds-gamerip"""

Scraper("./", links, format='mp3')
