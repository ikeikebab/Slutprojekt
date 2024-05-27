from blocks import Block, SpawnBlock, CheckpointBlock, GoalBlock  # Importera klasser för olika typer av block från filen blocks.py

class Level:
    def __init__(self, level_definition):
        self.level_definition = level_definition  # Definitionen av nivån som en tvådimensionell lista med symboler
        self.block_size = 96  # Storleken på varje block i nivån
        self.blocks = []  # Lista för att lagra alla block i nivån
        self.spawn_point = None  # Startpunkten för spelaren
        self.checkpoints = []  # Lista för att lagra alla kontrollpunkter i nivån
        self.goal_point = None  # Målpunkten för nivån
        self.parse_level_definition()  # Metod för att tolka nivådefinitionen och skapa nivån

    def parse_level_definition(self):
        # Metod för att tolka nivådefinitionen och skapa block och objekt för nivån
        for row_index, row in enumerate(self.level_definition):
            for col_index, symbol in enumerate(row):
                x = col_index * self.block_size  # X-koordinat för blocket baserat på kolumnindex och blockstorlek
                y = row_index * self.block_size  # Y-koordinat för blocket baserat på radindex och blockstorlek
                if symbol == "#":
                    # Om symbolen är "#" skapas ett vanligt block och läggs till i listan med block
                    block = Block(x, y, self.block_size)
                    self.blocks.append(block)
                elif symbol == "S":
                    # Om symbolen är "S" skapas en startpunkt och läggs till i listan med block
                    block = SpawnBlock(x, y, self.block_size)
                    self.blocks.append(block)
                    self.spawn_point = (x, y)  # Spara startpunkten för spelaren
                elif symbol == "C":
                    # Om symbolen är "C" skapas en kontrollpunkt och läggs till i listan med block och kontrollpunkter
                    block = CheckpointBlock(x, y, self.block_size)
                    self.blocks.append(block)
                    self.checkpoints.append((x, y))  # Spara positionen för kontrollpunkten
                elif symbol == "G":
                    # Om symbolen är "G" skapas en målpunkt och läggs till i listan med block
                    block = GoalBlock(x, y, self.block_size)
                    self.blocks.append(block)
                    self.goal_point = (x, y)  # Spara positionen för målpunkten

        if self.spawn_point is None:
            print("Spawn point is missing in level definition.")  # Meddelande om startpunkten saknas i nivådefinitionen

    def get_level_data(self):
        # Metod för att returnera nivådata såsom block, startpunkt, kontrollpunkter och målpunkt
        return self.blocks, self.spawn_point, self.checkpoints, self.goal_point

class LevelManager:
    def __init__(self):
        self.levels = {}  # En tom dictionary för att lagra nivådefinitioner

    def add_level(self, level_name, level_definition):
        # Metod för att lägga till en nivådefinition i LevelManager
        self.levels[level_name] = Level(level_definition)
        print(f"Added level '{level_name}': {level_definition}")  # Meddelande om att nivån har lagts till

    def import_level_definitions(self, filename):
        # Metod för att importera nivådefinitioner från en fil
        with open(filename, 'r') as file:
            lines = file.readlines()
            level_definition = [line.strip() for line in lines]  # Läs in varje rad och ta bort whitespace
            return level_definition  # Returnera nivådefinitionen som en lista av strängar

    def create_level(self, level_name):
        # Metod för att skapa en nivå baserat på dess namn
        level = self.levels.get(level_name)  # Hämta nivådefinitionen från vår dictionary
        if level:
            # Om nivån finns, hämta data för block, startpunkt, kontrollpunkter och målpunkt
            blocks, spawn_point, checkpoints, goal_point = level.get_level_data()
            if spawn_point is not None:
                return blocks, spawn_point, checkpoints, goal_point  # Returnera nivådata
            else:
                print("Spawn point is missing in level definition.")  # Meddelande om startpunkten saknas
        else:
            print(f"Level '{level_name}' not found.")  # Meddelande om att nivån inte hittades
        return None, None, None, None

# Skapar en instans av LevelManager
level_manager = LevelManager()
# Lägger till nivådefinitioner för "level_1" och "level_2"
level_manager.add_level("level_1", level_manager.import_level_definitions("level1.json"))
level_manager.add_level("level_2", level_manager.import_level_definitions("level2.json"))
