import os

while True:
    p_num = int(input('Enter a problem number:'))
    num_test = int(input(f'Enter the number of test cases for p{p_num}:'))
    for i in range(num_test):
        os.system(f'python p{p_num}.py < p{p_num}_in_{i}.txt > p{p_num}_ans_{i}.txt')
        with open(f'p{p_num}_ans_{i}.txt') as f:
            txt = f.read()
        with open(f'p{p_num}_ans_{i}.txt', 'w', encoding='utf-8') as f:
            written_bytes = 0
            while written_bytes < len(txt):
                written_bytes += f.write(txt[written_bytes:])
                
