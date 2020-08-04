from lib.common.output import Output
import config
import random
import requests
import custom


def fake_ua():
    ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'
    ]
    return random.choice(ua_list)


def fake_ip():
    a = str(int(random.uniform(1, 255)))
    b = str(int(random.uniform(1, 255)))
    c = str(int(random.uniform(1, 255)))
    d = str(int(random.uniform(1, 255)))
    ip = a + "." + b + "." + c + "." + d
    return ip


def get(url, headers=None, allow_redirects=True, fake=False):
    try:
        if headers:
            headers.update(custom.headers)
        else:
            headers = custom.headers
        if fake:
            ip = fake_ip()
            ua = fake_ua()
            headers['X-Forwarded-For'] = ip
            headers['X-Forwarded-Host'] = ip
            headers['X-Client-IP'] = ip
            headers['X-remote-IP'] = ip
            headers['X-remote-addr'] = ip
            headers['True-Client-IP'] = ip
            headers['X-Client-IP'] = ip
            headers['Client-IP'] = ip
            headers['X-Real-IP'] = ip
            headers['User-Agent'] = ua
        cookies = custom.cookies
        params = custom.params
        r = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False, allow_redirects=allow_redirects, timeout=config.timeout)
        try:
            html = r.content.decode(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                html = r.content.decode(encoding='gbk')
            except UnicodeDecodeError:
                html = r.text
        return [r, html]
    except Exception as e:
        return e


def save_result(path, headers, results):
    data = ','.join(headers)
    data += '\n'
    for i in results:
        line = ''
        for h in headers:
            line += '"'+str(i[h]).replace('"', '""')+'",'
        data += line.strip(',') + '\n'
    try:
        with open(path, 'w', errors='ignore', newline='') as file:
            file.write(data)
            return True
    except TypeError:
        with open(path, 'wb') as file:
            file.write(data.encode())
            return True
    except Exception as e:
        Output().error(e.args)
        return False