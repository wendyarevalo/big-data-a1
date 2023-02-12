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
   tbd
   ```
5. Insertion directly through shell
   ```
   tbd
   ```