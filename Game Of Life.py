import pygame
import random
from collections import deque

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
DESKTOP_W, DESKTOP_H = pygame.display.get_desktop_sizes()[0]

def switch_display(fullscreen: bool):

    global screen, background, WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT

    flags = pygame.FULLSCREEN | pygame.SCALED if fullscreen else 0

    if fullscreen:
        WIDTH, HEIGHT = DESKTOP_W, DESKTOP_H
        flags = pygame.FULLSCREEN 
    else:
        WIDTH, HEIGHT = 1200, 1200
        flags = 0
        

    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BLACK)
    GRID_WIDTH = WIDTH // TILE_SIZE
    GRID_HEIGHT = HEIGHT // TILE_SIZE

display_info = pygame.display.Info()
try: WIDTH, HEIGHT = display_info.current_w, display_info.current_h
except AttributeError:
    # Fallback to a default size if display_info is not available
    print("Display info not available, using default size.")
    WIDTH, HEIGHT = 1200, 1200

TILE_SIZE = 5
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

FPS = 60

HISTORY_LENGTH = 8
iterations = 0
re_generations = 0

pygame.display.set_caption(
        f"Conway's Game of Life  |  Gen {iterations}  | Alive 0 |  Press SPACE to start/stop  |  Press C to clear  |  Press G to generate random cells"
    )


fullscreen = True
switch_display(fullscreen)

clock = pygame.time.Clock()



def gen (num):
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(num)])



def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))




    
def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set ()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions


def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx >= GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy >= GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))

    return neighbors





def main():
    global iterations, re_generations, fullscreen 
    
    running = True
    playing = False
    count = 0
    update_freq = 10
    positions = set()
    STUCK_LIMIT = 10
    stuck_count = 0
    state_history = deque(maxlen=HISTORY_LENGTH)
    
    


    
    while running:
        clock.tick(FPS)
        
        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            new_positions = adjust_grid(positions)
            iterations += 1

            state_key = frozenset(new_positions)
            state_history.append(state_key)
            if (state_key in list(state_history)[:-1]) or (not new_positions):
                stuck_count += 1
            else:
                stuck_count = 0
            if stuck_count >= STUCK_LIMIT:
                print("Stuck for too long, generating new cells")
                re_generations += 1
                print("Re-generations: ", re_generations)
                new_positions = gen(random.randrange(14, 24) * GRID_WIDTH)
                iterations = 0
                state_history.clear()
                stuck_count = 0

            
            positions = new_positions
            pygame.display.set_caption(
        f"Conway's Game of Life  |  Gen {iterations}  |  Alive {len(positions)}  |  Press SPACE to start/stop  |  Press C to clear  |  Press G to generate random cells"
    )

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    switch_display(fullscreen)

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                    iterations = 0
                    state_history.clear()
                    stuck_count = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(14, 24) * GRID_WIDTH)
                    state_history.clear()
                    stuck_count = 0


        screen.blit(background, (0, 0))
        draw_grid(positions)
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()









