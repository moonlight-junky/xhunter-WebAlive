from celery.result import AsyncResult
from xcraw.tasks import save_results, send_request



save_results.delay("url,title,status,size,server,language,application,frameworks,system")
file = open("targets.txt")
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

for l in range(i):
	res=AsyncResult(reslist[l])
	result = res.get()
	print(datalist[l])
	if result==None:
		continue
	try:
		req = save_results.delay(result)
	except:
		pass
