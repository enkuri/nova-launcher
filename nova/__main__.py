from nova.config import Config
from nova.ge import manager as mgr
import logging
import pygame as pg
from screeninfo import get_monitors


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

# -- settings up pygame --

# primary monitor's size
size: tuple[int, int] = None
for monitor in get_monitors():
    if not monitor.is_primary:
        continue
    size = (monitor.width, monitor.height)

max_size = (1280, 720)

# determining proper window size
if size[0] > max_size[0] and size[1] > max_size[1]:
    width, height = max_size
elif size[0] < max_size[0]:
    width_ratio = size[0] / max_size[0]
    height = int(size[1] * 0.8)
    width = int(max_size[0] * width_ratio)
    if width > size[0]:
        width = size[0]
        height = int(width / max_size[0] * max_size[1])
else:
    width = size[0]
    height_ratio = size[1] / max_size[1]
    height = int(max_size[1] * height_ratio)

# initializing display
pg.display.init()
screen = pg.display.set_mode((width, height))


def run():
    pg.init()
    mgr.init(screen)

    fps = 30
    fps_clock = pg.time.Clock()

    pg.display.set_caption('Nova launcher - ekr!dev')

    dt = 1 / fps
    while True:
        mgr.draw(dt)
        mgr.update(dt)

        pg.display.flip()
        dt = fps_clock.tick(fps)


if __name__ == '__main__':
    run()