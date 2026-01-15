import pygame as pg
from entities.player import Player
from settings import WIDTH, HEIGHT, FPS, ENEMY_SIZE_MAX, PLAYER_SIZE
from systems.spawner import Spawner

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Šroubek')
        enemy_image = pg.image.load('assets/bolt.png')
        pg.display.set_icon(enemy_image)
        player_image = pg.image.load('assets/player.png')
        self.death_sound = pg.mixer.Sound('assets/metal_pipe.mp3')
        self.clock = pg.time.Clock()
        
        # Inicializace skupiny objektů
        self.all_sprites = pg.sprite.Group()
        
        # Vytvoření objektu hráče
        self.player = Player(game=self, pos=(WIDTH / 2, HEIGHT / 2), size=(PLAYER_SIZE, PLAYER_SIZE), image=player_image)
        self.all_sprites.add(self.player)
        
        # Inicializace systému vytváření nepřátel
        self.enemies = pg.sprite.Group()
        self.spawner = Spawner(self, enemy_image)
        
        # Stav hry
        self.timer = 0
        self.game_running = True
        self.app_running = True
        self.best_time = self.load_score()
    
    def run(self):
        while self.app_running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            if self.game_running:
                self.update(dt)
                self.draw_game()
            else:
                self.draw_end()
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.app_running = False
    
    def update(self, dt):
        self.all_sprites.update(dt)
        self.spawner.update(dt)

        self.timer += dt
        
        if pg.sprite.spritecollide(self.player, self.enemies, False):
            self.player.kill()
            self.game_running = False
            self.death_sound.play()
            if self.timer > self.best_time:
                self.save_score()
        
        for enemy in self.enemies:
            if enemy.pos.y > HEIGHT + ENEMY_SIZE_MAX:
                enemy.kill()
    
    def draw_game(self):
        self.screen.fill((0, 180, 180))

        self.all_sprites.draw(self.screen)

        font = pg.font.SysFont("Comic Sans", 30)
        text = font.render(f"Time: {self.timer:.1f}s", True, (0, 0, 0))
        self.screen.blit(text, (30, 30))

        pg.display.flip()
    
    def draw_end(self):
        self.screen.fill((0, 180, 180))

        font = pg.font.SysFont("Comic Sans", 50)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
        self.screen.blit(text, text_rect)

        font = pg.font.SysFont("Comic Sans", 30)
        text = font.render(f"Your time: {self.timer:.2f}s", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        self.screen.blit(text, text_rect)

        if self.timer > self.best_time:
            font = pg.font.SysFont("Comic Sans", 30)
            text = font.render("NEW RECORD !!", True, (50, 255, 0))
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
            self.screen.blit(text, text_rect)
        else:
            font = pg.font.SysFont("Comic Sans", 30)
            text = font.render(f"Best time: {self.best_time:.2f}s", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
            self.screen.blit(text, text_rect)

        pg.display.flip()
    
    def save_score(self):
        with open("score.txt", "w") as f:
            f.write(f"{self.timer:.2f}\n")
    
    def load_score(self) -> float:
        try:
            with open("score.txt", "r") as f:
                score = f.readline().strip()
                return float(score)
        except FileNotFoundError:
            return 0.0
