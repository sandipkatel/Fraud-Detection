# FRAUD DETECTION SYSTEM USING BAYESIAN NETWORKS
This repository contains a probabilistic fraud detection system using Bayesian networks. The system calculates fraud probabilities based on various transaction factors and provides a tiered risk assessment framework for financial institutions.


## Project Highlights
- Implementation of a Bayesian network for credit card fraud detection
- Probabilistic inference using variable elimination algorithm
- Conditional probability analysis across multiple fraud scenarios
- Risk visualization through radar charts
- Tiered risk assessment framework for operational implementation

## The Baysesian Network

![bayes-net](./Bayseian_Network.png?raw=true)

## Implementation
1. Evidence application to relevant factors
2. Variable elimination to handle hidden variables
3. Normalization to obtain valid probability distributions

## Requirements

```
Python 3.7+
NumPy
Pandas
Matplotlib
NetworkX 
``` 

## Running Instructions

- To run first install the ![requirements.txt](./requirements.txt?raw=True) file
- Run `python visualize.py`.


### Citation
If you use this code in your research, please cite:
```
@article{bayesian_fraud_detection,
  title={Fraud Detection System Using Bayseing Networks},
  author={S. Katel and S. Pokharel},
  year={2025}
}
```