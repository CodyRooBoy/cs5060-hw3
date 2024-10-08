import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

def process_csv(file_path):
    try:
        data = pd.read_csv(file_path, header=None)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return
    
    print(f"Processing {file_path}")

    if data.shape[1] > 0:
        returns = data[0]
    else:
        print(f"No data found in {file_path}.")
        return

    plt.figure(figsize=(10, 6))
    plt.hist(returns, bins=50, density=True, alpha=0.6, color='gray', label='Histogram')

    mu_norm, std_norm = stats.norm.fit(returns)
    x = np.linspace(min(returns), max(returns), 1000)
    plt.plot(x, stats.norm.pdf(x, mu_norm, std_norm), 'r-', lw=2, label='Normal fit')

    shape_log, loc_log, scale_log = stats.lognorm.fit(returns, floc=0)
    plt.plot(x, stats.lognorm.pdf(x, shape_log, loc_log, scale_log), 'g-', lw=2, label='Log-normal fit')

    data_min, data_max = min(returns), max(returns)
    data_scaled = (returns - data_min) / (data_max - data_min)

    data_scaled = data_scaled[(data_scaled > 0) & (data_scaled < 1)]

    if data_scaled.empty:
        print(f"No valid data to fit Beta distribution for {file_path}.")
    else:
        try:
            a_beta, b_beta, loc_beta, scale_beta = stats.beta.fit(data_scaled, floc=0, fscale=1)
            plt.plot(x, stats.beta.pdf((x - data_min) / (data_max - data_min), a_beta, b_beta, loc_beta, scale_beta) / (data_max - data_min), 'b-', lw=2, label='Beta fit')
        except Exception as e:
            print(f"Could not fit beta distribution for {file_path}: {e}")

    plt.title(f'Distribution Fit for {os.path.basename(file_path)}')
    plt.xlabel('Returns')
    plt.ylabel('Density')
    plt.legend()

    output_dir = 'images/'
    os.makedirs(output_dir, exist_ok=True)

    output_filename = os.path.join(output_dir, os.path.basename(file_path).replace('.csv', '_fit.png'))
    plt.savefig(output_filename)
    plt.close()

    print(f"Processed and saved fit for {file_path} as {output_filename}")

    ks_stat_norm, p_value_norm = stats.kstest(returns, 'norm', args=(mu_norm, std_norm))
    print(f'K-S test for Normal: stat={ks_stat_norm}, p-value={p_value_norm}')

    ks_stat_log, p_value_log = stats.kstest(returns, 'lognorm', args=(shape_log, loc_log, scale_log))
    print(f'K-S test for Log-normal: stat={ks_stat_log}, p-value={p_value_log}')

    ks_stat_beta, p_value_beta = stats.kstest(data_scaled, 'beta', args=(a_beta, b_beta, loc_beta, scale_beta))
    print(f'K-S test for Beta: stat={ks_stat_beta}, p-value={p_value_beta}')


csv_dir = 'datasets'
csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

for csv_file in csv_files:
    process_csv(os.path.join(csv_dir, csv_file))
