from loguru import logger as log

from sc2.ids.ability_id import AbilityId

from wrappers.base_wrapper import BaseWrapper

class SCV(BaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mine(self, mineral):
        log.info(f"Worker {self} is going to gather {mineral}")
        self.get_unit().gather(mineral.get_unit())
        self.my_mineral = mineral

    def get_my_mineral(self):
        return self.my_mineral.get_unit().tag

    def control_mining(self):
        if self.get_unit().orders:
            order = self.get_unit().orders[0]
            if order.ability.id == AbilityId.HARVEST_GATHER:
                if order.target != self.my_mineral.get_unit().tag:
                    print(f"{self} mining is not {order.target} --> {self.my_mineral.get_unit().tag}")
                    self.get_unit().gather(self.my_mineral.get_unit())
                else:
                    print(f"{self} mining is true mineral {order.target}")
        else:
            print(f'{self} needs "подзатыльник"!')
            self.get_unit().gather(self.my_mineral.get_unit())

    def update(self):
        self.control_mining()
