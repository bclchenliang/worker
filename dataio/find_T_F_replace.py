"""
---------------------------------
Author: biancl
  Email : bcl_persist@163.com
   Time : 2023/12/14 10:36
    File: find_T_F_replace.py
Software: PyCharm
---------------------------------
"""
import json
import os
import re

def re_write(F_json):
    with open(F_json, 'r',encoding='utf-8') as f:
        a = f.readlines()

    dict_list = []
    dict_str = ""
    for i in a:
        i = i.replace('\n', '')
        if i == "{":
           dict_str = i
        elif i == "}":
           dict_str += i
           if 'null' in dict_str:
               dict_str = dict_str.replace('null', '""', 1)
           dict_list.append(eval(dict_str))
        else:
           dict_str += i

    with open(F_json, 'w', encoding='utf-8') as f:
        if F_json.split(".", 1)[0][-2] == "l":
            json.dump(dict_list, f, ensure_ascii=False, indent=5)
        else:
            json.dump(dict_list, f, ensure_ascii=False, indent=4)

def remove_characters(s):
    # 使用正则表达式匹配中文字符和英文字符，并替换为空字符串
    return re.sub(r'[a-zA-Z\u4e00-\u9fa5]+', '', s)
def remove_chinese(s):
    return re.sub(r'[\u4e00-\u9fa5]+', '', s)

def f_json(file, figure_dir):
    # 处理图表json文件
    with open(file, 'r', encoding='utf-8') as f:
        content = []
        data = json.load(f)
        files = os.listdir(figure_dir)
        order = 0
        for ex in data["shapes"]:
            if len(ex["figure_name"]) < 2:
                continue
            if ex["figure_name"][0] != '图':
                order +=1
                figure_id = "unkown_{}".format(order)
            else:
                print(ex["figure_name"])

                if ex["figure_name"][1].isdigit():
                    figure_id = "图" + remove_characters(ex["figure_name"])
                else:

                    figure_id = "图" + remove_chinese(ex["figure_name"])

                figure_id = figure_id.replace(" ", "").replace("(", "").replace(")", "").replace("（","").replace("）","").replace("[","").replace("]","")
                figure_id = figure_id.replace("　", "").replace("、", "").replace("|", "").replace("【","").replace("】","")
                figure_id = figure_id.replace("“","").replace("。","").replace("，","")
                print(figure_id)

            index =0
            files = os.listdir(figure_dir)
            for file_ in files:
                count = file_.rfind('_')
                temp = file_[:count]
                if temp == ex["figure_name"]:
                    index += 1
                    new_name = figure_id+".jpg"
                    names = os.listdir(figure_dir)
                    if new_name in names:
                        new_name = figure_id + "_{}.jpg".format(index)
                    print(new_name)
                    os.rename(figure_dir + file_, figure_dir + new_name)

            content.append({"figure_id": figure_id, "figure_name": ex["figure_name"][len(figure_id):], "pageon": ex["pageon"]})

        with open(file, "w", encoding="utf-8") as f_:
            json.dump(content, f_, ensure_ascii=False, indent=4)

