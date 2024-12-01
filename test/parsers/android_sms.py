#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the Android SMS parser."""

import unittest

from plaso.lib import definitions
from plaso.parsers import android_sms

from tests.parsers import test_lib


class AndroidSMSParserTest(test_lib.ParserTestCase):
    """Tests for the Android SMS parser."""

    def testParseFile(self):
        """Tests the Parse function on an Android SMS database file."""
        parser = android_sms.AndroidSMSParser()
        storage_writer = self._ParseFile(['sms_test_data.db'], parser)

        # Verify the number of events parsed.
        self.assertEqual(storage_writer.GetNumberOfEvents(), 10)

        # Test attributes of one event.
        events = list(storage_writer.GetEvents())
        event = events[0]

        self.assertEqual(event.timestamp, '2024-12-01 10:15:45')
        self.assertEqual(event.sender, '+1234567890')
        self.assertEqual(event.message, 'Hello! Your verification code is 672845. Do not share this with anyone.')

        self.assertEqual(event.data_type, 'android:sms:message')

    def testParseInvalidFile(self):
        """Tests the Parse function with an invalid file."""
        parser = android_sms.AndroidSMSParser()

        with self.assertRaises(ValueError):
            self._ParseFile(['invalid_sms_data.db'], parser)


if __name__ == '__main__':
    unittest.main()
