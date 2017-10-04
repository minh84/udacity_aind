import argparse
import numpy as np

from asl_data import AslDb
from asl_utils import compute_errors

from my_model_selectors import SelectorBIC, SelectorDIC, SelectorCV
from my_recognizer import recognize

def build_features():
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

if __name__=='__main__':
    feature_ground = ['grnd-rx','grnd-ry','grnd-lx','grnd-ly']
    features_norm  = ['norm-rx', 'norm-ry', 'norm-lx', 'norm-ly']
    features_ground_norm = ['norm-grx', 'norm-gry', 'norm-glx', 'norm-gly']
    features_delta = ['delta-rx', 'delta-ry', 'delta-lx', 'delta-ly']
    features_polar = ['polar-rr', 'polar-rtheta',      'polar-lr', 'polar-ltheta']
    features_polar_norm = ['norm-prr', 'polar-rtheta', 'norm-plr', 'polar-ltheta']