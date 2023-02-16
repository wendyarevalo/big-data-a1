# Deployment/installation guide

### Prerequisites
* Docker
* Docker compose
* cURL or Postman to try the API

## coredms - Cassandra

To configure Cassandra, I have used the docker-compose.yml file provided in the tutorial
with the needed modifications to work in my environment. Assuming docker and docker compose
are installed and running, follow these steps:

1. Start the containers:
    ```
   docker-compose -f code/coredms/docker-compose.yml up
    ```
2. After some seconds (60s+), run the following command to add a
   key space, and a table:
   ```
   docker exec -it cassandra1 cqlsh -f conf_cassandra.cql 
   ```
To insert data manually access any cassandra container and use cqlsh to run this insertion:
   ```
   INSERT INTO reddit.comments_upvotes (id, created_utc, ups, author, subreddit, score, body)
   VALUES ('12345', '1430438437', 100, 'john_doe', 'r/Cassandra', 1000, 'some message');
   ```

## dataingest - Python + RabbitMQ

To ingest data from CSV to Cassandra cluster I have created producer and consumer containers which are connected to RabbitMQ.
Consumer and Producer files are based on tutorials from the RabbitMQ page.
To run them follow these steps:

1. Start RabbitMQ consumers and daas:
   ```
   docker build -t consumer code/dataingest/consumer/.
   ```
   ```
   docker build -t daas code/daas/app/.
   ```
   ```
   docker-compose -f code/dataingest/docker-compose.yml up
   ```
   Even though the docker-compose file specifies that the consumers should be created after
   rabbit, they might fail. Simply start them again after rabbit is running.

2. The producer needs to have a csv file called __sample.csv__ within the same folder, you can add the sample data in the data folder like this:
   ```
   cp data/small_sample_reddit_comments.csv code/dataingest/producer/sample.csv
   ```
3. Once the file is in the folder, build and run the produce:
   ```
   docker build -t producer code/dataingest/producer/.
   ```
   ```
   docker run --network bigdata-network producer
   ```
   
## daas - Flask API + RabbitMQ
The daas part of my design is a simple Flask API in python with GET and POST routes.
This runs automatically when running the dataingest docker compose file since it uses the
same rabbitMQ connection.
Unfortunately, the POST route is not sending data to the consumers, I have not solved this problem yet.

1. To test the GET route, use this curl request:
   ```
   curl --location 'http://127.0.0.1:8000/comments_by_id'
   ```
2. To test the POST route, use this curl request:
   ```
   curl --location 'http://127.0.0.1:8000/comments' \
   --header 'Content-Type: application/json' \
   --data '{
   "created_utc": "1430438433",
   "ups": "1000",
   "subreddit": "AskReddit",
   "id": "c123e8e22",
   "author": "usagi123",
   "score": "1",
   "body": "this is a test body"
   }'
   ```