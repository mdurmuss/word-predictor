#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa-durmuss@outlook.com]

import re
from collections import Counter, defaultdict

CORPUS_PATH = "./corpora/little_prince.txt"


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
            corpus = file.read().replace('\n', '')

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


if __name__ == '__main__':

    predictor = WordPredictor(CORPUS_PATH)
    # input from user.
    predictor.predict((input("Enter a word:\n")))
