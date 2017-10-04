import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    # return probabilities, guesses
    for word_id in test_set.get_all_Xlengths():
        X, lengths = test_set.get_item_Xlengths(word_id)
        best_score = float('-inf')
        best_guess = None
        word_scores = {}
        for w, model in models.items():
            try:
                score = model.score(X, lengths)
                word_scores[w] = score

                if score > best_score:
                    best_score = score
                    best_guess = w
            except:
                continue

        probabilities.append(word_scores)
        guesses.append(best_guess)

    return probabilities, guesses