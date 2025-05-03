prompt_input = "Hello \n" * 1000000

file = open('inputs/hello.txt', 'w', encoding='utf-8')

file.write(prompt_input)

file.close()