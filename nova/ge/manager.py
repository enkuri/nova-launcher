import os
import sys
import pygame as pg
import importlib
from glob import glob
from logging import getLogger
from importlib.metadata import PackagePath


log = getLogger('manager')


def switch_scene(target_scene: str, init=True, transition=None, *args, **kwargs) -> bool | None:
    """
    Switches to new scene

    Parameters
    ----------
    target_scene : str
        Name of scene you want to switch to

    Returns
    -------
    True if scene changed successfully, False/None otherwise
    """

    global current_scene, current_scene_name
    if target_scene not in scenes:
        log.error('tried to switch to unexistent scene {}'.format(target_scene))
        return False
    
    if transition:
        log.info('initializing new transition {} -> {}'.format(current_scene_name, target_scene))

        scene = scenes[transition]
        scene.init(''.join([x for x in current_scene_name]), target_scene, args, kwargs)

        current_scene_name = transition
        current_scene = scene

        log.info('transition initialized')
        return True

    scene = scenes[target_scene]

    if init:
        log.info('initializing scene {}'.format(target_scene))
        scene.init(*args, **kwargs)

    current_scene_name = target_scene
    current_scene = scene

    log.info('successfully switched to scene {}'.format(target_scene))


def init(screen_: pg.Surface):
    global scenes, current_scene, screen, previous_scene, current_scene_name
    # settings up variables
    screen = screen_
    scenes = {}
    current_scene = None
    current_scene_name = None

    log.info('Loading scenes')
    # loading scenes
    base_package = __name__.split('.')[0]
    for f in glob('{}/ui/*'.format(base_package)):
        if not f.endswith('.py'):
            continue

        scene = importlib.import_module(f.replace('/', '.').replace('\\', '.')[:-3])
        if not hasattr(scene, 'init'):
            log.debug('ignoring scene {}: no init() function'.format(scene.__name__))
            continue

        scenes[scene.__name__.split('.')[-1]] = scene
    
    if 'default' not in scenes:
        log.warning('can\'t find default scene')
    else:
        switch_scene('default')
        switch_scene('intro', transition='transition')

    log.info('loaded {} scenes'.format(len(scenes)))
    log.debug(str(scenes))


def draw(dt: float) -> None:
    """
    Draws currently chosen scene on screen
    (should be called after update)
    """

    screen.fill((0, 0, 0))

    current_scene.draw(screen, dt)

    pg.display.flip()


def update(dt: float) -> None:
    """
    Handles all the events.
    (should be called before draw)
    """
    
    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    current_scene.update(screen, events, dt)