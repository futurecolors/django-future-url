# coding: utf-8

""" Searches for templates in current directory recursively and
modernizes them to use new {% url %} syntax.
Adds {% load url from future %} on top of your template if necessary (Django 1.3-1.4).

From the Django docs
https://docs.djangoproject.com/en/1.4/ref/templates/builtins/#url

    In Django 1.5, the behavior of the url template tag will change, with the
    first argument being made into a context variable, rather than being a
    special case unquoted constant. This will allow the url tag to use a
    context variable as the value of the URL name to be reversed.

    In order to provide a forwards compatibility path, Django 1.3 provides
    a future compatibility library -- future -- that implements the new behavior.
    To use this library, add a load call at the top of any template using the url
    tag, and wrap the first argument to the url tag in quotes. For example:

    {% load url from future %}

    {% url 'app_views.client' %}
    {% url 'myapp:view-name' %}

    {% with view_path="app_views.client" %}
    {% url view_path client.id %}
    {% endwith %}

    {% with url_name="client-detail-view" %}
    {% url url_name client.id %}
    {% endwith %}
"""
from __future__ import unicode_literals

import re
import os
import logging

log = logging.getLogger(__name__)

CURRENT_PATH = os.path.abspath('.')
load_tag = "{% load url from future %}"
file_formats = ['.html', '.txt']

re_flags = re.I | re.X | re.U

# Deprecated url tag
r_depr_url_finder = re.compile(r" {% \s* url \s+ [^\"\'\s]+ \s+ ", re_flags)

# And url tag
r_url_finder = re.compile(r"{% \s* url \s+ ", re_flags)
# {% load url from future %}
r_load_finder = re.compile(r" {% \s* load \s+ url \s+ from \s+ future \s* %} ", re_flags)
# {% extends ... %} tag
r_extends_finder = re.compile(r"{% \s* extends \s* \S+ \s* %}", re_flags)

# Modernizing url tag replace pattern
r_url_pattern = re.compile(r"""
    (?P<before> {% \s*
        url \s+ )
        (?P<name> \S+ )
        (?P<attrs> \s+ .*? )
    (?P<after> \s* %} )
""", re_flags)

# Add load from future after extends
r_load_extends_pattern = re.compile(
    r"(?P<template_head> [\s\S]* {% \s* extends \s* \S+ \s* %} )",
    re_flags | re.M,
)

# Adding load tag pattern
r_load_extends_replace = """\g<template_head>\n\n%s\n""" % load_tag


def make_me_magic(write):
    """ Main script.

    Here we find templates, replace old-style url tags and add future import where necessary.
    """
    # Search for files with appropriate extensions.
    log.info('Files needing modification:')
    found = False
    for file_path in find_files(os.walk(CURRENT_PATH)):
        with open(file_path, 'r+') as t_file:
            file_content = t_file.read()
            # Checking for presence of old-style tags and absence of load url from future
            if has_deprecated_tag(file_content):
                found = True
                log.info(file_path.replace(CURRENT_PATH + '/', ''))
                new_content = parse_file(file_content)

                if write:
                    t_file.seek(0)
                    t_file.write(new_content)
                    log.info('    File updated')

    if not found:
        log.info('All files are up to date. Congrats!')
    else:
        if not write:
            log.info('No actual changes made. Run future_url --write to fix files right now.')



def find_files(paths):
    for dirpath, _, filenames in paths:
        for path in search_template_files(dirpath, filenames):
            yield path


def parse_file(file_content):
    if not has_deprecated_tag(file_content):
        return file_content

    # Handle files with deprecated url tags
    if r_depr_url_finder.search(file_content):
        if check_comma_in_attributes(file_content):
            log.warn("    Comma separated attributes in url tag are no longer supported.")
        file_content = process_url_tag(file_content)

    # Check if load url form future is present and add if necessary
    if r_url_finder.search(file_content) and not r_load_finder.search(file_content):
        file_content = process_load_tag(file_content)
        log.info("    Need to add {% load url from future %}")

    return file_content


def url_replacer(match):
    """ Handle single url tag. """

    matches = match.groupdict()
    if ',' in match.group('attrs'):
        matches['attrs'] = re.sub('\s*,\s*', ' ', match.group('attrs'))
    repl = "{before}'{name}'{attrs}{after}".format(**matches)
    logging.info("    Proposed replace: {0} -> {1}".format(match.group(0), repl))
    return repl


def process_load_tag(html):
    """ Add {% load url from future %} """

    if r_extends_finder.search(html):
        return r_load_extends_pattern.sub(r_load_extends_replace, html, count=1)
    else:
        return "{load_tag}\n{html}".format(
            load_tag=load_tag,
            html=html,
        )


def process_url_tag(html):
    """ Modernize url tag. """

    return r_url_pattern.sub(url_replacer, html)


def check_comma_in_attributes(html):
    """ Attributes of url tag can't be separated by comma. """

    search = r_url_pattern.search(html)
    return ',' in search.group('attrs')


def has_deprecated_tag(html):
    """ Check if html needs modernizing. """

    # File is already up-to-date
    has_load_tag = r_load_finder.search(html)

    # No load tag and (deprecated) url tag present
    return not has_load_tag and (r_depr_url_finder.search(html) or r_url_finder.search(html))


def search_template_files(dirname, fnames):
    """ Search for suitable files """

    for file_name in fnames:
        if os.path.splitext(file_name)[1] in file_formats:
            yield os.path.join(dirname, file_name)