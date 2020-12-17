from loguru import logger as log

from wrappers.base_wrapper import BaseWrapper

class SCV(BaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mine(self, mineral):
        self.unit.gather(mineral.get_unit())
        self.my_mineral = mineral
        log.info(f"Worker {self} is going to gather {mineral}")
