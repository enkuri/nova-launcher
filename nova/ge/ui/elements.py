import pygame as pg


class Element:
    """Base class for any UI element"""
    def __init__(self, visible):
        self._visible = visible
        self.hovering = False
        self.collidable = hasattr(self, 'check_collision')
    
    def check(self):
        if self._visible:
            assert hasattr(self, 'draw'), "trying to display element without draw method"

    def visible(self, val: bool) -> None:
        self._visible = val
        self.check()


class Button(Element):
    def __init__(self, visible: bool = True, clickable: bool = True):
        self._clickable = clickable

        super().__init__(visible)
        self.check()
    
    def check(self):
        super().check()
        if self._click:
            assert hasattr(self, 'click'), "object without click method can't be clicked"
    
    def clickable(self, val: bool) -> None:
        self._clickable = val
        self.check()


class InputField(Element):
    def __init__(self, visible: bool = True, editable: bool = True):
        self._editable = editable
        self.value = ''
        super().__init__(visible)
        self.check()
    
    def check(self):
        super().check()
    
    def editable(self, val: bool) -> None:
        self._editable = val
        self.check()