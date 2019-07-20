import os
import ujson
import json
import operator

def replace_sentences(text):
    text = text.replace(" #", "\n#")
    sentences = text.splitlines()   
    new_sentences = ''
    
    for index, i in enumerate(sentences):
        for index2, j in enumerate(i.split()):
            if index != 0 and index2 == 0:
                #print(j)
                continue
            else:
                new_sentences += " " + j
    
    return [new_sentences]


def write_pos_review(output_file_name, List):        # def(3) json 형태로 파일 저장 
    
    with open(output_file_name, "w", encoding="utf-8") as output_file:
        for line in List:
            review_str = ujson.dumps(line, ensure_ascii=False)
            print(review_str, file=output_file)


def make_total_user_json() :
    #find path
    directory =os.getcwd() 

    file_dir = directory + '/res/read'
    file_list = os.listdir(file_dir)

    table = dict()

    for file in file_list:
        path = directory + '/res/read/'+str(file)
        with open(path, "r", encoding='utf-8') as fp:
  
            for line in fp:
                lines = replace_sentences(line)

                for i in lines:
                    A = i.split()
                    user = A[0]
                    read = A[1:]

                    if user in table:
                        for j in read:
                            if j in table[user]:
                                table[user][j] += 1
                            else:
                                table[user][j] = 1
                    else:
                        table[user] = dict()
                        for j in read:
                            if j in table[user]:
                                table[user][j] += 1
                            else:
                                table[user][j] = 1

    List = []
    List.append(table)

    output_file_name = r"user_json.txt"
    write_pos_review(output_file_name, List)

def make_user_json():
    directory =os.getcwd()

    file_dir = directory + '/res/read'
    file_list = os.listdir(file_dir)

    new_file_list = []
    for f in file_list:
        name = f.split('_')
        if int(name[0]) >= 2019021400:
            new_file_list.append(f)
        
    table = dict()

    for file in new_file_list:
        path = directory + '/res/read/'+str(file)
        with open(path, "r", encoding='utf-8') as fp:

            for line in fp:
                lines = replace_sentences(line)

                for i in lines:
                    A = i.split()
                    user = A[0]
                    read = A[1:]
                    if user in table:
                        for j in read:
                            if j in table[user]:
                                table[user][j] += 1
                            else:
                                table[user][j] = 1
                    else:
                        table[user] = dict()
                        for j in read:
                            if j in table[user]:
                                table[user][j] += 1
                            else:
                                table[user][j] = 1

    List = []
    List.append(table)
        
    output_file_name = r"user_json2.txt"
    write_pos_review(output_file_name, List)

def make_user_json_file():
    make_total_user_json()
    make_user_json()