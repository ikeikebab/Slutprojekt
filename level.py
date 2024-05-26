from blocks import Block, SpawnBlock, CheckpointBlock, GoalBlock

class Level:
    def __init__(self, level_definition):
        self.level_definition = level_definition
        self.block_size = 96 # Storleken på varje block i nivån
        self.blocks = []
        self.spawn_point = None
        self.checkpoints = []
        self.goal_point = None
        self.parse_level_definition()

    def parse_level_definition(self):
        for row_index, row in enumerate(self.level_definition):
            for col_index, symbol in enumerate(row):
                x = col_index * self.block_size
                y = row_index * self.block_size
                if symbol == "#":
                    block = Block(x, y, self.block_size)
                    self.blocks.append(block)
                elif symbol == "S":
                    block = SpawnBlock(x, y, self.block_size)
                    self.blocks.append(block)
                    self.spawn_point = (x, y)
                elif symbol == "C":
                    block = CheckpointBlock(x, y, self.block_size)
                    self.blocks.append(block)
                    self.checkpoints.append((x, y))
                elif symbol == "G":
                    block = GoalBlock(x, y, self.block_size)
                    self.blocks.append(block)
                    self.goal_point = (x, y)

        if self.spawn_point is None:
            print("Spawn point is missing in level definition.")

    def get_level_data(self):
        return self.blocks, self.spawn_point, self.checkpoints, self.goal_point

class LevelManager:
    def __init__(self):
        self.levels = {} # En tom dictionary för att lagra nivådefinitioner

    def add_level(self, level_name, level_definition):
        self.levels[level_name] = Level(level_definition)
        print(f"Added level '{level_name}': {level_definition}")

    def import_level_definitions(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            level_definition = [line.strip() for line in lines]
            return level_definition

    def create_level(self, level_name):
        level = self.levels.get(level_name) # Hämtar nivådefinitionen från vår dictionary
        if level:
            blocks, spawn_point, checkpoints, goal_point = level.get_level_data()
            if spawn_point is not None:
                return blocks, spawn_point, checkpoints, goal_point
            else:
                print("Spawn point is missing in level definition.")
        else:
            print(f"Level '{level_name}' not found.")
        return None, None, None, None


# Skapar en instans av LevelManager
level_manager = LevelManager()
# Lägger till nivådefinitioner för "level_1" och "level_2"
level_manager.add_level("level_1", level_manager.import_level_definitions("level1.json"))
level_manager.add_level("level_2", level_manager.import_level_definitions("level2.json"))

