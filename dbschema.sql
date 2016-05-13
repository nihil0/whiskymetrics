-- Schema for WhiskyMetrics' main database

CREATE TABLE IF NOT EXISTS review (
    timestamp text,
    name text,
    reviewer text,
    linktopost text,
    score text,
    type text,
    price text,
    date text
    );

.separator ,
.import whisky_reviews.csv review

