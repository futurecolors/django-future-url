# -*- coding: utf-8 -*-
import codecs
import os
from distutils.core import setup

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

version = '0.1'

setup(
    name="django-future-url",
    version=version,
    author='Vitaly Olevinsky',
    author_email='olevinsky.v.s@gmail.com',
    packages=['django-future-url'],
    url='https://github.com/futurecolors/django-future-url/',
    description="Migration tool for django 1.4, fixs url template tag deprecation warnings.",
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.md')),
    license='MIT',
    scripts=['django-future-url/django-make-future-url.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
