#!/usr/bin/env python3
from bs4 import BeautifulSoup
from getpass import getpass
from pathlib import Path
import sys
import configparser
import asyncio
import aiohttp

async def get_session_info():
    try: 
        config = configparser.ConfigParser()
        config.read('config.ini')
        token = config.get("packt", "PACKT_SESSION_TOKEN") 
        username = config.get("packt", "PACKT_USERNAME") 
        password = config.get("packt", "PACKT_PASSWORD") 
        if not token and username:
            if not password: 
                password = getpass("No packt password found, enter manually: ") 
            payload = {
                'username': username,
                'password': password 
            }
            async with aiohttp.request('POST', 'https://services.packtpub.com/auth-v1/users/tokens', json=payload) as resp:
                token = (await resp.json())['data']['access']
        else:
            print("Please configure config.ini, see config.ini.example")
        
        cookies = ({ "access_token_live" : token })
        headers = ({ "authorization" : f'Bearer {token}' })

        return { 'cookies': cookies, 'headers': headers }
    except Exception as e:
        print(str(e))

async def get_book_info(s):
    try:
        async with s.get("https://services.packtpub.com/entitlements-v1/users/me/products") as resp:
            books = (await resp.json())['data']
            return [ { 'id' : x['productId'], 'name' : x['productName'] } for x in books ]
    except Exception as e:
        print(str(e))

async def get_book_pdf(s, book, location):
    try:
        async with s.get(f'https://services.packtpub.com/products-v1/products/{book["id"]}/files/pdf') as resp:
            book_location_url = (await resp.json())['data']
        async with s.get(book_location_url) as resp:
            with (location / f'{book["name"]}.pdf').open('wb+') as handle:
                async for (chunk, end) in resp.content.iter_chunks():
                    if end: 
                        break
                    handle.write(chunk)
    except Exception as e:
        print(str(e))

async def main():
    if len(sys.argv) > 1:
        location = Path(sys.argv[1])
        print(f'downloading books to {location}')
    else:
        print('No directory passed, will download to ./packt.d/{book}')
        location = Path('./packt.d')
    location.mkdir(parents=True, exist_ok=True)

    async with aiohttp.ClientSession(**(await get_session_info())) as s:
        books = await get_book_info(s)
        await asyncio.gather(*[get_book_pdf(s, book, location) for book in books])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
