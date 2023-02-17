import csv
import pika
import json
import time
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement


#cluster = Cluster(['cassandra1', 'cassandra2', 'cassandra3', 'cassandra4', 'cassandra5'])
cluster = Cluster(['cassandra1', 'cassandra2', 'cassandra3'])
session = cluster.connect()
session.execute("CREATE KEYSPACE IF NOT EXISTS reddit WITH REPLICATION = "
                "{'class': 'SimpleStrategy', "
                "'replication_factor': 3}")
session.set_keyspace('reddit')
session.execute("CREATE TABLE IF NOT EXISTS comments_by_subreddit ("
                "created_utc timestamp,"
                "ups int,"
                "subreddit text,"
                "id text,"
                "author text,"
                "score int,"
                "body text,"
                "PRIMARY KEY ((subreddit, id), ups)"
                ")"
                "WITH CLUSTERING ORDER BY (ups DESC)")


with open('data/sample.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    next(csvreader)

    start=time.time()
    print(start)
    ## enable only 1 option
    #consistency_level =ConsistencyLevel.ONE
    consistency_level =ConsistencyLevel.QUORUM
    #consistency_level =ConsistencyLevel.ALL

    for row in csvreader:
        if len(row) >= 18 :
            filtered_row = [row[0], row[1], row[8], row[9], row[14], row[15], row[17]]

            id = filtered_row[3]
            created_utc = filtered_row[0]
            ups = int(filtered_row[1])
            author = filtered_row[4]
            subreddit = filtered_row[2]
            score = int(filtered_row[5])
            body = filtered_row[6]

            # Create and execute the CQL INSERT statement
            insert_query = "INSERT INTO reddit.comments_by_subreddit (id, created_utc, ups, author, subreddit, score, body) " \
                                               "VALUES (%s, %s, %s, %s, %s, %s, %s)"

            statement = SimpleStatement(insert_query,
                    consistency_level=consistency_level)

            session.execute(statement, (id, created_utc, ups, author, subreddit, score, body))

    elapsed_time=time.time() - start
    print('Execution time:', elapsed_time, 'seconds')

