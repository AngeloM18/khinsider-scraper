class ResponseError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

class MissingArgumentError(Exception):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return f"{self.arg} is necessary, but received empty"
    
class WrongArgument(Exception):
    def __init__(self, format):
        self.format = format

    def __str__(self):
        return f"{self.format} is not recognized."
    
class WrongLink(Exception):
    def __init__(self, link, base_url):
        self.link = link
        self.base_url = base_url

    def __str__(self):
        return f"Invalid URL: ({self.link}). Only URLs with base: {self.base_url}"