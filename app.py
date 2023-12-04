from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/tweets', methods=['GET'])
def get_tweets():
    try:
        with open('tweets.json', 'r') as file:
            tweets = json.load(file)
        query_param = request.args.get('filter')
        if query_param:
            filtered_tweets = [tweet for tweet in tweets if query_param.lower() in tweet['text'].lower()]
            return jsonify(filtered_tweets)
        else:
            return jsonify(tweets)

    except FileNotFoundError:
        return jsonify({'error': 'Tweets file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tweet/<int:tweet_id>', methods=['GET'])
def get_tweet(tweet_id):
    try:
        with open('tweets.json', 'r') as file:
            tweets = json.load(file)

        tweet = next((t for t in tweets if t['id'] == tweet_id), None)
        if tweet:
            return jsonify(tweet)
        else:
            return jsonify({'error': 'Tweet not found'}), 404

    except FileNotFoundError:
        return jsonify({'error': 'Tweets file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

