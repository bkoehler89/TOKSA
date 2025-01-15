import pygame
import sys
import random
import time

import image_load

#TODO
# Testing an update
# Change color scheme to the first 100 spaces to be mostly greens
# Change the color scheme of 100-200 to be blues
# Add speed statistic to enemies
# Create a new item for each enemy to drop
# Treasure chests
# Allow enemies to walk over items
# Make chasm at location 200
# Item to get across chasm, wings probably
# Update artwork with left, right, up and down
# Create opening screen
# Box off boss at the beginning so player has to go back to kill it
# Grim reaper that kills you in the end and send you to valhalla
# Make background of images transparent
# Add attack and defense to right hand tab
# Make Grim reaper screen
# Make ending screen
# Make audio
# Randomize attack
# Add super attack and make it a different color



# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700  # Window size (wider to accommodate inventory)
MAP_WIDTH, MAP_HEIGHT = 300, 20  # Map size (shrunk to 30x30)
VIEWPORT_SIZE = 9  # 9x9 view
GRID_SIZE = (WIDTH - 200) // 9  # Each square size to fit the 9x9 view, leaving space for inventory

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200)

# Light shades of green and brown
LIGHT_GREENS = [(204, 255, 204), (229, 255, 229), (204, 255, 178)]
LIGHT_BROWNS = [(255, 229, 204), (255, 242, 229), (255, 229, 178)]

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Map")


class Equipment:
    def __init__(self, name, equip_type, defense=0, attack=0, image=None):
        self.name = name
        self.type = equip_type
        self.defense = defense
        self.attack = attack
        self.image = image


class Key:
    def __init__(self, name="Key", image=image_load.boss_key_image):
        self.name = name
        self.image = image
        self.type = 'Key'


class Enemy:
    def __init__(self, name, attack, defense, speed, health, alive_image, dead_image, drop_logic=None):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.alive = True
        self.alive_image = alive_image
        self.dead_image = dead_image
        self.health = health
        self.pos = (0, 0)
        self.item_drop = None  # Add item_drop to track dropped items
        self.drop_logic = drop_logic if drop_logic else {}

    def drop_item(self, global_kill_count):
        if global_kill_count in self.drop_logic:
            return self.drop_logic[global_kill_count]
        return None

    def die(self, global_kill_count):
        self.alive = False
        self.item_drop = self.drop_item(global_kill_count)


