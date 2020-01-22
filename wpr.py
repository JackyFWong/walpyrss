import feedparser as fp
from bs4 import BeautifulSoup
import random
import urllib
import subprocess
import sys
from PIL import ImageFile
import argparse
import os

WIDTH = 1920
HEIGHT = 1080

def get_img(rss_url):
    return fp.parse(rss_url)

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

def get_url(args):
    rss_url = ""

    if (args.order[0] and args.duration[0]):
        rss_url = (
            f"https://www.reddit.com/r/{args.subr}/{args.order[0]}.rss"
            f"?t={args.duration[0]}"
        )
    elif (args.order[0]):
        rss_url = f"https://www.reddit.com/r/{args.subr}/{args.order[0]}.rss"
    elif (args.duration[0]):
        rss_url = (
            f"https://www.reddit.com/r/{args.subr}/top.rss"
            f"?t={args.duration[0]}"
        )
    else:
        rss_url = f"https://www.reddit.com/r/{args.subr}/.rss"

    return rss_url

if __name__ == '__main__':
    # argparse setup
    parser = argparse.ArgumentParser(description="""Sets your wallpaper 
        to a random image from a subreddit.""")
    parser.add_argument('subr', help="subreddit to pull image from")
    parser.add_argument('-o', '--order', help="subreddit sorting order", 
        nargs=1, choices=["hot", "top", "new"], default=[False])
    parser.add_argument('-d', '--duration', help="subreddit post duration", 
        nargs=1, choices=["day", "week", "month", "year", "all"], 
        default=[False])

    env_group = parser.add_mutually_exclusive_group(required=True)
    env_group.add_argument('--feh', action='store_true', 
        help="use feh for wallpaper setting")
    env_group.add_argument('--plasma', action='store_true', 
        help="for KDE Plasma DEs")

    args = parser.parse_args()
    rss_url = get_url(args)

    print(rss_url)

    all_img = []
    posts = get_img(rss_url).entries
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
        print("No images with specified parameters found.")
        sys.exit(1)

    print(all_img)

    random.seed(random.randint(0, 100))
    final_img = all_img[random.randrange(len(all_img))]
    print(final_img)
    urllib.request.urlretrieve(final_img, "wall")

    # feh
    if (args.feh):
        print("Using feh")
        subprocess.run(["feh", "--bg-fill", "wall"])

    # plasma
    elif (args.plasma):
        print("Using Plasma script")
        cwd = os.getcwd()
        img_path = f"{cwd}/wall"
        print(img_path)
        subprocess.run(["bash", "./plasma_change.sh", img_path])
