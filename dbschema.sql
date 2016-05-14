-- Schema for WhiskyMetrics' main database

CREATE TABLE IF NOT EXISTS review (
    timestamp text,
    name text,
    reviewer text,
    url text,
    score text,
    type text,
    price text,
    date text
    );

.separator ,
.import whisky_reviews.csv review

CREATE TABLE IF NOT EXISTS distilleries (
    distillery text,
    location text,
    region text,
    status text
    );

.separator ,
.import distilleries.csv distilleries

