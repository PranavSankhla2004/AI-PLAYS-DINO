import pygame
import os
import random
import neat
import sys

# --- Constants ---
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
FPS = 60
INITIAL_GAME_SPEED = 20
POINT_INCREMENT = 0.25

# Load assets safely
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

def load_image(name):
    return pygame.image.load(os.path.join(ASSETS_PATH, name)).convert_alpha()

# --- Game Class ---
class DinoGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dino Game AI")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)

        # Load images
        self.RUNNING = [load_image("Dino/DinoRun1.png"), load_image("Dino/DinoRun2.png")]
        self.JUMPING = load_image("Dino/DinoJump.png")
        self.DUCKING = [load_image("Dino/DinoDuck1.png"), load_image("Dino/DinoDuck2.png")]
        self.SMALL_CACTUS = [load_image("Cactus/SmallCactus1.png"),
                             load_image("Cactus/SmallCactus2.png"),
                             load_image("Cactus/SmallCactus3.png")]
        self.LARGE_CACTUS = [load_image("Cactus/LargeCactus1.png"),
                             load_image("Cactus/LargeCactus2.png"),
                             load_image("Cactus/LargeCactus3.png")]
        self.BIRD = [load_image("Bird/Bird1.png"), load_image("Bird/Bird2.png")]
        self.CLOUD = load_image("Other/Cloud.png")
        self.BG = load_image("Other/Track.png")

        # Game state
        self.game_speed = INITIAL_GAME_SPEED
        self.points = 0
        self.x_pos_bg = 0
        self.death_count = 0
        self.generation = 0
        self.debug = False
        self.obstacles = []

    def reset(self):
        self.game_speed = INITIAL_GAME_SPEED
        self.points = 0
        self.x_pos_bg = 0
        self.player = Dinosaur(self)
        self.obstacles = []
        self.cloud = Cloud(self)

    def human_play(self):
        self.reset()
        run = True
        while run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.debug = not self.debug

            userInput = pygame.key.get_pressed()
            self.screen.fill((255, 255, 255))
            self.cloud.update()
            self.cloud.draw(self.screen)
            self.player.update(userInput)
            self.player.draw(self.screen)

            self.spawn_obstacles()

            for obstacle in list(self.obstacles):
                obstacle.draw(self.screen)
                if obstacle.update(self.game_speed):
                    self.obstacles.remove(obstacle)

            self.game_speed += 0.001
            self.points += POINT_INCREMENT

            self.draw_background()
            draw_score(self.screen, self.points, self.font)

            if check_collision(self.player, self.obstacles):
                self.menu(self.points)
                run = False

            pygame.display.update()

    def spawn_obstacles(self):
        if len(self.obstacles) == 0 or (len(self.obstacles) < 2 and random.randint(0, 60) == 0):
            choice = random.randint(0, 2)
            if choice == 0:
                self.obstacles.append(SmallCactus(self))
            elif choice == 1:
                self.obstacles.append(LargeCactus(self))
            else:
                self.obstacles.append(Bird(self))

    def run_ai_training(self, config_file):
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.StatisticsReporter())
        winner = population.run(self.eval_genomes, 50)
        return winner

    def eval_genomes(self, genomes, config):
        self.generation += 1
        self.nets, self.genomes, self.dinos = [], [], []
        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.genomes.append(genome)
            self.dinos.append(Dinosaur(self))

        self.obstacles = []
        self.cloud = Cloud(self)
        self.game_speed = INITIAL_GAME_SPEED
        self.points = 0

        run = True
        while run and len(self.dinos) > 0:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.debug = not self.debug

            self.screen.fill((255, 255, 255))
            self.cloud.update()
            self.cloud.draw(self.screen)
            self.spawn_obstacles()

            for obstacle in list(self.obstacles):
                obstacle.draw(self.screen)
                if obstacle.update(self.game_speed):
                    self.obstacles.remove(obstacle)

            survivors, nets, ge = [], [], []
            for dino, net, genome in zip(self.dinos, self.nets, self.genomes):
                output = net.activate(self.get_ai_inputs(dino))
                userInput = {pygame.K_UP: output[0] > 0.5, pygame.K_DOWN: output[1] > 0.5}
                dino.update(userInput)
                dino.draw(self.screen)

                genome.fitness += 0.1
                if not check_collision(dino, self.obstacles):
                    survivors.append(dino)
                    nets.append(net)
                    ge.append(genome)
                else:
                    genome.fitness -= 1

            self.dinos, self.nets, self.genomes = survivors, nets, ge
            self.game_speed += 0.001
            self.points += POINT_INCREMENT

            self.draw_background()
            draw_score(self.screen, self.points, self.font)

            if self.debug:
                for dino in self.dinos:
                    pygame.draw.rect(self.screen, (0, 255, 0), dino.dino_rect, 2)
                for obstacle in self.obstacles:
                    pygame.draw.rect(self.screen, (255, 0, 0), obstacle.rect, 2)
            # Show generation and remaining dinos
            gen_text = self.font.render(f"Gen: {self.generation}", True, (0, 0, 0))
            dino_text = self.font.render(f"Dinos: {len(self.dinos)}", True, (0, 0, 0))
            goal_text = self.font.render("Goal: Survive and avoid obstacles!", True, (0, 0, 0))
            self.screen.blit(gen_text, (50, 50))
            self.screen.blit(dino_text, (50, 90))
            self.screen.blit(goal_text, (50, 130))

            pygame.display.update()

    def draw_background(self):
        self.screen.blit(self.BG, (self.x_pos_bg, 380))
        self.screen.blit(self.BG, (self.x_pos_bg + self.BG.get_width(), 380))
        self.x_pos_bg -= self.game_speed
        if self.x_pos_bg <= -self.BG.get_width():
            self.x_pos_bg = 0

    def get_ai_inputs(self, dino):
        nearest = min((obs for obs in self.obstacles if obs.rect.x > dino.dino_rect.x),
                      default=None, key=lambda obs: obs.rect.x - dino.dino_rect.x)
        if nearest is None:
            return [0, 0, 0, 0, 0]

        return [
            (nearest.rect.x - dino.dino_rect.x) / SCREEN_WIDTH,
            nearest.rect.width / 100,
            nearest.rect.height / 100,
            dino.dino_rect.y / SCREEN_HEIGHT,
            self.game_speed / 50
        ]

    def menu(self, score):
        self.screen.fill((255, 255, 255))
        text = self.font.render("Press any key to start" if self.death_count == 0 else "Press any key to restart", True, (0, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
        if self.death_count > 0:
            score_text = self.font.render(f"Score: {int(score)}", True, (0, 0, 0))
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        pygame.display.update()

        self.death_count += 1
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    self.main()

    def main(self):
        print("1. Train AI\n2. Play Human\n3. Exit")
        choice = input("Choose mode: ")
        if choice == '1':
            config_path = os.path.join(os.path.dirname(__file__), "neat-config.txt")
            if os.path.exists(config_path):
                self.run_ai_training(config_path)
            else:
                print("Missing neat-config.txt")
        elif choice == '2':
            self.human_play()
        elif choice == '3':
            pygame.quit()
            sys.exit()
        else:
            print("Invalid choice.")
            self.main()

# --- Game Entities ---
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self, game):
        self.game = game
        self.run_img = game.RUNNING
        self.jump_img = game.JUMPING
        self.duck_img = game.DUCKING
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect(x=self.X_POS, y=self.Y_POS)
        self.jump_vel = self.JUMP_VEL
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.step_index = 0

    def update(self, userInput):
        if self.dino_jump:
            self.jump()
        elif userInput[pygame.K_UP] and not self.dino_jump and self.dino_rect.y == self.Y_POS:
            self.dino_jump = True
            self.dino_run = False
        elif userInput[pygame.K_DOWN]:
            self.dino_duck = True
            self.dino_run = False
        else:
            self.dino_run = True
            self.dino_duck = False

        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()

        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        self.dino_rect.y -= self.jump_vel * 4
        self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.image, self.dino_rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Cloud:
    def __init__(self, game):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = game.CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= 5
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, game, image_list, type):
        self.image_list = image_list
        self.image = image_list[type]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, speed):
        self.rect.x -= speed
        return self.rect.x < -self.rect.width

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class SmallCactus(Obstacle):
    def __init__(self, game):
        super().__init__(game, game.SMALL_CACTUS, random.randint(0, 2))
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, game):
        super().__init__(game, game.LARGE_CACTUS, random.randint(0, 2))
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, game):
        self.index = 0
        super().__init__(game, game.BIRD, 0)
        self.rect.y = 250

    def update(self, speed):
        self.index += 1
        self.image = self.image_list[self.index // 5 % 2]
        return super().update(speed)

# --- Utility Functions ---
def check_collision(dino, obstacles):
    dino_mask = dino.get_mask()
    for obs in obstacles:
        offset = (obs.rect.x - dino.dino_rect.x, obs.rect.y - dino.dino_rect.y)
        if dino_mask.overlap(obs.get_mask(), offset):
            return True
    return False

def draw_score(screen, points, font):
    text = font.render(f"Score: {int(points)}", True, (0, 0, 0))
    screen.blit(text, (900, 50))

# --- Entry Point ---
if __name__ == "__main__":
    DinoGame().main()
