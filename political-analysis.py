from flask import Flask, render_template, request, flash
from bs4 import BeautifulSoup
import indicoio
from indicoio.custom import Collection
import requests

app = Flask(__name__)

indicoio.config.api_key = '35b0d68ba113813880b422207eed08d3'
collection = Collection("pro_vs_con", domain="standard")


@app.route('/collect')
def collect_from_article():
    url = request.args.get("url")
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    _add_articles_to_collection(soup, "newblue-pro-quote-box", "pro")
    _add_articles_to_collection(soup, "newblue-con-quote-box", "con")

    return render_template("index.html", status="Articles successfully added!")


def _add_articles_to_collection(soup, class_name, label):
    articles = []
    for article in soup.find_all("div", {"class": class_name}):
        contents = article.text
        articles.append([contents, label])
        collection.add_data(articles)

    return articles


@app.route('/clear')
def clear_collection():
    collection.clear()
    return render_template("index.html", status="Collection successfully cleared!")


@app.route("/train")
def train():
    collection.train()
    collection.wait()
    return render_template("index.html", status="Training completed successfully!")


@app.route("/predict", methods=["POST"])
def predict():
    text = request.data
    return str(collection.predict(text))


if __name__ == '__main__':
    app.run(debug=True)
