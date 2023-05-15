#!/usr/bin/env python3

import unittest
import unittest.mock as mock
import sys

sys.path.append('..')

from check_nano import commandline
from check_nano import get_data
from check_nano import main

class CLITesting(unittest.TestCase):

    def test_commandline(self):
        actual = commandline(['-H', 'localhost'])
        self.assertEqual(actual.host, 'localhost')
        self.assertEqual(actual.protocol, 'https')
        self.assertFalse(actual.insecure)

class URLTesting(unittest.TestCase):

    @mock.patch('check_nano.urlopen')
    def test_get_data(self, mock_url):

        m = mock.MagicMock()
        m.getcode.return_value = 200
        m.read.return_value = b'foobar'
        mock_url.return_value = m

        actual = get_data('http://localhost', 10, True)
        expected = 'foobar'

        self.assertEqual(actual, expected)

    @mock.patch('check_nano.urlopen')
    def test_get_data_404(self, mock_url):

        m = mock.MagicMock()
        m.getcode.return_value = 404
        mock_url.return_value = m

        with self.assertRaises(RuntimeError) as context:
            get_data('http://localhost', 10, True)

class MainTesting(unittest.TestCase):

    @mock.patch('check_nano.get_data')
    def test_main_unknown(self, mock_data):
        d = """
        This no XML!
        """
        mock_data.return_value = d

        args = commandline(['-H', 'localhost'])
        actual = main(args)
        self.assertEqual(actual, 3)

    @mock.patch('check_nano.get_data')
    def test_main_ok(self, mock_data):
        d = """
        <response>
        <out>00000000</out>
        <on>00000000</on>
        <in>00000000</in>
        <counter1>0</counter1>
        <temp1>34.3</temp1>
        <mac>00:00:00:00:00:00</mac>
        </response>
        """
        mock_data.return_value = d

        args = commandline(['-H', 'localhost'])
        actual = main(args)
        self.assertEqual(actual, 0)

    @mock.patch('check_nano.get_data')
    def test_main_critical(self, mock_data):
        d = """
        <response>
        <out>00000000</out>
        <on>11111111</on>
        <in>00000000</in>
        <counter1>0</counter1>
        <temp1>34.3</temp1>
        <mac>00:00:00:00:00:00</mac>
        </response>
        """
        mock_data.return_value = d

        args = commandline(['-H', 'localhost'])
        actual = main(args)
        self.assertEqual(actual, 2)
