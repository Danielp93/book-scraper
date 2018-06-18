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
            books = ["https://goalkicker.com/" + x for x in soup.findAll("div", {"class", "bookContainer grow"})["href"]]
    except Exception as e:
        print(str(e))
    finally:
        return books


def get_url(book):
    return None


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
    print(get_books())


if __name__ == "__main__":
    main()