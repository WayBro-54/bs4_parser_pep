from pathlib import Path
from urllib.parse import urljoin

BASE_DIR = Path(__file__).parent
MAIN_DOC_URL = 'https://docs.python.org/3/'
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')
DOWLANDS_URL = urljoin(MAIN_DOC_URL, 'download.html')
MAIN_PEP_8 = 'https://peps.python.org/'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
STATUS_DT = '<dt class="field-odd">Status<span class="colon">:</span></dt>'

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
