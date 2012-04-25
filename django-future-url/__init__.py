VERSION = (0, 1)

def get_version(version=None):
    """ PEP386-compliant version. """
    if version is None:
        version = VERSION

    return '.'.join(str(x) for x in version)