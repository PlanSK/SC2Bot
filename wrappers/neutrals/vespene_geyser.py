from loguru import logger as log

from wrappers.base_wrapper import BaseWrapper

class VespeneGeyser(BaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._workers = []

    def update(self):
        pass
