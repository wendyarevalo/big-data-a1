from flask import Flask, jsonify, request

def create_app():
    app = Flask(__name__)

    @app.route('/comments', methods=['GET'])
    def get_comments():
        data = []
        return jsonify(data)

    @app.route('/comments', methods=['POST'])
    def create_comments():
        data = request.get_json()
        new_user = {'created_utc': data['created_utc'],
                    'ups': data['ups'],
                    'subreddit': data['subreddit'],
                    'id': data['id'],
                    'author': data['author'],
                    'score': data['score'],
                    'body': data['body']}
        return jsonify(new_user)

    return app