class Player:
    def __init__(self):
        self.pos = [110, MAP_HEIGHT // 2]  # Spawn
        self.health = 100
        self.alive = True
        self.alive_image = image_load.player_alive_image
        self.dead_image = image_load.player_dead_image
        self.image = self.alive_image
        self.base_attack = 5
        self.base_defense = 0
        self.attack = self.base_attack
        self.defense = self.base_defense

    def update_image(self):
        if self.health <= 0:
            self.alive = False
            self.image = self.dead_image

    def update_stats(self):
        self.attack = self.base_attack
        self.defense = self.base_defense
        for slot in ['helmet', 'right hand', 'left hand', 'armor', 'legs', 'Boots']:
            item = inventory.get(slot)
            if item:
                self.attack += item.attack
                self.defense += item.defense
        print(f"Defense: {self.defense}, Attack: {self.attack}")


# create equipment objects
katana = Equipment("Katana", "right hand", 1, 2, image_load.katana_image)
broken_shield = Equipment("Broken Shield", "left hand", 1, 0, image_load.broken_shield_image)
leather_armor = Equipment("Leather Armor", "armor", 1, 0, image_load.leather_armor_image)
helmet = Equipment(name="Leather Helmet", equip_type="helmet", defense=1, image=image_load.helmet_image)
apprentice_sword = Equipment(name="Apprentice Sword", equip_type="right hand", attack=1, defense=1, image=image_load.sword_image)
knight_boots = Equipment("Knight Boots", equip_type="Boots", defense=1, image=image_load.knight_boots_image)
leather_legs = Equipment("Leather Legs", equip_type="legs", defense=1, image=image_load.leather_legs_image)
crystal_boots = Equipment("Crystal Boots", equip_type="Boots", defense=1, image=image_load.crystal_boots_image)

# Initialize the player
player = Player()

# Create the map with coordinates and colors
game_map = [[(x, y, random.choice(LIGHT_GREENS + LIGHT_BROWNS)) for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]

# Add 50 mountains and 50 ponds randomly
obstacle_positions = set()
while len(obstacle_positions) < 100:
    obstacle_positions.add((random.randint(0, 99), random.randint(0, MAP_HEIGHT - 1)))

pond_positions = set(random.sample(obstacle_positions, 50))
mountain_positions = obstacle_positions - pond_positions

for col in range(90, 96):
    for row in range(MAP_HEIGHT):
        if random.random() < 0.4:  # 40% chance for each square to be a mountain
            mountain_positions.add((col, row))

for col in range(96, 101):
    for row in range(MAP_HEIGHT):
        if random.random() < 0.85:
            mountain_positions.add((col, row))

for mx, my in mountain_positions:
    game_map[my][mx] = (mx, my, 'mountain')

for px, py in pond_positions:
    game_map[py][px] = (px, py, 'pond')


def place_item_on_map(item_name, item_type, count=1, x_range=(0, MAP_WIDTH - 1), y_range=(0, MAP_HEIGHT - 1),
                      avoid_positions=None):
    if avoid_positions is None:
        avoid_positions = []

    for _ in range(count):
        item_pos = (random.randint(*x_range), random.randint(*y_range))
        while item_pos in obstacle_positions or item_pos in avoid_positions or \
                any(item_pos in pos for pos in avoid_positions if isinstance(pos, (list, set))):
            item_pos = (random.randint(*x_range), random.randint(*y_range))

        game_map[item_pos[1]][item_pos[0]] = (item_pos[0], item_pos[1], item_type)
        avoid_positions.append(item_pos)  # Add to avoid list for subsequent items

    return item_pos if count == 1 else avoid_positions


# Usage of the function:
potion_positions = place_item_on_map('Potion', 'potion', count=5, x_range=(0, 75), y_range=(0, MAP_HEIGHT - 1))
helmet_pos = place_item_on_map('Helmet', 'helmet', avoid_positions=list(potion_positions),
                               x_range=(0, 75), y_range=(0, MAP_HEIGHT - 1))
sword_pos = place_item_on_map('Sword', 'sword', avoid_positions=[helmet_pos] + list(potion_positions),
                              x_range=(0, 75), y_range=(0, MAP_HEIGHT - 1))
leather_armor_pos = place_item_on_map('Leather Armor', 'leather_armor',
                                      avoid_positions=[helmet_pos, sword_pos] + list(potion_positions),
                                      x_range=(0, 75), y_range=(0, MAP_HEIGHT - 1))
exit_pos = place_item_on_map('Exit', 'exit', x_range=(MAP_WIDTH - 5, MAP_WIDTH - 1),
                             avoid_positions=[helmet_pos, sword_pos, leather_armor_pos] + list(potion_positions))


# Consolidated function to add enemies to the map
def add_enemies_to_map(enemy_type, count, x_range, stats, images, drop_logic=None):
    enemies = []
    for _ in range(count):
        enemy_pos = (random.randint(x_range[0], x_range[1]), random.randint(0, MAP_HEIGHT - 1))
        while enemy_pos in obstacle_positions or enemy_pos in potion_positions or any(
                e.pos == enemy_pos for e in enemies
        ):
            enemy_pos = (random.randint(x_range[0], x_range[1]), random.randint(0, MAP_HEIGHT - 1))

        game_map[enemy_pos[1]][enemy_pos[0]] = (enemy_pos[0], enemy_pos[1], enemy_type.lower())
        enemy = Enemy(*stats, *images, drop_logic=drop_logic)  # Pass drop_logic here
        enemy.pos = enemy_pos
        enemies.append(enemy)
    return enemies


# For Trolls
trolls = add_enemies_to_map(
    "Troll", 5, (10, 40), ("Troll", 5, 0, 1, 30),
    (image_load.troll_alive_image, image_load.troll_dead_image),
    drop_logic={2: broken_shield, 3: katana, 4: leather_legs}  # Pass drop logic here
)

# For Orcs
orcs = add_enemies_to_map(
    "Orc", 2, (45, 70), ("Orc", 7, 2, 1, 50),
    (image_load.orc_alive_image, image_load.orc_dead_image),
    drop_logic={1: knight_boots}
)

# For Boss, assuming only one boss, we can handle it differently or use the same logic
bosses = add_enemies_to_map(
    "Boss", 1, (45, 70), ("Boss", 2, 1, 1, 20),
    (image_load.boss_alive_image, image_load.boss_dead_image),
    drop_logic={1: crystal_boots}
)

tomatoes = add_enemies_to_map(
    "Tomato", 5, (110, 140), ("Tomato", 2, 1, 1.5, 20),
    (image_load.tomato_alive_image, image_load.tomato_dead_image),
    drop_logic={1: broken_shield}
)

eggplants = add_enemies_to_map(
    "Eggplant", 3, (130, 170), ("Eggplant", 2, 1, 1.5, 20),
    (image_load.eggplant_alive_image, image_load.eggplant_dead_image),
    drop_logic={1: broken_shield}
)

pumpkin_bosses = add_enemies_to_map(
    "Pumpkin", 1, (180, 190), ("Pumpkin", 2, 1, 5, 20),
    (image_load.boss_pumpkin_alive_image, image_load.boss_pumpkin_dead_image),
    drop_logic={1: broken_shield}
)


enemies = trolls + orcs + bosses + tomatoes + eggplants + pumpkin_bosses
enemy_names = list(set([enemy.name.casefold() for enemy in enemies]))

# Initialize the player
player = Player()

# Inventory labels
inventory_slots = ['helmet', 'right hand', 'left hand', 'armor', 'legs', 'Boots', 'Key']
inventory = {slot: None for slot in inventory_slots}
enemy_colors = ['troll', 'dead_troll', 'orc', 'dead_orc', 'boss', 'dead_boss', 'tomato', 'dead_tomato',
                'eggplant', 'dead_eggplant', 'pumpkin', 'dead_pumpkin']


# Function to draw the map
def draw_map(center):
    start_x = center[0] - VIEWPORT_SIZE // 2
    start_y = center[1] - VIEWPORT_SIZE // 2
    for y in range(VIEWPORT_SIZE):
        for x in range(VIEWPORT_SIZE):
            map_x = start_x + x
            map_y = start_y + y
            if 0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT:
                color = game_map[map_y][map_x][2]
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                tile_types = ['mountain', 'pond', 'helmet', 'potion', 'sword', 'leather_armor']

                if color in tile_types:
                    screen.blit(getattr(image_load, f"{color}_image"), rect.topleft)

                elif color in enemy_colors:
                    enemy_types = {
                        'troll': trolls,
                        'orc': orcs,
                        'boss': bosses,
                        'tomato': tomatoes,
                        'eggplant': eggplants,
                        'pumpkin': pumpkin_bosses
                    }
                    for enemy_type, enemy_list in enemy_types.items():
                        if color == enemy_type or color == f'dead_{enemy_type}':
                            draw_enemy(enemy_type, enemy_list, map_x, map_y, rect)
                elif color == 'exit':  # New condition for the exit
                    screen.blit(image_load.exit_image, rect.topleft)
                elif isinstance(color, tuple) and len(color) == 3:  # Ensure it's a valid color
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                    text = font.render(f"{map_x},{map_y}", True, BLACK)
                    screen.blit(text, (x * GRID_SIZE + 2, y * GRID_SIZE + 2))

    # Draw player
    player_screen_x = (center[0] - start_x) * GRID_SIZE
    player_screen_y = (center[1] - start_y) * GRID_SIZE
    screen.blit(player.image, (player_screen_x, player_screen_y))
    draw_player_health(player.pos, player.health)


# Function to draw the player's health
def draw_health(health):
    health_text = font.render(f"Health: {health}", True, RED)
    screen.blit(health_text, (WIDTH - 190, 10))


# New function to draw player's health
def draw_player_health(player_pos, health):
    player_screen_x = (player_pos[0] - player.pos[0] + VIEWPORT_SIZE // 2) * GRID_SIZE
    player_screen_y = (player_pos[1] - player.pos[1] + VIEWPORT_SIZE // 2) * GRID_SIZE
    health_text = small_font.render(f"{health}", True, RED)
    screen.blit(health_text, (player_screen_x, player_screen_y - 20))  # Place text above player


def show_health_gain(amount):
    health_gain_texts.append((f"+{amount}", (player.pos[0], player.pos[1]), time.time()))


def pick_up_item(item_pos, item_type, item_class):
    if player.alive and tuple(player.pos) == item_pos:
        print(f"Picked up {item_type}")
        new_equipment = item_class()
        slot = new_equipment.type

        if slot in inventory:
            # If there's an item in the slot, drop it
            if inventory[slot]:
                dropped_item = inventory[slot]
                game_map[item_pos[1]][item_pos[0]] = (item_pos[0], item_pos[1], dropped_item.name.lower())
            # Add new item to inventory
            inventory[slot] = new_equipment
        else:
            print(f"Error: No slot '{slot}' in inventory for {item_type}")

        # Change the map to reflect item removal
        game_map[item_pos[1]][item_pos[0]] = (item_pos[0], item_pos[1], random.choice(LIGHT_GREENS + LIGHT_BROWNS))
        player.update_stats()
        return None
    return item_pos


def draw_enemy(enemy_type, enemies, map_x, map_y, rect):
    enemy = next((e for e in enemies if e.pos == (map_x, map_y)), None)
    if enemy:
        if enemy.alive:
            screen.blit(enemy.alive_image, rect.topleft)
            draw_enemy_health(enemy.pos, enemy.health)
        else:
            screen.blit(enemy.dead_image, rect.topleft)
            if enemy.item_drop:
                # Draw the dropped item on top of the dead enemy
                screen.blit(enemy.item_drop.image, rect.topleft)


# Function to draw the enemy's health
def draw_enemy_health(enemy_pos, health):
    enemy_screen_x = (enemy_pos[0] - player.pos[0] + VIEWPORT_SIZE // 2) * GRID_SIZE
    enemy_screen_y = (enemy_pos[1] - player.pos[1] + VIEWPORT_SIZE // 2) * GRID_SIZE
    health_text = small_font.render(f"{health}", True, RED)
    screen.blit(health_text, (enemy_screen_x, enemy_screen_y - 20))


# Function to draw the inventory
def draw_inventory():
    inventory_x = WIDTH - 200
    inventory_y = 50
    slot_height = GRID_SIZE + 10  # Increase the slot height to fit the images
    slot_width = GRID_SIZE + 10   # Increase the slot width to fit the images

    for i, slot in enumerate(inventory_slots):
        rect = pygame.Rect(inventory_x, inventory_y + i * (slot_height + 10), slot_width, slot_height)
        pygame.draw.rect(screen, GREY, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = font.render(slot.capitalize(), True, BLACK)
        screen.blit(text, (inventory_x + 10, inventory_y + i * (slot_height + 10) + 10))
        if inventory[slot]:
            # Center the image within the slot
            image_rect = inventory[slot].image.get_rect(center=rect.center)
            screen.blit(inventory[slot].image, image_rect.topleft)


# Function to draw the health full message
def draw_health_full_message():
    health_full_text = font.render("Health full", True, RED)
    screen.blit(health_full_text, (WIDTH // 2 - 50, HEIGHT // 2 - 15))


def are_touching(pos1, pos2):
    return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1


# Function to move the enemy
def move_enemy(enemy_pos, player_pos):
    blockers = ['mountain', 'pond', 'troll']
    x, y = enemy_pos
    player_x, player_y = player_pos
    new_x, new_y = x, y

    if abs(player_x - x) <= 6 and abs(player_y - y) <= 6:
        if player_x < x and game_map[y][x - 1][2] not in blockers and (x - 1, y) != tuple(player_pos):
            new_x -= 1
        elif player_x > x and game_map[y][x + 1][2] not in blockers and (x + 1, y) != tuple(player_pos):
            new_x += 1
        elif player_y < y and game_map[y - 1][x][2] not in blockers and (x, y - 1) != tuple(player_pos):
            new_y -= 1
        elif player_y > y and game_map[y + 1][x][2] not in blockers and (x, y + 1) != tuple(player_pos):
            new_y += 1

    if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
        return new_x, new_y

    return x, y


# Main game loop
font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 20)
running = True
clock = pygame.time.Clock()
last_enemy_move_time = time.time()
last_combat_time = time.time()  # Time tracker for combat
last_health_loss_display_time = 0  # Time tracker for health loss display
health_full_message_time = 0  # Initialize health_full_message_time
health_loss_display_duration = 0.5  # Duration for displaying health loss
health_loss_texts = []  # Store health loss texts to display
health_gain_texts = []
troll_kill_count = 0
orc_kill_count = 0
boss_kill_count = 0
tomato_kill_count = 0
eggplant_kill_count = 0
pumpkin_kill_count = 0
current_enemy = None

while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif player.alive:
                can_cross_mountain = inventory.get('Boots') and inventory['Boots'].name == "Crystal Boots"
                directions = {
                    pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}

                for key, (dx, dy) in directions.items():
                    if event.key == key:
                        new_pos = player.pos[0] + dx, player.pos[1] + dy
                        if (0 <= new_pos[0] < MAP_WIDTH and 0 <= new_pos[1] < MAP_HEIGHT and
                                game_map[new_pos[1]][new_pos[0]][2] != 'pond' and
                                (game_map[new_pos[1]][new_pos[0]][2] != 'mountain' or can_cross_mountain) and
                                (game_map[new_pos[1]][new_pos[0]][2] not in enemy_names or
                                 not any(e.pos == new_pos and e.alive for e in enemies))):
                            player.pos = list(new_pos)  # Update with new position
                            current_enemy = None
                            break
        elif event.type == pygame.MOUSEBUTTONDOWN and not player.alive:
            running = False  # Exit the game if the player is dead and the mouse is clicked

    # Use the function for each item
    helmet_pos = pick_up_item(helmet_pos, 'helmet', lambda: helmet)
    sword_pos = pick_up_item(sword_pos, 'sword', lambda: apprentice_sword)
    leather_armor_pos = pick_up_item(leather_armor_pos, 'leather_armor', lambda: leather_armor)

    # Check if player steps on potion
    if player.alive and tuple(player.pos) in potion_positions:
        if player.health < 100:
            health_gain = min(100 - player.health, 20)  # Determine how much health is actually gained
            player.health += health_gain
            show_health_gain(health_gain)
            potion_positions.remove(tuple(player.pos))
            game_map[player.pos[1]][player.pos[0]] = (
                player.pos[0], player.pos[1], random.choice(LIGHT_GREENS + LIGHT_BROWNS))
        else:
            health_full_message_time = current_time

    # In your main game loop where you check for item pickup:
    for enemy in enemies:
        if not enemy.alive and enemy.item_drop and tuple(player.pos) == enemy.pos:
            # Use the new pick_up_item function
            enemy.pos = pick_up_item(enemy.pos, enemy.item_drop.name, lambda: enemy.item_drop)
            if enemy.pos is None:  # Item was picked up
                enemy.item_drop = None

    # Combat logic: Player and enemy lose health if they are touching
    touching_enemies = [e for e in enemies if e.alive and are_touching(player.pos, e.pos)]
    if player.alive and touching_enemies:
        player.update_stats()
        if current_enemy is None or not current_enemy.alive or not are_touching(player.pos, current_enemy.pos):
            current_enemy = touching_enemies[0]
        if current_time - last_combat_time >= 1:
            for enemy in touching_enemies:
                damage_to_player = max(0, enemy.attack - player.defense)
                player.health -= damage_to_player
                health_loss_texts.append((f"-{damage_to_player}", (player.pos[0], player.pos[1]), current_time))

            if current_enemy:
                damage_to_enemy = max(0, player.attack - current_enemy.defense)
                current_enemy.health -= damage_to_enemy
                health_loss_texts.append(
                    (f"-{damage_to_enemy}", (current_enemy.pos[0], current_enemy.pos[1]), current_time))

                if current_enemy.health <= 0:
                    globals()[f"{current_enemy.name.lower()}_kill_count"] += 1  # Increment first
                    current_enemy.die(globals()[f"{current_enemy.name.lower()}_kill_count"])
                    # Update map to show dead enemy
                    game_map[current_enemy.pos[1]][current_enemy.pos[0]] = (
                        current_enemy.pos[0], current_enemy.pos[1], 'dead_' + current_enemy.name.lower())

            last_combat_time = current_time

    # Update player image based on health
    player.update_image()

    # Move the enemies
    if current_time - last_enemy_move_time >= 1:
        for enemy in enemies:
            if enemy.alive:
                new_enemy_pos = move_enemy(enemy.pos, player.pos)
                if new_enemy_pos != enemy.pos and all(new_enemy_pos != e.pos for e in enemies):
                    game_map[enemy.pos[1]][enemy.pos[0]] = (
                        enemy.pos[0], enemy.pos[1], random.choice(LIGHT_GREENS + LIGHT_BROWNS))
                    enemy.pos = new_enemy_pos
                    game_map[enemy.pos[1]][enemy.pos[0]] = (enemy.pos[0], enemy.pos[1], enemy.name.lower())
        last_enemy_move_time = current_time

    screen.fill(BLACK)
    draw_map(player.pos)
    draw_health(player.health)
    draw_inventory()
    if current_time - health_full_message_time < 1:
        draw_health_full_message()

    # Draw health loss texts
    for text, pos, timestamp in health_loss_texts:
        if current_time - timestamp < health_loss_display_duration:
            screen_x = (pos[0] - player.pos[0] + VIEWPORT_SIZE // 2) * GRID_SIZE
            screen_y = (pos[1] - player.pos[1] + VIEWPORT_SIZE // 2) * GRID_SIZE
            health_loss_text = small_font.render(text, True, RED)
            screen.blit(health_loss_text, (screen_x, screen_y - 40))
        else:
            health_loss_texts.remove((text, pos, timestamp))

    # Draw health gain texts
    for text, pos, timestamp in health_gain_texts[:]:  # Using a copy to modify list during iteration
        if current_time - timestamp < health_loss_display_duration:  # Use the same duration for consistency
            screen_x = (pos[0] - player.pos[0] + VIEWPORT_SIZE // 2) * GRID_SIZE
            screen_y = (pos[1] - player.pos[1] + VIEWPORT_SIZE // 2) * GRID_SIZE
            health_gain_text = small_font.render(text, True, (0, 255, 0))  # Green color
            screen.blit(health_gain_text, (screen_x, screen_y - 40))
        else:
            health_gain_texts.remove((text, pos, timestamp))

    if player.alive and tuple(player.pos) == exit_pos:
        if inventory['Key']:  # Assuming you need a key to exit
            print("You've reached the exit with the key! Game completed.")
            running = False  # Or you could transition to a new level or end screen here
        else:
            key_text = font.render("Need boss key to exit!.", True, RED)
            screen.blit(key_text, (WIDTH // 2 - key_text.get_width() // 2, HEIGHT // 2 - key_text.get_height() // 2))

    # Display "You died" message if the player is dead
    if not player.alive:
        death_text = font.render("You died. Click to exit.", True, RED)
        screen.blit(death_text, (WIDTH // 2 - death_text.get_width() // 2, HEIGHT // 2 - death_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(30)  # Limit to 30 frames per second

pygame.quit()
sys.exit()
