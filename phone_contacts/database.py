"""This module provides a database connection."""

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


def _createContactsTable():
    """Create the contacts table in the database."""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            phone VARCHAR(50) NOT NULL,
            email VARCHAR(40) NOT NULL
        )
        """
    )

def createConnection(databaseName):
    """Create and open a database connection."""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "Phone_Contacts",
            f"Database Error: {connection.lastError().text()}",
        )
        return False
    _createContactsTable()
    return True