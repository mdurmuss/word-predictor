#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa-durmuss@outlook.com]

from flask import Flask, render_template, redirect, url_for, request

from predictor import WordPredictor
from spell_check import spell_checking

# creating the flask app.
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", todos=result, input_word=word,
                           is_in_dict_flag=is_in_dict_flag,
                           did_u_mean_words=did_u_mean_words)


@app.route("/add",methods = ["POST"])
def addTodo():
    global result, word, is_in_dict_flag, did_u_mean_words
    # kelime
    word = request.form.get("title")
    if not word == "":
        # sonraki kelimeler ve ihtimalleri bir dizi şeklinde elde edilir.
        result = predictor.predict(word, return_flag=True)
        if not result:
            is_in_dict_flag = False
            did_u_mean_words = spell_checking(word, predictor)
        else:
            is_in_dict_flag = True
    else:
        result = []
    return redirect(url_for("index"))


@app.route("/test_add", methods = ["POST"])
def test_button():
    global result, word, is_in_dict_flag
    word = request.form['test_button']
    # sonraki kelimeler ve ihtimalleri bir dizi şeklinde elde edilir.
    result = predictor.predict(word, return_flag=True)
    is_in_dict_flag = True
    return redirect(url_for("index"))


if __name__ == "__main__":

    # these variables should be global.
    result = []
    word = ""
    is_in_dict_flag = True
    did_u_mean_words = []
    predictor = WordPredictor('./corpora/little_prince.txt')

    app.run(debug=True)
