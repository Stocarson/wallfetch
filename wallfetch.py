#!/usr/bin/python3
import requests
import re
import urllib
import multiprocessing as mp
import argparse
from multiprocessing import Process, Pool

def downloadAll():
    parameters = {"categories":"111", "purity":"110", "sorting":"random", "order":"desc"}
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", nargs = "?")
    parser.add_argument("--sfw", help = "show only safe for work wallpapers")
    args = parser.parse_args()
    if args.sfw:
        parameters[purity] = "100"
    if args.keyword is not None:
        parameters["q"] = args.keyword
    sourceURL = "http://alpha.wallhaven.cc/search"
    response = requests.get(sourceURL, params = parameters)
    html = response.content.decode("utf-8")
    images = re.findall('data-wallpaper.id="(.*?)"', html)
    pool = Pool(processes = mp.cpu_count())
    pool.map(downloadImage, images)
            
def downloadImage(index):
    imageURL = "http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-"
    print("Downloading image no "+index)
    try:
        r = urllib.request.urlopen(imageURL+index+".jpg")
        f = open(index+".jpg", "bw")
        f.write(r.read())
    except urllib.error.URLError:
        print("Cannot download image number "+index)

def main():
    downloadAll()

if __name__ == "__main__":
    main()
