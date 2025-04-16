import time
from tqdm import tqdm

collatz_lengths_cache = {1: 1}

def get_collatz_sequence_length(n):
    if n <= 0:
        raise ValueError("Input must be a positive integer.")
    if n in collatz_lengths_cache:
        return collatz_lengths_cache[n]
    
    stack = []
    current = n
    while current not in collatz_lengths_cache:
        stack.append(current)
        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1
    
    length = collatz_lengths_cache[current]
    while stack:
        current = stack.pop()
        length += 1
        collatz_lengths_cache[current] = length
    
    return length

def find_longest_collatz_in_range(start, end):
    if start < 1 or end <= start:
        raise ValueError("Start must be >= 1 and end must be greater than start.")
    
    max_len = 0
    start_num = 0

    for i in tqdm(range(start, end), desc=f"Checking {start}-{end}", unit="num"):
        current_len = get_collatz_sequence_length(i)
        if current_len > max_len:
            max_len = current_len
            start_num = i

    return start_num, max_len

if __name__ == "__main__":
    try:
        # Get input from user
        start = int(input("Enter the starting number of the range: "))
        end = int(input("Enter the ending number of the range (exclusive): "))

        print(f"\nCalculating the longest Collatz sequence for numbers between {start} and {end}...")

        start_time = time.time()
        start_num, max_len = find_longest_collatz_in_range(start, end)
        end_time = time.time()
        duration = end_time - start_time

        print("-" * 30)
        print(f"Starting number: {start_num}")
        print(f"Sequence length: {max_len}")
        print(f"Time taken: {duration:.4f} seconds")
        print("-" * 30)

    except ValueError as e:
        print(f"Error: {e}")
