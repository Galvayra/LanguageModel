from .variables import *
import re
import json
from collections import OrderedDict


class MyDataHandler:
    def __init__(self):
        self.__vocab_dict = OrderedDict()
        self.__table = OrderedDict()
        self.__sent_list = list()
        self.__sentence = str()
        self.__is_sent = False

    @property
    def vocab_dict(self):
        return self.__vocab_dict

    @property
    def table(self):
        return self.__table

    @property
    def sent_list(self):
        return self.__sent_list

    @sent_list.setter
    def sent_list(self, sentence):
        self.__sent_list.append(sentence)

    @property
    def sentence(self):
        return self.__sentence

    @sentence.setter
    def sentence(self, sentence):
        self.__sentence = sentence

    @property
    def is_sent(self):
        return self.__is_sent

    @is_sent.setter
    def is_sent(self, is_sent):
        self.__is_sent = is_sent

    @staticmethod
    def __read_corpus():
        try:
            with open(dir_path + corpus_path, 'r') as r_file:
                lines = r_file.readlines()
                return lines
        except FileNotFoundError:
            print("Can not find read file!\n\n")
            return False

    # append sentence in the self.sent_list
    def __append_sent_in_list(self):
        if self.sentence:
            self.sent_list = "<s> " + self.sentence.strip() + " </s>"
        self.sentence = str()

    # set list of sentence in the corpus
    def __set_sentence_list(self):
        lines = self.__read_corpus()
        p = re.compile("[\S]+/[\S]+")

        for line in lines:
            plist = p.findall(line)

            if plist:
                if not self.is_sent:
                    self.__append_sent_in_list()

                self.sentence += ' '.join(plist) + ' '
                self.is_sent = True
            else:
                self.is_sent = False

        # to append last sentence in the list
        self.__append_sent_in_list()

    @staticmethod
    def __get_key(word):
        word = word.split('/')

        if len(word) > 1:
            key = word[0].lower() + "/" + word[1]
        else:
            key = word[0]

        return key

    # initialize vocab using count
    def __init_vocab_dict(self, n_gram):
        for sentence in self.sent_list:
            sentence = sentence.split()
            for i in range(len(sentence) + 1 - n_gram):
                keys = [self.__get_key(sentence[j]) for j in range(i, i + n_gram)]
                key = ' '.join(keys[0:-1])

                # vocab = { key: [ num of key, { given key: num of given key, ... , } ],
                #                   ... ,
                #         }
                if key not in self.vocab_dict:
                    self.vocab_dict[key] = [1, OrderedDict()]
                else:
                    self.vocab_dict[key][0] += 1

    def __extend_vocab_dict(self, n_gram):
        for sentence in self.sent_list:
            sentence = sentence.split()
            for i in range(len(sentence) + 1 - n_gram):
                keys = [self.__get_key(sentence[j]) for j in range(i, i + n_gram)]
                key = ' '.join(keys[0:-1])
                target_key = keys[-1]
                target_dict = self.vocab_dict[key][1]

                if target_key not in target_dict:
                    target_dict[target_key] = 1
                else:
                    target_dict[target_key] += 1

    def __set_probability(self):
        for value in self.vocab_dict.values():
            total = value[0]
            target_dict = value[1]

            for key in target_dict:
                target_dict[key] = target_dict[key] / total

    # set vocab for counting
    def __set_vocab_dict(self, n_gram=SET_N_GRAM):
        self.__init_vocab_dict(n_gram)
        self.__extend_vocab_dict(n_gram)
        self.__set_probability()

    def pre_processing(self):
        self.__set_sentence_list()
        self.__set_vocab_dict()

        # print(len(self.vocab_dict))

    def print_dict(self):
        keys = sorted(self.vocab_dict.keys())

        print("\n===============================\n")
        print("Vocab Size -", len(keys), "\n\n")
        for key in keys:
            print(key.ljust(30), self.vocab_dict[key])

    def dump(self):
        def __sorted(vocab_dict):
            dump_dict = OrderedDict()

            for key in sorted(vocab_dict.keys()):
                dump_dict[key] = vocab_dict[key]

            return dump_dict

        try:
            with open(dir_path + save_path, 'w') as w_file:
                json.dump(__sorted(self.vocab_dict), w_file, indent=4)
                print("\n\nSuccess Save File !! \n")
                print("File name is", "'" + save_path + "'", "in the", "'" + dir_path[:-1] + "'", "directory", "\n\n")
        except FileNotFoundError:
            print("Can not save dump file!\n\n")

    def can_load(self):
        def __load(vocab_dict):
            for k in sorted(vocab_dict.keys()):
                self.vocab_dict[k] = vocab_dict[k]
        try:
            with open(dir_path + save_path, 'r') as r_file:
                __load(json.load(r_file))
                print("\nSuccess loading from", "'" + save_path + "'", "!!\n\n")
                return True
        except FileNotFoundError:
            print("\nCan not find to load file!\n\n")
            return False
