import re
import logging
from collections import Counter
from urllib.parse import urljoin
from constants import BASE_DIR, MAIN_DOC_URL, MAIN_PEP_8, STATUS_DT
from requests_cache import CachedSession
from bs4 import BeautifulSoup
from tqdm import tqdm
from outputs import control_output

from config import configure_argument_parser, configure_logging
from utils import get_response, find_tag, clear_list, status_matching


def whats_new():
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    session = CachedSession()
    get_response(session, whats_new_url)
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})

    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})

    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'})

    # print(sections_by_python[0].prettify())
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        # print(version_link)

        response = session.get(version_link)

        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(h1, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )

        return results


def latest_versions():
    session = CachedSession()
    response = get_response(session, MAIN_DOC_URL)
    soup = BeautifulSoup(response.text, features='lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не найдено')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )

    return results


def download():
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    session = CachedSession()
    response = get_response(session, downloads_url)
    soup = BeautifulSoup(response.text, features='lxml')
    div_main = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(div_main, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    arhive_url = urljoin(downloads_url, pdf_a4_link)
    filename = arhive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    response = session.get(arhive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep():
    session = CachedSession()
    response = get_response(session, MAIN_PEP_8)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features='lxml')
    section_pep_contant = find_tag(soup, 'section', {'id': 'pep-content'})
    # нашли все таблицы в section_pep_contant 10 таблиц.
    div_table_wrapper = section_pep_contant.find_all(
        'table', class_='pep-zero-table docutils align-default')
    # перебараем первую таблицу [:1]
    counter_status = []
    result = [('Статус', 'Количество')]
    for table in tqdm(div_table_wrapper, desc='Получаем ссылки PEP'):
        # нашли все строки таблиц.
        rows = table.find_all('tr')
        for link in rows:
            # находим первый тег а
            status = link.find('abbr')
            href_pep = link.find('a')
            if href_pep:
                # получили из тега a, href создали ссылку.
                if status:
                    preview_status = status.text[1:]
                else:
                    preview_status = ''
                # preview_type = status.text[0:1]
                link_pep = urljoin(MAIN_PEP_8, href_pep['href'])
                session = CachedSession()
                response = get_response(session, link_pep)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, features='lxml')
                section_main = find_tag(
                    soup, 'section', {'id': 'pep-content'})
                dl_list = list(find_tag(section_main, 'dl', {
                               'class': 'rfc2822 field-list simple'}))
                # Отчищаем список
                clear_list(dl_list)

                c = 0
                for i in dl_list:
                    if i.text == 'Status:':
                        # print(dl_list[c+1].text)
                        counter_status.append(dl_list[c+1].text)
                        status_matching(dl_list[c+1].text, preview_status)
                    c += 1

    # print(result)
    x = Counter(counter_status)
    for i in x:
        result.append(
            (i, x[i])
        )
    result.append(
        ('Total', sum(x.values()))
    )
    return result


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки {args}')
    session = CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode]()
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
