import matplotlib.pyplot as plt
from tqdm import tqdm

def collatz_steps(start):
    number = start
    count = 0
    while number != 1:
        number = number // 2 if number % 2 == 0 else 3 * number + 1
        count += 1
    return count

def plot_steps_summary(start=100_000_000, end=900_000_000):
    numbers = list(range(start, end + 1))
    
    print(f"Calculating Collatz steps for numbers {start:,} to {end:,}...")
    steps_required = []
    max_steps = 0
    number_with_max_steps = start

    for n in tqdm(numbers):
        steps = collatz_steps(n)
        steps_required.append(steps)

        if steps > max_steps:
            max_steps = steps
            number_with_max_steps = n

    # Plot
    plt.figure(figsize=(14, 6))
    plt.plot(numbers, steps_required, linewidth=0.5, color='blue')
    plt.title(f'3x + 1: Steps to Reach 1 (From {start:,} to {end:,})', fontsize=14)
    plt.xlabel('Starting Number')
    plt.ylabel('Steps to Reach 1')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    # Output max info
    print(f"\n🔥 Number with the most steps: {number_with_max_steps:,}")
    print(f"📈 Maximum steps to reach 1: {max_steps}")

def main():
    plot_steps_summary(100_000_000, 900_000_000)

if __name__ == "__main__":
    main()
