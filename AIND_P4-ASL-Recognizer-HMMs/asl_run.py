import argparse
from asl_data import AslDb
from asl_utils import compute_errors

from my_model_selectors import SelectorBIC, SelectorDIC, SelectorCV
from my_recognizer import recognize

if __name__=='__main__':
    pass