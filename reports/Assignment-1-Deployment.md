# Deployment/installation guide

## coredms - Cassandra

To configure Cassandra, I have used the docker-compose.yml file provided in the tutorial
with the needed modifications to work in my environment. Assuming docker and docker compose
are installed and running follow these steps:

1. Start the containers:
    ```
    docker-compose up
    ```
2. Access the shell command in any of the nodes:
    ```
    cqlsh
    ```
3. Creation of keyspace
   ```
   CREATE KEYSPACE reddit
   WITH REPLICATION = {
   'class' : 'SimpleStrategy',
   'replication_factor' : 3
   };
   ```
4. Creation of tables
   ```
   CREATE TABLE reddit.comments_upvotes (
   id text PRIMARY KEY,
   created_utc timestamp,
   ups int,
   author text,
   subreddit text,
   score int
   );
   ```
5. Insertion directly through shell
   ```
   INSERT INTO reddit.comments_upvotes (id, created_utc, ups, author, subreddit, score)
   VALUES ('12345', '2022-01-01 12:00:00', 100, 'john_doe', 'r/Cassandra', 1000);
   ```