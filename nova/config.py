import appdirs
import nova
from os.path import join, isfile, isdir, split
from os import makedirs
import json
from logging import getLogger


log = getLogger('config')


class Config:
    jsons = {
        'nova-config.json': {
            'login': '',
            'password': '',
            'ram': 2048,
            'discord-rpc': False
        },
        'nova-data.json': {
            'skins': {},
            'mods-release': '',
            'nova-release': nova.__version__,
            'game-instance': ''
        }
    }

    @classmethod
    def init(cls):
        app = appdirs.AppDirs('NoVaLauncher', 'JustLian', nova.__version__)
        d = split(app.user_config_dir)[0]
        log.info('Working directory: {}'.format(d))
        cls.paths = {
            'dir': d,
            'cfg': join(d, 'nova-config.json'),
            'data': join(d, 'nova-data.json')
        }

        for f in cls.paths.keys():
            if cls.paths[f].endswith('.json'):
                if not isfile(cls.paths[f]):
                    with open(cls.paths[f], 'w', encoding='utf8') as d:
                        json.dump(cls.jsons[split(cls.paths[f])[1]], d)
            else:
                makedirs(cls.paths[f], exist_ok=True)

    @classmethod
    def load(cls):
        with open(cls.paths['cfg'], encoding='utf8') as f:
            cls.cfg = json.load(f)
        with open(cls.paths['data'], encoding='utf8') as f:
            cls.data = json.load(f)

    @classmethod
    def dump(cls):
        with open(cls.paths['cfg'], 'w', encoding='utf8') as f:
            json.dump(cls.cfg, f)
        with open(cls.paths['data'], 'w', encoding='utf8') as f:
            json.dump(cls.data, f)