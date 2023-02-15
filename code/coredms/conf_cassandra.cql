DROP KEYSPACE IF EXISTS reddit;

CREATE KEYSPACE reddit
WITH REPLICATION = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 3
};

CREATE TABLE reddit.comments_upvotes (
    created_utc timestamp,
    ups int,
    subreddit text,
    id text PRIMARY KEY,
    author text,
    score int,
    body text
);

CONSISTENCY QUORUM;
