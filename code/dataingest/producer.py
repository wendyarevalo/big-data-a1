import csv
import pika

with open('../../data/small_sample_reddit_comments.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    next(csvreader)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='comments')

    for row in csvreader:
        filtered_row = ','.join([row[0], row[1], row[8], row[9], row[14], row[15], row[17]])
        print(filtered_row)
        channel.basic_publish(exchange='', routing_key='comments', body=filtered_row)

    connection.close()
