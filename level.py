from blocks import Block # Importerar Block-klassen från modulen blocks

class LevelManager:
    def __init__(self):
        self.levels = {} # En tom dictionary för att lagra nivådefinitioner

    def add_level(self, level_name, level_definition):
        self.levels[level_name] = level_definition  # Lägger till nivådefinitionen i vår dictionary
        print(f"Added level '{level_name}': {level_definition}")  # Bara till så jag kunde se att rätt level kom upp i konsolen


    def import_level_definitions(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            level_definition = [line.strip() for line in lines] # Läser in varje rad från filen och tar bort whitespace
            return level_definition

    def create_level(self, level_name):
        level_definition = self.levels.get(level_name) # Hämtar nivådefinitionen från vår dictionary
        if level_definition:
            blocks = self.parse_level_definition(level_definition) # Parsar nivådefinitionen till block
            return blocks
        else:
            print(f"Level '{level_name}' not found.")
            return None, None

    def parse_level_definition(self, level_definition):
        block_size = 96 # Storleken på varje block i nivån
        blocks = []

        for row_index, row in enumerate(level_definition):
            for col_index, symbol in enumerate(row):
                x = col_index * block_size # Beräknar x-koordinaten för blocket
                y = row_index * block_size # Beräknar y-koordinaten för blocket
                if symbol == "#": # Om symbolen är "#" skapar det ett block
                    block = Block(x, y, block_size)
                    blocks.append(block)


        return blocks 
    
# Skapar en instans av LevelManager
level_manager = LevelManager()

# Lägger till nivådefinitioner för "level_1" och "level_2"
level_manager.add_level("level_1", level_manager.import_level_definitions("level1.json"))
level_manager.add_level("level_2", level_manager.import_level_definitions("level2.json"))
