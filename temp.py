import numpy as np
import pandas as pd

# Define probabilities from the Bayesian Network
P_T = [0.05, 0.95]  # P(Travel)
P_F_given_T = [[0.05, 0.95], [0.01, 0.99]]  # P(Fraudulent Transaction | Travel)
P_Fp_given_T_F = [[0.95, 0.05], [0.9, 0.1], [0.1, 0.9], [0.01, 0.99]]  # P(Fraudulent Purchase)
P_Oc = [0.9, 0.1]   # P(Owns Credit Card)
P_Crp_given_Oc = [[0.7, 0.3], [0.2, 0.8]]   # P(Credit Card Report)
P_Ip_given_Oc_F = [[0.1, 0.9], [0.85, 0.15], [0.05, 0.95], [0.6, 0.4]] # P(Identity Proofing)

# Number of samples
n_samples = 10000

# Initialize dataset
data = []

for _ in range(n_samples):
    # Sample Travel (T)
    T = np.random.choice([1, 0], p=P_T)
    
    # Sample Fraudulent Transaction (F) given T
    F = np.random.choice([1, 0], p=P_F_given_T[T])
    
    # Sample Fraudulent Purchase (Fp) given T and F
    Fp_idx = T * 2 + F
    Fp = np.random.choice([1, 0], p=P_Fp_given_T_F[Fp_idx])
    
    # Sample Owns Credit Card (Oc)
    Oc = np.random.choice([1, 0], p=P_Oc)
    
    # Sample Credit Card Report (Crp) given Oc
    Crp = np.random.choice([1, 0], p=P_Crp_given_Oc[Oc])
    
    # Sample Identity Proofing (Ip) given Oc and F
    Ip_idx = Oc * 2 + F
    Ip = np.random.choice([1, 0], p=P_Ip_given_Oc_F[Ip_idx])
    
    # Add row to dataset
    data.append([T, F, Fp, Oc, Crp, Ip])

# Convert to DataFrame for easier manipulation and analysis
columns = ['T', 'F', 'Fp', 'Oc', 'Crp', 'Ip']
df = pd.DataFrame(data, columns=columns)

# Save dataset to CSV
df.to_csv('bayesian_network_dataset.csv', index=False)

print(df.head())
