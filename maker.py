from LanguageModel.dataset.dataHandler import MyDataHandler
import random

START_FLAG = "<s> "


class SentenceMaker(MyDataHandler):
    def __init__(self):
        super().__init__()
        if not self.can_load():
            exit(-1)

    def __get_prob_dict(self, word):
        key = self.get_key(word, tagging=False)

        if key in self.vocab_dict:
            return self.vocab_dict[key][1]
        else:
            return dict()

    def __sentence_maker(self):
        prob_dict = self.__get_prob_dict(self.get_key_from_sent())

        if not prob_dict:
            self.init_sentence()
            return

        max_key_list = list()
        max_value = float()

        for k, v in prob_dict.items():
            if v > max_value:
                max_value = v
                max_key_list = [k]
            elif v == max_value:
                max_key_list.append(k)

        # get arg max from key list
        max_key = self.get_key(random.choice(max_key_list), tagging=False)

        # if max key is "</s>"
        if max_key == self.end_flag:
            return

        self.sentence += max_key + " "
        self.__sentence_maker()

    def making(self):
        word = input("\nInput word in dictionary(EXIT) - ")

        while word != "EXIT":
            self.init_sentence(START_FLAG + word + " ")
            self.__sentence_maker()

            if self.sentence:
                print(self.sentence[len(START_FLAG):])
            else:
                print("\nThere is no key in dict!\n")

            word = input("\n\nInput word in dictionary(EXIT) - ")
