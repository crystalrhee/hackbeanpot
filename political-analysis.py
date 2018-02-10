from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import indicoio
from indicoio.custom import Collection
from htmllaundry import sanitize
import requests

app = Flask(__name__)

indicoio.config.api_key = '35b0d68ba113813880b422207eed08d3'
collection = Collection("collection_name")

@app.route('/abstract')
def get_abstract():
    url = request.args.get("url")

    abstract_content = _find_abstract(url)
    sentiment = indicoio.sentiment(sanitize(abstract_content))

    # collection.add_data([["text1", "label1"], ["text2", "label2"], ...])

    return render_template("index.html", content=abstract_content, output=sentiment)


def _find_abstract(url):
    abstract_box = _scrape_page(url, "div", {"class":"article-con"})
    return abstract_box.find('p').text


def _scrape_page(url, name, attributes):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find(name, attrs=attributes)

#def train():
   #collection.train()
   #collection.wait()
   #return collection.predict("indico is so easy to use!")

if __name__ == '__main__':
    app.run(debug=True)