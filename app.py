#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa-durmuss@outlook.com]

from flask import Flask, render_template, redirect, url_for, request

# insert path for predicting word.
import sys
sys.path.insert(1, '/home/hummingbird/Desktop/MD/github/word-predictor')
from predictor import WordPredictor


app = Flask(__name__)

predictor = WordPredictor('./corpora/little_prince.txt')

result = []
word = ""
@app.route("/")
def index():
    return render_template("index.html", todos=result, input_word=word)


@app.route("/add",methods = ["POST"])
def addTodo():
    global result, word
    # kelime
    word = request.form.get("title")
    # sonraki kelimeler ve ihtimalleri bir dizi şeklinde elde edilir.
    result = predictor.predict(word, return_flag=True)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
