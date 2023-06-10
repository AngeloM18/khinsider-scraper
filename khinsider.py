from requests import get
from wrapper import Downloader
from lib.utils import check_arguments
from lib.utils import handle_naming
from __exceptions__.errors import WrongArgument
from __exceptions__.errors import WrongLink
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

class Scraper():
    __formats__ = ("mp3", "flac")

    def __init__(self, path: str = None, link: str = None, format: str = "flac"):
        self._logger = logging.getLogger(__name__)
        self._album_name = None
        self._soup = None
        self._base_url = "https://downloads.khinsider.com/"
        
        self.base_path = path
        self.link = link
        self.format = format.lower()

        if path and link:
            self.base_path = path
            self.link = link.split(" ")
        
        self.args = parser.parse_args()
        if self.args.link and self.args.path:
            self.base_path = self.args.path
            self.link = self.args.link
            if self.args.fileformat:
                self.format = self.args.fileformat.lower()

        if not (self.format in self.__formats__):
            raise WrongArgument(self.args.fileformat)

        if not (self.base_path and self.link):
            arguments = {"path": self.base_path, "link": self.link}
            check_arguments(arguments)

        self.start(self.link)

    def start(self, link):
        downloader = Downloader()
        for url in link:
            self._logger.debug(link)

            if not url.startswith(self._base_url):
                raise WrongLink(url, self._base_url)
            
            self._soup = bs4.BeautifulSoup(get(url).text, 'html.parser')
            self._name()
            downloader.download(self._art())
            downloader.download(self._landing_page())

    def _name(self) -> None:
        name = self._soup.select('#pageContent > h2')[0].getText()
        self._album_name = handle_naming(''.join(name.split(':')))
        print(f"\nSCRAPING {self._album_name.upper()}")
        os.makedirs(self._album_name, exist_ok=True)

    def _art(self) -> iter:
        elements = self._soup.find_all('div', 'albumImage')
        if elements == []:
            return
        
        directory = os.path.join(self.base_path, self._album_name, 'Art')
        os.makedirs(directory, exist_ok=True)

        print(f"\nSCRAPING {self._album_name.upper()} ALBUM ART:")
        for i, tag in enumerate(elements):
            url = tag.find('a').get('href')
            art_name = f"{self._album_name} {str(i).zfill(3)}.jpg"
            file_path = os.path.join(directory, art_name)

            yield file_path, url, art_name
            
    def _landing_page(self) -> iter:
        multiple_cds = True
        header = self._soup.select('#songlist > #songlist_header > th')
        
        if header[1].getText() != 'CD':
            directory = os.path.join(self.base_path, self._album_name)
            multiple_cds = False
        
        print(f"\nSCRAPING {self._album_name.upper()} SONGS:")
        table = self._soup.select('#songlist > tr')
        for row in table:
            if row.get('id') == 'songlist_header':
                continue
            if row.get('id') == 'songlist_footer':
                break

            if multiple_cds:
                cd_volume = row.find_all('td', attrs={'align':'center'})
                cd_folder = f"Disc {cd_volume[-1].getText()}"
                directory = os.path.join(self.base_path, self._album_name, cd_folder)
            os.makedirs(directory, exist_ok=True)

            landing_page = row.find('td', attrs={'class':'playlistDownloadSong'}).find('a').get('href')
            soup = bs4.BeautifulSoup(get(self._base_url + landing_page).text, 'html.parser')

            link_container = soup.select('#pageContent > p > a')
            if len(link_container) > 28 and self.format == "flac":
                format, idx = ".flac", -1
            elif len(link_container) == 28 and self.format == 'flac':
                format, idx = ".mp3", -1
            else:
                format, idx = ".mp3", -2

            url = link_container[idx].get("href")
            song_name = handle_naming(soup.select('#pageContent > p > b')[2].getText())
            file_path = os.path.join(directory, song_name + format)
            
            yield file_path, url, song_name + format
        

def main():
    Scraper()

if __name__ == '__main__':
    main()
