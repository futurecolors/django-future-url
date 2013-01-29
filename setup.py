# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup, find_packages

import django_future_url

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

setup(
    name="django-future-url",
    version=django_future_url.__version__,
    author='Vitaly Olevinsky',
    author_email='olevinsky.v.s@gmail.com',
    packages=find_packages(),
    url='https://github.com/futurecolors/django-future-url/',
    description="Migration tool for django 1.4, fixes url template tag deprecation warnings.",
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    license='MIT',
    install_requires=['docopt'],
    entry_points = {
       'console_scripts': [
           'future_url = django_future_url.main:future_url',
       ],
    },
    tests_require=['cram==0.5'],
    test_suite='django_future_url.test',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
)
