#!venv/bin/python
from flask import Flask, jsonify, request, abort
from newspaper import Article

app = Flask(__name__)

@app.route("/")

def get_index():
  return 'Hello'

@app.route('/details', methods = ['GET'])

def get_details():
    url = request.args.get('url', '')
    if not url:
      abort(400)

    article = Article(url)
    article.download()
    article.parse()

    
    result = {
      "url": url,
      "top_image": article.top_image,
      "text": article.text
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug = True)