#!venv/bin/python
from flask import Flask, jsonify, request, abort, redirect
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

    try:
      article.parse()
    except (IOError, UnicodeDecodeError):
      return '', 422

    try:
      top_image = article.top_image.rsplit('?',1)[0]
    except AttributeError:
      top_image = ''

    result = {
      "url": url,
      "top_image": top_image,
      "text": article.text,
    }

    return jsonify(result)

@app.route('/image', methods = ['GET'])
def get_image():
  url = request.args.get('url', '')
  if not url:
    abort(400)

  image_extensions = ['.jpg', '.gif', '.png', '.jpg', '.bmp', '.webp', '.webm']
  extension = url[url.rfind('.'):]

  if extension in image_extensions:
    return redirect(url)

  article = Article(url)
  article.download()

  try:
    article.parse()
  except (IOError, UnicodeDecodeError):
    return '', 422

  try:
    top_image = article.top_image.rsplit('?',1)[0]
  except AttributeError:
    top_image = ''

  if not top_image == '':
    return redirect(top_image)
  else:
    return '', 422


if __name__ == '__main__':
    app.run(debug = True)
