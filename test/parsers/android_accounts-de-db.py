#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the Android accounts_de.db parser."""

import unittest

from plaso.parsers import accounts_de
from tests.parsers import test_lib


class AccountsDeDBParserTest(test_lib.ParserTestCase):
    """Tests for the Android accounts_de.db parser."""

    def testParseFile(self):
        """Tests the Parse function on a sample accounts_de.db file."""
        parser = accounts_de.AccountsDeDBParser()
        storage_writer = self._ParseFile(['accounts_de.db'], parser)

        # Validate number of events produced.
        self.assertEqual(storage_writer.GetNumberOfAttributeContainers('event'), 3)

        # Get and validate specific event data.
        events = list(storage_writer.GetEvents())
        self.assertEqual(events[0].data_type, 'android:accounts:entry')

        expected_account_name = 'example@gmail.com'
        expected_account_type = 'com.google'
        expected_last_authenticated_time = '2023-11-10T12:34:56.000Z'

        self.assertEqual(events[0].account_name, expected_account_name)
        self.assertEqual(events[0].account_type, expected_account_type)
        self.assertEqual(events[0].last_authenticated_time, expected_last_authenticated_time)


if __name__ == '__main__':
    unittest.main()
