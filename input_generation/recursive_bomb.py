#!/usr/bin/env python3
"""
Generate recursive prompts whose recursion depth and branching-factor can be adjusted.

Usage:
    python recursive_bomb.py --base 4 --exp 10 --n 60

Result:
    Writes 60 prompts into inputs/recursive_bomb.txt
"""

import argparse, os, random, textwrap

topics = [
    "structure of an atom",
    "history of the Roman Empire",
    "global supply-chain logistics",
    "quantum entanglement",
    "IPv6 header format",
    "Mandarin phonology",
    "cell mitosis",
    "general relativity",
    "Unicode normalisation",
    "hidden Markov models"
]

recursive_template = textwrap.dedent("""
    Describe **{topic}** in **{base}** sentences.
    After every sentence, expand it into **{base}** new sentences,
    and repeat this expansion **{exp}** more times.
    Do **not** stop expanding until explicitly instructed.
""").strip()

def build_prompt(base: int, exp: int) -> str:
    return recursive_template.format(
        topic=random.choice(topics), base=base, exp=exp
    )

def main():
    ap = argparse.ArgumentParser(
        description="Generate recursive-bomb prompts."
    )
    ap.add_argument("--base", type=int, required=True,
        help="branch-factor: how many new sentences per sentence")
    ap.add_argument("--exp", type=int, required=True,
        help="expansion depth (how many times to repeat)")
    ap.add_argument("--n",   type=int, default=50,
        help="number of prompts to generate (default 50)")
    args = ap.parse_args()

    os.makedirs("inputs", exist_ok=True)
    path = "inputs/recursive_bomb.txt"

    with open(path, "w", encoding="utf-8") as f:
        for _ in range(args.n):
            f.write(build_prompt(args.base, args.exp) + "\n\n")

    print(f"Wrote {args.n} prompts to: {path}")

if __name__ == "__main__":
    main()
