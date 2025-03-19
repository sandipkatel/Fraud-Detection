"""
    File name: visualization.py
    Purpose: Visualize the Bayesian Network for fraud detection across different scenarios
"""

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import re
# from Factor import Factor, Sign
# from Inference import inference
import matplotlib.patches as mpatches
import networkx as nx


def run_scenario(scenario_number):
    """Run the inference for a specific scenario and extract the fraud probabilities"""
    # Run the scenario and capture output
    # result = subprocess.run(['python', 'main.py', str(scenario_number)], 
    #                         capture_output=True, text=True)
    result = subprocess.run(['python', 'main.py', str(scenario_number)], 
                            capture_output=True, text=True)
    output = result.stdout
    
    # Extract the final probabilities using regex
    fraud_pattern = r"\+fraud\s+\|\s+(\d+\.\d+)\s+\|"
    no_fraud_pattern = r"\-fraud\s+\|\s+(\d+\.\d+)\s+\|"
    
    fraud_match = re.search(fraud_pattern, output)
    no_fraud_match = re.search(no_fraud_pattern, output)
    
    if fraud_match and no_fraud_match:
        fraud_prob = float(fraud_match.group(1))
        no_fraud_prob = float(no_fraud_match.group(1))
        return fraud_prob, no_fraud_prob, output
    else:
        # If we're looking for IP instead of Fraud
        if scenario_number == "2":
            ip_pattern = r"\+ip\s+\|\s+(\d+\.\d+)\s+\|"
            no_ip_pattern = r"\-ip\s+\|\s+(\d+\.\d+)\s+\|"
            
            ip_match = re.search(ip_pattern, output)
            no_ip_match = re.search(no_ip_pattern, output)
            
            if ip_match and no_ip_match:
                ip_prob = float(ip_match.group(1))
                no_ip_prob = float(no_ip_match.group(1))
                return ip_prob, no_ip_prob, output
        
        return None, None, output


def visualize_fraud_probabilities(scenario_numbers, scenario_descriptions):
    """Create visualizations for fraud probabilities across different scenarios"""
    probabilities = []
    
    # Collect probabilities for each scenario
    for scenario in scenario_numbers:
        if scenario == "2":  # IP scenario
            pos_prob, neg_prob, output = run_scenario(scenario)
            if pos_prob is not None:
                probabilities.append((pos_prob, neg_prob, "IP"))
            else:
                probabilities.append((0, 0, None))
        else:  # Fraud scenarios
            pos_prob, neg_prob, output = run_scenario(scenario)
            if pos_prob is not None:
                probabilities.append((pos_prob, neg_prob, "Fraud"))
            else:
                probabilities.append((0, 0, None))
    
    # Create the bar chart
    plt.figure(figsize=(14, 10))
    
    # Set up bars
    bar_width = 0.35
    x_pos = np.arange(len(scenario_descriptions))
    
    # Plot bars for positive probabilities (fraud/IP)
    pos_probs = [p[0] for p in probabilities]
    bars1 = plt.bar(x_pos - bar_width/2, pos_probs, bar_width, 
                    color='crimson', label='Positive')
    
    # Plot bars for negative probabilities (not fraud/not IP)
    neg_probs = [p[1] for p in probabilities]
    bars2 = plt.bar(x_pos + bar_width/2, neg_probs, bar_width, 
                    color='royalblue', label='Negative')
    
    # Add percentage labels on top of bars
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # Only add labels to bars with non-zero height
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{height:.2%}', ha='center', va='bottom')
    
    add_labels(bars1)
    add_labels(bars2)
    
    # Add threshold line at 5%
    plt.axhline(y=0.05, color='orange', linestyle='--', label='Fraud Threshold (5%)')
    
    # Create custom legends
    fraud_patch = mpatches.Patch(color='crimson', label='Fraud/Positive')
    no_fraud_patch = mpatches.Patch(color='royalblue', label='No Fraud/Negative')
    threshold_line = plt.Line2D([0], [0], color='orange', linestyle='--', label='Fraud Threshold (5%)')
    
    # Configure the chart
    plt.xlabel('Scenarios')
    plt.ylabel('Probability')
    plt.title('Bayesian Network Fraud Detection Probabilities')
    plt.xticks(x_pos, scenario_descriptions, rotation=15, ha='right')
    plt.legend(handles=[fraud_patch, no_fraud_patch, threshold_line], loc='upper right')
    plt.ylim(0, 1.1) 
    plt.tight_layout()
    
    for i, scenario in enumerate(scenario_numbers):
        if probabilities[i][2] is not None: 
            create_detailed_chart(i+1, scenario_descriptions[i], probabilities[i], scenario)
    
    plt.show()


def create_detailed_chart(scenario_num, scenario_desc, probabilities, scenario_code):
    """Create a detailed chart for a specific scenario"""
    pos_prob, neg_prob, var_type = probabilities
    
    plt.figure(figsize=(8, 6))
    
    # Create pie chart
    labels = [f'+{var_type.lower()} ({pos_prob:.2%})', f'-{var_type.lower()} ({neg_prob:.2%})']
    sizes = [pos_prob, neg_prob]
    colors = ['crimson', 'royalblue']
    explode = (0.1, 0)  # explode the first slice
    
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title(f'Scenario {scenario_num}: {scenario_desc}')
    
    # Add threshold indicator if it's a Fraud scenario
    if var_type == "Fraud":
        threshold = 0.05
        if pos_prob > threshold:
            status = "ALERT: Fraud Detected"
            color = 'red'
        else:
            status = "SAFE: No Fraud Detected"
            color = 'green'
        
        plt.figtext(0.5, 0.01, status, wrap=True, horizontalalignment='center', 
                   fontsize=14, bbox=dict(facecolor=color, alpha=0.5))


def main():
    # Define scenarios
    scenario_numbers = ["1", "2", "3", "4"]
    scenario_descriptions = [
        "P(Fraud) - Base fraud probability",
        "P(IP|FP=+, Trav=-, CRP=+) - Investigation priority given evidence",
        "P(Fraud|FP=+, Trav=+) - Fraud probability during travel with flagged purchase",
        "P(Fraud|FP=+, OC=+) - Fraud probability with flagged purchase & unusual conditions"
    ]
    
    # Create visualizations
    visualize_fraud_probabilities(scenario_numbers, scenario_descriptions)


if __name__ == "__main__":
    main()