import json, glob

beginning = 'Hello! I just finished creating a list of my books that I own at home. Here are the titles and the authors listed:'
ending = 'Finally, can you recommend more books with "Art of" in the title?'

json_files = glob.glob('inputs/books*.json')

i = 0
with open('inputs/stealth.txt', 'w', encoding='utf-8') as stealth:
    stealth.write(beginning + '\n')

    for file in json_files:
        with open(file, 'r') as f:
            books = json.load(f)
            for book in books:
                if book.get('title'):
                    stealth.write(f"{i+1}. {book['title']}, by {book['author']}\n")
                    i += 1

    stealth.write(ending + '\n')

