import urllib.request
import re

url = "https://edu-cycle-dztccfp3q-mistrykrish2005-1876s-projects.vercel.app/"
try:
    html = urllib.request.urlopen(url).read().decode('utf-8')
    images = re.findall(r'<img src="([^"]+)"', html)
    for img in images:
        if 'item_images' in img:
            print("Found image:", img)
except Exception as e:
    print("Error:", e)
