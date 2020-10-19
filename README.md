# xhunter-WebAlive
分布式web资产发现


# Usage:

windows:

 celery -A xalive.app worker -n xalive.%h -Q ascan -l info -P eventlet
 
 celery -A xalive.app worker -n xalive.%h -Q save -l info -P eventlet
 
 python3 start.py
 
Linux:

 celery -A xalive.app worker -n xalive.%h -Q ascan -l info -Ofair
 
 celery -A xalive.app worker -n xalive.%h -Q save -l info -Ofair
 
 python3 start.py
 
# readme

使用时需修改start.py中节点的值，十一结束后有空会写具体分布式搭建与使用方式

 results.csv会生成在start.py同目录下
 
 修改task.py中参数可修改扫描参数
 
 默认为 webscan.py --target ip --port large --brute True
 
 具体参数见\xalive\WebAliveScan\readme.md

 修改\xalive\WebAliveScan\config.py可修改线程数等参数
 
 # Todo
 
  对接子域名扫描
  
  对接fofa api查询
