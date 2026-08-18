import random
import pygame

pygame.init()
WIDTH, HEIGHT = 1800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
pygame.display.set_caption("Friday Night Funkin (Reverse Engine)")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)

COLORS = {
    0: {"normal": (194, 75, 153), "pressed": (255, 150, 220)},  
    1: {"normal": (0, 255, 255),   "pressed": (150, 255, 255)},  
    2: {"normal": (0, 255, 0),     "pressed": (150, 255, 150)},  
    3: {"normal": (255, 0, 0),     "pressed": (255, 150, 150)}   
}

def create_arrow_texture(color, size=110):
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    points = [
        (size // 2, 8),                 
        (size - 8, size // 2),          
        (size * 0.72, size // 2),        
        (size * 0.72, size - 8),         
        (size * 0.28, size - 8),         
        (size * 0.28, size // 2),        
        (8, size // 2)                  
    ]
    pygame.draw.polygon(surface, color, points)
    return surface

ARROW_TEXTURES = {}
RECEPTOR_TEXTURES = {}

for lane, col in COLORS.items():
    rotation_angles = {0: 90, 1: 180, 2: 0, 3: -90}
    angle = rotation_angles[lane]
    
    base_normal = create_arrow_texture(col["normal"])
    base_pressed = create_arrow_texture(col["pressed"])
    
    ARROW_TEXTURES[lane] = {
        "normal": pygame.transform.rotate(base_normal, angle),
        "pressed": pygame.transform.rotate(base_pressed, angle)
    }
    
    receptor_base = pygame.Surface((110, 110), pygame.SRCALPHA)
    points = [
        (55, 8), (102, 55), (79, 55), (79, 102), (31, 102), (31, 55), (8, 55)
    ]
    pygame.draw.polygon(receptor_base, col["normal"], points, 5) 
    RECEPTOR_TEXTURES[lane] = pygame.transform.rotate(receptor_base, angle)

key_states = {0: False, 1: False, 2: False, 3: False}
score = 0
combo = 0

class Note:
    def __init__(self, lane):
        self.lane = lane
        self.y = HEIGHT + 20
        self.speed = 14        
        self.hit = False

notes_list = []
running = True
lane_width = 130  
start_x = (WIDTH // 2) + 150  
spawn_timer = 0
font = pygame.font.SysFont("utf", 24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            lane_pressed = None
            if event.key == pygame.K_LEFT:    lane_pressed = 0
            elif event.key == pygame.K_DOWN:  lane_pressed = 1
            elif event.key == pygame.K_UP:    lane_pressed = 2
            elif event.key == pygame.K_RIGHT: lane_pressed = 3
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
            
            if lane_pressed is not None:
                key_states[lane_pressed] = True
                
                for note in notes_list:
                    if note.lane == lane_pressed and not note.hit:
                        if -30 <= note.y <= 170:  
                            note.hit = True
                            score += 100
                            combo += 0
                            print(f"HIT! Score: {score}")
                            break

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:    key_states[0] = False
            elif event.key == pygame.K_DOWN:  key_states[1] = False
            elif event.key == pygame.K_UP:    key_states[2] = False
            elif event.key == pygame.K_RIGHT: key_states[3] = False

    screen.fill(BLACK)

    spawn_timer += 1
    if spawn_timer >= 25:
        random_lane = random.randint(0, 3)
        notes_list.append(Note(random_lane))
        spawn_timer = 0

    for i in range(4):
        x = start_x + (i * lane_width)
        y = 50
        
        pygame.draw.rect(screen, GRAY, (x + 5, 0, lane_width - 10, HEIGHT), 1)
        asset_x = x + 10
        
        if key_states[i]:
            screen.blit(ARROW_TEXTURES[i]["pressed"], (asset_x, y))
        else:
            screen.blit(RECEPTOR_TEXTURES[i], (asset_x, y))

    for note in notes_list[:]:
        if not note.hit:
            note.y -= note.speed
            x = start_x + (note.lane * lane_width)
            screen.blit(ARROW_TEXTURES[note.lane]["normal"], (x + 10, note.y))
            
            if note.y < -120:
                notes_list.remove(note)
                combo = 0
                print("MISS!")
        else:
            notes_list.remove(note)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (675, 850))

    pygame.display.flip()
    clock.tick(75)

pygame.quit()
