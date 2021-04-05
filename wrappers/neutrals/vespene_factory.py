from loguru import logger as log

from wrappers.base_wrapper import BaseWrapper

class VespeneFactory(BaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._workers = []
        self.geyser_id = None

    def get_workers(self):
        return [worker.get_unit().tag for worker in self._workers]

    def get_workers_amount(self):
        return len(self._workers)

    def add_worker(self, worker):
        log.info(f"Added worker {worker} to list")
        self._workers.append(worker)

    def remove_worker(self, worker):
        log.info(f"Removed worker {worker}")

    def update(self):
        pass
