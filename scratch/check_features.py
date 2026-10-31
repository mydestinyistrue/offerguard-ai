import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = 'https://www.clean_design.cloud/assets/index-BPe6nzEI.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

matches = [m.start() for m in re.finditer(r'features', js, re.I)]
print('Matches count:', len(matches))
for m in matches:
    sub = js[m-50:m+200]
    if 'section' in sub or 'grid' in sub:
        print('--- MATCH AT', m, '---')
        print(js[m-100:m+2500])
        break
