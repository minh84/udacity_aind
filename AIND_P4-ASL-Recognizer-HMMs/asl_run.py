import argparse
import numpy as np
import time
from asl_data import AslDb
from asl_utils import compute_errors, show_errors

from my_model_selectors import SelectorBIC, SelectorDIC, SelectorCV
from my_recognizer import recognize

def build_asl_db():
    asl = AslDb()

    # ground features
    asl.df['grnd-ry'] = asl.df['right-y'] - asl.df['nose-y']
    asl.df['grnd-rx'] = asl.df['right-x'] - asl.df['nose-x']
    asl.df['grnd-ly'] = asl.df['left-y'] - asl.df['nose-y']
    asl.df['grnd-lx'] = asl.df['left-x'] - asl.df['nose-x']

    # polar features
    asl.df['polar-rr'] = np.sqrt(asl.df['grnd-rx'] ** 2 + asl.df['grnd-ry'] ** 2)
    asl.df['polar-rtheta'] = np.arctan2(asl.df['grnd-rx'], asl.df['grnd-ry'])
    asl.df['polar-lr'] = np.sqrt(asl.df['grnd-lx'] ** 2 + asl.df['grnd-ly'] ** 2)
    asl.df['polar-ltheta'] = np.arctan2(asl.df['grnd-lx'], asl.df['grnd-ly'])

    # compute mean/std
    df_means = asl.df.groupby('speaker').mean()
    df_stds  = asl.df.groupby('speaker').std()

    # normalized features
    refs = ['right-x', 'right-y', 'left-x', 'left-y']
    features_norm = ['norm-rx', 'norm-ry', 'norm-lx', 'norm-ly']
    for ref, feat in zip(refs, features_norm):
        asl.df[feat] = (asl.df[ref] - asl.df['speaker'].map(df_means[ref])) / asl.df['speaker'].map(df_stds[ref])

    refs = ['grnd-rx', 'grnd-ry', 'grnd-lx', 'grnd-ly']
    features_norm = ['norm-grx', 'norm-gry', 'norm-glx', 'norm-gly']
    for ref, feat in zip(refs, features_norm):
        asl.df[feat] = (asl.df[ref] - asl.df['speaker'].map(df_means[ref])) / asl.df['speaker'].map(df_stds[ref])

    refs = ['polar-rr', 'polar-lr']
    polars_norm = ['norm-prr', 'norm-plr']
    for ref, feat in zip(refs, polars_norm):
        asl.df[feat] = (asl.df[ref] - asl.df['speaker'].map(df_means[ref])) / asl.df['speaker'].map(df_stds[ref])

    return asl

def train_all_words(asl_db, features, model_selector):
    training  = asl_db.build_training(features)  # Experiment here with different feature sets defined in part 1
    sequences = training.get_all_sequences()
    Xlengths  = training.get_all_Xlengths()
    model_dict = {}
    for word in training.words:
        model = model_selector(sequences, Xlengths, word,
                        n_constant=3).select()
        model_dict[word]=model
    return model_dict

if __name__=='__main__':
    feature_ground       = ['grnd-rx','grnd-ry','grnd-lx','grnd-ly']
    features_norm        = ['norm-rx', 'norm-ry', 'norm-lx', 'norm-ly']
    features_ground_norm = ['norm-grx', 'norm-gry', 'norm-glx', 'norm-gly']
    features_polar       = ['polar-rr', 'polar-rtheta',      'polar-lr', 'polar-ltheta']
    features_polar_norm  = ['norm-prr', 'polar-rtheta', 'norm-plr', 'polar-ltheta']
    features_delta       = ['delta-rx', 'delta-ry', 'delta-lx', 'delta-ly']

    feat_dict = {'ground'       : feature_ground,
                 'norm'         : features_norm,
                 'ground_norm'  : features_ground_norm,
                 'polar'        : features_polar,
                 'polar_norm'   : features_polar_norm,
                 'delta'        : features_delta}

    selector_dict = {'CV'  : SelectorCV,
                     'BIC' : SelectorBIC,
                     'DIC' : SelectorDIC}

    parser = argparse.ArgumentParser()
    parser.add_argument('--features', action='store', type=str,
                        choices=['ground', 'norm', 'ground_norm', 'polar', 'polar_norm', 'delta'],
                        help='type of feature to be used')
    parser.add_argument('--selector', action='store', type=str,
                        choices=['CV', 'BIC', 'DIC'],
                        help = 'type of selector to be used')

    parser.add_argument('--run_all', action='store_true',
                        help='flag to run all features/selectors')

    parser.add_argument('--verbose', action='store_true',
                        help='flag to turn on verbose mode')

    args = parser.parse_args()

    ts = time.time()
    asl_db = build_asl_db()
    te = time.time()
    print('Loading data took {:.2f}s'.format(te - ts))

    if args.run_all:
        wer_results = {}
        training_time = {}
        feats =['ground_norm']
        selectors = ['CV', 'BIC', 'DIC']
        for feat in feats:
            test_set = asl_db.build_test(feat_dict[feat])

            for selector in selectors:
                ts = time.time()
                models = train_all_words(asl_db,
                                         feat_dict[feat],
                                         selector_dict[selector])
                te = time.time()

                probabilities, guesses = recognize(models, test_set)
                wer = compute_errors(guesses, test_set)

                wer_results[(feat, selector)] = wer
                training_time[(feat, selector)] = ts - te

                print('Training with feature {:12s} and Selector {:3s} took {:.2f}s, WER={:.4f}'.format('\'{}\''.format(feat), selector,
                                                                                                         te - ts, wer))

        print('Summary\n---------------------------------------\n\n')
        print('|             | {} |'.format(' | '.join(['{:6s}'.format(s) for s in selectors])))
        print('|------------:|{}|'.format('|'.join([':------:'] * len(selector_dict))))
        for feat in feats:
            row = [' {:11s} '.format(feat)]
            for selector in selectors :
                row.append(' {:.4f} '.format(wer_results[(feat, selector)]))
            print('|{}|'.format('|'.join(row)))
    else:
        ts = time.time()
        models = train_all_words(asl_db,
                                 feat_dict[args.features],
                                 selector_dict[args.selector])
        te = time.time()
        print('Training with feature \'{}\' and Selector \'{}\' took {:.2f}s'.format(args.features, args.selector, te - ts))
        print('Number of word-models returned = {}'.format(len(models)))

        ts = time.time()
        test_set = asl_db.build_test(feat_dict[args.features])
        probabilities, guesses = recognize(models, test_set)
        te = time.time()
        print('Testing took {:.2f}s'.format(te - ts))
        if args.verbose:
            show_errors(guesses, test_set)
        else:
            print('**** WER = {:.4f}'.format(compute_errors(guesses, test_set)))