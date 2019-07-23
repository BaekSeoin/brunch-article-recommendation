import fire
import operator
import ujson
from preprocessing import make_user_json_file

class Recommendation(object) :

    def __init__(self):
        make_user_json_file()
    
    #삭제 리스트 확인
    def check_delete(self, delete_article_check ,x):
        try:
            A = delete_article_check[x]
            return True
        except:
            return False 

    def inRange(self, a, b, c, d):
        if (a == 1) or (b==1) or (c==1) or(d==1):
            return True
        return False
        
    def recommend(self, userlist_path, out_path):
        users = [u.strip() for u in open(userlist_path)]
        self.make_result(out_path, users)


    def make_result(self, out_path, result_users) :
        test_users = []
        path2 = './res/predict/' + 'test.users'
        with open(path2,'r') as test:
            for line in test:
                line = line.rstrip()
                test_users.append(line)

        #test 유저가 전체 기간동안 읽은 글 확인
        USER = dict()
        file_path = 'user_json.txt'
        with open(file_path,'r') as file_name:
            for users in file_name:
                users = ujson.loads(users)
                for key, values in users.items():
                    if key in test_users:                    
                        for k,v in values.items():
                            try:
                                USER[key].append(k)
                            except:
                                USER[key] = []
                                USER[key].append(k)
        article = dict()
        file_path = 'user_json2.txt'
        with open(file_path,'r') as file_name:
            for users in file_name:
                users = ujson.loads(users)
                for key, values in users.items():
                    for k,v in values.items():
                        a = k.split('_')
                        writer = a[0]
                        article_n = a[1]
                        try:
                            article[writer][k] +=v
                        except:
                            try:
                                article[writer][k] = dict()
                                article[writer][k] = v
                            except:
                                article[writer] = dict()
                                article[writer][k] = dict()
                                article[writer][k] = v

        article2 = dict()
        for k,v in article.items():
            article2[k] = []
            for a,b in v.items():
                article2[k].append((a,b))

        for k,v in article2.items():
            a = sorted(v, reverse=True,key= lambda x : (x[1],x[0]))
            article2[k] = a

        USER_writer = dict()
        for i,j in USER.items():
            USER_writer[i] = dict()
            for k in j:
                a = str(k).split('_')
                try:
                    USER_writer[i][a[0]] +=1
                except:
                    try:
                        USER_writer[i][a[0]] =0
                        USER_writer[i][a[0]] +=1
                    except:
                        USER_writer[i]=dict()
                        USER_writer[i][a[0]] =0
                        USER_writer[i][a[0]] +=1

        USER_writer2 = dict()
        for k,v in USER_writer.items():
            USER_writer2[k] = []
            for a,b in v.items():
                USER_writer2[k].append((a,b))

        #정렬/ 많이 읽은 작가 순서대로 정렬
        for k,v in USER_writer2.items():
            v =  sorted(v, key=operator.itemgetter(1), reverse=True)
            USER_writer2[k] = v
            
        USER_ver2 = dict()
        file_path = 'user_json2.txt'
        with open(file_path,'r') as file_name:
            for users in file_name:
                users = ujson.loads(users)
                for key, values in users.items():
                    if key in test_users:                    
                        for k,v in values.items():
                            try:
                                USER_ver2[key].append(k)
                            except:
                                USER_ver2[key] = []
                                USER_ver2[key].append(k)
        
        #각 유저별로 작가수 count
        USER_writer_ver2 = dict()
        for i,j in USER_ver2.items():
            USER_writer_ver2[i] = dict()
            for k in j:
                a = str(k).split('_')
                try:
                    USER_writer_ver2[i][a[0]] +=1
                except:
                    try:
                        USER_writer_ver2[i][a[0]] =0
                        USER_writer_ver2[i][a[0]] +=1
                    except:
                        USER_writer_ver2[i]=dict()
                        USER_writer_ver2[i][a[0]] =0
                        USER_writer_ver2[i][a[0]] +=1
        
        USER_writer2_ver2 = dict()
        for k,v in USER_writer_ver2.items():
            USER_writer2_ver2[k] = []
            for a,b in v.items():
                USER_writer2_ver2[k].append((a,b))
        #정렬
        for k,v in USER_writer2_ver2.items():
            v =  sorted(v, key= lambda x : (x[1],x[0]), reverse=True)
            USER_writer2_ver2[k] = v

                
        USER_article = dict()
        for i,j in USER_ver2.items():
            USER_article[i] = dict()
            for k in j:
                try:
                    USER_article[i][k] +=1
                except:
                    try:
                        USER_article[i][k] =0
                        USER_article[i][k] +=1
                    except:
                        USER_article[i]=dict()
                        USER_article[i][k] =0
                        USER_article[i][k] +=1

        for test in test_users:
            if test not in USER_article:
                USER_article[test] = dict()

        #각 유저에 대해 읽은 작가와 그 작가의 어떤 글을 읽었는지 확인
        user_writer_count = dict()
        for k,v in USER_article.items():
            user_writer_count[k] = dict()
            for key, value in v.items():
                a = key.split('_')
                try:
                    user_writer_count[k][a[0]].append(key)
                except:
                    user_writer_count[k][a[0]] = []
                    user_writer_count[k][a[0]].append(key)

        #user_writer_count 를 독자가 가장 많은 글을 읽은 작가 순으로 정렬
        new_user_writer_count = dict()
        for i,j in user_writer_count.items():
            new_user_writer_count[i] = []
            for k,v in j.items():
                length = [len(v)] + v
                #print(length)
                new_user_writer_count[i].append(length)
            new_user_writer_count[i] = sorted(new_user_writer_count[i], key = operator.itemgetter(0),reverse = True)
       
        #가장 인기있는 글을 확인하기 위해/전체기간동안의 독자의 글 방문 count
        path4 = './user_json2.txt'

        read2 = {}
        with open(path4,'r') as F:
            for x in F:
                x = ujson.loads(x)
                for k,v in x.items():
                    for q,w in v.items():
                        try:
                            read2[q] += w
                        except:
                            read2[q] = 0
                            read2[q] += w
        
        #가장 많이 읽힌 글 순서대로 정렬
        Total = sorted(read2.items(), reverse=True,key=lambda t : (t[1],t[0]))
        Total2 = []

        for t in Total:
            Total2.append(t[0])    
        
        #following 한 작가가 있는지 확인
        file = r'./res/users.json'
        following_list = dict()
        with open(file,'r') as fp:
            for line in fp:
                line = ujson.loads(line)
                following_list[line['id']] = line['following_list']
                
        #삭제된 글 확인
        delete_article_check = dict()
        file = r'./res/metadata.json'
        with open(file,'r') as fp:
            for i in fp:
                i = ujson.loads(i)
                delete_article_check[i["id"]] = True

        with open(out_path,'w') as fp:
            for n_count ,dev in enumerate(result_users):
                person = []
                total_count = 0
                print(dev,file = fp,end = ' ')
                
                #1. 내가 읽은 글 번호 앞/뒤 글 추천
                try:
                    read_list = new_user_writer_count[dev]
                    for read in read_list:
                        range_check = [0 for i in range(10000)]
                        Min = 10000
                        Max = 0

                        if read[0] > 0:
                            for Range in read[1:]:
                                split_str = Range.split('_')
                                writer = split_str[0]
                                I = int(split_str[1])
                                range_check[I] = 1
                                if I < Min:
                                    Min = I
                                if I > Max:
                                    Max = I
                            if Min == 1:
                                Min = 3

                            for add in range(Max+1, Min-2,-1):
                                add_list = range_check[add]
                                down1 = range_check[add-1]
                                down2 = range_check[add-2]
                                up1 = range_check[add+1]
                                up2 = range_check[add+2]
                                Article = writer + '_' + str(add)
                                if (add_list == 0) and (Article not in person) and (self.check_delete(delete_article_check, Article)) and self.inRange(down1,down2, up1, up2):
                                    total_count+=1
                                    person.append(Article)                            
                                    if total_count ==100:
                                        break
                            
                            if total_count == 100:
                                break   
                except:
                    pass
                
                if total_count == 100:
                    for n,peo in enumerate(person):
                        if n !=99:
                            print(peo,file = fp, end=' ')
                        if n == 99:
                            print(peo,file = fp)
                            break
                    continue
                                        
                #2. 내가 팔로잉한 작가의 인기글 추천 
                if (total_count <100) and (dev in following_list) and (len(following_list[dev]) >0):
                    w_List = following_list[dev] 
                    R = 15
                    for w in w_List:
                        try:
                            pop_read =article2[w] #해당 작가가 쓴 글, 조회수가 많은 순서대로
                        except:
                            continue
                        cc = 0
                        for i in pop_read:
                            if i[0] not in person and self.check_delete(delete_article_check, i[0]) and (i[0] not in USER_article[dev]):
                                total_count +=1
                                if total_count <100:
                                    #print(i[0],file = fp, end=' ')
                                    person.append(i[0])
                                else:
                                    #print(i[0],file = fp)       
                                    person.append(i[0])
                                if total_count == 100:
                                    break                        
                                cc+=1
                                if cc == R:
                                    break
                        if total_count == 100:
                                    break
                    if total_count < 100:
                        index = 0
                        for i in Total2:
                            if (i not in person) and (self.check_delete(delete_article_check, i)) and (i not in USER_article[dev]):
                                if index != (99-total_count):
                                    #print(i,file=fp,end=' ')
                                    person.append(i)
                                    index +=1
                                elif index == (99-total_count):
                                    #print(i,file = fp)
                                    person.append(i)
                                    break

                 #3. 모든 사람이 가장 많이 읽은 글 추천  / 기간 수정 :  전체기간 -> 2.22~3.1   
                if total_count < 100:  
                    index = 0
                    for i in Total2:
                        if (index !=99) and (i not in person) and (i not in USER_article[dev]):
                            #print(i,file = fp, end=' ')
                            person.append(i)
                            index+=1
                        elif (index == 99) and (i not in person) and (i not in USER_article[dev]):
                            #print(i,file = fp)
                            person.append(i)
                            break

                for n,peo in enumerate(person):
                    if n !=99:
                        print(peo,file = fp, end=' ')
                    if n == 99:
                        print(peo,file = fp)
                        break

if __name__ == '__main__':
    fire.Fire(Recommendation)
