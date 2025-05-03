import random

words = ["Hello", "hello", "World", "Attack", "Random", "Example", "Input", "Large", "File", "Words", "LLM Overload", "Team", ".", "?", "!", ":", ";"]

lines = []
for _ in range(1000000):
    line = ' '.join(random.choices(words, k=10))
    lines.append(line)

with open('inputs/strong_sponge.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
