# -*- coding: utf-8 -*-
"""Tests for the SQLite parser plugin for Android accounts database files."""

import unittest

from plaso.parsers.sqlite_plugins import android_accounts  # Replace with actual import
from tests.parsers.sqlite_plugins import test_lib


class AndroidAccountsPluginTest(test_lib.SQLitePluginTestCase):
  """Tests for the SQLite parser plugin for Android accounts database files."""

  def testParse(self):
    """Tests the ParseAccountRow method."""
    plugin = android_accounts.AndroidAccountsPlugin()  # Replace with actual class name
    storage_writer = self._ParseDatabaseFileWithPlugin(
        ['accounts_de.db'], plugin)

    number_of_event_data = storage_writer.GetNumberOfAttributeContainers(
        'event_data')
    self.assertEqual(number_of_event_data, 10)  # Adjust this number based on expected events

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'extraction_warning')
    self.assertEqual(number_of_warnings, 0)

    expected_event_values = {
        'timestamp': '2020-02-13T20:19:15.000000+00:00',  # Adjust the timestamp format based on actual data
        'account_type': 'Google',  # Adjust based on actual account type in the DB
        'username': 'thisisdfir@gmail.com',  # Example username
        'identifier': 'com.google',  # Example identifier
        'owning_bundle_id': 'com.google.android.gm'  # Example owning bundle ID
    }

    event_data = storage_writer.GetAttributeContainerByIndex(
        'event_data', 3)  # Adjust the index if necessary
    self.CheckEventData(event_data, expected_event_values)


if __name__ == '__main__':
  unittest.main()
