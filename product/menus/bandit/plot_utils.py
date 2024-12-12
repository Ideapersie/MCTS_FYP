import matplotlib.pyplot as plt
import numpy as np


def plot_simulation_results(all_rewards, all_counts, all_means, algorithm_name):
    """
    Plots the results of a bandit algorithm simulation over multiple runs.

    Parameters:
    - all_rewards: total rewards per arm from multiple simulations
    - all_counts: total counts of arm pulls from multiple simulations
    - all-means: mean of the estimated probability of each arm 
    - algorithm_name: Name of the algorithm for labeling the graphs
    """
    # Calculate averages
    avg_rewards = np.mean(all_rewards, axis=0)  # Average total rewards per arm
    avg_counts = np.mean(all_counts, axis=0)    # Average pull count for each arm
    avg_means = np.mean(all_means, axis=0) # Average probability per arm
    
    total_rewards = np.sum(all_rewards)

    # Plotting, 3 graphs 
    plt.figure(figsize=(18, 6))

    # Plot 1: Average Total Rewards Per Arm
    arms = [f"{i}" for i in range(all_rewards.shape[1])]
    plt.subplot(1, 3, 1)
    plt.bar(arms, avg_rewards, color='mediumseagreen')
    plt.title(f"Average Total Rewards Per Arm ({algorithm_name})")
    
    # Axis labels 
    plt.xlabel("Arm Number", fontsize=12)
    plt.ylabel("Average Total Rewards", fontsize=12)
    
    # Adjust x-axis to show every 10th arm
    plt.xticks(ticks=np.arange(0, len(arms), 10), fontsize=10)
    plt.xlim(0, len(arms) - 0.5)


    # Plot 2: Average Total Pulls Per Arm
    plt.subplot(1, 3, 2)
    plt.bar(arms, avg_counts, color='cornflowerblue')
    plt.title(f"Average Pull Count Per Arm ({algorithm_name})")
    
    # Axis labels 
    plt.xlabel("Arm Number", fontsize=12)
    plt.ylabel("Average Pull Count", fontsize=12)
    plt.annotate(f"Total Rewards: {total_rewards:.0f}", 
                 xy=(0.5, 1.15), xycoords='axes fraction', ha='center', fontsize=20, color='darkblue')
    
    # Adjust x-axis to show every 10th arm
    plt.xticks(ticks=np.arange(0, len(arms), 10), fontsize=10)
    plt.xlim(0, len(arms) - 0.5)
    
    # Plot 3: Estimated Probability Mean Per Arm
    plt.subplot(1, 3, 3)
    bars = plt.bar(arms, avg_means, color='goldenrod')
    plt.title(f"Estimated Mean Values Per Arm ({algorithm_name})")
    
    # Axis labels 
    plt.xlabel("Arm Number", fontsize=12)
    plt.ylabel("Average Estimated Mean", fontsize=12)
    
    # Adjust x-axis to show every 10th arm
    plt.xticks(ticks=np.arange(0, len(arms), 10), fontsize=10)
    plt.xlim(0, len(arms) - 0.5)
    # set y limits and ticks to show difference in probability
    plt.ylim(0, 1)
    plt.yticks(np.arange(0,1.1,0.2))
    # Use grid to be able to compare estimated value with real probability value of each arm 
    plt.grid(color='darkgrey', linewidth=0.85)
    # Final Layout
    plt.tight_layout()
    plt.show()