def find_f(file, F_json):

    with open(F_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        content = []
        for ex in data:
            content.append(ex["figure_id"])

    con = []
    with open(file, 'r', encoding='utf-8') as f_:
        data = json.load(f_)
        for example in data:
            temp = example["text"]
            temp_text = ""

            for in_ in content:
                temp_in = in_

                if len(in_) < 2:
                    continue

                flag = temp.find(in_)
                if flag == -1:
                    continue
                if flag + len(in_) < len(temp)-1:
                    if temp[flag+len(in_)] != '.':

                        temp_text += "![{}](./figure/{}.jpg)".format(in_,temp_in)+","+"\n"
                        continue
                else:

                    temp_text += "![{}](./figure/{}.jpg)".format(in_,temp_in)+","+"\n"
                    continue
            try:
                other = example["other"]
                other = other + temp_text
            except:
                other = temp_text

            try:
                page = example["page"]
            except:
                page = ""

            con.append({"fir_key": example["fir_key"], "sec_key":example["sec_key"], "text": temp, "page":page,"other":other})

    with open(file, "w", encoding="utf-8") as f_:
        json.dump(con, f_, ensure_ascii=False, indent=5)

def t_json(file, table_dir):

    # 处理表json文件
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(type(data))
        content = []
        order = 0
        index = 0
        for ex in data["shapes"]:

            if len(ex["table_name"]) < 2:
                continue
            if ex["table_name"][0] == "续":

                if len(ex["table_name"]) > 2 and ex["table_name"][2].isdigit():
                    table_id = "续表" + remove_characters(ex["table_name"])
                else:
                    table_id = "续表" + remove_chinese(ex["table_name"])

                # table_id = "续表" + remove_chinese(ex["table_name"])
            elif ex["table_name"][0] == "表":

                if ex["table_name"][1].isdigit():
                    table_id = "表" + remove_characters(ex["table_name"])
                else:
                    table_id = "表" + remove_chinese(ex["table_name"])

                # table_id = "表" + remove_chinese(ex["table_name"])
            else:
                order += 1
                table_id = "unkown_{}".format(order)

            #print(table_id)

            table_id = table_id.replace(" ", "").replace("，", "").replace("（","").replace("）","")
            table_id = table_id.replace("、", "").replace("m", "").replace("　", "").replace("。", "")

            files = os.listdir(table_dir)
            for file_ in files:
                count = file_.rfind('_')
                temp = file_[:count]
                if temp == ex["table_name"]:

                    new_name = table_id + ".jpg"
                    names = os.listdir(table_dir)
                    if new_name in names:
                        index += 1
                        new_name = table_id + "_{}.jpg".format(index*2)
                    print(new_name)
                    os.rename(table_dir + file_, table_dir + new_name)


            content.append({"table_id": table_id, "table_name": ex["table_name"][len(table_id):], "table_text":ex["table_text"], "pageon": ex["pageon"]})

        with open(file, "w", encoding="utf-8") as f_:
            json.dump(content, f_, ensure_ascii=False, indent=5)

def find_t(file, T_json):

    with open(T_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        content = []
        for ex in data:
            content.append(ex["table_id"])

    con = []
    with open(file, 'r', encoding='utf-8') as f_:
        data = json.load(f_)
        for example in data:
            temp = example["text"]
            temp_text = ""

            for in_ in content:
                temp_ = in_
                if len(in_) < 2:
                    continue

                flag = temp.find(in_)
                if flag == -1:
                    continue

                if flag + len(in_) < len(temp) - 1:
                    if temp[flag + len(in_)] != '.':
                        temp_text+="![{}](./table/{}.jpg)".format(in_, temp_)+","+"\n"
                        continue
                else:
                    temp_text += "![{}](./table/{}.jpg)".format(in_, temp_)+","+"\n"
                    continue
            try:
                other = example["other"]
                other = other + temp_text
            except:
                other = temp_text

            try:
                page = example["page"]
            except:
                page = ""
            con.append({"fir_key": example["fir_key"], "sec_key":example["sec_key"], "text": temp,"page":page, "other":other})

    with open(file, "w", encoding="utf-8") as f_:
        json.dump(con, f_, ensure_ascii=False, indent=5)

if __name__ == '__main__':
    # 整个流程
    dir = ("C:/Users/biancl/Desktop/设计新数据/temp/")
    file_dir = os.listdir(dir)
    for file_ in file_dir:
        print(file_)
        files = os.listdir(dir + file_)
        if len(files) > 1:
            if "table" in files:

                T_json = dir + file_ + "/table.json"
                table_dir = dir + file_ + "/table/"

                for fi in files:
                    if len(fi) > 12:
                        file_text = dir + file_ + "/"  + fi

                        t_json(T_json, table_dir)
                        find_t(file_text, T_json)
                        break

            if "figure" in files:

                F_json = dir + file_ + "/figure.json"
                figure_dir = dir + file_ + "/figure/"
                for fi in files:
                    if len(fi) > 12:
                        file_text = dir + file_ + "/"  + fi
                        f_json(F_json, figure_dir)
                        find_f(file_text, F_json)
                        break





