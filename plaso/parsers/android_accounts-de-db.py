# -*- coding: utf-8 -*-
"""Parser for Android accounts_de.db SQLite database."""

from plaso.parsers import sqlite
from plaso.parsers import manager

class AccountsDeDBParser(sqlite.SQLiteParser):
    """Parser for Android accounts_de.db SQLite database."""

    NAME = 'accounts_de_db'
    DATA_FORMAT = 'Android accounts_de.db SQLite database'

    # SQL query to retrieve relevant data from the database
    QUERIES = [
        ((
            'SELECT accounts.name AS account_name, accounts.type AS account_type, '
            'auth_tokens.auth_token AS auth_token, accounts.last_authenticated_time AS last_authenticated_time '
            'FROM accounts '
            'LEFT JOIN auth_tokens ON accounts._id = auth_tokens.account_id'),
          'ParseAccountsDeEntry')
    ]

    REQUIRED_TABLES = frozenset(['accounts', 'auth_tokens'])

    def ParseAccountsDeEntry(self, parser_mediator, query, row, **unused_kwargs):
        """Parses an account entry from the database.

        Args:
            parser_mediator (ParserMediator): mediates interactions between parsers and other components.
            query (str): the SQL query producing the row.
            row (sqlite.Row): the row resulting from the query.
        """
        event_data = {
            'account_name': row['account_name'],
            'account_type': row['account_type'],
            'auth_token': row.get('auth_token', None),
            'last_authenticated_time': row.get('last_authenticated_time', None),
        }

        # Convert the event data into a Plaso event.
        parser_mediator.ProduceEventData(event_data)

# Register the parser with Plaso
manager.ParsersManager.RegisterParser(AccountsDeDBParser)
