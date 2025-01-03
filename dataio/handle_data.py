"""
---------------------------------
Author: biancl
  Email : bcl_persist@163.com
   Time : 2023/12/7 14:34
    File: handle_data.py
Software: PyCharm
---------------------------------
"""
import json
import os
import re

# 判断字符串是否包括数字
def contains_number(s):
    return any(char.isdigit() for char in s)

def remove_digits(input_str):
    return re.sub(r'\d+', '', input_str)

def remove_non_chinese_chars(input_str):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    return pattern.sub('', input_str)

def remove_non__char(input_str):
    pattern = re.compile(r'\.')
    return pattern.sub('', input_str)

def relace_(string_):
    s1 = string_.replace("\n","")
    s2 = s1.replace("。","。\n")
    return s2

def find_flag(file):
    flag = 0
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

        for example in data["pdf_text"]:
            temp = example["text"]
            temp_key = remove_digits(temp)
            temp_key = remove_non__char(temp_key)
            flag += 1
            if temp_key == "总则" or temp_key == "一总则" :
                return flag

if __name__ == '__main__':

    dir = ("./设计新数据/temp/")

    file_dir = os.listdir(dir)
    for file_ in file_dir:
        files = os.listdir(dir+file_)
        for ex in files:
            if len(ex) > 12:
                file = dir+file_+"/"+ ex
                # print(file)
                flag = find_flag(file)

                with open(file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    flag_ = 0
                    first_title = ""
                    sec_title=""
                    result = []

                    for example in data["pdf_text"]:
                        flag_ += 1
                        if flag_ < (flag - 1):
                            continue

                        if example["label"] == "title" or example["label"] == "subtitle":
                            temp = remove_digits(example["text"])
                            temp = remove_non__char(temp)
                        else:
                            temp = example["text"]

                        if len(temp) > 1:
                            if temp[0] == "附" and temp[1] == "录":
                                break

                        if example["label"] == "title":
                            if len(first_title) > 0:
                                first_title = ""
                            first_title += temp
                            continue

                        if example["label"] == "subtitle":

                            sec_title += temp
                            continue

                        if example["label"] == "paragraph":
                            if first_title == "总则" or first_title == "一总则":
                                first_title = remove_non_chinese_chars(data["pdf_filename"]) + "总则"

                            # if first_title.find("符号") != -1:
                            #     continue
                            if first_title.find("用词说明") != -1:   #质量监督与工程检测
                                continue
                            if first_title == "引用标准名录":
                                continue
                            if first_title .find("附录") != -1:
                                continue
                            result.append({"fir_key": first_title.replace("\n",""),
                                           "sec_key": sec_title.replace("\n", ""),
                                           "text": relace_(temp),
                                           "page": example["page"]
                                           })
                            sec_title = ""
                        else:
                            continue

                with open("{}{}/{}.json".format(dir,file_,ex.split(".",1)[0]), "w", encoding="utf-8") as f_:
                    json.dump(result, f_, ensure_ascii=False, indent=2)

