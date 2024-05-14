from blocks import Block

# level.py

class LevelManager:
    def __init__(self):
        self.levels = {}

    def add_level(self, level_name, level_definition):
        self.levels[level_name] = level_definition

    def import_level_definitions(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            level_definition = [line.strip() for line in lines]
            return level_definition

    def create_level(self, level_name):
        level_definition = self.levels.get(level_name)
        if level_definition:
            blocks, fire_positions = self.parse_level_definition(level_definition)
            return blocks, fire_positions
        else:
            print(f"Level '{level_name}' not found.")
            return None, None

    def parse_level_definition(self, level_definition):
        block_size = 96
        blocks = []
        fire_positions = []

        for row_index, row in enumerate(level_definition):
            for col_index, symbol in enumerate(row):
                x = col_index * block_size
                y = row_index * block_size
                if symbol == "#":
                    block = Block(x, y, block_size)
                    blocks.append(block)
                elif symbol == "F":
                    fire_positions.append((x, y))

        return blocks, fire_positions

# Instantiate LevelManager
level_manager = LevelManager()
level_manager.add_level("level_1", level_manager.import_level_definitions("level1.json"))
level_manager.add_level("level_2", level_manager.import_level_definitions("level2.json"))


blocks, fire_positions = level_manager.create_level("level_1")