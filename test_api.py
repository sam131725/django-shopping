import urllib.request
import urllib.error
import re

try:
    urllib.request.urlopen('http://localhost:8000/api/products/')
except urllib.error.HTTPError as e:
    html = e.read().decode('utf-8')
    with open('error.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Error saved to error.html")
