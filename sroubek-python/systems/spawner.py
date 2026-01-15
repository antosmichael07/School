import random
from entities.enemy import Enemy
from settings import SPAWN_COUNT_START, SPAWN_COUNT_MAX, SPAWN_COUNT_ACCELERATION, ENEMY_SIZE_MIN, ENEMY_SIZE_MAX, WIDTH

class Spawner:
    def __init__(self, game, enemy_image):
        self.game = game
        self.enemy_image = enemy_image
        self.timer = 0
        # per second
        self.spawn_count = SPAWN_COUNT_START
        # +1 spawn count per SPAWN_COUNT_ACCELERATION spawn iterations
        self.spawn_count_accelerator = 0
        self.last_spawn = -10000
    
    def update(self, dt):
        self.timer += dt
        
        while self.timer >= 1 / self.spawn_count:
            self.spawn_count_accelerator += 1
            if self.spawn_count < SPAWN_COUNT_MAX and self.spawn_count_accelerator >= SPAWN_COUNT_ACCELERATION:
                self.spawn_count += 1
                self.spawn_count_accelerator = 0
            
            self.timer -= 1 / self.spawn_count
            self.spawn_enemy()
    
    def spawn_enemy(self):
        size = random.randint(ENEMY_SIZE_MIN, ENEMY_SIZE_MAX)
        pos = random.randint(int(size / 2), int(WIDTH - size / 2))
        while pos > self.last_spawn - ENEMY_SIZE_MAX * 3 and pos < self.last_spawn + ENEMY_SIZE_MAX * 3:
            pos = random.randint(int(size / 2), int(WIDTH - size / 2))
        self.last_spawn = pos
        enemy = Enemy(self.game, (pos, -ENEMY_SIZE_MAX), (size, size * 3), self.enemy_image)
        self.game.enemies.add(enemy)
        self.game.all_sprites.add(enemy)
