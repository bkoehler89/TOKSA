import pygame

# Constants
WIDTH, HEIGHT = 1000, 800  # Window size (wider to accommodate inventory)
MAP_WIDTH, MAP_HEIGHT = 100, 20  # Map size (shrunk to 30x30)
VIEWPORT_SIZE = 9  # 9x9 view
GRID_SIZE = (WIDTH - 200) // 9  # Each square size to fit the 9x9 view, leaving space for inventory

# Load images
player_alive_image = pygame.image.load('images/player.png')
player_alive_image = pygame.transform.scale(player_alive_image, (GRID_SIZE, GRID_SIZE))

player_dead_image = pygame.image.load('images/player_dead.png')
player_dead_image = pygame.transform.scale(player_dead_image, (GRID_SIZE, GRID_SIZE))

mountain_image = pygame.image.load('images/mountain.png')
mountain_image = pygame.transform.scale(mountain_image, (GRID_SIZE, GRID_SIZE))

pond_image = pygame.image.load('images/pond.png')
pond_image = pygame.transform.scale(pond_image, (GRID_SIZE, GRID_SIZE))

helmet_image = pygame.image.load('images/helmet.png')
helmet_image = pygame.transform.scale(helmet_image, (GRID_SIZE, GRID_SIZE))

potion_image = pygame.image.load('images/potion.png')
potion_image = pygame.transform.scale(potion_image, (GRID_SIZE, GRID_SIZE))

troll_alive_image = pygame.image.load('images/troll.png')
troll_alive_image = pygame.transform.scale(troll_alive_image, (GRID_SIZE, GRID_SIZE))

troll_dead_image = pygame.image.load('images/troll_dead.png')
troll_dead_image = pygame.transform.scale(troll_dead_image, (GRID_SIZE, GRID_SIZE))

sword_image = pygame.image.load('images/sword.png')
sword_image = pygame.transform.scale(sword_image, (GRID_SIZE, GRID_SIZE))

katana_image = pygame.image.load('images/katana.png')
katana_image = pygame.transform.scale(katana_image, (GRID_SIZE, GRID_SIZE))

boss_key_image = pygame.image.load('images/boss_key.png')
boss_key_image = pygame.transform.scale(boss_key_image, (GRID_SIZE, GRID_SIZE))

exit_image = pygame.image.load('images/exit.png')
exit_image = pygame.transform.scale(exit_image, (GRID_SIZE, GRID_SIZE))

broken_shield_image = pygame.image.load('images/broken_shield.png')
broken_shield_image = pygame.transform.scale(broken_shield_image, (GRID_SIZE, GRID_SIZE))

orc_alive_image = pygame.image.load('images/orc.png')
orc_alive_image = pygame.transform.scale(orc_alive_image, (GRID_SIZE, GRID_SIZE))

orc_dead_image = pygame.image.load('images/orc_dead.png')
orc_dead_image = pygame.transform.scale(orc_dead_image, (GRID_SIZE, GRID_SIZE))

leather_armor_image = pygame.image.load('images/leather_armor.png')
leather_armor_image = pygame.transform.scale(leather_armor_image, (GRID_SIZE, GRID_SIZE))

boss_alive_image = pygame.image.load('images/boss_demon.png')
boss_alive_image = pygame.transform.scale(boss_alive_image, (GRID_SIZE, GRID_SIZE))

boss_dead_image = pygame.image.load('images/boss_demon_dead.png')
boss_dead_image = pygame.transform.scale(boss_dead_image, (GRID_SIZE, GRID_SIZE))

knight_boots_image = pygame.image.load('images/knight_boots.png')
knight_boots_image = pygame.transform.scale(knight_boots_image, (GRID_SIZE, GRID_SIZE))

leather_legs_image = pygame.image.load('images/leather_legs.png')
leather_legs_image = pygame.transform.scale(leather_legs_image, (GRID_SIZE, GRID_SIZE))

crystal_boots_image = pygame.image.load('images/crystal_boots.jpg')
crystal_boots_image = pygame.transform.scale(crystal_boots_image, (GRID_SIZE, GRID_SIZE))

boss_pumpkin_alive_image = pygame.image.load('images/boss_pumpkin.png')
boss_pumpkin_alive_image = pygame.transform.scale(boss_pumpkin_alive_image, (GRID_SIZE, GRID_SIZE))

boss_pumpkin_dead_image = pygame.image.load('images/boss_pumpkin_dead.png')
boss_pumpkin_dead_image = pygame.transform.scale(boss_pumpkin_dead_image, (GRID_SIZE, GRID_SIZE))

tomato_alive_image = pygame.image.load('images/tomato.png')
tomato_alive_image = pygame.transform.scale(tomato_alive_image, (GRID_SIZE, GRID_SIZE))

tomato_dead_image = pygame.image.load('images/tomato_dead.png')
tomato_dead_image = pygame.transform.scale(tomato_dead_image, (GRID_SIZE, GRID_SIZE))

eggplant_alive_image = pygame.image.load('images/eggplant.png')
eggplant_alive_image = pygame.transform.scale(eggplant_alive_image, (GRID_SIZE, GRID_SIZE))

eggplant_dead_image = pygame.image.load('images/eggplant_dead.png')
eggplant_dead_image = pygame.transform.scale(eggplant_dead_image, (GRID_SIZE, GRID_SIZE))