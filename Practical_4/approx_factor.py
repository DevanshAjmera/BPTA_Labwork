import os
import csv

def read_factors(path):
    factors = []
    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        col = None
        for idx, name in enumerate(header):
            if "factor" in name.strip().lower():
                col = idx
        for row in reader:
            if len(row) > col and row[col].strip() != "":
                factors.append(row[col].strip())
    return factors


def main():
    os.makedirs("Input", exist_ok=True)

    p2 = read_factors("../Practical_2/result.csv")
    p3 = read_factors("../Practical_3/result.csv")

    all_factors = p2 + p3

    with open("Input/approx_factor.txt", "w") as f:
        for val in all_factors:
            f.write(val + "\n")

    print(f"Saved {len(all_factors)} approximation factors "
          f"({len(p2)} from P2, {len(p3)} from P3)")

main()