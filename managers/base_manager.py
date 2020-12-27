class BaseManager:
    _instances = set()

    def __init__(self):
        self._instances.add(self)

    @classmethod
    def set_bot_instance(cls, bot):
        cls.bot = bot

    @classmethod
    def update_subclasses(cls):
        for manager in cls._instances:
            if manager is not None:
                manager.update()
            else:
                cls._instances.remove(manager)

    @classmethod
    def unit_destroyed(cls, unit):
        for manager in cls._instances:
            if manager is not None:
                manager.remove_unit(unit)

    def update(self):
        raise NotImplementedError("Forgot to override update method")

    def remove_unit(self, unit):
        raise NotImplementedError("Forgot to clean up units")
