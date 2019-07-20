import fire
import operator
import ujson
from preprocessing import make_user_json_file

class Recommendation(object) :
    USER = dict()
    article2 = dict()
    USER_writer2 = dict()
    USER_writer2_ver2 = dict()
    user_writer_count = dict()
    Total2 = []
    following_list = dict()
    delete_article_check = dict() # 여기에는 현재 존재하는 article이 들어감. 삭제되었으면 이 리스트에 없음
    
    def __init__(self):
        make_user_json_file()
    
    #삭제 리스트 확인
    def check_delete(self, x):
        try:
            A = self.delete_article_check[x]
            return True
        except:
            return False 

    def make_data(self) :
        article = dict()

        test_users = []
        path2 = './res/predict/' + 'test.users.txt'
        with open(path2,'r') as test:
            for line in test:
                line = line.rstrip()
                test_users.append(line)

        #test 유저가 전체 기간동안 읽은 글 확인
        file_path = 'user_json.txt'
        with open(file_path,'r') as file_name:
            for users in file_name:
                users = ujson.loads(users)
                for key, values in users.items():
                    if key in test_users:                    
                        for k,v in values.items():
                            try:
                                self.USER[key].append(k)
                            except:
                                self.USER[key] = []
                                self.USER[key].append(k)
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

        for k,v in article.items():
            self.article2[k] = []
            for a,b in v.items():
                self.article2[k].append((a,b))

        for k,v in self.article2.items():
            v =  sorted(v, key=operator.itemgetter(1), reverse=True)
            self.article2[k] = v

        USER_writer = dict()
        for i,j in self.USER.items():
            USER_writer[i] = dict()
            for k in j:
                a = k.split('_')
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

        for k,v in USER_writer.items():
            self.USER_writer2[k] = []
            for a,b in v.items():
                self.USER_writer2[k].append((a,b))

        #정렬/ 많이 읽은 작가 순서대로 정렬
        for k,v in self.USER_writer2.items():
            v =  sorted(v, key=operator.itemgetter(1), reverse=True)
            self.USER_writer2[k] = v
            
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
                a = k.split('_')
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
        
        for k,v in USER_writer_ver2.items():
            self.USER_writer2_ver2[k] = []
            for a,b in v.items():
                self.USER_writer2_ver2[k].append((a,b))

        #정렬
        for k,v in self.USER_writer2_ver2.items():
            v =  sorted(v, key=operator.itemgetter(1), reverse=True)
            self.USER_writer2_ver2[k] = v
                
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

        #각 유저에 대해 읽은 작가와 그 작가의 어떤 글을 읽었는지 확인
        for k,v in USER_article.items():
            self.user_writer_count[k] = dict()
            for key in v.items():
                a = key.split('_')
                try:
                    self.user_writer_count[k][a[0]].append(key)
                except:
                    self.user_writer_count[k][a[0]] = []
                    self.user_writer_count[k][a[0]].append(key)

        #가장 인기있는 글을 확인하기 위해/전체기간동안의 독자의 글 방문 count
        path4 = 'user_json.txt'

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
        Total = sorted(read2.items(), reverse=True,key=lambda t : t[1])

        for t in Total:
            self.Total2.append(t[0])
        
        #following 한 작가가 있는지 확인
        file = r'users.json.txt'

        with open(file,'r') as fp:
            for line in fp:
                line = ujson.loads(line)
                self.following_list[line['id']] = line['following_list']
                
        #삭제된 글 확인
        file = r'metadata.json.txt'
        with open(file,'r') as fp:
            for i in fp:
                i = ujson.loads(i)
                self.delete_article_check[i["id"]] = True
              
    def recommend(self, userlist_path, out_path):
        users = [u.strip() for u in open(userlist_path)]
        self.make_result(out_path, users)


    def make_result(self, out_path, users) :
        with open(out_path,'w') as fp:
            for n_count ,dev in enumerate(users):
                person = []
                total_count = 0
                print(dev,file = fp,end = ' ')
                
                #1. 내가 읽은 글 번호 앞/뒤 글 추천
                try:
                    read_list = self.user_writer_count[dev]
                    for key, value in read_list.items():

                        if len(value) > 1:
                            for i in value:
                                ww = i.split('_')
                                down = ww[0] + '_' +str(int(ww[1])-1)
                                up = ww[0] + '_' +str(int(ww[1])+1)
                                up2 = ww[0] + '_' +str(int(ww[1])+2)
                                if (down not in value) and ((int(ww[1])-1) != 0) and (down not in person) and check_delete(down):
                                    total_count +=1
                                    if total_count < 100:                                
                                        person.append(down)
                                    else:
                                        person.append(down)
                                        break
                                if (up not in value) and (up2 not in value) and (up not in person) and check_delete(up): #중복체크 237, 239 일 경우 238을 한 번만 세도록
                                    total_count +=1
                                    if total_count < 100:           
                                        person.append(up)
                                    else:
                                        person.append(up)
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
                                        
                #2. 내가 읽은 작가 리스트 중 많이 읽은 순서대로 추천/기간:2/14~3/1
                if dev in self.USER_writer2_ver2:
                    w_List = self.USER_writer2_ver2[dev] # 내가 읽은 작가 리스트_많이 읽은 순서대로
                    R = 15
                    for w in w_List:
                        pop_read = self.article2[w[0]] #해당 작가가 쓴 글, 조회수가 많은 순서대로
                        cc = 0
                        for i in pop_read:
                            if (i[0] not in self.USER[dev]) and (i[0] not in person) and self.check_delete(i[0]): #작가의 글 중 내가 안읽은 글을 추천
                                total_count +=1
                                if total_count <100:
                                    person.append(i[0])
                                else:
                                    person.append(i[0])
                                if total_count == 100:
                                    break                        
                                cc+=1
                                if cc == R:
                                    if R >1:
                                        R -=1
                                    break
                        if total_count == 100:
                                    break

                #3. 내가 읽은 작가 리스트 중 많이 읽은 순서대로 추천/기간:전체기간
                if (total_count < 100) and (dev in self.USER_writer2):
                    w_List = self.USER_writer2[dev] # 내가 읽은 작가 리스트_많이 읽은 순서대로
                    R = 15
                    for w in w_List:
                        pop_read = self.article2[w[0]] #해당 작가가 쓴 글, 조회수가 많은 순서대로
                        cc = 0
                        for i in pop_read:
                            if (i[0] not in self.USER[dev]) and (i[0] not in person) and self.check_delete(i[0]): #작가의 글 중 내가 안읽은 글을 추천
                                total_count +=1
                                if total_count <100:
                                    person.append(i[0])
                                else:
                                    person.append(i[0])
                                if total_count == 100:
                                    break                        
                                cc+=1
                                if cc == R:
                                    if R >1:
                                        R -=1
                                    break
                        if total_count == 100:
                                    break
                
                #4. 내가 팔로잉한 작가의 글 추천 
                if (total_count <100) and (dev in self.following_list) and (len(self.following_list[dev]) >0):
                    w_List = self.following_list[dev] 
                    R = 15
                    for w in w_List:
                        try:
                            pop_read =article2[w] #해당 작가가 쓴 글, 조회수가 많은 순서대로
                        except:
                            continue
                        cc = 0
                        for i in pop_read:
                            if i[0] not in person and self.check_delete(i[0]):
                                total_count +=1
                                if total_count <100:
                                    person.append(i[0])
                                else:
                                    person.append(i[0])
                                if total_count == 100:
                                    break                        
                                cc+=1
                                if cc == R:
                                    if R >1:
                                        R -=1
                                    break
                        if total_count == 100:
                                    break
                    if total_count < 100:
                        index = 0
                        for i in self.Total2:
                            if (i not in person) and (self.check_delete(i)):
                                if index != (99-total_count):
                                    person.append(i)
                                    index +=1
                                elif index == (99-total_count):
                                    person.append(i)
                                    break
                                    
                #5. 모든 사람이 가장 많이 읽은 글 추천                   
                if total_count < 100:  
                    index = 0
                    for i in self.Total2:
                        if (index !=99) and (i not in person):
                            person.append(i)
                            index+=1
                        elif (index == 99) and (i not in person):
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
