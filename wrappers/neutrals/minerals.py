from loguru import logger as log

from wrappers.base_wrapper import BaseWrapper

class Mineral(BaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        capacity = self.unit.mineral_contents

        log.info(f'Tag {self.unit.tag} contains {capacity}')

    def workers_list(self):
        pass

    def add_worker(self):
        pass

    def remove_worker(self):
        pass