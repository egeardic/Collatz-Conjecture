#!/usr/bin/env python3

import sys
import time
import os
import pickle
from typing import Dict, Tuple
from array import array
from tqdm import tqdm

# File to store memoization dictionary
MEMO_FILE = "collatz_memo.pkl"

def load_memo() -> Dict[int, int]:
    """Load memoization dictionary from file if it exists."""
    if os.path.exists(MEMO_FILE):
        try:
            with open(MEMO_FILE, 'rb') as f:
                memo = pickle.load(f)
            print(f"Loaded {len(memo)} pre-calculated results from storage.")
            return memo
        except Exception as e:
            print(f"Error loading memoization data: {e}")
            return {}
    return {}

def save_memo(memo: Dict[int, int]) -> None:
    """Save memoization dictionary to file."""
    try:
        with open(MEMO_FILE, 'wb') as f:
            pickle.dump(memo, f)
        print(f"Saved {len(memo)} calculated results to storage for future use.")
    except Exception as e:
        print(f"Error saving memoization data: {e}")

def collatz_steps(n: int, memo: Dict[int, int]) -> int:
    """
    Calculate the number of steps to reach 1 in the Collatz sequence for number n.
    Uses memoization to avoid recalculating sequences.
    """
    # Return from memo if already calculated
    if n in memo:
        return memo[n]
    
    # Base case
    if n == 1:
        return 0
    
    # Use bitwise operations for odd/even check and calculations
    if n & 1 == 0:  # Even number
        steps = 1 + collatz_steps(n >> 1, memo)  # n/2 using right shift
    else:  # Odd number
        # For very large numbers, use intermediate calculation to avoid overflow
        next_n = ((n << 1) + n + 1)  # 3n+1 using left shift
        steps = 1 + collatz_steps(next_n, memo)
    
    # Store result in memo
    memo[n] = steps
    return steps

def find_max_steps_in_range(start: int, end: int, memo: Dict[int, int]) -> Tuple[int, int, int, int]:
    """
    Find the number with the maximum number of steps in the Collatz sequence
    within the given range. Shows progress with tqdm.
    Returns max_num, max_steps, new_calculations, total_cached
    """
    max_steps = 0
    max_num = start
    initial_memo_size = len(memo)
    
    # Use tqdm for progress bar
    for n in tqdm(range(start, end + 1), desc="Calculating", unit="numbers"):
        steps = collatz_steps(n, memo)
        if steps > max_steps:
            max_steps = steps
            max_num = n
    
    new_calculations = len(memo) - initial_memo_size
    return max_num, max_steps, new_calculations, len(memo)

def get_collatz_sequence(n: int) -> list:
    """Generate the full Collatz sequence for a number."""
    sequence = [n]
    while n != 1:
        if n & 1 == 0:
            n = n >> 1
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

def format_time(seconds: float) -> str:
    """Format time in a human-readable way."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes} minutes and {secs} seconds"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours} hours, {minutes} minutes and {secs} seconds"

def main():
    try:
        print("Collatz Conjecture - Maximum Steps Calculator")
        print("--------------------------------------------")
        
        # Load existing memoization data
        memo = load_memo()
        
        start = int(input("Enter the starting number: "))
        end = int(input("Enter the ending number: "))
        
        if start <= 0 or end <= 0:
            print("Please enter positive integers only.")
            return
        
        if start > end:
            print("Starting number must be less than or equal to ending number.")
            return
        
        # Start timing
        start_time = time.time()
        
        # Run calculation with progress bar
        max_num, max_steps, new_calculations, total_cached = find_max_steps_in_range(start, end, memo)
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        time_str = format_time(elapsed_time)
        
        print(f"\nResults:")
        print(f"The number with the maximum steps is: {max_num}")
        print(f"Number of steps: {max_steps}")
        print(f"Calculation completed in: {time_str}")
        print(f"New calculations: {new_calculations}")
        print(f"Total cached results: {total_cached}")
        
        # Ask if user wants to save the updated memoization data
        save_option = input("\nWould you like to save calculated results for future use? (y/n): ")
        if save_option.lower() == 'y':
            save_memo(memo)
        
        # Show the sequence for the max number
        show_sequence = input("\nWould you like to see the sequence for the maximum steps number? (y/n): ")
        if show_sequence.lower() == 'y':
            sequence = get_collatz_sequence(max_num)
            
            # Format sequence nicely
            if len(sequence) > 20:
                print(f"Sequence for {max_num} (showing first 10 and last 10 elements, {len(sequence)} total):")
                sequence_str = " → ".join(map(str, sequence[:10]))
                sequence_str += " → ... → "
                sequence_str += " → ".join(map(str, sequence[-10:]))
                print(sequence_str)
            else:
                print(f"Sequence for {max_num}:")
                print(" → ".join(map(str, sequence)))
        
        # Save detailed results for large calculations if needed
        save_results = input("\nWould you like to save detailed results to a file? (y/n): ")
        if save_results.lower() == 'y':
            filename = f"collatz_results_{start}_to_{end}.txt"
            with open(filename, 'w') as f:
                f.write(f"Collatz Conjecture Results for range {start} to {end}\n")
                f.write(f"The number with the maximum steps is: {max_num}\n")
                f.write(f"Number of steps: {max_steps}\n")
                f.write(f"Calculation completed in: {time_str}\n")
                f.write(f"New calculations: {new_calculations}\n")
                f.write(f"Total cached results: {total_cached}\n")
                
                # Save sequence for the maximum steps number
                f.write(f"\nSequence for {max_num}:\n")
                sequence = get_collatz_sequence(max_num)
                f.write(" → ".join(map(str, sequence)))
                
                # Optionally save full data for numbers in range
                save_all = input("Would you like to include results for all numbers in the range? (y/n): ")
                if save_all.lower() == 'y':
                    f.write(f"\n\nDetailed results for all numbers in range:\n")
                    for i in range(start, end + 1):
                        if i in memo:
                            f.write(f"{i}: {memo[i]} steps\n")
            
            print(f"Results saved to {filename}")
    
    except ValueError:
        print("Please enter valid integers.")
    except KeyboardInterrupt:
        print("\nCalculation interrupted.")
        # Save memo on interrupt
        save_on_exit = input("Would you like to save calculated results before exiting? (y/n): ")
        if save_on_exit.lower() == 'y':
            save_memo(memo)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()