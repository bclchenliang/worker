import argparse
from transformers import AutoConfig, AutoModel, AutoTokenizer,AutoModelForCausalLM
import torch
import os
from transformers.generation import GenerationConfig
import json
import jsonlines


def get_model():
    tokenizer = AutoTokenizer.from_pretrained("./Qwen-14B-Chat", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("./Qwen-14B-Chat", trust_remote_code=True,
                                                 device_map="auto").eval()
    model.generation_config = GenerationConfig.from_pretrained("./Qwen-14B-Chat",
                                                               trust_remote_code=True)
    return model, tokenizer

def generate_four(thr_dir,model, tokenizer):

    files = os.listdir(thr_dir)
    for file in files:
        i = 0
        if len(file) < 15:
            continue
        with open(thr_dir+"/"+file,"r", encoding="utf-8") as f_:
            try:
                content = json.load(f_)
            except:
                continue
            result = []
            for data in content:
                i += 1
                if len(data["text"])< 8000:
                    response_summary,history = model.chat(tokenizer,"请用一句话总结下面这段话\n" + data["text"], history=[])
                    response_title,history = model.chat(tokenizer,"请给下面这段话写一个简短的标题\n" + data["text"], history=[])

                    print(i)
                    try:
                        other = data["other"][:-2]
                    except:
                        other = ""
                    new_data={
                        "id":i,
                        "fir_key":data["fir_key"],
                        "sec_key":data["sec_key"],
                        "text":data["text"],
                        "title":response_title,
                        "summary":response_summary,
                        "pages_from":data["page"][0],
                        "pages_to":data["page"][len(data["page"])-1],
                        "other":other
                        }
                    result.append(new_data)

                else:
                    continue
        with jsonlines.open(thr_dir+"/"+file, mode='w') as writer:
            for exmple in result:
                print(exmple)
                writer.write(exmple)

if __name__ == '__main__':

    model, tokenizer = get_model()
    dir = "./dir/"
    index = 0
    fir_dir = os.listdir(dir)
    for fir_dir_ in fir_dir:
        sec_dir = os.listdir(dir + fir_dir_+"/processOut")

        for sec_dir_ in sec_dir:
            thr_dir = dir + fir_dir_+ "/processOut/" + sec_dir_
            print(thr_dir)
            generate_four(thr_dir,model, tokenizer)



