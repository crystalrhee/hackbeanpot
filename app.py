import indicoio
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, flash
from indicoio.custom import Collection
from wtforms import Form, TextAreaField, validators, SelectField

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class TextAreaForm(Form):
    name = TextAreaField('Text', validators=[validators.required()])
    choices = SelectField('Model', choices=[("gun_control", "Gun Control"), ("death_penalty", "Death Penalty"),
                                            ("climate_change", "Climate Change")])


indicoio.config.api_key = '35b0d68ba113813880b422207eed08d3'
gc_collection = Collection("gun_control", domain="standard")
dp_collection = Collection("death_penalty", domain="standard")
cc_collection = Collection("climate_change", domain="standard")
questions = {"gun_control": "Should More Gun Control Laws Be Enacted?",
             "death_penalty": "Should the Death Penalty Be Allowed?",
             "climate_change": "Is Human Activity Primarily Responsible for Global Climate Change?"}

@app.route('/collect')
def collect_from_article():
    url = request.args.get("url")
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    model_name = request.args.get("model_name")
    _add_articles_to_collection(soup, "newblue-pro-quote-box", "pro", model_name)
    _add_articles_to_collection(soup, "newblue-con-quote-box", "con", model_name)

    return "Articles successfully added"


def _add_articles_to_collection(soup, class_name, label, model_name):
    articles = []
    for article in soup.find_all("div", {"class": class_name}):
        contents = article.text
        articles.append([contents, label])

    if model_name == "gun_control":
        gc_collection.add_data(articles)
    elif model_name == "death_penalty":
        dp_collection.add_data(articles)
    elif model_name == "climate_change":
        cc_collection.add_data(articles)

    return articles


@app.route('/clear')
def clear_collection():
    gc_collection.clear()
    return "Collection successfully cleared!"


@app.route("/train")
def train():
    model_name = request.args.get("model_name")
    if model_name == "gun_control":
        gc_collection.train()
        gc_collection.wait()
    elif model_name == "death_penalty":
        dp_collection.train()
        dp_collection.wait()
    elif model_name == "climate_change":
        cc_collection.train()
        cc_collection.wait()
    return "Training completed successfully!"


@app.route("/predict", methods=["GET", "POST"])
def predict():
    form = TextAreaForm(request.form)

    if request.method == 'POST':
        text = request.form['name']
        model_name = request.form['choices']
        if model_name == "gun_control":
            prediction = gc_collection.predict(text)
        elif model_name == "death_penalty":
            prediction = dp_collection.predict(text)
        elif model_name == "climate_change":
            prediction = cc_collection.predict(text)
        flash(str(prediction))

    return render_template('index.html', wordform=form)


if __name__ == '__main__':
    app.run(debug=True)
