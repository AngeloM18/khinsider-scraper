import requests
import time
from __exceptions__.errors import ResponseError
from __version__ import __version__

class Downloader(object):
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(
            {"User-Agent": "khinsder-scraper/" + __version__}
        )
        
    def download(self, generator):
        for path, link, name in generator:
            print(f"Downloading {name}")

            with self.session.get(link, stream=True) as response:
                self._handle_response(response)
                with open(path, "wb") as file:
                    for chunk in response.iter_content(None):
                        file.write(chunk)

    def _handle_response(self, response):
        status_code = response.status_code
        if status_code == 200:
            return
        raise ResponseError(status_code, response.text)

    

