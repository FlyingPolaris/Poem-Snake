# -*- coding:utf-8 -*-
from xpinyin import Pinyin
from collections import defaultdict
import re
import json

with open('poem.txt', 'rb') as f:
    poems = f.readlines()
    f.close()
legal_parts = []


def clean_str(str):
    str = str.replace('；', '').replace('。', '').replace(
        '，', '').replace('！', '').replace('、', '').replace('？', '').replace('：', '')
    return str


for poem in poems:
    poem = poem.decode('utf-8')
    parts = re.findall(r'[\s\S]*?[。？！，；、：]', poem)
    for i in range(len(parts)):
        parts[i] = clean_str(parts[i])
        # if len(parts[i]) >= 5:
        #     legal_parts.append(parts[i])
        # elif i < len(parts) - 1:
        #     parts[i+1] = clean_str(parts[i+1])
        #     legal_parts.append(parts[i] + ' ' + parts[i+1])
        error_flag = 0
        while(len(parts[i].replace(" ", "")) < 5):
            k = 1
            if i+k == len(parts):
                error_flag = 1
                break
            parts[i] = parts[i] + ' ' + clean_str(parts[i+k])
            k += 1
        if error_flag == 0:
            legal_parts.append(parts[i])


poem_dict_head = defaultdict(list)
poem_dict_tail = defaultdict(list)


for part in legal_parts:
    head = Pinyin().get_pinyin(part[0])
    poem_dict_head[head].append(part)
    tail = Pinyin().get_pinyin(part[-1])
    poem_dict_tail[tail].append(part)


with open('head.json', 'w') as f:
    json.dump(poem_dict_head, f)  
    f.close() 

with open('tail.json', 'w') as f:
    json.dump(poem_dict_tail, f)  
    f.close() 