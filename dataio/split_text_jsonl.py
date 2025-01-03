# coding=utf-8
"""
---------------------------------
Author: biancl
  Email : bcl_persist@163.com
   Time : 2024/2/29 9:48
    File: split_text_jsonl.py
Software: PyCharm
---------------------------------
"""
import re
import json
import os

def find_x_x_x(text):

    # 使用正则表达式匹配
    pattern = r'\d+\.\d+\.\d+'
    pattern_one = r'\d+\．\d+\．\d+'
    pattern_two = r'\d+\．\d+\.\d+'
    pattern_three = r'\d+\.\d+\．\d+'
    pattern_four = r'\d+\．\d+\．\d+'
    matches = re.findall(pattern, text)
    matches_one = re.findall(pattern_one, text)
    matches_two = re.findall(pattern_two, text)
    matches_three = re.findall(pattern_three, text)
    matches_four = re.findall(pattern_four, text)

    return matches+matches_1+matches_2+matches_3+matches_4

if __name__ == '__main__':

    file_dir = "./设计新数据/new_data/拆分数据/"
    fir_dir = os.listdir(file_dir)

    for fir_ in fir_dir:
        sec_dir = os.listdir(file_dir+fir_)

        for sec_ in sec_dir:
            if len(sec_) > 13:
                # new_data = []
                id = 0
                result_ = []
                with open(file_dir+fir_+"/"+sec_, 'r', encoding='utf-8') as f:
                       for line in f:
                            data = json.loads(line)

                            text = data['text']
                            try:
                                result = find_x_x_x(text)
                                print(f"找到的模式: {result}")
                            except:
                                continue

                            flags = []
                            for index in result:
                                if index[0] == "0":
                                    continue
                                flag = text.find(index)
                                if text[flag-1] == '图' or text[flag-1] == '表' or text[flag-1]=="（":
                                    continue
                                else:
                                    flags.append(flag)
                            flags.sort()
                            print("处理过的：", flags)
                            new_text = []
                            for i in range(len(flags)):
                                if i < len(flags) - 1:
                                    if text[flags[i]:flags[i+1]] == "":
                                        continue
                                    if len(text[flags[i]:flags[i + 1]]) < 6:
                                        continue
                                    new_text.append(text[flags[i]:flags[i+1]])
                                else:
                                    if text[flags[i]:] == "":
                                        continue
                                    if len(text[flags[i]:]) < 6:
                                        continue
                                    new_text.append(text[flags[i]:])

                            print(new_text)
                            for temp_text in new_text:
                                try:
                                    other = data["other"].split(",")
                                except:
                                    other = []
                                im = []
                                for other_ in other:

                                    try:
                                        match = re.search(r'\[([^\]]*)\]', other_)

                                        if temp_text.find(match.group(1)) != -1 :
                                            if temp_text[temp_text.find(match.group(1))+1] == "." or temp_text[temp_text.find(match.group(1))+1] == "．":
                                                continue
                                            else:
                                                im.append(other_.replace("\n",""))
                                    except:
                                        continue

                                im = list(set(im))
                                if data["fir_key"] != "" and data["sec_key"] == "":
                                    if temp_text[2] == "." or temp_text[2] == "．":
                                        fir_key = temp_text[:2] + " " + data["fir_key"]
                                    else:
                                        fir_key = temp_text[0] + " " + data["fir_key"]
                                    sec_key = ""

                                elif data["fir_key"] != "" and data["sec_key"] != "":
                                    if temp_text[2] == "." or temp_text[2] == "．":
                                        fir_key = temp_text[:2] + " " + data["fir_key"]
                                    else:
                                        fir_key = temp_text[0] + " " + data["fir_key"]
                                    if temp_text[2] == "." or temp_text[2] == "．":
                                        sec_key =  temp_text[:4] + " " + data["sec_key"]
                                    else:
                                        sec_key = temp_text[:3] + " " + data["sec_key"]
                                else:

                                    fir_key = data["fir_key"]
                                    sec_key = data["sec_key"]

                                result_.append({"id": id,
                                                "file_name": sec_.split("_", 1)[0],
                                                "fir_key": fir_key,
                                                "sec_key": sec_key,
                                                "Serial Number": find_x_x_x(temp_text)[0].replace("．","."),
                                                "text": temp_text,
                                                "page":list(set([data["pages_from"],data["pages_to"]])),
                                                "other": im
                                               })
                                id += 1

                with open(file_dir+fir_+"/"+sec_, 'w', encoding='utf-8') as f:
                    json.dump(result_, f, ensure_ascii=False,indent=5)



