# django-future-url

Migration tool for old style “url” tags.
“In Django 1.5, the behavior of the url template tag will change”
[https://docs.djangoproject.com/en/1.4/ref/templates/builtins/#url](https://docs.djangoproject.com/en/1.4/ref/templates/builtins/#url)

If you use old style url tags in django 1.4 you will see that:
“DeprecationWarning: The syntax for the url template tag is changing. Load the `url` tag from the `future` tag library to start using the new behavior.”

## How it works

* Finds all *.html, *.txt files.
* Replaces all old style “url” tags.
* Inserts “{% load url from suture %}” when it's needed.


## Installation

```bash
python setup.py install
```

## Usage

```bash
cd ~/projects/my_django_14_project/
django-make-future-url.py
```
It will update all templates in directory “~/projects/my_django_14_project/” and subdirectories.

### Options

_You can use `django-make-future-url.py --help` for help._

Only shows changes to be made without actually modifying files:
```bash
django-make-future-url.py --dry-run
```

Verbose output:
```bash
django-make-future-url.py --verbose
```

## Example

`cat ./template1`
```django
{% url path.to.view arg arg2 %}
{%  url path.to.view arg arg2 %}
{%url myapp:view-name %}
{% url path.to.view as the_url%}
{% url   path.to.view arg arg2   as   the_url %}
{%url app_views.client client.id%}
```

`django-make-future-url.py`

`cat ./template1`
```django
{% load url from future %}
{% url 'path.to.view' arg arg2 %}
{%  url 'path.to.view' arg arg2 %}
{%url 'myapp:view-name' %}
{% url 'path.to.view' as the_url%}
{% url   'path.to.view' arg arg2   as   the_url %}
```