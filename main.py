import sys
from os import path

try:
    import LanguageModel
except ImportError:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from LanguageModel.maker import SentenceMaker

if __name__ == '__main__':
    sentence_maker = SentenceMaker()
    sentence_maker.making()
