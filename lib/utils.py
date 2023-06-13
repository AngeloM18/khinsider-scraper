from __exceptions__.errors import MissingArgumentError

def check_missing(arguments):
    for key, argument in arguments.items():
        if argument is None:
            raise MissingArgumentError(key)
