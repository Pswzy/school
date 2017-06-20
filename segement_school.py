# -*- coding: utf-8 -*-
import codecs
import sys
from bs4 import BeautifulSoup
import io
import json
import pynlpir
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')         #改变标准输出的默认编码
pynlpir.open()
with codecs.open('step_two_home.json', 'r', 'utf-8') as fl:
    load_list=json.load(fl)
    error_list=[]
    print(len(load_list))
    delete_index = []
    for person in load_list:
        person['birth']=pynlpir.segment(person['birth'], pos_names=None, pos_english=False)
        person['home']=pynlpir.segment(person['home'], pos_names=None, pos_english=False)
        school_list=re.split(r',|，|、|（现', person['school'])
        person['school']=[]
        for school in school_list:
            if re.search(r'[原现]?(.+?(大学|学院))', school) is not None:
                person['school'].append(re.search(r'[原现]?(.+?(大学|学院))', school).group(1))
        person['text']=pynlpir.segment(person['text'], pos_names=None, pos_english=False)
    with codecs.open('school_segement.json', 'w', 'utf-8') as result_fl:
        json.dump(load_list, result_fl, skipkeys=False, ensure_ascii=False)