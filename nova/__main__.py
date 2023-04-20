import os
import nova
from nova.config import Config
from nova.modules.api import API
from nova.modules import mc
import logging


# -- logging --
root = logging.getLogger()
root.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s', '%Y-%m-%d %H:%M:%S')

terminal = logging.StreamHandler()
terminal.setFormatter(formatter)
root.addHandler(terminal)

# Settings up all folders
Config.init()
Config.load()

mc.check_for_installation('1')

# -- authorization --
if Config.cfg['login'] == '' or Config.cfg['password'] == '':
    root.info('No authorization data. Please provide your credentials')
    login, pwd = input('Login> '), input('Password> ')
    Config.cfg['login'] = login
    Config.cfg['password'] = pwd
    Config.dump()
else:
    login, pwd = Config.cfg['login'], Config.cfg['password']
    if pwd is None:
        pwd = input('Password> ')
        Config.cfg['pasword'] = pwd
        Config.dump()

root.info('Checking authorization')
if API.check_auth(login, pwd):
    root.info('Credentials are valid')
else:
    root.error('Wrong credentials')
    Config.cfg['password'] = None
    exit()

# -- check version --
game_info = API.get_game_info()

forge_version = mc.find_forge_version(game_info['version'])
if not mc.check_for_installation(forge_version):
    root.warning('Can\'t find forge game instance')
    mc.install_forge(forge_version)

root.info('Starting game')

mc.launch_game(
    Config.cfg['login'],
    forge_version
)