django-future-url
=================

.. image:: https://travis-ci.org/futurecolors/django-future-url.png?branch=master
        :target: https://travis-ci.org/futurecolors/django-future-url

Migration tool for old style “url” tags.
`“In Django 1.5, the behavior of the url template tag will change”`_

If you use old style url tags in django 1.4 you will see that:
“DeprecationWarning: The syntax for the url template tag is changing.
Load the ``url`` tag from the ``future`` tag library to start using the
new behavior.”

The new library also drops support for the comma syntax
for separating arguments to the url template tag.

In Django 1.5, the old behavior will be replaced with the behavior
provided by the future tag library. Existing templates be migrated to use the new syntax.

.. _“In Django 1.5, the behavior of the url template tag will change”: https://docs.djangoproject.com/en/1.4/ref/templates/builtins/#url

How it works
------------

-  Finds all ``\*.html``, ``\*.txt`` files.
-  Replaces all old style “url” tags.
-  Inserts ``{% load url from future %}`` when it's needed.

Installation
------------
::

    $ pip install django-future-url

Usage
-----
::

    $ cd ~/projects/my_django_14_project/
    $ future_url --verbose

It will show needed midification for all templates in directory
“~/projects/my\_django\_14\_project/” and subdirectories.::

    $ future_url --write

It will modernize all your templates in place (see above).

Options
~~~~~~~

You can use ``future_url --help`` for help.

Only shows changes to be made without actually modifying files::

    $ future_url

Verbose output: ``$ future_url --verbose``

Example
-------
::

    $ cat ./template1.html

    {% url path.to.view arg arg2 %}
    {%  url path.to.view arg arg2 %}
    {%url myapp:view-name %}
    {% url path.to.view as the_url%}
    {% url   path.to.view arg arg2   as   the_url %}
    {%url app_views.client client.id%}

::

    $ future_url --write

    $ cat ./template1.html

    {% load url from future %}
    {% url 'path.to.view' arg arg2 %}
    {%  url 'path.to.view' arg arg2 %}
    {%url 'myapp:view-name' %}
    {% url 'path.to.view' as the_url%}
    {% url   'path.to.view' arg arg2   as   the_url %}


Tests
-----

Install ``cram`` and run ``python setup.py test``