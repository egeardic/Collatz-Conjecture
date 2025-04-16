#!/usr/bin/env python3

import sys
import time
from typing import Dict, Tuple
from array import array
from tqdm import tqdm

def collatz_steps(n: int, memo: Dict[int, int] = None) -> int:
    """
    Calculate the number of steps to reach 1 in the Collatz sequence for number n.
    Uses memoization to avoid recalculating sequences.
    """
    if memo is None:
        memo = {}
    
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

def find_max_steps_in_range(start: int, end: int) -> Tuple[int, int, Dict[int, int]]:
    """
    Find the number with the maximum number of steps in the Collatz sequence
    within the given range. Shows progress with tqdm.
    """
    max_steps = 0
    max_num = start
    memo = {}  # Memoization dictionary to avoid recalculations
    
    # Use tqdm for progress bar
    for n in tqdm(range(start, end + 1), desc="Calculating", unit="numbers"):
        steps = collatz_steps(n, memo)
        if steps > max_steps:
            max_steps = steps
            max_num = n
            
    return max_num, max_steps, memo

def main():
    try:
        print("Collatz Conjecture - Maximum Steps Calculator")
        print("--------------------------------------------")
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
        max_num, max_steps, memo = find_max_steps_in_range(start, end)
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        # Format time appropriately
        if elapsed_time < 60:
            time_str = f"{elapsed_time:.2f} seconds"
        elif elapsed_time < 3600:
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            time_str = f"{minutes} minutes and {seconds} seconds"
        else:
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            time_str = f"{hours} hours, {minutes} minutes and {seconds} seconds"
        
        print(f"\nResults:")
        print(f"The number with the maximum steps is: {max_num}")
        print(f"Number of steps: {max_steps}")
        print(f"Calculation completed in: {time_str}")
        print(f"Cached results: {len(memo)} numbers")
        
        # Show the sequence for the max number
        show_sequence = input("\nWould you like to see the sequence for the maximum steps number? (y/n): ")
        if show_sequence.lower() == 'y':
            n = max_num
            sequence = [n]
            while n != 1:
                if n & 1 == 0:
                    n = n >> 1
                else:
                    n = 3 * n + 1
                sequence.append(n)
            
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
        save_option = input("\nWould you like to save detailed results to a file? (y/n): ")
        if save_option.lower() == 'y':
            filename = f"collatz_results_{start}_to_{end}.txt"
            with open(filename, 'w') as f:
                f.write(f"Collatz Conjecture Results for range {start} to {end}\n")
                f.write(f"The number with the maximum steps is: {max_num}\n")
                f.write(f"Number of steps: {max_steps}\n")
                f.write(f"Calculation completed in: {time_str}\n")
                f.write(f"Cached results: {len(memo)} numbers\n")
                
                # Save sequence for the maximum steps number
                f.write(f"\nSequence for {max_num}:\n")
                n = max_num
                sequence = [n]
                while n != 1:
                    if n & 1 == 0:
                        n = n >> 1
                    else:
                        n = 3 * n + 1
                    sequence.append(n)
                f.write(" → ".join(map(str, sequence)))
                
                # Optionally save full data for all numbers in range
                f.write(f"\n\nDetailed results for all numbers in range:\n")
                for i in range(start, end + 1):
                    if i in memo:
                        f.write(f"{i}: {memo[i]} steps\n")
            
            print(f"Results saved to {filename}")
    
    except ValueError:
        print("Please enter valid integers.")
    except KeyboardInterrupt:
        print("\nCalculation interrupted.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()