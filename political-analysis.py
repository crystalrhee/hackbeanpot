from flask import Flask, render_template, request
import urllib2
from bs4 import BeautifulSoup
import indicoio

app = Flask(__name__)

indicoio.config.api_key = '35b0d68ba113813880b422207eed08d3'

@app.route('/analyze')
def hello_world():
    url = request.args.get("url")

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    img_box = soup.find("figure", attrs={"class": "lead-img"})
    img = img_box.find("img")
    img_src = str(img['src']).split("?")[0]

    print(indicoio.fer(img_src))

    return render_template("index.html", url=img_src)


if __name__ == '__main__':
    app.run(debug=True)
