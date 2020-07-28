# xhunter-WebAlive
分布式web资产发现


# Usage:

windows:

 celery -A xcraw.app worker -n xcraw.%h -Q ascan -l info -P eventlet
 
 celery -A xcraw.app worker -n xcraw.%h -Q save -l info -P eventlet
 
 python3 start.py
 
Linux:

 celery -A xcraw.app worker -n xcraw.%h -Q ascan -l info
 
 celery -A xcraw.app worker -n xcraw.%h -Q save -l info
 
 python3 start.py
 
# readme

 results.txt会生成在start.py同目录下
 
 修改task.py中参数可修改扫描参数
 
 具体参数见\xcraw\WebAliveScan\readme.md
