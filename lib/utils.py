from __exceptions__.errors import MissingArgumentError

def check_arguments(arguments):
    for key, argument in arguments.items():
        if argument is None:
            raise MissingArgumentError(key)
        
def handle_naming(name: str) -> str:
    name = "".join([c for c in name if not c in ":/?*<>|\"\\"])
    name = " ".join(map(str.capitalize, name.replace("_", " ").split(" ")))
    return name.rstrip("mp3flac.").lstrip("0123456789 ")