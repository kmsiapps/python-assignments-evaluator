while True:
    p_num = int(input('Enter a problem number:'))
    num_test = int(input(f'Enter the number of test cases for p{p_num}:'))
    
    f = open(f'p{p_num}_ban_keyword.txt', 'w')
    f.close()

    f = open(f'p{p_num}_req_keyword.txt', 'w')
    f.close()
    
    for i in range(num_test):
        f = open(f'p{p_num}_in_{i}.txt', 'w')
        f.close()

