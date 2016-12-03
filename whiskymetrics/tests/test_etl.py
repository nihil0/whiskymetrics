# -*- coding: utf-8 -*-
import whiskymetrics
import whiskymetrics.etl as etl
import os 
from datetime import date, datetime
import pandas as pd
from pandas.util.testing import assert_frame_equal


dir_path = os.getcwd()
static_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'static')

def test_download_review_file():
    etl.download_review_file()
    filename = date.today().strftime("%Y-%m-%d-review.csv")
    assert os.path.isfile(os.path.join(dir_path, filename))
    os.remove(os.path.join(dir_path, filename))

def test_transform():
    tbl = etl.transform(os.path.join(static_dir_path, "review_sample.csv"))
    tbl_compare = pd.read_csv(os.path.join(static_dir_path, "transformed_reviews.csv"), index_col=0)
    assert_frame_equal(tbl, tbl_compare)

def test_load():
    pass
