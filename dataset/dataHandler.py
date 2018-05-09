from .variables import *
import re
import json
from collections import OrderedDict


class MyDataHandler:
    def __init__(self):
        self.__vocab_dict = OrderedDict()
        self.__sent_list = list()
        self.__sentence = str()
        self.__is_sent = False
        self.__num_sent = 0

    @property
    def vocab_dict(self):
        return self.__vocab_dict

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

    @property
    def num_sent(self):
        return self.__num_sent

    @num_sent.setter
    def num_sent(self, num_sent):
        self.__num_sent = num_sent

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
            self.num_sent += 1
            self.sent_list = self.sentence.strip()
        self.sentence = str()

    # set vocab for counting
    def __set_vocab_dict(self, plist):
        
        # append sentence for one context
        self.sentence += ' '.join(plist) + ' '
        
        for word in plist:
            word = word.split('/')
            key = word[0].lower()
            value = word[1]

            if key not in self.__vocab_dict:
                self.vocab_dict[key] = [value]
            else:
                if value not in self.vocab_dict[key]:
                    self.vocab_dict[key].append(value)

    def __parsing(self, plist):
        if plist:
            if not self.is_sent:
                self.__append_sent_in_list()

            self.__set_vocab_dict(plist)
            self.is_sent = True
        else:
            self.is_sent = False

    def pre_processing(self):
        lines = self.__read_corpus()
        p = re.compile("[\S]+/[\S]+")

        for i, line in enumerate(lines):
            self.__parsing(p.findall(line))

        # to append last sentence in the list
        self.__append_sent_in_list()

        print(len(self.sent_list))
        print(self.sent_list[-1])

    def print_dict(self):
        keys = sorted(self.vocab_dict.keys())

        print("\n===============================\n")
        print("Vocab Size -", len(keys), "\n\n")
        for key in keys:
            print(key.ljust(15), self.vocab_dict[key])

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
