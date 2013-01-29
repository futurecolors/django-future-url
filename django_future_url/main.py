"""
Django future url.

Migration tool for django 1.4, fixes url template tag deprecation warnings.

    -  Finds all html``, txt files.
    -  Replaces all old style url tags.
    -  Inserts {% load url from future %} when it's needed.

Usage:
  future_url [options]
  future_url -h | --help
  future_url --version

Options:
  -w --write    Actually make replacements.
  -q --quiet    Do not print anything to stdout.
  -h --help     Show this screen.
  --version     Show version.
"""
import logging

from docopt import docopt
import django_future_url
from django_future_url.core import make_me_magic


def future_url():
    arguments = docopt(__doc__, version='Django future url ' + django_future_url.__version__)

    # Set up logging handler
    level = logging.CRITICAL if arguments['--quiet'] else logging.INFO
    logging.basicConfig(format='%(message)s', level=level)

    make_me_magic(write=arguments['--write'])
