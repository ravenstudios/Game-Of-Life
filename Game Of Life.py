import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 1200, 1200
TILE_SIZE = 5
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

FPS = 60

iterations = 0
re_generations = 0

pygame.display.set_caption(
        f"Conway's Game of Life  |  Gen {iterations}  | Alive 0 |  Press SPACE to start/stop  |  Press C to clear  |  Press G to generate random cells"
    )


screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(BLACK)

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
    global iterations, re_generations
    running = True
    playing = False
    count = 0
    update_freq = 10
    positions = set()
    prev_positions = set()
    STUCK_LIMIT = 10
    stuck_count = 0
    


    
    while running:
        clock.tick(FPS)
        
        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            new_positions = adjust_grid(positions)
            iterations += 1

            if (new_positions == positions or new_positions == prev_positions or not new_positions):
                stuck_count += 1
                print("Stuck for ", stuck_count, " iterations")
            else: 
                stuck_count = 0
            if stuck_count >= STUCK_LIMIT:
                print("Stuck for too long, generating new cells")
                re_generations += 1
                print("Re-generations: ", re_generations)
                new_positions = gen(random.randrange(14, 24) * GRID_WIDTH)
                iterations = 0
                stuck_count = 0

            prev_positions = positions
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

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                    iterations = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(14, 24) * GRID_WIDTH)


        screen.blit(background, (0, 0))
        draw_grid(positions)
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()









