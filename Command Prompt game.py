import json
import random
import time
from collections import defaultdict
from requests.api import head
from xpinyin import Pinyin

with open('head.json', 'r') as f:
    poem_dict_head = json.load(f)
    f.close()

with open('tail.json', 'r') as f:
    poem_dict_tail = json.load(f)
    f.close()

def Snake_head(str):
    answer = ''
    if str not in poem_dict_head.keys():
        print('Oh, I am defeated\n')
    else:
        answer = random.sample(poem_dict_head[str], 1)[-1]
        print('My answer is:\n',answer)
    return answer

def Snake_tail(str):
    answer = ''
    if str not in poem_dict_tail.keys():
        print('I am defeated\n')
    else:
        answer = random.sample(poem_dict_tail[str], 1)[0]
        print('My answer is:\n', answer)
    return answer

def Game():
    mode = str(input("Please input the MODE(1 for head and 2 for tail):\n"))
    while True:
        if mode == '1':
            verse = str(input('Please input a verse:\n'))
            tail = verse[-1]
            # tail = Pinyin().get_pinyin(tail_pinyin)
            while tail != '':
                time.sleep(2)
                tail_pinyin = Pinyin().get_pinyin(tail)
                answer = Snake_head(tail_pinyin)
                if answer == '':
                    return 0
                else:
                    tail = answer[-1]
        elif mode == '2':
            verse = str(input('Please input a verse:\n'))
            head = verse[0]
            # tail = Pinyin().get_pinyin(tail_pinyin)
            while head != '':
                time.sleep(2)
                head_pinyin = Pinyin().get_pinyin(head)
                answer = Snake_tail(head_pinyin)
                if answer == '':
                    return 0
                else:
                    head = answer[0]
            return 0
        else:
            print('Please input right number')
            return -1

OVER = Game()
if OVER == 0:
    print('Game over. Thank you for playing!\n')
else:
    print('Sorry, some errors happened\n')
