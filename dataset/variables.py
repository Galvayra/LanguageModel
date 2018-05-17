import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)


def get_arguments():
    parser.add_argument("-ngram", "--ngram", help="set n-gram (default is 2(bi-gram))\n"
                                                  "UseAge : python preprocessing.py -ngram 2\n"
                                                  "UseAge : python main.py -ngram 2\n\n")
    parser.add_argument("-dict", "--dict", help="set dictionary file name\n"
                                                "(default is dict_$ngram)\n")
    _args = parser.parse_args()

    return _args


args = get_arguments()

if not args.ngram:
    N_GRAM = 2
else:
    try:
        N_GRAM = int(args.ngram)
    except ValueError:
        print("\nInput Error type of ngram option!\n")
        exit(-1)
    else:
        if N_GRAM < 2 or N_GRAM > 6:
            print("\nInput Error ngram option! (boundary is 2~5)\n")
            exit(-1)


if not args.dict:
    NAME_SAVE = "dict_" + str(N_GRAM)
else:
    NAME_SAVE = args.dict

PATH_SAVE = "dictionary/"
PATH_CORPUS = "dataset/"
NAME_CORPUS = "WSJ_3005.POS"
END_FLAG = "</s>"
