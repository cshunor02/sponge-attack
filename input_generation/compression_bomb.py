#!/usr/bin/env python3
"""
Very short compression prompts
Usage:
    python compression_bomb.py --n 100
Writes N lines to inputs/compression_bomb.txt
"""

import os, random, argparse, string

verb   = ["Rep", "Rpt", "Echo", "Dup", "Print"]
ranges  = ["1e5", "1e6", "100k", "1M", "65k", "262k", "0xFFFF"]
char   = list(string.ascii_uppercase + string.digits) + ["#", "@", "&"]
pi     = ["π1e5", "π1e6", "pi70k"]
enum   = ["1-", "0-", "00-"]
hex = ["hex", "0x"]
times = ["", "x"]

def t_repeat():    # Rep A 1e6
    return f"{random.choice(verb)} {random.choice(char)} {random.choice(ranges)}{random.choice(times)}"

def t_compact():   # RepA1e6
    return f"{random.choice(verb)}{random.choice(char)}{random.choice(ranges)}{random.choice(times)}"

def t_star():      # A*1e5
    return f"{random.choice(char)}*{random.choice(ranges)}"

def t_pow():       # Z^1e6
    return f"{random.choice(char)}^{random.choice(ranges)}"

def t_enum():      # 1-1e5
    return f"{random.choice(enum)}{random.choice(ranges)}"

def t_pi():        # π1e6
    return random.choice(pi)

def t_hex():       # hexFFFF
    return f"{random.choice(hex)}{random.choice(ranges).replace('0x','')}"


templates = [t_repeat, t_compact, t_star, t_pow, t_enum, t_pi, t_hex]

def main():
    ap = argparse.ArgumentParser(description="Generate micro-mix compression prompts.")
    ap.add_argument("--n", type=int, default=50, help="how many prompts")
    args = ap.parse_args()

    os.makedirs("inputs", exist_ok=True)
    path = "inputs/compression_bomb.txt"

    with open(path, "w", encoding="utf-8") as f:
        for _ in range(args.n):
            f.write(random.choice(templates)() + "\n")

    print(f"Wrote {args.n} micro prompts to {path}")

if __name__ == "__main__":
    main()
