"""This module provides a model to manage the contacts table."""

from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtSql import QSqlTableModel
import csv
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem


class ContactsModel:
    def __init__(self ):
        self.model = self.createModel()
        self.proxy = self.create_proxy_model()
        

    # @staticmethod
    def createModel(self):
        """Create and set up the model."""
        tablemodel = QSqlTableModel()
        tablemodel.setTable("contacts")
        tablemodel.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        tablemodel.select()
        headers = ("ID", "Name", "Phone", "Email")
        for columnIndex, header in enumerate(headers):
            tablemodel.setHeaderData(
                columnIndex, Qt.Orientation.Horizontal, header)
        return tablemodel
    def create_proxy_model(self):
        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(self.model)
        proxy_model.setFilterKeyColumn(0)
        return proxy_model

    
    def addContact(self, data):
        """Add a contact to the database."""
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()

    def deleteContact(self, row):
        """Remove a contact from the database."""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()
        

    def clearContacts(self):
        """Remove all contacts in the database."""
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.select()


    def handleSave(self):
        path, _ = QFileDialog.getSaveFileName(
                self, 'Save File', '', 'CSV(*.csv)')
        if not path:
            with open(str(path), 'wb') as stream:
                writer = csv.writer(stream)
                for row in range(self.model.rowCount()):
                    rowdata = []
                    for column in range(self.model.columnCount()):
                        item = self.model.item(row, column)
                        if item is not None:
                            rowdata.append(
                                item.text().encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)

    def handleOpen(self):
        path, _ = QFileDialog.getOpenFileName(
                self, 'Open File', '', 'CSV(*.csv)')
        if not path:
            with open(str(path), 'rb') as stream:
                self.model.setRowCount(0)
                self.model.setColumnCount(0)
                for rowdata in csv.reader(stream):
                    row = self.model.rowCount()
                    self.model.insertRow(row)
                    self.model.setColumnCount(len(rowdata))
                    for column, data in enumerate(rowdata):
                        item = QTableWidgetItem(data.decode('utf8'))
                        self.model.setItem(row, column, item)