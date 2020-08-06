# xhunter-WebAlive
分布式web资产发现


# Usage:

注意: python版本需要是3.7/3.8

config.py与w.sh内的路径记得修改

windows:

 celery -A xcraw.app worker -n xcraw.%h -Q ascan -l info -P eventlet
 
 celery -A xcraw.app worker -n xcraw.%h -Q save -l info -P eventlet
 
 python3 start.py
 
Linux:

 celery -A xcraw.app worker -n xcraw.%h -Q ascan -l info
 
 celery -A xcraw.app worker -n xcraw.%h -Q save -l info
 
 python3 start.py
 
# readme

 results.csv会生成在start.py同目录下
 
 修改task.py中参数可修改扫描参数
 
 默认为 webscan.py --target ip --port large --brute True
 
 具体参数见\xcraw\WebAliveScan\readme.md

 修改\xcraw\WebAliveScan\config.py可修改线程数等参数
 
 # Todo
 
  对接子域名扫描
  
  对接fofa api查询
