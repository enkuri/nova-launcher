import minecraft_launcher_lib as mll
import subprocess
import sys
from nova.config import Config
from logging import getLogger
from nova import utils


log = getLogger('mc')


def find_forge_version(game_version: str) -> str:
    log.info('Looking for latest forge version')
    forge_version = mll.forge.find_forge_version(game_version)

    if forge_version is None:
        log.error('No valid forge version found!')
        return ''
    return forge_version


def check_for_installation(forge_version: str) -> bool:
    installed_versions = [x['id'] for x in mll.utils.get_installed_versions(Config.paths['dir'])]
    return forge_version in installed_versions


def install_forge(forge_version: str) -> bool:
    log.info('Installing forge {}'.format(forge_version))
    mll.forge.install_forge_version(forge_version, Config.paths['dir'])
    Config.data['game-instance'] = forge_version
    return True


def launch_game(username, version_id):
    options = {
        "username": username,
        "uuid": utils.construct_offline_player_uuid(username),
        "token": "-"
    }

    mc_cmd = mll.command.get_minecraft_command(version_id, Config.paths['dir'], options=options)
    subprocess.call(mc_cmd)