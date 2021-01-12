#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa-durmuss@outlook.com]

import re
from collections import Counter
import string

CORPUS_PATH = "./corpora/little_prince.txt"


class WordPredictor():

    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.process_corpus()

    def process_corpus(self):

        # get corpus and delete newlines.
        with open(self.corpus_path, 'r') as file:
            corpus = file.read().replace('\n', '')

        # noktalama işaretlerini silelim.
        # regex kullanalım. :tada:
        corpus = re.sub(r'[^\w\s]', '', corpus)

        # tüm kelimeleri metinde görünme sayılarıyla beraber tutalım.
        word_list = dict(Counter(corpus.lower().split()))
        self.dict = {}

        this_text = corpus.lower().split()

        for token, value in word_list.items():
            # ilgili kelime için sözlükte yer oluşturalım.
            self.dict[token] = {}
            for idx, word in enumerate(this_text):
                if word == token:
                    try:
                        next_word = this_text[idx + 1]
                    except IndexError as e:
                        continue

                    is_exist = self.dict.get(token).get(next_word)
                    # ilk kez sözlüğe ekleniyorsa değer     None geliyor.
                    # Bu sebeple or kapısı kullanıldı.
                    self.dict[token][next_word] = round(number=(1 / value) + (is_exist or 0),
                                                        ndigits=4)

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


if __name__ == '__main__':

    predictor = WordPredictor(CORPUS_PATH)
    # input from user.
    predictor.predict((input("Enter a word:\n")))
