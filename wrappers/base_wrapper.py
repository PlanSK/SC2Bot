class BaseWrapper(object):
    def __init__(self, unit):
        self.unit = unit

    def __str__(self):
        return f"{self.unit.tag}"

    def get_unit(self):
        return self.unit