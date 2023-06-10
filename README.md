![2](https://github.com/1898Angelo/khinsider-scraper/assets/123282394/7241ae57-06c3-4326-8758-7bc6e05ac369)

# KHINSIDER SCRAPER
Scraper built on Python to batch download albums from https://downloads.khinsider.com/.

 - Download and store albums in a structured folder tree in the path choosen.
 - Download album art (if any)
 - Can download multiple albums one after another.
 - Can choose the preferred audio file format to download the songs as.

![Animation](https://github.com/1898Angelo/khinsider-scraper/assets/123282394/5cbafc72-e16d-4ef3-a13e-6c14081cfcde)


(excuse my slow download speed)

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
 
 ![1](https://github.com/1898Angelo/khinsider-scraper/assets/123282394/4e8f463a-55d3-4efa-ba56-64b83df76755)

