CREATE TABLE IF NOT EXISTS  metadata (
    post_id varchar(8) PRIMARY KEY,
    time_stamp timestamp,
    author varchar(255),
    topic varchar(255),
    region varchar(255),
    score int
    );

CREATE TABLE IF NOT EXISTS review (
    post_id varchar(8) PRIMARY KEY,
    review_text text
    );
