import time

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
import asyncio
import aiohttp
from bs4 import BeautifulSoup

from pricechecker.models import Product, Price

URL = 'https://shop.samberi.com'

HEADERS = {
    'Accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.54 Safari/537.36'
}

async def get_products(url):
    connector = aiohttp.TCPConnector(limit=8, limit_per_host=8)
    async with aiohttp.ClientSession(connector=connector) as session:
        res = await session.get(url=url, headers=HEADERS)
        bs = BeautifulSoup(await res.text(), 'lxml')
        cats = [URL + cat.get('href') + '?SHOWALL_1=1'
                for cat in bs.find('ul', id='vertical-multilevel-menu')
                .find_all('a', class_='parent')] + \
               [
            #Костыль, не могу получить эти ссылки автоматически(
            'https://shop.samberi.com/catalog/aziya/?SHOWALL_1=1',
            'https://shop.samberi.com/catalog/sportivnye_tovary/?SHOWALL_1=1',
            'https://shop.samberi.com/catalog/upakovka/?SHOWALL_1=1'
        ]
        tasks = [parse_page(session, url) for url in cats]

        await asyncio.gather(*tasks)


async def parse_page(session, cat_url):
    async with session.get(url=cat_url, headers=HEADERS) as res:
        if res.status != 200:
            print(f'Статус: {res.status}\nСсылка: {cat_url}')
            await asyncio.sleep(3)
            await parse_page(session, cat_url)
        res_text = await res.text()
        pagebs = BeautifulSoup(res_text, 'lxml')
        products_on_page = pagebs.find_all('div', class_='product-item')
        for product in products_on_page:
            name = product.find('div', class_='product-item-title').text.strip()
            price = product.find('span', class_='product-item-price-current')\
                .text.strip().strip('₽').strip()

            prod, _ = await sync_to_async(Product.objects.get_or_create)(name=name, defaults={'name': name})
            await sync_to_async(Price.objects.create)(product_id=prod, price=float(price))


async def main():
    time_start = time.time()
    await get_products(URL)

    print(f'Время выполнения: {round(time.time()-time_start, 2)}')
    print('Dump to DB complete...')


class Command(BaseCommand):
    help = 'Parses data from Samberi shop and saves it to the database'

    def handle(self, *args, **options):
        #Эта строка - для Windows
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
