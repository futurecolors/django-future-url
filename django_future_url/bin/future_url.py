#!/usr/bin/env python
"""
Django future url.

Usage:
  future_url
  future_url -h | --help
  future_url --version

Options:
  -D --dry-run  Only shows changes to be made without actually modifying files.
  -v --verbose  Print status messages to stdout.
  -h --help     Show this screen.
  --version     Show version.
"""
import logging

from docopt import docopt
import django_future_url
from django_future_url.core import make_me_magic


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Django future url' + django_future_url.__version__)

    # Set up logging handler
    level = logging.DEBUG if arguments['--verbose'] else logging.INFO
    logging.basicConfig(format='%(name)s: %(message)s', level=level)

    make_me_magic(dry_run=arguments['--dry-run'])