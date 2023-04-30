import pygame as pg
from nova.ge import manager, easing


def init(p_scene, n_scene, args_, kwargs_) -> None:
    global prev_scene, next_scene, ani, frame, next_scene_name, args, kwargs

    args = args_
    kwargs = kwargs_
    next_scene_name = n_scene
    prev_scene = manager.scenes[p_scene]
    next_scene = manager.scenes[n_scene]
    
    size = manager.screen.get_size()
    ani = easing.Combo([
        easing.Animation('CircularEaseOut', -size[1], 0, 1200),
        easing.Pause(0, 600),
        easing.Animation('CircularEaseOut', 0, size[1], 1200)
    ])

    frame = pg.Surface(size)
    font = pg.font.Font('./nova/assets/mplus_medium.ttf', 30)
    top_text = font.render('NoVa', True, (255, 255, 255))

    font = pg.font.Font('./nova/assets/mplus_medium.ttf', 16)
    bottom_text = font.render('www.ekr.moe', True, (255, 255, 255))

    space = size[1] * 0.05 // 2

    frame.blit(top_text, (
        size[0] // 2 - top_text.get_width() // 2,
        size[1] // 2 - space - bottom_text.get_height() // 2
    ))
    frame.blit(bottom_text, (
        size[0] // 2 - bottom_text.get_width() // 2,
        size[1] // 2 + space + top_text.get_height() // 2
    ))


def update(*_) -> None:
    if ani.ended:
        manager.switch_scene(next_scene_name, init=False, args=args, kwargs=kwargs)


def draw(screen: pg.Surface, dt: float) -> None:
    if ani.current_animation == 0:
        prev_scene.draw(screen, dt)
    elif ani.current_animation == 2:
        next_scene.draw(screen, dt)
    
    offset = ani.tick(dt)
    screen.blit(frame, (0, offset))