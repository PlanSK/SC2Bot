import sc2
from sc2.bot_ai import BotAI

from managers.base_manager import BaseManager
from managers.mining_manager import MiningManager

from wrappers.base_wrapper import BaseWrapper


class BaseBot(BotAI):
    def __init__(self):
        BaseWrapper.set_bot_instance(self)

    async def update(self):
        BaseWrapper.update_subclasses()
        BaseManager.update_subclasses()

    def get_xyz(self, point):
        if isinstance(point, sc2.position.Point3):
            x, y, z = point
        elif isinstance(point, sc2.position.Point2):
            x, y, z = (*point, self.get_terrain_z_height(point))
        else:
            raise NotImplementedError("get_xyz not implemented for this type")

        return (x, y, z)

    def draw_sphere(self, position, radius=1, color=None):
        x, y, z = self.get_xyz(position)
        position = sc2.position.Point3((x, y, z))
        color = (255, 255, 255) if not color else color

        self.client.debug_sphere_out(
            p=position,
            r=radius,
            color=color
        )
