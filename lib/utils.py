from __exceptions__.errors import MissingArgumentError

def check_arguments(arguments):
    for key, argument in arguments.items():
        if argument is None:
            raise MissingArgumentError(key)
