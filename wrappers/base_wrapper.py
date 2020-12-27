from .state import State
from managers.base_manager import BaseManager


class BaseWrapper(object):
    _instances = set()

    def __init__(self, tag):
        self.tag = tag
        self._instances.add(self)
        self._unit = self.bot.all_units.by_tag(self.tag)
        self._state = State.IDLE

    def __str__(self):
        return f"{self._unit.tag}"

    @classmethod
    def set_bot_instance(cls, bot):
        cls.bot = bot
    
    @classmethod
    def update_subclasses(cls):
        for unit in cls._instances.copy():
            if unit is not None and unit.tag in unit.bot.all_units.tags:
                unit.update_unit()
                unit.update()
            else:
                cls._instances.remove(unit)
                BaseManager.unit_destroyed(unit)

    def update_unit(self):
        self._unit = self.bot.all_units.by_tag(self.tag)

    def get_unit(self):
        return self._unit

    def get_tag(self):
        return self._unit.tag

    def update(self):
        raise NotImplementedError()
