import requests
from bs4 import BeautifulSoup
import os
import errno
import re
import sys


def get_sections(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            sections = soup.find_all("section")
    except Exception as e:
        print(str(e))
    finally:
        return sections


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


def get_books(path):
    for url in get_sections('https://www.oreilly.com/free/reports.html'):
        directory = path + '\\' + url['id']
        url = "https://www.oreilly.com/" + url['id'] + "/free"
        for section in get_sections(url):
            for book in section.find_all('a'):

                # very specific usecase with first link, http is missing
                if not book['href'].startswith('http:'):
                    book['href'] = "http:" + book['href']

                book['href'] = book['href'].replace('.csp', '.pdf').replace('/free/', '/free/files/')
                book['title'] = re.sub('[^\\w\\s-]', '', book['title']).strip()
                book['title'] = re.sub('[-\\s]+', '_', book['title'])

                location = directory + '\\' + section['id'] if section.has_attr('id') else directory
                make_dir(location)
                location += '\\' + book['title'] + '.pdf'
                download_pdf(book['href'], location)


def main():
    path = sys.argv[1]
    make_dir(path)
    get_books(path)


if __name__ == "__main__":
    main()