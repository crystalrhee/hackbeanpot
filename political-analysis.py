from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import indicoio
from indicoio.custom import Collection
from htmllaundry import sanitize
import requests

app = Flask(__name__)

indicoio.config.api_key = '35b0d68ba113813880b422207eed08d3'
collection = Collection("pro_vs_con", domain="standard")

@app.route('/abstract')
def get_abstract():
    url = request.args.get("url")

    abstract_content = _find_abstract(url)

    return render_template("index.html", content=abstract_content, output=abstract_content)



def _find_abstract(url):
    abstract_box = _scrape_page(url, "div", {"class":"article-con"})
    return abstract_box


def _scrape_page(url, name, attributes):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    cons = []
    for att in soup.find_all(name, attributes):
        p = att.find('p')
        cons.append(p.text)
        collection.add_data([p.text, "gun control con"])
    return cons

def train():
   collection.train()
   #collection.wait()
   return collection.predict("gun control sucks")

if __name__ == '__main__':
    app.run(debug=True)