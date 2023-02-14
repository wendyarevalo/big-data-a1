# Deployment/installation guide

## coredms - Cassandra

To configure Cassandra, I have used the docker-compose.yml file provided in the tutorial
with the needed modifications to work in my environment. Assuming docker and docker compose
are installed and running, follow these steps:

1. Start the containers:
    ```
   cd cassandra 
   docker-compose up
    ```
2. After some seconds, run the following command to add a
   key space, and a table:
   ```
   docker exec -it cassandra1 cqlsh -f conf_cassandra.cql 
   ```
3. If desired, insertion directly through cqlsh should be done like this:
   ```
   INSERT INTO reddit.comments_upvotes (id, created_utc, ups, author, subreddit, score)
   VALUES ('12345', '2022-01-01 12:00:00', 100, 'john_doe', 'r/Cassandra', 1000);
   ```