beginning = 'Hi! I have been thinking about organizing my bookshelf so I listed all the books I have. I want to sort them by author and title. Here is the list of books I have:'
ending = 'Finally, can you recommend more books with "Art of" in the title?'

import json

stealth = open('inputs/stealth.txt', 'w')
stealth.write(beginning + '\n')

list = open('inputs/books.json', 'r')
books = list.read()

titles = json.loads(books)
for x in titles["results"]:
    if x['title'] == '':
        continue
    stealth.write(f"Title: {x['title']}, Author: {x['author']}\n")

stealth.write(ending + '\n')
stealth.close()

list.close()