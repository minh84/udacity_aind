#!/bin/bash
set -e

PROBLEM=$1

# bfs
python run_search.py -p $PROBLEM -s 1  | head -n 7
python run_search.py -p $PROBLEM -s 3  | head -n 7
python run_search.py -p $PROBLEM -s 5  | head -n 7
python run_search.py -p $PROBLEM -s 7  | head -n 7
python run_search.py -p $PROBLEM -s 9  | head -n 7
python run_search.py -p $PROBLEM -s 10 | head -n 7

