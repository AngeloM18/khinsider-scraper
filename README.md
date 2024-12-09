One year later, I reckon the code is kinda crap! Don't laugh - thanks!

![1](https://github.com/1898Angelo/khinsider-scraper/assets/123282394/f48ba80d-e4c5-4a08-a1c2-62a67df51b2c)

# KHINSIDER SCRAPER
Scraper built on Python to batch download albums from https://downloads.khinsider.com/.

 - Download and store albums in a structured folder tree in the path choosen.
 - Download album art (if any)
 - Can download multiple albums one after another.
 - Can choose the preferred audio file format to download the songs as.

![Animation](https://github.com/1898Angelo/khinsider-scraper/assets/123282394/a0538ca3-e79d-4b42-839b-d73d3ffd2dc6)
![Animation2](https://github.com/1898Angelo/khinsider-scraper/assets/123282394/2fd92e8f-2d5f-493e-8102-3e898e9ba1c4)

 ## USAGE
 ```
 khinsider.py [-h] [-p PATH] [-l LINK [LINK ...]] [-F FILEFORMAT]
 ```
 #### ... OPTIONS
 ```
-p PATH -- Enter the full path to downloads the albums in
-l LINK -- enter the album links separated by a space between each album link
-F (uppercase) FILEFORMAT -- (optional) specifies the audio file format
 ```
 #### ... EXAMPLE
 ```
 khinsider.py -p C:\Users\Angelo\Documents -l https://downloads.khinsider.com/game-soundtracks/album/88-games-arcade https://downloads.khinsider.com/game-soundtracks/album/007-nightfire-2002-xbox
 ```

## DEPENDENCIES
```
beautifulsoup4
requests
```
 
 ## HOW TO
Manually download the package as a zip file or clone the repository using git. 
After that, place the package in a directory of your choosing, open the terminal (Unix) or CMD (Windows) and move to that directory, then call the script from the terminal/CMD as in the example above.
```
cd directory/of/your/choosing
git clone https://github.com/1898Angelo/khinsider-scraper.git (if cloning with git) 
khinsider.py ...
```
 #### ... INSTALL DEPENDENCIES
 ```
 pip install beautifulsoup4 requests
 ```
 OR if you want to install the specific version of the dependencies used, move to the directory where you downloaded the package and run from the terminal/CMD.
 ```
 pip install -r requirements.txt
 ```
 
 ## DONATE
 Consider donating to https://downloads.khinsider.com/ by following the Donate button on the left side bar.
 
 ![2](https://github.com/1898Angelo/khinsider-scraper/assets/123282394/8b5f9569-78e2-4e0b-853a-6ba5ad24bf7b)

 
