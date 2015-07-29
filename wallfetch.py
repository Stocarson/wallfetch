#!/usr/bin/python3
import requests
import re
import urllib.request
import multiprocessing as mp
import argparse
from multiprocessing import Pool

def downloadAll():
    parameters = {"categories": "111", "purity": "110",
                  "sorting": "random", "order": "desc"}
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", nargs="?")
    parser.add_argument("-s", "--sfw", action="store_true",
                        help="show only safe for work wallpapers")
    args = parser.parse_args()
    if args.sfw:
        parameters["purity"] = "100"
    if args.keyword is not None:
        parameters["q"] = args.keyword
    sourceURL = "http://alpha.wallhaven.cc/search"
    response = requests.get(sourceURL, params=parameters)
    html = response.content.decode("utf-8")
    images = re.findall('data-wallpaper.id="(.*?)"', html)
    pool = Pool(processes=mp.cpu_count())
    pool.map(downloadImage, images)
 
def downloadImage(index):
    imageURL = "http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-"
    print("Downloading image no " + index)
    try:
        url = imageURL + index + ".jpg"
        userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
                "(KHTML, like Gecko) Ubuntu Chromium/43.0.2357.130 Chrome/43.0.2357.130 Safari/537.36"
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": userAgent}))
        f = open(index + ".jpg", "bw")
        f.write(r.read())
    except urllib.error.URLError:
        print("Cannot download image number " + index)
 
def main():
    downloadAll()
 
if __name__ == "__main__":
    main()
