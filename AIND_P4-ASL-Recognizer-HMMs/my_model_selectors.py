import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences
from collections import defaultdict

class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        N = len(self.lengths)
        best_score = float('inf')
        best_model = None
        for num_states in range(self.min_n_components, self.max_n_components+1):
            model = self.base_model(num_states)
            if model is not None:
                try:
                    logL = model.score(self.X, self.lengths)
                    # there are
                    #       num_state - 1 free-parameters in initial probability
                    #       num_state(num_state - 1) free-parameter in transition-matrix
                    #       2 * num_state * n_features (since we use Gaussian HMM with covariance_type = 'diag'
                    p    = num_states**2 - 1 + 2 * num_states * model.n_features
                    bic  = -2*logL + p * np.log(N)
                    if bic < best_score:
                        best_score = bic
                        best_model = model
                except:
                    if self.verbose:
                        print('failure to score-BIC on {} with {} states'.format(self.this_word, num_states))

        return best_model

class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        M = len(self.words)
        best_score = float('-inf')
        best_model = None
        for num_states in range(self.min_n_components, self.max_n_components+1):
            model = self.base_model(num_states)
            if model is not None:
                try:
                    logL = model.score(self.X, self.lengths)
                    logOther = 0.
                    for w in self.words:
                        if w == self.this_word:
                            continue

                        otherX, otherlengths = self.hwords[w]
                        logOther += model.score(otherX, otherlengths)

                    dic = logL - logOther / (M-1)

                    if dic > best_score:
                        best_score = dic
                        best_model = model
                except:
                    if self.verbose:
                        print('failure to score-DIC on {} with {} states'.format(self.this_word, num_states))

        return best_model

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("error", category=RuntimeWarning)

        # TODO implement model selection using CV
        split_method = KFold(n_splits = min(3, len(self.sequences)))

        best_score = float('-inf')
        best_num_states = None

        for num_states in range(self.min_n_components, self.max_n_components+1):
            try:
                fold_scores = []
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    # modify so that we can call self.base_model (train with fold-in/out)
                    self.X, self.lengths = combine_sequences(cv_train_idx, self.sequences)
                    testX, testLengths = combine_sequences(cv_test_idx, self.sequences)

                    model = self.base_model(num_states)
                    if model is not None:
                        fold_scores.append(model.score(testX, testLengths))
                    else:
                        raise Exception('Failed to fit on {} with {} states and cv_train_idx={}'.format(self.this_word, num_states,
                                                                                                        cv_train_idx))

                cv = np.mean(fold_scores)
                if cv > best_score:
                    best_score = cv
                    best_num_states = num_states
            except:
                if self.verbose:
                    print("failure to score CV on {} with {} states".format(self.this_word, num_states))

        # reset self.X, self.lengths
        self.X, self.lengths = self.hwords[self.this_word]

        # compute best-mean-score
        return self.base_model(best_num_states)
