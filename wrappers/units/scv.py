from loguru import logger as log

from sc2.ids.ability_id import AbilityId

from wrappers.base_wrapper import BaseWrapper

from wrappers.state import State


class SCV(BaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mine(self, mineral):
        log.info(f"Worker {self} is going to gather {mineral}")
        self.get_unit().gather(mineral.get_unit())
        self.my_mineral = mineral
        self._state = State.MINING

    def get_my_mineral(self):
        return self.my_mineral.get_unit().tag

    def control_mining(self):
        if self.get_unit().orders:
            order = self.get_unit().orders[0]
            if order.ability.id == AbilityId.HARVEST_GATHER:
                if order.target != self.my_mineral.get_unit().tag:
                    self.get_unit().gather(self.my_mineral.get_unit())
        else:
            self.get_unit().gather(self.my_mineral.get_unit())
        # print(f'W: {self.get_unit().tag} My state {self.get_state()} Target: {self.my_mineral.get_unit().name}')

    def get_state(self):
        return self._state

    def update(self):
        if self._state == State.IDLE:
            pass
        elif self._state == State.MINING:
            self.control_mining()
        else:
            log.warning(f"WARN: wrong state: {self._state}")
