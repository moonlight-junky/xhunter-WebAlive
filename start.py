from celery.result import AsyncResult
from xalive.tasks import save_results, send_request
import time

#定义节点数
EP0 = 4
save_results.delay("url,title,status,size,server,language,application,frameworks,system")
save_results.delay("url,status,size")
file = open("targets.txt")
result = ''


i = 0
reslist = []
datalist = []
urllist0 = []
urllist1 = []
for url in file.readlines():
    data = url.strip('\n')
	urllist0.append(data)


if(len(urllist0)< EP0*10):
	urllist1.append(urllist0+'\n')
else:
	flag = 0
	url0 = ''
	for urls in urllist0:
		url0 = url0 + urls + "\n"
		if flag == 9:
			urllist1.append(url0)
			url0 = ''
		flag = flag +1
	if url0 != '':
		urllist1.append(url0)
		url0 = ''


for data in urllist1:
	#任务扔给request节点
    resobj = send_request.delay(data)
    reslist.append(resobj.id)
    datalist.append(data)
    i+=1
    if i >= EP0:
        #扫描节点的数量
        flag = 0
        while flag == 0:

			#每秒检查节点任务完成情况
            time.sleep(1)
            for l in range(i):
                try:
					#为true表示单个任务结束
                    if AsyncResult(reslist[l]).ready() == True:
                        flag = 1
                        break
                except:
                    pass

        #当有任务完成后退出循环并取结果
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



#当所有任务分配完后，等待最后的结果
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