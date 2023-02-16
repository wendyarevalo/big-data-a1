DROP KEYSPACE IF EXISTS reddit;

CREATE KEYSPACE reddit
WITH REPLICATION = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 3
};

CREATE TABLE reddit.comments_by_subreddit (
    created_utc timestamp,
    ups int,
    subreddit text,
    id text,
    author text,
    score int,
    body text,
    PRIMARY KEY ((subreddit, id), ups)
)
WITH CLUSTERING ORDER BY (ups DESC);

CONSISTENCY QUORUM;
