CREATE TABLE IF NOT EXISTS  metadata (
    review_id serial PRIMARY KEY,
    url varchar(2083),
    time_stamp timestamp,
    author varchar(255),
    topic varchar(255),
    region varchar(255),
    score int
    );

CREATE TABLE IF NOT EXISTS review (
    review_id integer UNIQUE references metadata(review_id),
    review_text text
    );

