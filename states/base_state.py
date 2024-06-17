"""Module which contain class for base state"""


class State:

    def __init__(self) -> None:
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

    def set_undone(self) -> None:
        self.done = False

    def get_event(self) -> None:
        """Method which handle event in this state"""
        return

    def load_graphics(self) -> None:
        """Method to load all graphics for this state"""
        return

    def get_keys(self, keys) -> None:
        """Method which handle pressed keys (pg.key.Scancodewrapper object passed as keys)"""
        return

    def cleanup(self) -> None:
        """Calling when state is done"""
        self.next = None  # Setting next state to None
        return

    def startup(self) -> None:
        """Calling when this state is started"""
        return

    def update(self) -> None:
        """Updating state in every frame"""
        return

    def draw(self, screen) -> None:
        """Method to draw all objects from this state"""
        return
