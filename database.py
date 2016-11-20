"""WhiskyMetrics Database Module

This module implements classes to interact with the new Microsoft Azure SQL
database.

Before using, ensure that the azuredbconf.py_template file is renamed as .py and
that the variables within it are set to the appropriate values.

"""

import azuredbconf, pymssql

class WhiskyDB():
    """ Class to interact with the WhiskyMetrics Database"""
    def__init__(self):
        self.dbconn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+azuredbconfig.server+';DATABASE='+azuredbconfig.database+';UID='+azuredbconfig.username+';PWD='+ azuredbconfig.password)
        self.crsr = dbconn.cursor()



