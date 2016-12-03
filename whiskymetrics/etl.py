""" WhiskyMetrics ETL tools

This module provides tools for managing the ETL workflow to load and update
the "metadata" table in the whiskymetrics database.

The general ETL workflow is as follows:

    Extract: data source a Google Sheet which is downloaded as a CSV
    Transforms: 1. Filter out single malt whiskies
                2. Select only those whiskies that have 10 reviews or more
    Load: Load into Azure SQL database with schema described in 'whiskymetrics-schema.sql'
"""
import requests
from datetime import date, datetime
import pandas as pd
import numpy as np
import codecs
import os 

def download_review_file():
    """ Downloads review data from Google Sheets as CSV. """
    print(os.getcwd())
    file_id = "1X1HTxkI6SqsdpNSkSSivMzpxNT-oeTbjFFDdEkXD30o"
    url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv".format(file_id)

    resp = requests.get(url)

    filename = date.today().strftime("%Y-%m-%d-review.csv")

    with codecs.open(filename, 'w+', "utf-8") as file:
        file.write(resp.text)

def transform(filename):
    """ Returns a list of tuples representing the 'metadata' table in the
    whiskymetrics database.

    """

    tbl = pd.read_csv(filename)

    # Drop the Date and Price columns
    tbl = tbl[tbl.columns[0:6]]

    # Convert text to lower case and strip whitespace
    tbl['Whisky Name'] = tbl['Whisky Name'].replace(np.nan, "", regex=True).map(lambda x: x.strip().lower())
    tbl['Reviewer Username'] = tbl['Reviewer Username'].replace(np.nan, "", regex=True).map(lambda x: x.strip())
    tbl['Region'] = tbl['Region'].replace(np.nan, "", regex=True).map(lambda x: x.strip().lower())

    # Filter out single malts
    tbl = tbl.loc[tbl['Region'].isin(('highland','lowland','campbeltown','island','islay','japan','taiwan','india','sweden','finland'))]

    # Select only those whiskies with over 10 reviews
    rev_count = tbl['Whisky Name'].value_counts()
    whisky_list = rev_count[rev_count >= 10].index
    tbl = tbl.loc[tbl['Whisky Name'].isin(whisky_list)]

    # Change timestamp format to ISO 8601
    def format_timestamp(time_string):
        ''' Formats timestamp to ISO 8601 form. Empty string is returned if NaN '''
        if pd.isnull(time_string):
            return ''
        else:
            return datetime.strptime(time_string, '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')

    tbl['Timestamp'] = tbl['Timestamp'].map(format_timestamp)

    return tbl








