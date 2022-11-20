import logging
from requests import RequestException
from exceptions import ParserFindTagException
from constants import EXPECTED_STATUS


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def clear_list(list_):
    n = 0
    for i in list_:
        if i == '\n':
            del list_[n]
        n += 1


def status_matching(dl_status, preview_status, link):
    if preview_status:
        if dl_status not in EXPECTED_STATUS[preview_status]:
            logging.info(f'''Несовпадающие статусы:
            {link}
            Статус в карточке: {dl_status}
            Ожидаемые статусы: {EXPECTED_STATUS[preview_status]}''')
