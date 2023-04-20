from urllib3 import PoolManager
from logging import getLogger


log = getLogger('nova-api')


BASE = 'http://testing.euphoverse.moe'
log.info('API: {}'.format(BASE))
http = PoolManager()
default_headers = {}


def request(
    endpoint: str,
    method: str = 'GET',
    params: dict = {},
    headers: dict = default_headers,
    body = None
) -> tuple:
    log.debug('Request {}'.format(endpoint))

    r = http.request(
        BASE + endpoint, method=method,
        params=params, headers=headers, body=body
    )

    if r.status != 200:
        log.error('Request {} failed ({})'.format(endpoint, r.status))
        return r.status, r.json()

    log.debug('Request {} succeeded')
    return r.status, r.json()


class API:
    @classmethod
    def auth_user(cls, login, pwd):
        # TODO: Api request
        log.info('Authorized session for next 30 minutes')
    
    @classmethod
    def check_auth(cls, login, pwd) -> bool:
        # TODO: Api request
        return True
    
    @classmethod
    def get_game_info(cls) -> dict:
        # TODO: Api request
        return {'version': '1.16.5', 'modification': 'forge'}

    @classmethod
    def get_mods_release(cls) -> dict:
        # TODO: Api request
        return {'version': ''}