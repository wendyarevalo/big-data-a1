from flask import Flask, jsonify, request
import pika
import json
from cassandra.cluster import Cluster

app = Flask(__name__)

cluster = Cluster(['cassandra1'])
session = cluster.connect()
session.set_keyspace('reddit')


@app.route('/comments_by_subreddit', methods=['GET'])
def get_comments_by_subreddit():
     data = []
     rows = session.execute('SELECT * FROM comments_by_subreddit')
     for row in rows:
        data.append(row)
     return jsonify(data)

@app.route('/comments', methods=['POST'])
def create_comments():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
    channel = connection.channel()

    channel.queue_declare(queue='comments', durable=True)

    data = request.get_json()
    new_user = {
                'created_utc': data['created_utc'],
                'ups': data['ups'],
                'subreddit': data['subreddit'],
                'id': data['id'],
                'author': data['author'],
                'score': data['score'],
                'body': data['body']
                }
    message = json.dumps(new_user)
    channel.basic_publish(exchange='', routing_key='comments', body=message, properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    print(" [x] Sent %r" % message)
    return jsonify(new_user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)