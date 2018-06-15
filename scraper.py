import requests
from bs4 import BeautifulSoup
import os
import errno


def get_sections(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36 ',
    }
    try:
        response = requests.get(url, headers=headers)
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
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36 ',
        's_pers': '%20s_cc%3Dtrue%3B%20s_sq%3D%3B',
        's_sess': '%20s_cc%3Dtrue%3B%20s_sq%3D%3B'
    }
    response = requests.get(url, stream=True, headers=headers)
    handle = open(location, 'wb+')
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            handle.write(chunk)


def get_books(startingpage):
    for url in get_sections(startingpage):
        dir = os.getcwd() + '\\' + url['id']
        url = "https://www.oreilly.com/" + url['id'] + "/free"
        for section in get_sections(url):
            for book in section.find_all('a'):

                #very specific usecase with first link, http is missing
                if(not book['href'].startswith('http:')):
                    book['href'] = "http:" + book['href']


                book['href'] = book['href'].replace('.csp', '.pdf').replace('/free/', '/free/files/')
                book['title'] = book['title'].replace(' ', '_')\
                                             .replace(':', '_')\
                                             .replace('\'','')\
                                             .replace('?','')\
                                             .replace('/','')
                if section.has_attr('id'):
                    location = dir + '\\' + section['id']
                else:
                    location = dir
                make_dir(location)
                location += '\\' + book['title'] + '.pdf'
                print(book['href'] + ' : ' + location)
                download_pdf(url, location)

get_books('https://www.oreilly.com/free/reports.html')
