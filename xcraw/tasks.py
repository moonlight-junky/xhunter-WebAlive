#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tasks.py
from xalive.app import app
from .config import WA_PATH, PY_PATH, RS_PATH
import requests
import os
import time
import simplejson
import subprocess
import warnings
warnings.filterwarnings(action='ignore')



# 需要使用一个装饰器，来管理该任务(函数)
@app.task
def save_results(request):
    print(request)
    try:
        f = open('result.csv','a')
        f.write(request + '\n')
    finally:
        f.close()
    return True




@app.task(time_limit=1800)
def send_request(target):
    cmd = ["/root/xhunter-WebAlive/xalive/w.sh",target]
    print(cmd)
    try:
        output = subprocess.check_output(cmd)
    except:
        return None
    results = ''
    with open(RS_PATH + '/results/alive_results.csv') as file:
        next(file)
        for line in file:
            results += line
    with open(RS_PATH + '/results/brute_results.csv') as f:
        next(f)
        for line1 in f:
            results += line1
    if results:
        try:
            return results
        except:
            return None
