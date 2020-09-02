from celery.result import AsyncResult
from xalive.tasks import save_results, send_request
import time


save_results.delay("url,title,status,size,server,language,application,frameworks,system")
file = open("domain.txt")
result = ''


def ascan(data):
    resobj = send_request.delay(data)
    return resobj

i = 0
reslist = []
datalist = []
for url in file.readlines():
    data = url.strip('\n')
    resobj = ascan(data)
    reslist.append(resobj.id)
    datalist.append(data)
    i+=1
    if i >= 5:
        #扫描节点的数量+1
        flag = 0
        while flag == 0:
            time.sleep(1)
            for l in range(i):
                try:
                    if AsyncResult(reslist[l]).ready() == True:
                        flag = 1
                        break
                except:
                    pass
        #当有任务完成后退出循环
        res=AsyncResult(reslist[l])
        try:
            result = res.get()
            #获取返回值
        except:
            continue
        print(datalist[l])
        print(reslist[l])
        del reslist[l]
        del datalist[l]
        #删除对应的list值
        if result==None:
            continue
        try:
            req = save_results.delay(result)
            #返回值扔给save task
        except:
            pass
        i = i-1

for l in range(i):
    try:
        res=AsyncResult(reslist[l])
        result = res.get()
            #获取返回值
    except:
        continue
    print(datalist[l])
    print(reslist[l])
    if result==None:
        continue
    try:
        req = save_results.delay(result)
        #返回值扔给save task
    except:
        pass