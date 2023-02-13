DROP KEYSPACE IF EXISTS reddit;

CREATE KEYSPACE reddit
WITH REPLICATION = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 3
};

CREATE TABLE reddit.comments_upvotes (
    id text PRIMARY KEY,
    created_utc timestamp,
    ups int,
    author text,
    subreddit text,
    score int
);

CONSISTENCY QUORUM;
