
from core.GameElements.SystemItems.Block import Block, pg, App
from Libraries.SimplePyGame.Positions import Vec2
from Libraries.SimplePyGame.Colors import Colors


class BlockSystem:
    def __init__(self, blocks: list[Block] | None = None, screen: pg.Surface = None):

        self.screen = screen if screen else App.Screen.screen

        # statick blocks (for now name is just blocks) todo: Rename to Static Blocks
        self.Blocks = blocks if blocks else []

        # dynamic blocks
        self.DynamicBlocks = []

        # all blocks, to not recreate pg.Rect todo add with dynamic
        self._CashedBlocks = [block.hitbox for block in self.Blocks]


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

    def draw(self):

        for block in self.Blocks:
            block.draw()




