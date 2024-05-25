
from blocks import Block, SpawnBlock, CheckpointBlock, GoalBlock 

class LevelManager:
    def __init__(self):
        self.levels = {}

    def add_level(self, level_name, level_definition):
        self.levels[level_name] = level_definition
        print(f"Added level '{level_name}': {level_definition}")

    def import_level_definitions(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            level_definition = [line.strip() for line in lines]
            return level_definition

    def create_level(self, level_name):
        level_definition = self.levels.get(level_name)
        if level_definition:
            blocks, spawn_point, checkpoints, goal_point = self.parse_level_definition(level_definition)
            return blocks, spawn_point, checkpoints, goal_point,
        else:
            print(f"Level '{level_name}' not found.")
            return None, None, None, None

    def parse_level_definition(self, level_definition):
        block_size = 96
        blocks = []
        spawn_point = None
        checkpoints = []
        goal_point = None

        for row_index, row in enumerate(level_definition):
            for col_index, symbol in enumerate(row):
                x = col_index * block_size
                y = row_index * block_size
                if symbol == "#":
                    block = Block(x, y, block_size)
                    blocks.append(block)
                elif symbol == "S":
                    block = SpawnBlock(x, y, block_size)
                    blocks.append(block)
                    spawn_point = (x, y)
                elif symbol == "C":
                    block = CheckpointBlock(x, y, block_size)
                    blocks.append(block)
                    checkpoints.append((x, y))
                elif symbol == "G":
                    block = GoalBlock(x, y, block_size)
                    blocks.append(block)
                    goal_point = (x, y)


        return blocks, spawn_point, checkpoints, goal_point

level_manager = LevelManager()
level_manager.add_level("level_1", level_manager.import_level_definitions("level1.json"))
level_manager.add_level("level_2", level_manager.import_level_definitions("level2.json"))
