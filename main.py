"""
    File name: main.py
    Author: Sandip Katel, Sharad Pokharel
"""

import sys

from Factor import Factor, Sign
from Inference import inference


def main() -> None:
    if len(sys.argv) <= 1:
        print('Usage: python main.py [1 or 2 for 2b part 1 and 2 respectively]')
        exit(-1)

    sim_to_run = sys.argv[1]

    factors = [Factor(['Trav'], [], [0.05, 0.95]),
               Factor(['Fraud'], ['Trav'], [0.05, 0.95, 0.01, 0.99]),
               Factor(['OC'], [], [0.9, 0.1]),
               Factor(['CRP'], ['OC'], [0.7, 0.3, 0.2, 0.8]),
               Factor(['FP'], ['Trav', 'Fraud'], [0.95, 0.05, 0.9, 0.1,
                                                  0.1, 0.9, 0.01, 0.99]),
               Factor(['IP'], ['OC', 'Fraud'], [0.1, 0.9, 0.85, 0.15,
                                                0.05, 0.95, 0.6, 0.4])]

    if sim_to_run == '1':
        inference(factors, ['Fraud'], ['Trav', 'FP', 'IP', 'OC', 'CRP'], [])
    else:
        inference(factors, ['IP'], ['Fraud', 'OC'],
                  [('FP', Sign.POSITIVE), ('Trav', Sign.NEGATIVE), ('CRP', Sign.POSITIVE)])


if __name__ == '__main__':
    main()
