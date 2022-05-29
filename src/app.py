import requests

from MemeGenerator.MemeEngine import MemeEngine
from QuoteEngine.QuoteEngine import Ingestor
from flask import Flask, render_template, request
import random
import os
from datetime import datetime
from meme import generate_meme

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for file in quote_files:
        quotes.extend(Ingestor.parse(file))

    # check for ingestible files with os.walk
    images_path = "./_data/photos/dog/"
    imgs = []
    for root, dirs, files in os.walk(images_path):
        for file_name in files:
            imgs.append(os.path.join(root, file_name))

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    image_url = request.form["image_url"]
    time = datetime.now().strftime("%H_%M_%S")
    temp_img = f"./temp_img{time}.jpg"
    try:
        img_content = requests.get(image_url, stream=True).content
        with open(temp_img, "wb") as file:
            file.write(img_content)

        body = request.form["body"]
        author = request.form["author"]
        path = generate_meme(temp_img, body, author)
    except requests.exceptions.RequestException as error:
        print(error)
        return "cant open url"

    # remove temp image
    os.remove(temp_img)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    if not os.path.isdir("./static"):
        os.makedirs("./static")
    if not os.path.isdir("./temp"):
        os.makedirs("/.temp")
    app.run()
