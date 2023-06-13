"""
Downloading albums into the current working directory (./) by importing the module.
"""
from khinsider import Scraper

links = """https://downloads.khinsider.com/game-soundtracks/album/88-games-arcade https://downloads.khinsider.com/game-soundtracks/album/007-nightfire-2002-gc"""

"""
Initialize an instance by passing in a path (absolute or relative) to download the albums in.
Optionally, pass in a preferred file format for the songs (flac or mp3).
"""
scraper = Scraper("./", format="mp3")

"""
Call the starter method. Pass it the link OR links delimited by a space.
"""
scraper.start(links)

"""
Change the filepath or preferred format after an instance has already been created
"""
#scraper.change_directory("../")
#scraper.change_format("flac")
