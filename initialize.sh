#!/usr/bin/env bash

function get-csv {
    url="https://docs.google.com/spreadsheets/d/$1/export?format=csv"

    wget --output-document=$2 $url
}

# Google sheet id for reviews
rev="1X1HTxkI6SqsdpNSkSSivMzpxNT-oeTbjFFDdEkXD30o"

get-csv $rev "whisky_reviews.csv"

# Google sheet id for distillery info
dis="1Q4FJQvQrPJSBvw1cmkXNT3EJc3eiEn0SoHaWWMhW_z4"

get-csv $dis "distilleries.csv"

# Some stemming
sed -i -e 's/Lowlands/Lowland/' -e 's/Highlands/Highland/' distilleries.csv

# Create database
sqlite3 whisky.db < dbschema.sql


