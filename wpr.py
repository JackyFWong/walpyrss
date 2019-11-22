import feedparser as fp
from bs4 import BeautifulSoup
import random
import urllib
import subprocess
import sys
from PIL import ImageFile

# rss url
RSSURL = "https://www.reddit.com/r/moescape/top.rss?t=month"
WIDTH = 1920
HEIGHT = 1080

def get_img():
    return fp.parse(RSSURL)

def img_size(img_url):
    file = urllib.request.urlopen(img_url)
    size = file.headers.get("content-length")
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return p.image.size
            break
    file.close()
    return None

if __name__ == '__main__':
    all_img = []

    posts = get_img().entries
    for entry in posts:
        post_content = entry['content'][0]
        link = BeautifulSoup(post_content['value'], features="html5lib").span
        cur_url = link.find("a")["href"]
        cur_img_size = img_size(cur_url)

        if (cur_img_size == None):
            continue

        if (cur_img_size[0] >= WIDTH and cur_img_size[1] >= HEIGHT):
            if (float(cur_img_size[0]) / float(cur_img_size[1]) >= 1):
                all_img.append(cur_url)

    if (len(all_img) < 1):
        sys.exit(1)

    random.seed(random.randint(0, 100))
    final_img = all_img[random.randrange(len(all_img))]
    urllib.request.urlretrieve(final_img, "wall")

    subprocess.run(["feh", "--bg-fill", "wall"])
