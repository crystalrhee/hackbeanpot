"""
Flask application to train an ML algorithm on for/against arguments for a given set of topics.
"""
import csv

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from indicoio.custom import Collection

from predictionform import PredictionForm

app = Flask(__name__)
app.config.from_object('config')

gc_collection = Collection("gun_control", domain="standard")
dp_collection = Collection("death_penalty", domain="standard")
cc_collection = Collection("climate_change", domain="standard")
ii_collection = Collection("illegal_immigration", domain="standard")
ar_collection = Collection("abortion_right", domain="standard")
questions = {
    "gun_control": "Should More Gun Control Laws Be Enacted?",
    "death_penalty": "Should the Death Penalty Be Allowed?",
    "climate_change": "Is Human Activity Primarily Responsible for Global Climate Change?",
    "illegal_immigration": "Should the Government Allow Immigrants Who Are Here Illegally to Become US Citizens?",
    "abortion_right": "Should Abortion Be Legal?"
}


@app.route('/collect')
def collect_from_article():
    """
    Scrape arguments for/against an argument from a given procon.org site and
    add to the appropriate collection.
    """
    url = request.args.get("url")
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    model_name = request.args.get("model_name")
    _add_articles_to_collection(soup, "newblue-pro-quote-box", "pro", model_name)
    _add_articles_to_collection(soup, "newblue-con-quote-box", "con", model_name)

    return "Articles successfully added"


def _add_articles_to_collection(soup, class_name, label, model_name):
    """
    Helper function to pull argument text from a div string and add the text to
    the appropriate collection.
    :param soup:       scraped html page
    :param class_name: name of html class containing argument text
    :param label:      which argument the given text corresponds to
    :param model_name: which collection the given data is being added to
    """
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
    elif model_name == "illegal_immigration":
        ii_collection.add_data(articles)
    elif model_name == "abortion_right":
        ar_collection.add_data(articles)
    else:
        raise RuntimeError("No model named %s" % model_name)


@app.route('/clear')
def clear_collection():
    """
    Clear data from the given collection.
    """
    model_name = request.args.get("model_name")
    if model_name == "gun_control":
        gc_collection.clear()
    elif model_name == "death_penalty":
        dp_collection.clear()
    elif model_name == "climate_change":
        cc_collection.clear()
    elif model_name == "illegal_immigration":
        ii_collection.clear()
    elif model_name == "abortion_right":
        ar_collection.clear()
    else:
        raise RuntimeError("No model named %s" % model_name)

    return "Collection successfully cleared!"


@app.route("/train")
def train():
    """
    Trigger the training of the given model, and wait for its completion before exiting.
    """
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
    elif model_name == "illegal_immigration":
        ii_collection.train()
        ii_collection.wait()
    elif model_name == "abortion_right":
        ar_collection.train()
        ar_collection.wait()
    else:
        raise RuntimeError("No model named %s" % model_name)

    return "Training completed successfully!"


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    Predict the pro/con value for the inputted form text.
    """
    form = PredictionForm(request.form)
    prediction = None
    question = None

    if request.method == 'POST':
        text = request.form['name']
        model_name = request.form['choices']
        if model_name == "gun_control":
            prediction = gc_collection.predict(text)
        elif model_name == "death_penalty":
            prediction = dp_collection.predict(text)
        elif model_name == "climate_change":
            prediction = cc_collection.predict(text)
        elif model_name == "illegal_immigration":
            prediction = ii_collection.predict(text)
        elif model_name == "abortion_right":
            prediction = ar_collection.predict(text)

        question = questions[model_name]

    return render_template('index.html',
                           wordform=form,
                           prediction=prediction,
                           question=question)


@app.route("/collect/text", methods=["POST"])
def add_text():
    """
    Add a given passage of text to the specified model.
    """
    model_name = request.get_json()["model_name"]
    text = request.get_json()["text"]
    side = request.get_json()["side"]
    data = [(text, side)]

    if model_name == "gun_control":
        gc_collection.add_data(data)
    elif model_name == "death_penalty":
        dp_collection.add_data(data)
    elif model_name == "climate_change":
        cc_collection.add_data(data)
    elif model_name == "illegal_immigration":
        ii_collection.add_data(data)
    elif model_name == "abortion_right":
        ar_collection.add_data(data)
    else:
        raise RuntimeError("No model named %s" % model_name)

    return "Text successfully added"


@app.route("/collect/csv")
def add_batch_text():
    """
    Add a set of text passages to the specified collection from a csv file.
    """
    model_name = request.args.get("model_name")
    if model_name == "gun_control":
        read_csv("csv/guns.csv", gc_collection)
    elif model_name == "death_penality":
        read_csv("csv/death.csv", dp_collection)
    elif model_name == "climate_change":
        read_csv("csv/climate.csv", cc_collection)
    elif model_name == "illegal_immigration":
        read_csv("csv/immigration.csv", ii_collection)
    elif model_name == "abortion":
        read_csv("csv/abortion.csv", ar_collection)
    else:
        raise RuntimeError("No model named %s" % model_name)

    return "CSV successfully added"


def read_csv(filepath, collection):
    """
    Read the specified csv file and add its contents to the given collection.
    :param filepath:   path to csv file
    :param collection: collection to add data to
    """
    articles = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)
        # skip headers
        next(reader, None)
        for row in reader:
            pro = row[0]
            con = row[2]
            if pro != "":
                articles.append([pro, "pro"])
            if con != "":
                articles.append([con, "con"])

    collection.add_data(articles)


if __name__ == '__main__':
    app.run(debug=True)
