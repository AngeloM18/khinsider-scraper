from requests import get
from sys import argv
from wrapper import Downloader
from lib.utils import check_missing
from __exceptions__.errors import WrongArgument
from __exceptions__.errors import WrongLink
from __exceptions__.errors import InvalidPath
import logging
import argparse
import bs4
import os


print("""
██╗  ██╗██╗  ██╗██╗███╗   ██╗███████╗██╗██████╗ ███████╗██████╗ 
██║ ██╔╝██║  ██║██║████╗  ██║██╔════╝██║██╔══██╗██╔════╝██╔══██╗
█████╔╝ ███████║██║██╔██╗ ██║███████╗██║██║  ██║█████╗  ██████╔╝
██╔═██╗ ██╔══██║██║██║╚██╗██║╚════██║██║██║  ██║██╔══╝  ██╔══██╗
██║  ██╗██║  ██║██║██║ ╚████║███████║██║██████╔╝███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗         
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗        
███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝        
╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗        
███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║        
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝                                                                        
""")

parser = argparse.ArgumentParser(
    description="Script to download albums from https://downloads.khinsider.com/")
parser.add_argument("-p", "--path", help="enter the path to downloads the albums in")
parser.add_argument("-l", "--link", nargs="+", help="enter the album links separated by spaces")
parser.add_argument("-F", "--fileformat", help="(optional) specifies in which format to download the songs as: flac or mp3 (flac by default)")
parser.print_help()

class Scraper(Downloader):
    """Scraper class
        Arguments:
        base_path (str): Directory (absolute or relative) to download the albums in.
        Keyword arguments: 
        format (str - optional): File format for the songs (mp3 or flac). Default file format: "flac"
    """ 
    __formats__ = ("mp3", "flac")
    __base_url__ = "https://downloads.khinsider.com/"

    def __init__(self, base_path: str = None, format: str = "flac"):
        self.format = format.lower()
        self.base_path = base_path
        self._logger = logging.getLogger(__name__)
        super().__init__()

        if len(argv) > 1:
            args = parser.parse_args()
            if args.link and args.path:
                self.base_path = args.path
                link = args.link
                if args.fileformat:
                    self.format = args.fileformat.lower()
        
        if not (self.format in self.__formats__):
            raise WrongArgument(self.format)
        if not os.path.exists(self.base_path):
            raise InvalidPath(self.base_path)

        if len(argv) > 1:
            self.start(link)

    def start(self, link: str = None):
        """Starter method, calls all the other functions inside the class needed to scrape and download albums.
        Arguments:
        link (str): Link(s) of the albums to download. Must have https://downloads.khinsider.com/ as their base.
        """
        if not len(argv) > 1:
            link = link.split(" ") 
        if not (self.base_path and link):
            arguments = {"path": self.base_path, "link": link}
            check_missing(arguments)

        for url in link:
            if not url.startswith(self.__base_url__):
                raise WrongLink(url, self.__base_url__)
            
            soup = bs4.BeautifulSoup(get(url).text, "html.parser")
            album_name = self.name(soup)
            self.download(self.art(soup, album_name))
            self.download(self.links(soup, album_name))

    def name(self, soup: bs4.BeautifulSoup) -> str:
        attributes = {"album_name": "#pageContent > h2"}
        name = soup.select(attributes["album_name"])[0].getText().split(":")
        name = self._handle_naming("".join(name))
        directory = os.path.join(self.base_path, name)
        os.makedirs(directory, exist_ok=True)

        print(f"\nSCRAPING {name.upper()}")
        return name

    def art(self, soup: bs4.BeautifulSoup, album_name: str) -> iter:
        attributes = {"images": ["div", "albumImage"]}
        elements = soup.find_all(*attributes["images"])
        if elements == []:
            return
        directory = os.path.join(self.base_path, album_name, "Art")
        os.makedirs(directory, exist_ok=True)

        print(f"\nSCRAPING {album_name.upper()} ALBUM ART:")
        for idx, tag in enumerate(elements):
            url = tag.find("a").get("href")
            name = f"{album_name} {str(idx).zfill(3)}.jpg"
            file_path = os.path.join(directory, name)

            yield file_path, url, name
            
    def links(self, soup: bs4.BeautifulSoup, album_name: str) -> iter:
        attributes = {"header": "#songlist > #songlist_header > th",
                      "table": "#songlist > tr",
                      "volume": {"align":"center"},
                      "landing": {"class":"playlistDownloadSong"},
                      "songlink": "#pageContent > p > a",
                      "songname": "#pageContent > p > b"
        }
        multiple_volumes = True
        header = soup.select(attributes["header"])
        
        if header[1].getText() != "CD":
            directory = os.path.join(self.base_path, album_name)
            multiple_volumes = False
        
        print(f"\nSCRAPING {album_name.upper()} SONGS:")
        table = soup.select(attributes["table"])
        for row in table:
            if row.get("id") == "songlist_header":
                continue
            if row.get("id") == "songlist_footer":
                break

            if multiple_volumes:
                cd_volume = row.find_all("td", attrs=attributes["volume"])[-1].getText()
                cd_folder = f"Disc %s" % cd_volume #Disc 1|2|3...
                directory = os.path.join(self.base_path, album_name, cd_folder)
            os.makedirs(directory, exist_ok=True)

            landing_page = row.find("td", attrs=attributes["landing"]).find("a").get("href")
            songsoup = bs4.BeautifulSoup(get(self.__base_url__ + landing_page).text, "html.parser")

            link = songsoup.select(attributes["songlink"])
            if len(link) > 28 and self.format == "flac":
                format, idx = ".flac", -1
            elif len(link) == 28 and self.format == "flac":
                format, idx = ".mp3", -1
            else:
                format, idx = ".mp3", -2

            url = link[idx].get("href")
            name = self._handle_naming(songsoup.select(attributes["songname"])[2].getText())
            file_path = os.path.join(directory, name + format)
            
            yield file_path, url, name + format

    def change_directory(self, directory: str):
        """Changes the set download path for the instance.
        Arguments:
        directory (str): New directory for the albums.
        """
        self.base_path = directory
        if not os.path.exists(self.directory):
            raise InvalidPath(directory)
        return self
    
    def change_format(self, format: str):
        """Changes the set audio file format for the instance.
        Arguments:
        format (str): Set format for the songs. Valid audio file formats mp3 or flac
        """
        self.format = format
        if not (format in self.__formats__):
            raise WrongArgument(self.format)
        return self
    
    @staticmethod
    def _handle_naming(name: str) -> str:
        name = "".join([c for c in name if not c in ":/?*<>|\"\\"])
        name = " ".join(map(str.capitalize, name.replace("_", " ").split(" ")))
        return name.rstrip("mp3flac.").lstrip("0123456789 ")
    

def main():
    Scraper()

if __name__ == "__main__":
    main()
