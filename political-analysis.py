import indicoio
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, flash
from indicoio.custom import Collection
from wtforms import Form, TextAreaField, validators, StringField

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.required()])


class TextAreaForm(Form):
    name = TextAreaField('Text', validators=[validators.required()])


indicoio.config.api_key = '35b0d68ba113813880b422207eed08d3'
collection = Collection("pro_vs_con", domain="standard")


@app.route('/collect', methods=["GET", "POST"])
def collect_from_article():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        url = request.form['name']
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "lxml")

        _add_articles_to_collection(soup, "newblue-pro-quote-box", "pro")
        _add_articles_to_collection(soup, "newblue-con-quote-box", "con")

        flash("Articles successfully added")

    return render_template('index.html', form=form, title="hey")


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


@app.route("/predict", methods=["GET", "POST"])
def predict():
    # text = request.data
    # return str(collection.predict(text))
    form = TextAreaForm(request.form)

    if request.method == 'POST':
        text = request.form['name']
        prediction = collection.predict(text)
        flash(str(prediction))

    return render_template('index.html', wordform=form, title="hey")


if __name__ == '__main__':
    app.run(debug=True)
