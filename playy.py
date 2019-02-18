import urllib.request

response = urllib.request.urlopen('http://www.baidu.com')
html = response.read().decode('utf-8')
print(html)