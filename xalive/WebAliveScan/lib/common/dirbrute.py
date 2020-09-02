# encoding: utf-8
from concurrent.futures import ThreadPoolExecutor
from gevent import pool, monkey, Timeout;

monkey.patch_all()
import urllib3
import random
import json
import chardet
from lib.utils.FileUtils import *
from lib.utils.tools import *
from urllib.parse import urlparse
from os import path

urllib3.disable_warnings()


class Dirbrute:
    def __init__(self, alive_list, output, wappalyzer):
        self.alive_list = alive_list
        self.output = output
        self.wappalyzer = wappalyzer
        self.all_rules = self.get_all_rules()
        self.scan_url_list = self.get_scan_url_list()
        self.index = 1
        self.total = len(self.scan_url_list)
        self.brute_result_list = []

    def format_url(self, url, p):
        if url.endswith('/'):
            url = url.strip('/')
        if not p.startswith('/'):
            p = '/' + p
        return url + p

    def get_scan_url_list(self):
        scan_url_list = []
        for alive in self.alive_list:
            for p, rule in self.all_rules:
                if alive.get('redirect'):
                    origin = urlparse(alive['url'])
                    redirect = urlparse(alive['redirect'])
                    if (origin.netloc == redirect.netloc) and (
                            path.dirname(origin.path) != path.dirname(redirect.path)):
                        redirect_url = path.dirname(alive['redirect']) + '/'
                        scan_url_list.append({'url': self.format_url(redirect_url, p), 'rule': rule})
                scan_url_list.append({'url': self.format_url(alive['url'], p), 'rule': rule})
        return scan_url_list

    def get_all_rules(self):
        all_rules = []
        f = open(config.realpath.joinpath('rules.json'), encoding='utf-8')
        rules = json.load(f)
        for name, app in rules.items():
            for p in app['paths']:
                mode = 'AND' if app.get('mode') == 'AND' else 'OR'
                rule = {'status': app.get('status'), 'headers': app.get('headers'), 'html': app.get('html'),
                        'mode': mode, 'application': name}
                self.wappalyzer.prepare_app(rule)
                all_rules.append((p, rule))
        return all_rules

    def brute(self, scan_url):
        url = scan_url['url']
        rule = scan_url['rule']
        headers = {'Connection': 'Keep-Alive', 'Range': 'bytes=0-102400'}
        try:
            r, html = get(url, allow_redirects=False, fake=True)
            if r.status_code in [206, rule.get('status')]:
                status = r.status_code
                size = FileUtils.sizeHuman(len(r.text)).strip()
                response_info = {'url': url, 'html': html, 'headers': r.headers, 'scripts': '', 'meta': ''}
                if self.wappalyzer.has_app(rule, rule['mode'], response_info):
                    url_info = {'url': url, 'size': size, 'status': status, 'application': [rule['application']]}
                    self.output.statusReport(url_info)
                else:
                    raise Exception
                self.brute_result_list.append(url_info)
        except Exception as e:
            return e
        finally:
            self.output.lastPath(url, self.index, self.total)
            self.index = self.index + 1
            return

    def run(self):
        random.shuffle(self.scan_url_list)
        # gevent_pool = pool.Pool(config.threads)
        gevent_pool = pool.Pool(config.threads)
        while self.scan_url_list:
            tasks = [gevent_pool.spawn(self.brute, self.scan_url_list.pop())
                     for i in range(len(self.scan_url_list[:config.threads * 10]))]
            for task in tasks:
                try:
                    task.join(timeout=6)
                except Exception as e:
                    pass
            del tasks
        # random.shuffle(self.scan_url_list)
        # with ThreadPoolExecutor(config.threads) as pool:
        #     for scan_url in self.scan_url_list:
        #         pool.submit(self.brute, scan_url)
