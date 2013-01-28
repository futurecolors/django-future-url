import codecs
import os
import subprocess
import unittest
from django_future_url.core import parse_file


class ModernizeUrlTagTestCase(unittest.TestCase):

    def assertTemplateFixed(self, template_name):
        base = os.path.abspath(os.path.dirname(__file__))
        input_filepath = os.path.join(base, 'examples', template_name + '.html')
        expected_filepath = os.path.join(base, 'expected', template_name + '.fixed.html')

        output = parse_file(codecs.open(input_filepath, 'r', 'utf-8').read())
        expected_output = codecs.open(expected_filepath, 'r', 'utf-8').read()
        self.assertEqual(output, expected_output)


class SimpleTest(ModernizeUrlTagTestCase):

    def test_deprecated_urls(self):
        self.assertTemplateFixed('deprecated_urls')

    def test_deprecated_urls_extends(self):
        self.assertTemplateFixed('deprecated_urls_extends')

    def test_deprecated_urls_extends2(self):
        self.assertTemplateFixed('deprecated_urls_extends2')

    def test_deprecated_urls_false_load(self):
        self.assertTemplateFixed('deprecated_urls_false_load')

    def test_should_not_be_upgraded(self):
        self.assertTemplateFixed('should_not_be_upgraded')