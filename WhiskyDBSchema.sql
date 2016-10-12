CREATE TABLE IF NOT EXISTS  metadata (
    review_id serial PRIMARY KEY,
    post_id varchar(8),
    time_stamp timestamp,
    author varchar(255),
    topic varchar(255),
    region varchar(255),
    score int
    );

CREATE TABLE IF NOT EXISTS review (
    review_id integer references metadata(review_id),
    post_id varchar(8) PRIMARY KEY,
    review_text text
    );
