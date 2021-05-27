#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa-durmuss@outlook.com]


from flask import Flask, render_template, redirect, url_for, request
from collections import Counter, defaultdict
import re


def iterative_levenshtein(s, t, costs=(1, 1, 2)):
    """
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings 
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein 
        distance between the first i characters of s and the 
        first j characters of t

        costs: a tuple or a list with three integers (d, i, s)
               where d defines the costs for a deletion
                     i defines the costs for an insertion and
                     s defines the costs for a substitution
    """

    rows = len(s)+1
    cols = len(t)+1
    deletes, inserts, substitutes = costs

    dist = [[0 for x in range(cols)] for x in range(rows)]

    # source prefixes can be transformed into empty strings
    # by deletions:
    for row in range(1, rows):
        dist[row][0] = row * deletes

    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in range(1, cols):
        dist[0][col] = col * inserts

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row-1][col] + deletes,
                                 dist[row][col-1] + inserts,
                                 dist[row-1][col-1] + cost) # substitution

    # printing env.
    # for r in range(rows):
    #     print(dist[r])


    return dist[row][col]


def spell_checking(inp_word, predictor):

    # getting all the words as list.
    words = list(predictor.dict.keys())

    result_dict = {}
    for idx, word in enumerate(words):
        distance = iterative_levenshtein(inp_word, word)  # mesafeyi bul.
        if distance in [1,2,3]:  # sadece 1-2-3 mesafelerindeki kelimeleri kaydet.
            result_dict.setdefault(str(distance), []).append(idx)  # bir key için birden fazla value eklemek.

    count = 0
    did_u_mean_words = []
    for key, value in sorted(result_dict.items()):
        for idx in value:
            #print(f'\t{words[idx]} -- ({key})')
            count += 1
            did_u_mean_words.append(words[idx])
            if count == 3:
                return did_u_mean_words
                break


class WordPredictor:

    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.dict = defaultdict(dict)
        self.process_corpus()
        self.this_text = []

    def find_indices(self, word):
        """
        Kelimenin kelime listesinde geçtiği tüm indeksleri döndürür.
        :param word: ilgili kelime.
        """
        return [i for i, x in enumerate(self.this_text) if x == word]

    def process_corpus(self):
        # get corpus and delete newlines.
        with open(self.corpus_path, 'r') as file:
            corpus = file.read().replace('\n', ' ')

        # noktalama işaretlerini silelim.
        # regex kullanalım. :tada:
        corpus = re.sub(r'[^\w\s]', '', corpus)

        # tüm kelimeleri metinde görünme sayılarıyla beraber tutalım.
        word_list = dict(Counter(corpus.lower().split()))

        self.this_text = corpus.lower().split()

        for word, value in word_list.items():
            for idx in self.find_indices(word):
                try:
                    next_word = self.this_text[idx + 1]
                    # eğer word'den sonra next_word daha önce geldiyse 1 gelmediyse 0 atar.
                    # doğal halinde NoneType dönüyor, aşağıdaki toplamında hata alınıyor.
                    is_exist = (self.dict.get(word).get(next_word) or 0)
                except AttributeError:
                    is_exist = 0
                except IndexError:  # sonraki index sınırı aşarsa.
                    continue
                self.dict[word][next_word] = round((1 / value) + is_exist, 4)

    def predict(self, input_word, number=5, return_flag=False):
        try:
            input_result = sorted(self.dict[input_word.lower()].items(),
                                  key=lambda k: k[1], reverse=True)
        except KeyError as e:
            # böyle bir kelime sözlükte bulunmadı.
            return False

        if return_flag:
            return input_result[:number]
        else:
            for _, (next_word, value) in zip(range(number), input_result):
                print(f'{input_word} {next_word} : {value}')
                print("-" * 50)


app = Flask(__name__)

result = []
word = ""
is_in_dict_flag = True
did_u_mean_words = []

predictor = WordPredictor('./corpora/little_prince.txt')

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
