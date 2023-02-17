import csv
import pika
import json
import time

with open('data/sample.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    next(csvreader)
    start=time.time()
    print(start)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
    channel = connection.channel()

    channel.queue_declare(queue='comments', durable=True)

    for row in csvreader:
        if len(row) >= 18 :
            filtered_row = [row[0], row[1], row[8], row[9], row[14], row[15], row[17]]

            data = {
                'created_utc': filtered_row[0],
                'ups': filtered_row[1],
                'subreddit': filtered_row[2],
                'id': filtered_row[3],
                'author': filtered_row[4],
                'score': filtered_row[5],
                'body': filtered_row[6]
            }
            message = json.dumps(data)
            channel.basic_publish(exchange='', routing_key='comments', body=message, properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    connection.close()
    elapsed_time=time.time() - start
    print('Execution time:', elapsed_time, 'seconds')
