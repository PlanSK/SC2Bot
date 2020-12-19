from loguru import logger as log

from wrappers.base_wrapper import BaseWrapper

class SCV(BaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mine(self, mineral):
        log.info(f"Worker {self} is going to gather {mineral}")
        self.get_unit().gather(mineral.get_unit())
        self.my_mineral = mineral

    def get_my_mineral(self):
        return self.my_mineral

    def update(self):
        pass
