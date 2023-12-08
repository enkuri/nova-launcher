import pygame as pg
from ge.ui.elements import Element, Button, InputField


class Manager:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.elements = []
    
    def add_elements(self, *elements):
        for e in elements:
            assert isinstance(e, Element), "only ge.ui.elements.Element are accepted"
            self.elements.append(e)
    
    def update(self, events, dt: float):
        mouse = pg.mouse.get_pos()
        for e in self.elements:
            if not e.collidable:
                return

            e.hovering = e.check_collision(mouse)

            if (
                isinstance(e, Button) or isinstance(e, InputField) and e.hovering
                and (pg.BUTTON_LEFT in events or pg.BUTTON_RIGHT in events)
            ):
                e.click()
    
    def draw(self,  dt: float, screen: pg.Surface | None = None):
        s = screen or self.screen
        for e in self.elements:
            if e._visible:
                e.draw(s, dt)