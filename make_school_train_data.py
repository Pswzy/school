# -*- coding: utf-8 -*-
#  L = ( B-EＲ，I-EＲ，B-OBJECT，I -OBJECT，E-OBJECT, O) ，
# 其中各个标记的意义分别是语义关系词汇( 实例属性) 首部、语义关系词汇内部、属性值首部、属性值内部及其他。
import codecs
import sys
import json
import re
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

def character_tagging(input_file, train_file, test_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    train_data = codecs.open(train_file, 'w', 'utf-8')
    test_data = codecs.open(test_file, 'w', 'utf-8')
    school_data = codecs.open('schoolList.json', 'a', 'utf-8')
    data_list = json.load(input_data)
    index = 0
    for i,data in enumerate(data_list):
        have_school = True
        schoolList = data['school']
        if len(schoolList) == 0:
            have_school = False
        obj_begin_tag = False
        obj_list = []
        if have_school:
            # 标记数据，生成训练数据
            for school in schoolList:
                school_data.write(school + '\n')
                re_str = '毕业|毕业于'  # 属性正则
                re_obj = r'^'
                for word in data['text']:
                    if re.match(u'^[\u4e00-\u9fa5]',u''+word[0]) is not None or re.match(r'\w', word[0]) is not None:
                        word[0] = re.sub(r'[*+?\\/]', '', word[0])
                        match_v = re.match(re_str, word[0])
                        match_bo = re.search(re_obj + word[0], school)
                        if match_v is not None:
                            obj_begin_tag = False
                            re_obj = r'^'
                            for tmp_word in obj_list:
                                train_data.write(tmp_word[0] + "\t" + tmp_word[1] + "\tO\n")
                            obj_list = []
                            train_data.write(word[0] + "\t" + word[1] + "\tB-ER\n")
                        elif match_bo is not None and obj_begin_tag == False:
                            if len(word[0]) < len(school):
                                obj_begin_tag = True
                                obj_list.append(word)
                                re_obj = re_obj + word[0]
                            elif len(word[0]) == len(school):
                                obj_begin_tag = False
                                re_obj = r'^'
                                train_data.write(word[0] + "\t" + word[1] + "\tB-OBJECT\n")
                            else:
                                obj_begin_tag = False
                                re_obj = r'^'
                                train_data.write(word[0] + "\t" + word[1] + "\tO\n")
                        elif match_bo is not None and obj_begin_tag:
                            if len(re_obj) - 1 + len(word[0]) < len(school):
                                obj_begin_tag = True
                                obj_list.append(word)
                                re_obj = re_obj + word[0]
                            elif len(re_obj) - 1 + len(word[0]) == len(school):
                                obj_begin_tag = False
                                re_obj = r'^'
                                train_data.write(obj_list[0][0] + "\t" + obj_list[0][1] + "\tB-OBJECT\n")
                                for tmp_word in obj_list[1:]:
                                    train_data.write(tmp_word[0] + "\t" + tmp_word[1] + "\tI-OBJECT\n")
                                train_data.write(word[0] + "\t" + word[1] + "\tI-OBJECT\n")
                                obj_list = []
                            else:
                                obj_begin_tag = False
                                re_obj = r'^'
                                for tmp_word in obj_list:
                                    train_data.write(tmp_word[0] + "\t" + tmp_word[1] + "\tO\n")
                                train_data.write(word[0] + "\t" + word[1] + "\tO\n")
                                obj_list = []
                        else:
                            obj_begin_tag = False
                            re_obj = r'^'
                            if len(obj_list) != 0:
                                for obj in obj_list:
                                    train_data.write(obj[0] + "\t" + obj[1] + "\tO\n")
                                obj_list = []
                            if word[0] == '。':
                                train_data.write(word[0] + "\t" + word[1] + "\tO\n\n")
                            else:
                                train_data.write(word[0] + "\t" + word[1] + "\tO\n")
                    else:
                        obj_begin_tag = False
                        re_obj = r'^'
                        if len(obj_list) != 0:
                            for obj in obj_list:
                                train_data.write(obj[0] + "\t" + word[1] + "\tO\n")
                            obj_list = []
                        if word[0] == '。':
                            train_data.write(word[0] + "\t" + word[1] + "\tO\n\n")
                        else:
                            train_data.write(word[0] + "\t" + word[1] + "\tO\n")
        else:
            # 生成测试数据
            test_data.write("index" + str(index) + "\t" + "m" + "\tO\n")
            for word in data['text']:
                if word[1] is not None:
                    if word[0] == '。':
                        test_data.write(word[0] + "\t" + word[1] + "\tO\n\n")
                    else:
                        test_data.write(word[0] + "\t" + word[1] + "\tO\n")
                else:
                    continue
        test_data.write("\n")
        index += 1
    input_data.close()
    train_data.close()
    test_data.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ("pls use: python make_crf_train_data.py input train_output test_output")
        sys.exit()
    input_file = sys.argv[1]
    train_file = sys.argv[2]
    test_file = sys.argv[3]
    character_tagging(input_file, train_file, test_file)