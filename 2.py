import asyncio
import aiohttp
import time

"""
Задание выполнено с использование MediaWiki Action API
https://www.mediawiki.org/wiki/API:Main_page
"""

url = "https://ru.wikipedia.org/w/api.php"

base_params = {
    'action':   'query',
    'format':   'json',
    'list':     'categorymembers',
    'cmtitle':  'Категория:Животные_по_алфавиту',
    'cmprop':   'title',
    'cmlimit':  '500',
}

pages_by_first_letter = {chr(i): 0 for i in range(1040, 1072)}  # Создание словаря с парами буква:кол-во


def binary_search(array, req_letter):
    """
    Бинарный поиск последней требуемой буквы в списке статей.
    :param array: список статей.
    :param req_letter: требуемая буква.
    :return: сколько раз эта буква встречается в списке.
    """
    if len(array) == 0:
        return 0
    if array[0]['title'][0] != req_letter:
        return 0
    elif array[-1]['title'][0] == req_letter:
        return len(array)

    search_start = 1
    search_end = len(array) - 1

    while search_start <= search_end:
        search_mid = (search_start + search_end) // 2
        if array[search_mid - 1]['title'][0] == req_letter:
            if array[search_mid]['title'][0] != req_letter:
                return search_mid
            else:
                search_start = search_mid + 1
        else:
            search_end = search_mid - 1

    return 0


async def request_by_first_letter(letter, session: aiohttp.ClientSession):
    """
    Отправляет запросы по выбранной букве.
    :param letter: буква русского алфавита, представленная в десятичном формате по юникоду.
    :param session: объект сессии
    """
    req_letter = chr(letter)
    # next_letter = chr(letter+1) if letter != 1071 else chr(65)
    page = 1
    cmcontinue = False
    while True:
        # print(f'запрос: {req_letter} страница: {page}')
        params = {
            **base_params,
            'cmstartsortkeyprefix': req_letter,
            # 'cmendsortkeyprefix': next_letter,  # К сожаления этот параметр не работает корректно
        }

        if cmcontinue:
            params['cmcontinue'] = cmcontinue

        response = await (await session.get(url, params=params)).json()

        pages = binary_search(response['query']['categorymembers'], req_letter)
        pages_by_first_letter[req_letter] += pages

        if pages < len(response['query']['categorymembers']):
            break

        if 'continue' in response:
            cmcontinue = response['continue']['cmcontinue']
            page += 1
        else:
            break
    # print(f'запрос по букве {req_letter} завершён')


async def main():
    """
    Отправка асинхронных запросов по каждой первой букве статей.
    """
    async with aiohttp.ClientSession() as session:
        requests_by_letter = []
        for i in range(1040, 1072):
            requests_by_letter.append(request_by_first_letter(i, session))
        await asyncio.gather(*requests_by_letter)


if __name__ == '__main__':
    start = time.time()

    asyncio.run(main())
    for pair in pages_by_first_letter.items():
        print(f'{pair[0]}: {pair[1]}')

    end = time.time()
    delta = end-start
    print(f'Время отработки скрипта: {delta}')
