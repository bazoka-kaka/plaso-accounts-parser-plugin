from dfdatetime import posix_time as dfdatetime_posix_time
from plaso.containers import events
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface


class AndroidAccountsEventData(events.EventData):
    """Android accounts event data.
    
    Attributes:
        timestamp (dfdatetime.PosixTime): Time of the event.
        account_name (str): Name of the account.
        account_type (str): Type of the account.
        previous_name (str): Previous name of the account.
        last_password_entry_time (dfdatetime.PosixTime): Last time password was updated.
    """

    DATA_TYPE = 'android:accounts:account'

    def __init__(self):
        """Initializes event data."""
        super(AndroidAccountsEventData, self).__init__(data_type=self.DATA_TYPE)
        self.timestamp = None
        self.account_name = None
        self.account_type = None
        self.previous_name = None
        self.last_password_entry_time = None


class AndroidAccountsPlugin(interface.SQLitePlugin):
    """SQLite parser plugin for Android accounts (accounts_de.db) database."""

    NAME = 'android_accounts'
    DATA_FORMAT = 'Android accounts SQLite database (accounts_de.db)'

    REQUIRED_STRUCTURE = {
        'accounts': frozenset(['_id', 'name', 'type', 'previous_name', 'last_password_entry_time_millis_epoch']),
        'shared_accounts': frozenset(['_id', 'name', 'type'])
    }

    QUERIES = [(
        'SELECT _id, name, type, previous_name, last_password_entry_time_millis_epoch '
        'FROM accounts',
        'ParseAccountRow'
    )]

    SCHEMAS = {
        'accounts': (
            'CREATE TABLE accounts ('
            '_id INTEGER PRIMARY KEY, '
            'name TEXT NOT NULL, '
            'type TEXT NOT NULL, '
            'previous_name TEXT, '
            'last_password_entry_time_millis_epoch INTEGER DEFAULT 0, '
            'UNIQUE(name, type))'
        ),
        'shared_accounts': (
            'CREATE TABLE shared_accounts ('
            '_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'name TEXT NOT NULL, '
            'type TEXT NOT NULL, '
            'UNIQUE(name, type))'
        )
    }

    REQUIRES_SCHEMA_MATCH = False

    def _GetTimestampRowValue(self, query_hash, row, value_name):
        """Retrieves a POSIX timestamp value from the row."""
        timestamp = self._GetRowValue(query_hash, row, value_name)
        if timestamp is None:
            return None
        return dfdatetime_posix_time.PosixTime(timestamp=timestamp // 1000)

    def ParseAccountRow(self, parser_mediator, query, row, **unused_kwargs):
        """Parses an account row."""
        query_hash = hash(query)

        event_data = AndroidAccountsEventData()
        event_data.timestamp = self._GetTimestampRowValue(query_hash, row, 'last_password_entry_time_millis_epoch')
        event_data.account_name = self._GetRowValue(query_hash, row, 'name')
        event_data.account_type = self._GetRowValue(query_hash, row, 'type')
        event_data.previous_name = self._GetRowValue(query_hash, row, 'previous_name')

        parser_mediator.ProduceEventData(event_data)


sqlite.SQLiteParser.RegisterPlugin(AndroidAccountsPlugin)
