import requests
from bs4 import BeautifulSoup
import os
import errno
import re
import sys


def get_books():
    try:
        response = requests.get("https://goalkicker.com/")
        if response.status_code == 200:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            return soup.findAll("div", {"class", "bookContainer grow"})]
    except Exception as e:
        print(str(e))
        

def get_download(book_url):
    try:
        response = requests.get(book_url)
        if response.status_code == 200:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            return book_url + soup.find(id="frontpage").find('a')["href"]
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
    lambda x: download_pdf(get_download("https://goalkicker.com/" + x.a["href"]), path + x.a["href"])

if __name__ == "__main__":
    main()

# ["https://goalkicker.com/" + x.a["href"] for x in soup.findAll("div", {"class", "bookContainer grow"})]