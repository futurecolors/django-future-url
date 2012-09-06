#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Description and comments in Russian language.

Ищет в текущаей папке шаблоны и заменяет в них шаблонные теги «url» под
новый формат.
Дописывает в начало файла «{% load url from future %}», если это нужно.

В версии 1.5 поведение шаблонного тега «url» изменится:
https://docs.djangoproject.com/en/1.4/ref/templates/builtins/#url

Из документации:

«In Django 1.5, the behavior of the url template tag will change, with the
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
    {% endwith %}»

"""

import re
import os
from optparse import OptionParser

version = __import__('django-future-url').get_version()

CURRENT_PATH = os.path.abspath('.')
template_files = []
load_tag = "{% load url from future %}"
file_formats = ['.html', '.txt']

re_flags = re.I | re.X | re.U

# Устаревший url тег
r_depr_url_finder = re.compile(ur" {% \s* url \s+ [^\"\'\s]+ \s+ ", re_flags)

# Любой url тег
r_url_finder = re.compile(ur"{% \s* url \s+ ", re_flags)
# Тег разгрузки url из будущего
r_load_finder = re.compile(ur" {% \s* load \s+ url \s+ from \s+ future \s* %} ", re_flags)
# Тег extends
r_extends_finder = re.compile(ur"{% \s* extends \s* \S+ \s* %}", re_flags)

# Для замены тега url
r_url_pattern = re.compile(ur"""
    (?P<before> {% \s*
        url \s+ )
        (?P<name> \S+ )
        (?P<attrs> \s+ .*? )
    (?P<after> \s* %} )
""", re_flags)

# Для вставки тега load, когда тег extends есть в шаблоне
r_load_extends_pattern = re.compile(
    ur"(?P<template_head> [\s\S]* {% \s* extends \s* \S+ \s* %} )",
    re_flags | re.M,
)

# Шаблон для в ставки тега load
r_load_extends_replace = """\g<template_head>\n\n%s\n""" % load_tag

# Опции
parser = OptionParser("usage: %prog [options]", version='%prog ' + version)
parser.add_option(
    "-v", "--verbose",
    action="store_true",
    dest="verbose",
    default=False,
    help="Print status messages to stdout"
)
parser.add_option(
    "-D", "--dry-run",
    dest="dryrun",
    action="store_true",
    default=False,
    help='Only shows changes to be made without actually modifying files'
)
(options, args) = parser.parse_args()


def make_me_magic():
    """ Основной скрипт.

    Тут происходит поиск файлов, замена
    старых url тегов в найденных шаблонах и вставка
    тега «{% load url from future %}», где это нужно.
    """

    # Находим файлы с подходящим расширением.
    os.path.walk(CURRENT_PATH, search_template_files, template_files)

    for file_path in template_files:
        with open(file_path, 'r+') as t_file:
            file_content = t_file.read()

            # Проверяем наличие в файле старых тегов или
            # отсутствие «load» тега.
            if has_deprecated_tag(file_content):
                print file_path

                # Обрабатываем файлы с «deprecated» url тегами.
                if r_depr_url_finder.search(file_content):
                    # Говорим о том что указание атрибутов через «,»
                    # больше не подерживается.
                    if check_comma_in_attributes(file_content):
                        message("Comma separated attribudes in “future” url tag are not supported.")
                    file_content = process_url_tag(file_content)

                # Проверяем наличие «load» тега, добавляем если нужно.
                if r_url_finder.search(file_content) and not r_load_finder.search(file_content):
                    file_content = process_load_tag(file_content)
                    message("Added {% load url from future %}")

                if not getattr(options, 'dryrun', True):
                    t_file.seek(0)
                    t_file.write(file_content)
                    message("File updated")

                message('\n')


def url_replacer(match):
    """ Обработка одного url тега. """

    matches = match.groupdict()
    if ',' in match.group('attrs'):
        matches['attrs'] = re.sub('\s*,\s*', ' ', match.group('attrs'))
    repl = "{before}'{name}'{attrs}{after}".format(**matches)
    message(u"replaced: {0} -> {1}".format(match.group(0), repl))
    return repl


def process_load_tag(html):
    """ Добавляем «load url from future». """

    if r_extends_finder.search(html):
        return r_load_extends_pattern.sub(r_load_extends_replace, html, count=1)
    else:
        return "{load_tag}\n{html}".format(
            load_tag=load_tag,
            html=html,
        )


def process_url_tag(html):
    """ Приводим тег url к формату. """

    return r_url_pattern.sub(url_replacer, html)


def check_comma_in_attributes(html):
    """ Проверка на наличие запятой в атрибутах. """

    search = r_url_pattern.search(html)
    return ',' in search.group('attrs')


def has_deprecated_tag(html):
    """ Проверка на наличие НЕ «future» url тега в тексте. """

    # File is already up-to-date
    has_load_tag = r_load_finder.search(html)

    # нет load тега и есть устаревший url тег или любой url тег
    return not has_load_tag and (r_depr_url_finder.search(html) or r_url_finder.search(html))


def search_template_files(template_files, dirname, fnames):
    """ Поиск подходящих файлов. """

    for file_name in fnames:
        if os.path.splitext(file_name)[1] in file_formats:
            file_path = os.path.join(dirname, file_name)
            template_files.append(file_path)


def message(txt):
    if getattr(options, 'verbose', False) or getattr(options, 'dryrun', False):
        print txt


if __name__ == '__main__':
    make_me_magic()
