from pygame._sdl2.video import Renderer

from core.GameElements.Systems.BonusSystem import BonusSystem
from Items.Block.Block import Block, pg, App
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.Colors import Colors
from Items.Block.DestroyingBlock import DestroyingBlock


class BlockSystem:
    def __init__(self, bonus_system: BonusSystem, blocks: list[Block] | None = None, render: Renderer = None):

        self.render = render if render else App.Screen.render

        # static blocks (for now name is just blocks) todo: Rename to Static Blocks
        self.Blocks = blocks if blocks else []

        # dynamic blocks
        self.DynamicBlocks = []

        # all blocks, to not recreate pg.Rect todo add with dynamic
        self._CashedBlocks = [block.hitbox for block in self.Blocks]

        self.DestroyedBlocks: list[DestroyingBlock] = []

        self.BonusSystem = bonus_system


    @property
    def blocks(self) -> list[pg.Rect]:
        """
        Returns a list of all blocks rects in the game
        :return:
        """
        return self._CashedBlocks

    def __getitem__(self, index):
        return self.Blocks[index]

    def __setitem__(self, index, value):
        self.Blocks[index] = value


    def add_block(self, block: Block):
        self.Blocks.append(block)
        self._CashedBlocks.append(block.hitbox)

    def add(self, pos, size: Vec2 = Vec2(10, 10), color: Colors = Colors.BLACK, screen: pg.Surface = None):
        block = Block(pos, size, color, screen)
        self.Blocks.append(block)
        self._CashedBlocks.append(block.hitbox)

    def kill(self, index, rate: float = 0.2):
        block = self.pop(index)
        self.DestroyedBlocks.append(DestroyingBlock(block=block))
        self.BonusSystem.spawn(block.center, rate)

    def remove_block(self, block: Block):
        self.Blocks.remove(block)
        self._CashedBlocks.remove(block.hitbox)

    def remove(self, index: int):
        self.Blocks.pop(index)
        self._CashedBlocks.pop(index)

    def pop(self, index: int) -> Block:
        self._CashedBlocks.pop(index)
        return self.Blocks.pop(index)

    def clear(self):
        self.Blocks.clear()
        self._CashedBlocks.clear()

    def cast_shadows(self):
        for block in self.Blocks:
            block.cast_shadow()

        for block in self.DestroyedBlocks:
            block.cast_shadow()

    def update(self):

        for block in self.DestroyedBlocks[:]:

            if block.is_gone:
                self.DestroyedBlocks.remove(block)
                continue

            block.update()

    def draw(self):

        for block in self.Blocks[:]:
            block.draw()

        for block in self.DestroyedBlocks[:]:
            block.draw()




