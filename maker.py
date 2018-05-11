from LanguageModel.dataset.dataHandler import MyDataHandler


class SentenceMaker(MyDataHandler):
    def __init__(self):
        super().__init__()
        if not self.can_load():
            exit(-1)

    def __get_key(self, word):
        key = self.get_key(word, tagging=False)

        if key in self.vocab_dict:
            return self.vocab_dict[key]
        else:
            return False

    def making(self):
        word = input("Input word in dictionary(EXIT) - ")

        while word != "EXIT":
            key = self.__get_key(word)
            print(key)

            word = input("Input word in dictionary(EXIT) - ")
