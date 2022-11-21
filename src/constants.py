from pathlib import Path
from urllib.parse import urljoin

BASE_DIR = Path(__file__).parent
MAIN_DOC_URL = 'https://docs.python.org/3/'
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')
DOWLANDS_URL = urljoin(MAIN_DOC_URL, 'download.html')
MAIN_PEP_8 = 'https://peps.python.org/'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_DIR = BASE_DIR / 'logs'
RESULT_DIR = 'results'
TAG_SECTION = 'section'
TAG_DIV = 'div'
TAG_TABLE = 'table'


EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
