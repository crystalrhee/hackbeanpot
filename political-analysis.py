from flask import Flask, render_template, request
import urllib2
from bs4 import BeautifulSoup
import indicoio
from htmllaundry import sanitize

app = Flask(__name__)


@app.route('/abstract')
def get_abstract():
    url = request.args.get("url")

    abstract_content = _find_abstract(url)
    sentiment = indicoio.sentiment(sanitize(abstract_content))

    return render_template("index.html", content=abstract_content, output=sentiment)


@app.route('/image')
def get_image():
    url = request.args.get("url")

    img_box = _scrape_page(url, "figure", {"class": "lead-img"})
    img = img_box.find("img")
    img_src = str(img['src']).split("?")[0]

    fer = indicoio.fer([img_src], detect=True)

    return render_template("index.html", img=img, output=str(fer))


def _find_abstract(url):
    domain = url.split(".")[1]

    if domain == 'nature':
        abstract_box = _scrape_page(url, "div", {"id": "abstract-content"})
        return abstract_box.find("p")

    elif domain == 'sciencedirect':
        abstract_box = _scrape_page(url, "div", {"class": "abstract author"})
        return abstract_box.find("p")


def _scrape_page(url, name, attributes):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    return soup.find(name, attributes)


if __name__ == '__main__':
    app.run(debug=True)
