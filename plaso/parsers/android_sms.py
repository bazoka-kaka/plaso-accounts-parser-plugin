# -*- coding: utf-8 -*-
"""Parser for Android SMS database files."""

from plaso.parsers import interface
from plaso.parsers import manager
from plaso.lib import definitions
from plaso.containers import events
import sqlite3


class AndroidSmsEventData(events.EventData):
    """Android SMS event data."""
    DATA_TYPE = 'android:sms:message'

    def __init__(self):
        """Initializes event data."""
        super(AndroidSmsEventData, self).__init__(data_type=self.DATA_TYPE)
        self.address = None
        self.body = None
        self.date_sent = None
        self.date_received = None
        self.type = None


class AndroidSmsParser(interface.FileObjectParser):
    """Parser for Android SMS database files."""

    NAME = 'android_sms'
    DATA_FORMAT = 'Android SMS SQLite database'

    def ParseFileObject(self, parser_mediator, file_object, **kwargs):
        """Parses an Android SMS SQLite database file.

        Args:
          parser_mediator (ParserMediator): parser mediator.
          file_object (dfvfs.FileIO): file-like object to be parsed.

        Raises:
          WrongParser: when the format is not supported by the parser.
        """
        # Attempt to open the file object as an SQLite database.
        try:
            connection = sqlite3.connect(file_object)
        except sqlite3.DatabaseError as exception:
            raise interface.WrongParser(
                f'Unable to open SQLite database with error: {exception}'
            )

        # Verify the database contains the necessary table.
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
            tables = [row[0] for row in cursor.fetchall()]
        except sqlite3.DatabaseError as exception:
            raise interface.WrongParser(
                f'Unable to query SQLite database with error: {exception}'
            )

        if 'sms' not in tables:
            raise interface.WrongParser('Database does not contain an "sms" table.')

        # Query the SMS table and extract relevant fields.
        try:
            cursor.execute(
                'SELECT _id, address, date, date_sent, body, type FROM sms'
            )
            rows = cursor.fetchall()
        except sqlite3.DatabaseError as exception:
            parser_mediator.ProduceExtractionError(
                f'Error querying SMS table: {exception}'
            )
            return

        for row in rows:
            event_data = AndroidSmsEventData()
            event_data.address = row[1]
            event_data.body = row[4]
            event_data.date_received = row[2] / 1000.0  # Convert milliseconds to seconds
            event_data.date_sent = row[3] / 1000.0 if row[3] else None
            event_data.type = row[5]

            timestamp = event_data.date_received
            parser_mediator.ProduceEventWithEventData(
                timestamp, definitions.TIME_DESCRIPTION_RECEIVED, event_data
            )

            # If date_sent is available, produce a separate event.
            if event_data.date_sent:
                parser_mediator.ProduceEventWithEventData(
                    event_data.date_sent,
                    definitions.TIME_DESCRIPTION_SENT,
                    event_data,
                )

        # Clean up the database connection.
        connection.close()


# Register the parser with the Plaso framework.
manager.ParsersManager.RegisterParser(AndroidSmsParser)
