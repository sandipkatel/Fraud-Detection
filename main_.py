"""
    File name: main.py (Modified)
    Author: Updated version with realistic probabilities
"""

import sys
from Factor import Factor, Sign
from Inference import inference


def main() -> None:
    if len(sys.argv) <= 1:
        print('Usage: python main.py [1 or 2 for 2b part 1 and 2 respectively]')
        exit(-1)

    sim_to_run = sys.argv[1]

    # Updated probabilities for more realistic fraud detection scenario
    factors = [
        # P(Trav) - Probability of travel (10% chance of travel)
        Factor(['Trav'], [], [0.10, 0.90]),
        
        # P(Fraud|Trav) - Probability of fraud given travel status
        # Higher fraud risk during travel (2%) vs non-travel (0.5%)
        Factor(['Fraud'], ['Trav'], [0.02, 0.98, 0.005, 0.995]),
        
        # P(OC) - Probability of other suspicious conditions (unusual activity pattern)
        # 5% chance of unusual activity pattern
        Factor(['OC'], [], [0.95, 0.05]),
        
        # P(CRP|OC) - Probability of credit reporting pattern given other conditions
        # Credit reporting pattern more likely (80%) when other conditions are normal,
        # less likely (30%) when other conditions are unusual
        Factor(['CRP'], ['OC'], [0.80, 0.20, 0.30, 0.70]),
        
        # P(FP|Trav,Fraud) - Probability of flagged purchase given travel and fraud
        # Format: [P(FP|+Trav,+Fraud), P(-FP|+Trav,+Fraud), P(FP|+Trav,-Fraud), P(-FP|+Trav,-Fraud),
        #          P(FP|-Trav,+Fraud), P(-FP|-Trav,+Fraud), P(FP|-Trav,-Fraud), P(-FP|-Trav,-Fraud)]
        Factor(['FP'], ['Trav', 'Fraud'], [0.98, 0.02, 0.20, 0.80,
                                          0.95, 0.05, 0.03, 0.97]),
        
        # P(IP|OC,Fraud) - Probability of investigation priority given other conditions and fraud
        # Format: [P(IP|+OC,+Fraud), P(-IP|+OC,+Fraud), P(IP|+OC,-Fraud), P(-IP|+OC,-Fraud),
        #          P(IP|-OC,+Fraud), P(-IP|-OC,+Fraud), P(IP|-OC,-Fraud), P(-IP|-OC,-Fraud)]
        Factor(['IP'], ['OC', 'Fraud'], [0.05, 0.95, 0.01, 0.99,
                                        0.90, 0.10, 0.40, 0.60])]

    if sim_to_run == '1':
        # Computing P(Fraud) by eliminating all other variables
        inference(factors, ['Fraud'], ['Trav', 'FP', 'IP', 'OC', 'CRP'], [])
    elif sim_to_run == '2':
        # Computing P(IP|FP=+, Trav=-, CRP=+) - Investigation priority given evidence
        inference(factors, ['IP'], ['Fraud', 'OC'],
                  [('FP', Sign.POSITIVE), ('Trav', Sign.NEGATIVE), ('CRP', Sign.POSITIVE)])
    elif sim_to_run == '3':
        # New scenario: Computing P(Fraud|FP=+, Trav=+) - Fraud probability given flagged purchase during travel
        inference(factors, ['Fraud'], ['IP', 'OC', 'CRP'],
                  [('FP', Sign.POSITIVE), ('Trav', Sign.POSITIVE)])
    elif sim_to_run == '4':
        # New scenario: Computing P(Fraud|FP=+, OC=+) - Fraud probability given flagged purchase with unusual conditions
        inference(factors, ['Fraud'], ['IP', 'Trav', 'CRP'],
                  [('FP', Sign.POSITIVE), ('OC', Sign.POSITIVE)])


if __name__ == '__main__':
    main()