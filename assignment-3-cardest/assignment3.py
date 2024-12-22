import random
import os
import time
import numpy as np
from prettytable import PrettyTable, NONE
import randomhash
import matplotlib.pyplot as plt

# Constants for predefined alpha values in HyperLogLog
alpha_values = {16: 0.673, 32: 0.697, 64: 0.709}
n_bits = 32  # Bits for HyperLogLog

def get_alpha(m):
    """Return the alpha value for HyperLogLog based on the value of m."""
    return alpha_values.get(m, 0.7213 / (1 + 1.079 / m))

def print_progress_bar(title, iteration, total, bar_length=40):
    """Display a textual progress bar for the task."""
    percent = (iteration / total) * 100
    filled_length = int(bar_length * iteration // total)
    bar = '#' * filled_length + '.' * (bar_length - filled_length)
    
    # Print the progress bar with a carriage return to overwrite the line
    print(f'\r{title}: [{bar}] {percent:.0f}%', end='', flush=True)

    # Clear line at 100%
    if iteration == total:
        print(f'\r{" " * (len(title) + bar_length + 10)}', end='', flush=True)
        print(f'{title} completed!')

def hyperLogLog(Z, b):
    """HyperLogLog cardinality estimation algorithm."""
    m = 2**b
    M = [0] * m
    alpha = get_alpha(m)

    for z in Z:
        bin_z = bin(z)[2:].zfill(n_bits)
        j = int(bin_z[:b], 2)  # first log_m bits of x in binary
        w = int(bin_z[b:], 2)  # remaining bits of x in binary
        M[j] = max(M[j], n_bits - b - w.bit_length() + 1)

    return alpha * m**2 * 1 / sum([1 / (2**Mi) for Mi in M])

def recordinality(Z, k):
    """Recordinality estimation algorithm."""
    R = k
    S = []
    for z in Z:
        if len(S) < k:
            S.append(z)
        else:
            z_min = min(S)
            if z > z_min and z not in S:
                z_min = min(S)
                R += 1
                S.remove(z_min)
                S.append(z)
    return k * (1 + 1 / k)**(R - k + 1) - 1

def process_estimation(Z, real_cardinality, iters, table_rows=8):
    """Process the estimation for Recordinality and HyperLogLog."""
    h = randomhash.RandomHashFamily(count=iters)
    Z = np.transpose(np.array([h.hashes(z) for z in Z]))

    # Create a PrettyTable object for the current dataset
    table = PrettyTable()
    table.header = False
    table.vrules = NONE
    table.padding_width = 3

    print(f"\nDataset containing n = {real_cardinality} distinct words")

    start_time = time.time()

    for u in range(2, 2 + table_rows):  # k = 2, 4, ..., 512
        k = 2**u
        cumulative_recordinality = 0
        cumulative_recordinality_error = 0
        cumulative_hyperloglog = 0
        cumulative_hyperloglog_error = 0

        for i in range(iters):
            recordinality_result = recordinality(Z[i], k)
            recordinality_error = abs(recordinality_result - real_cardinality) / real_cardinality
            cumulative_recordinality += recordinality_result
            cumulative_recordinality_error += recordinality_error

            hyperloglog_result = hyperLogLog(Z[i], u)
            hyperloglog_error = abs(hyperloglog_result - real_cardinality) / real_cardinality
            cumulative_hyperloglog += hyperloglog_result
            cumulative_hyperloglog_error += hyperloglog_error

            print_progress_bar('Progress', (u - 2)*iters + i + 1, table_rows*iters)

        recordinality_estimate = cumulative_recordinality / iters
        recordinality_error = cumulative_recordinality_error / iters
        hyperloglog_estimate = cumulative_hyperloglog / iters
        hyperloglog_error = cumulative_hyperloglog_error / iters

        # Add row to the table
        table.add_row([k, f"{round(recordinality_estimate)}", f"{round(recordinality_error, 2)}",
                       f"{round(hyperloglog_estimate)}", f"{round(hyperloglog_error, 2)}"])

    end_time = time.time()
    print(f'Time taken: {end_time - start_time:.2f} seconds')

    # Print the comparison table for this dataset
    print("\n-------------------------------------------------------")
    print("     k      -- RECORDINALITY --    -- HYPERLOGLOG --   ")
    print("              Avg.       Error      Avg.       Error   ")
    print(table)
    print()

def make_comparison_table(txt_file, dat_file, iters=1000):
    """Generate comparison table between Recordinality and HyperLogLog."""
    with open(txt_file, 'r') as file:
        Z = file.readlines()

    with open(dat_file, 'r') as file:
        real_cardinality = len(file.readlines())

    # Call the abstracted process_estimation function
    process_estimation(Z, real_cardinality, iters)

def zipf_sample(n, alpha):
    """Generate a single Zipf-distributed sample."""
    c_n = 1 / sum(1 / (k ** alpha) for k in range(1, n + 1))
    r = random.uniform(0, 1)
    cumulative_probability = 0
    for i in range(1, n + 1):
        p_i = c_n / (i ** alpha)
        cumulative_probability += p_i
        if r < cumulative_probability:
            return i
    return -1

def generate_zipf_sequence(n, alpha, N):
    """Generate a Zipf-distributed sequence of samples."""
    Z = [i for i in range(1, n + 1)]
    Z.extend([zipf_sample(n, alpha) for _ in range(N - n)])
    return Z

def process_synthetic_data(n, alpha, N, iters=1000):
    """Process synthetic Zipf-distributed dataset."""
    Z = generate_zipf_sequence(n, alpha, N)
    
    Z = [str(z) for z in Z]

    # Call the abstracted process_estimation function
    process_estimation(Z, n, iters)

def main():
    """Main entry point for the script."""
    # You can modify these file paths based on your dataset
    txt_file = './datasets/crusoe.txt'
    dat_file = './datasets/crusoe.dat'

    # Handle actual files
    if os.path.exists(txt_file) and os.path.exists(dat_file):
        make_comparison_table(txt_file, dat_file, 100)

    # Handle synthetic data
    n = 10000
    alpha = 1.5
    N = 100000
    process_synthetic_data(n, alpha, N, 1000)

if __name__ == "__main__":
    main()
