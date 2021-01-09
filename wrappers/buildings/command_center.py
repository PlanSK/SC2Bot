from loguru import logger as log

from sc2.ids.ability_id import AbilityId

from wrappers.base_wrapper import BaseWrapper


class CommandCenter(BaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        self.update_unit()

    def train_unit(self, unit_type):
        self.get_unit().train(unit=unit_type)
        log.info(f"Added to the training queue: {unit_type}")

