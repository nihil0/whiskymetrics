"""WhiskyMetrics Database Module

This module implements classes to interact with the new Microsoft Azure SQL
database.

Before using, ensure that the azuredbconf.py_template file is renamed as .py and
that the variables within it are set to the appropriate values.

"""
from configparser import ConfigParser
from sqlalchemy import create_engine
from urllib.parse import quote_plus

config = ConfigParser()
config.read("config.ini")

class WhiskyDB():
    """ Class to interact with the WhiskyMetrics Database"""
    def __init__(self):
        conn_string = "DRIVER={{ODBC Driver 13 for SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3}".format(
            config['DATABASE']['server'],
            config['DATABASE']['database'],
            config['DATABASE']['username'],
            config['DATABASE']['password']
        )

        self.engine = create_engine("mssql+pyodbc:///?odbc_connect={0}".format(quote_plus(conn_string)))

        #self.dbconn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+azuredbconfig.server+';DATABASE='+azuredbconfig.database+';UID='+azuredbconfig.username+';PWD='+ azuredbconfig.password)
        #self.crsr = dbconn.cursor()


#params = urllib.quote_plus("DRIVER={SQL Server Native Client 10.0};SERVER=dagger;DATABASE=test;UID=user;PWD=password")

#engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)