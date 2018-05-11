from LanguageModel.dataset.dataHandler import MyDataHandler


class SentenceMaker(MyDataHandler):
    def __init__(self):
        super().__init__()
        if not self.can_load():
            exit(-1)
    #
    # @staticmethod
    # def __get_keyword():
    #
    #
    # def __search(self, word):
    #
    #
    # def making(self):
    #     word = input("Input word in dictionary(EXIT) - ")
    #
    #     while word != "EXIT":
    #
    #
    #         word = input("Input word in dictionary(EXIT) - ")
