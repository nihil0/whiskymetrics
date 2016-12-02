# -*- coding: utf-8 -*-
import whiskymetrics
import whiskymetrics.etl as etl
import os 
from datetime import date, datetime

dir_path = os.getcwd()

def test_download_file():
    etl.download_file()
    filename = date.today().strftime("%Y-%m-%d-review.csv")
    assert os.path.isfile(os.path.join(dir_path, filename))
    os.remove(os.path.join(dir_path, filename))


