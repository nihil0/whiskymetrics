"""WhiskyMetrics Database Module

This module implements classes to interact with the new Microsoft Azure SQL
database.

Before using, ensure that the azuredbconf.py_template file is renamed as .py and
that the variables within it are set to the appropriate values.

"""
from configparser import ConfigParser
from sqlalchemy import create__engine
from sqlalchemy import Table, Column, String, MetaData, Integer, DateTime
from sqlalchemy.exc import DBAPIError
from urllib.parse import quote_plus
import os, whiskymetrics

# Test is config file exists in $HOME/.whiskymetrics
try:
    open(os.path.join(os.environ['HOME'], ".whiskymetrics", "config.ini")).read()
except IOError:
    print("Config file $HOME/.whiskymetrics/config.ini not found.")
else:
    config = ConfigParser()
    config.read(os.path.join(os.environ['HOME'], ".whiskymetrics", "config.ini"))
    conn_string = "DRIVER={{ODBC Driver 13 for SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3}".format(
        config['DATABASE']['server'],
        config['DATABASE']['database'],
        config['DATABASE']['username'],
        config['DATABASE']['password']
        )
    _engine = create_engine("mssql+pyodbc:///?odbc_connect={0}".format(quote_plus(conn_string)))

def test_connection():
    """ Test connection to database """
    try:
        _engine.connect()
    except DBAPIError as err:
        print("Could not connect to the database. Here is some debugging info")
        raise err

    print("Connection successsful!")




# Create table objects
def create_metadata():
    """ Returns a SQLAlchemy metadata object with tables specified as below """
    metadata = MetaData()

    # Distillery table
    distillery_col_names = ["id","Distillery","Body","Sweetness","Smoky","Medicinal","Tobacco","Honey","Spicy","Winey","Nutty","Malty","Fruity","Floral","Postcode","Latitude","Longitude"]
    distillery_col_types = [Integer,String,Integer,Integer,Integer,Integer,Integer,Integer,Integer,Integer,Integer,Integer,Integer,Integer,String,String,String]
    columns = [Column(name,coltype) for name, coltype in zip(distillery_col_names,distillery_col_types)]
    columns[0].primary_key = True
    distillery = Table("distillery", metadata,*columns)

    review_col_names = ["id","timestamp","whisky_name","user","link","rating","region"]
    review_col_types = [Integer,DateTime,String,String,String,Integer,String]
    columns = [Column(name,coltype) for name, coltype in zip(review_col_names,review_col_types)]
    columns[0].primary_key = True
    distillery = Table("review", metadata,*columns)


    return metadata

def create_tables():
    """ Creates tables in the database pointed to by `whiskymetrics.database._engine` """
    metadata = create_metadata()
    metadata.create_all(_engine)

'''class WhiskyDB():
    """ Class to interact with the WhiskyMetrics Database"""
    def __init__(self):
        
'''
        #self.dbconn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+azuredbconfig.server+';DATABASE='+azuredbconfig.database+';UID='+azuredbconfig.username+';PWD='+ azuredbconfig.password)
        #self.crsr = dbconn.cursor()


#params = urllib.quote_plus("DRIVER={SQL Server Native Client 10.0};SERVER=dagger;DATABASE=test;UID=user;PWD=password")

#_engine = create__engine("mssql+pyodbc:///?odbc_connect=%s" % params)
