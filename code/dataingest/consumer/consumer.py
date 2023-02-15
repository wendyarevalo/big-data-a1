import json
import os
import pika
import sys
from cassandra.cluster import Cluster

cluster = Cluster(['cassandra1'])
session = cluster.connect()
session.execute("CREATE KEYSPACE IF NOT EXISTS reddit WITH REPLICATION = "
                "{'class': 'SimpleStrategy', "
                "'replication_factor': 3}")
session.set_keyspace('reddit')
session.execute("CREATE TABLE IF NOT EXISTS comments_upvotes ("
                "created_utc timestamp,"
                "ups int,"
                "subreddit text,"
                "id text PRIMARY KEY,"
                "author text,"
                "score int,"
                "body text)")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
    channel = connection.channel()

    channel.queue_declare(queue='comments')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        message_data = json.loads(body)
        id = message_data['id']
        created_utc = message_data['created_utc']
        ups = int(message_data['ups'])
        author = message_data['author']
        subreddit = message_data['subreddit']
        score = int(message_data['score'])
        body = message_data['body']

        # Create and execute the CQL INSERT statement
        insert_query = "INSERT INTO reddit.comments_upvotes (id, created_utc, ups, author, subreddit, score, body) " \
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        session.execute(insert_query, (id, created_utc, ups, author, subreddit, score, body))

    channel.basic_consume(queue='comments', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
