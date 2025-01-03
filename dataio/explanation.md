# handle_data.py 从原始数据中提取出标题和文本
# find_T_F_replace.py  从文本中找到图名和表名，并增加other字段存储，处理相应文件夹中的图和表命名。
# generate_T_S.py   利用大模型生成titile和summary，并拆分page字段，分为page_from和page_to。
# split_text_jsonl.py 细粒度拆分文本，增加Serial Number字段，根据拆分的文本重新计算other字段。