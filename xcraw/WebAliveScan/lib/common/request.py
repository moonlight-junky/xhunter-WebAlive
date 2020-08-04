# encoding: utf-8
from gevent import monkey, pool; monkey.patch_all()
from lib.utils.FileUtils import *
import config
import chardet
import time
import urllib3
from bs4 import BeautifulSoup
from lib.utils.tools import get
urllib3.disable_warnings()


class Request:
    def __init__(self, target, port, output, wappalyzer):
        self.output = output
        self.wappalyzer = wappalyzer
        self.url_list = self.gen_url_list(target, port)
        self.total = len(self.url_list)
        self.output.config(config.threads, self.total)
        self.output.target(target)
        self.index = 0
        self.alive_path = config.result_save_path.joinpath('alive_results.csv')
        self.brute_path = config.result_save_path.joinpath('brute_results.csv')
        self.alive_result_list = []
        self.main()

    def gen_url_by_port(self, domain, port):
        protocols = ['http://', 'https://']
        if port == 80:
            url = f'http://{domain}/'
            return url
        elif port == 443:
            url = f'https://{domain}/'
            return url
        else:
            url = []
            for protocol in protocols:
                url.append(f'{protocol}{domain}:{port}/')
            return url

    def gen_url_list(self, target, port):
            # 获取端口
            ports = set()
            if isinstance(port, set):
                ports = port
            elif isinstance(port, list):
                ports = set(port)
            elif isinstance(port, tuple):
                ports = set(port)
            elif isinstance(port, int):
                if 0 <= port <= 65535:
                    ports = {port}
            elif port in {'default', 'small', 'medium', 'large'}:
                ports = config.ports.get(port)
            if not ports:  # 意外情况
                ports = {80}

            # 生成URL
            url_list = []
            domain_list = []
            domain_list.append(target)
            for domain in domain_list:
                domain = domain.strip()
                if ':' in domain:
                    domain, port = domain.split(':')
                    url = self.gen_url_by_port(domain, int(port))
                    if isinstance(url, list):
                        url_list = url_list + url
                    else:
                        url_list.append(url)
                else:
                    for port in ports:
                        url = self.gen_url_by_port(domain, int(port))
                        if isinstance(url, list):
                            url_list += url
                        else:
                            url_list.append(url)
            return url_list

    def request(self, url):
        try:
            r, html = get(url, allow_redirects=config.allow_redirects)
            url_info = self.analysis_response(url, r, html)
            if url_info:
                self.output.statusReport(url_info)
            else:
                raise Exception
            self.alive_result_list.append(url_info)
            return r,
        except Exception as e:
            return e
        finally:
            self.index = self.index + 1
            self.output.lastPath(url, self.index, self.total)
            return

    def get_cookies(self):
        cookies = {'rememberMe': 'test'}
        return cookies

    def get_title(self, markup):
        """
        获取标题
        :param markup: html标签
        :return: 标题
        """
        soup = BeautifulSoup(markup, 'lxml')

        title = soup.title
        if title:
            return title.text

        h1 = soup.h1
        if h1:
            return h1.text

        h2 = soup.h2
        if h2:
            return h2.text

        h3 = soup.h3
        if h2:
            return h3.text

        desc = soup.find('meta', attrs={'name': 'description'})
        if desc:
            return desc['content']

        word = soup.find('meta', attrs={'name': 'keywords'})
        if word:
            return word['content']

        text = soup.text
        if len(text) <= 200:
            return text
        return ''

    def analysis_response(self, url, response, html):
        if response.status_code in config.ignore_status_code:
            return None
        title = self.get_title(html).strip().replace('\r', '').replace('\n', '')
        status = response.status_code
        size = FileUtils.sizeHuman(len(response.text)).strip()

        soup = BeautifulSoup(html, "html.parser")
        scripts = [script['src'] for script in soup.findAll('script', src=True)]
        meta = {
            meta['name'].lower():
                meta['content'] for meta in soup.findAll(
                'meta', attrs=dict(name=True, content=True))
        }
        detected_apps = self.wappalyzer.analyze(response.url, html, response.headers, scripts, meta)
        application = detected_apps.get('Application') if detected_apps.get('Application') else []
        server = detected_apps.get('Server') if detected_apps.get('Server') else []
        language = detected_apps.get('Language') if detected_apps.get('Language') else []
        frameworks = detected_apps.get('Frameworks') if detected_apps.get('Frameworks') else []
        system = detected_apps.get('System') if detected_apps.get('System') else []
        redirect = response.url if url != response.url else ''
        return {'url': url, 'title': title, 'status': status, 'size': size, 'application': application,
                'server': server, 'language': language, 'frameworks': frameworks, 'system': system,
                'redirect': redirect}

    def main(self):
        gevent_pool = pool.Pool(config.threads)
        while self.url_list:
            tasks = [gevent_pool.spawn(self.request, self.url_list.pop())
                     for i in range(len(self.url_list[:config.threads*10]))]
            for task in tasks:
                task.join()
            del tasks

