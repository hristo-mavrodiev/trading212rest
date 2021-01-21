import requests
from time import sleep
from trading212rest.logger import logger, logging

logger = logging.getLogger(__name__)

def get_request(url, headers, cookies):
    """
    Simple GET Request

    """
    logger.debug(f'Get Request on {url}')
    res = requests.get(url, 
                       headers = headers,
                       cookies = cookies)
    if res.status_code == requests.codes['ok']:
        logger.debug('Request code is ok......')
        return res.json()
    else:
        logger.warning(f'Request code not ok......{res.status_code} - {res.json()}')
        return None
