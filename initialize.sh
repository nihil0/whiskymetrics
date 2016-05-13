#!/usr/bin/env bash

# Google sheet id
id="1X1HTxkI6SqsdpNSkSSivMzpxNT-oeTbjFFDdEkXD30o"

url="https://docs.google.com/spreadsheets/d/$id/export?format=csv&id=$id"

wget --output-document="whisky_reviews.csv" $url

sqlite3 whisky.db < dbschema.sql

