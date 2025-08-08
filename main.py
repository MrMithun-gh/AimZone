import math
import random
import time
import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AimZone")

# --- Game constants and variables ---
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
LIVES = 3
HIGHSCORE_FILE = "highscore.txt"

# --- Design variables ---
BG_COLOR = (12, 12, 24)  # Deep, dark blue for a modern feel
TOP_BAR_HEIGHT = 60
LABEL_FONT = pygame.font.SysFont("helvetica", 28, bold=True)
BUTTON_FONT = pygame.font.SysFont("helvetica", 36, bold=True)
TEXT_COLOR = (255, 255, 255) # White text for high contrast

# --- Game states ---
START_SCREEN = 0
GAME_LOOP = 1
END_SCREEN = 2

# --- File I/O functions for high score ---
def load_highscore():
    """Loads the high score from a file, returns 0 if the file doesn't exist."""
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except (ValueError, IndexError):
                return 0
    return 0

def save_highscore(score):
    """Saves the new high score to a file."""
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# --- Helper function to draw a button (bug fixed) ---
def draw_button(win, text, x, y, width, height, active_color, inactive_color, font):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    rect = pygame.Rect(x, y, width, height)
    
    # Change color on hover
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(win, active_color, rect, border_radius=10)
        # Check for click (bug fixed here)
        if click[0]:
            return True
    else:
        pygame.draw.rect(win, inactive_color, rect, border_radius=10)
    
    # Draw text
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    win.blit(text_surface, text_rect)
    return False

# --- Target Class with New Design ---
class Target:
    MAX_SIZE = 35
    GROWTH_RATE = 0.3
    COLOR = (50, 200, 255) # Cyan
    HOTSPOT_COLOR = (255, 255, 255) # White

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size, 5)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.7, 5)
        pygame.draw.circle(win, self.HOTSPOT_COLOR, (self.x, self.y), self.size * 0.3)
        
    def collide(self, x, y):
        dis = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return dis <= self.size

# --- Drawing and UI Functions ---

def draw(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    top_bar_surface = pygame.Surface((WIDTH, TOP_BAR_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(top_bar_surface, (0, 0, 0, 150), (0, 0, WIDTH, TOP_BAR_HEIGHT))
    pygame.draw.line(top_bar_surface, TEXT_COLOR, (0, TOP_BAR_HEIGHT - 1), (WIDTH, TOP_BAR_HEIGHT - 1), 2)
    win.blit(top_bar_surface, (0, 0))

    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, TEXT_COLOR)
    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, TEXT_COLOR)
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, TEXT_COLOR)
    lives_color = (255, 50, 50) if LIVES - misses <= 1 else TEXT_COLOR
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, lives_color)
    
    win.blit(time_label, (20, TOP_BAR_HEIGHT // 2 - time_label.get_height() // 2))
    win.blit(speed_label, (220, TOP_BAR_HEIGHT // 2 - speed_label.get_height() // 2))
    win.blit(hits_label, (450, TOP_BAR_HEIGHT // 2 - hits_label.get_height() // 2))
    win.blit(lives_label, (650, TOP_BAR_HEIGHT // 2 - lives_label.get_height() // 2))

def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

# --- Game Screens ---

def start_screen(personal_best):
    global game_state
    run = True
    while run:
        WIN.fill(BG_COLOR)
        
        title_font = pygame.font.SysFont("helvetica", 60, bold=True)
        title_label = title_font.render("AimZone", 1, TEXT_COLOR)
        title_rect = title_label.get_rect(center=(WIDTH/2, 150))
        WIN.blit(title_label, title_rect)
        
        # Display Personal Best
        personal_best_label = LABEL_FONT.render(f"Personal Best: {personal_best} hits", 1, (200, 200, 200))
        personal_best_rect = personal_best_label.get_rect(center=(WIDTH/2, 250))
        WIN.blit(personal_best_label, personal_best_rect)
        
        button_x = WIDTH/2 - 100
        button_y = HEIGHT/2 + 50
        button_width = 200
        button_height = 60
        
        # Draw Start button
        if draw_button(WIN, "Start Game", button_x, button_y, button_width, button_height, (50, 200, 255), (20, 100, 150), BUTTON_FONT):
            game_state = GAME_LOOP
            return

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

def end_screen(elapsed_time, targets_pressed, clicks, personal_best):
    global game_state
    run = True
    while run:
        WIN.fill(BG_COLOR)
        
        # Check and save new high score
        new_personal_best = False
        if targets_pressed > personal_best:
            personal_best = targets_pressed
            save_highscore(personal_best)
            new_personal_best = True
        
        # Render end screen stats
        title_font = pygame.font.SysFont("helvetica", 50, bold=True)
        game_over_label = title_font.render("Game Over", 1, TEXT_COLOR)
        WIN.blit(game_over_label, (get_middle(game_over_label), 50))
        
        if new_personal_best:
            new_pb_label = LABEL_FONT.render("New Personal Best!", 1, (50, 255, 50))
            WIN.blit(new_pb_label, (get_middle(new_pb_label), 120))
        
        time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, TEXT_COLOR)
        speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0
        speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, TEXT_COLOR)
        hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, TEXT_COLOR)
        accuracy = round(targets_pressed / clicks * 100, 1) if clicks > 0 else 0
        accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, TEXT_COLOR)
        personal_best_label = LABEL_FONT.render(f"Personal Best: {personal_best} hits", 1, (200, 200, 200))

        WIN.blit(time_label, (get_middle(time_label), 170))
        WIN.blit(speed_label, (get_middle(speed_label), 230))
        WIN.blit(hits_label, (get_middle(hits_label), 290))
        WIN.blit(accuracy_label, (get_middle(accuracy_label), 350))
        WIN.blit(personal_best_label, (get_middle(personal_best_label), 410))
        
        # Draw Play Again button
        if draw_button(WIN, "Play Again", WIDTH/2 - 150, 480, 300, 60, (50, 200, 255), (20, 100, 150), BUTTON_FONT):
            game_state = GAME_LOOP
            return
            
        # Draw Exit button
        if draw_button(WIN, "Exit", WIDTH/2 - 150, 550, 300, 60, (255, 50, 50), (150, 20, 20), BUTTON_FONT):
            pygame.quit()
            quit()
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

# --- Main Game Logic ---
def main_game_loop():
    global game_state
    
    run = True
    targets = []
    clock = pygame.time.Clock()
    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)
    
    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
                
        for target in targets[:]:
            target.update()
            if target.size <= 0:
                targets.remove(target)
                misses += 1
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1
        
        if misses >= LIVES:
            game_state = END_SCREEN
            return elapsed_time, targets_pressed, clicks
        
        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()
        
    pygame.quit()

# --- Main program loop ---
if __name__ == "__main__":
    game_state = START_SCREEN
    personal_best = load_highscore()
    
    while True:
        if game_state == START_SCREEN:
            start_screen(personal_best)
        elif game_state == GAME_LOOP:
            elapsed_time, targets_pressed, clicks = main_game_loop()
            personal_best = targets_pressed if targets_pressed > personal_best else personal_best
        elif game_state == END_SCREEN:
            end_screen(elapsed_time, targets_pressed, clicks, personal_best)
