import requests
from bs4 import BeautifulSoup
import os
import errno
import sys
from multiprocessing.pool import ThreadPool


def get_books():
    try:
        response = requests.get("https://goalkicker.com/")
        if response.status_code == 200:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            return ["https://goalkicker.com/" + x.a["href"] + "/" for x in soup.findAll("div", {"class", "bookContainer grow"})]
    except Exception as e:
        print(str(e))
        

def get_download(book_url):
    try:
        response = requests.get(book_url)
        if response.status_code == 200:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            return soup.find(id="frontpage").a["href"]
    except Exception as e:
        print(str(e))


def make_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


def download_pdf(url, location):
    try:
        response = requests.get(url, stream=True)
        handle = open(location, 'wb+')
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                handle.write(chunk)
    except Exception as e:
        print(str(e))


def main():
    pool = ThreadPool(10)
    tuples = pool.map(lambda x: (x, get_download(x)), get_books())
    pool.starmap(lambda x, y: download_pdf(x + y, sys.argv[1] + y), tuples)


if __name__ == "__main__":
    main()
