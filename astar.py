import pygame
import sys
import heapq


pygame.init()


# Constants
TILE_SIZE = 30
ROWS, COLS = 11,15
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE+100  
WHITE = (255, 255, 255)
BLACK = (34, 40, 49)
PATH = (83, 125, 93)
VISITED =(242, 97, 63)
font = pygame.font.Font(None, 14)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm de A*")

path_btn = pygame.Rect(10, HEIGHT-80, 100, 50)
path_text = font.render("Afficher le chemin", True, WHITE)
visited_btn = pygame.Rect(180, HEIGHT-80, 100, 50)
visited_text = font.render("Cases visitées", True, WHITE)
reset_btn  = pygame.Rect(330, HEIGHT-80, 100, 50)
reset_text = font.render("Effacer", True, WHITE)

maze = [
    ["D",1,1,1,0,0,0,0,0,1,1,1,1,0,0],
    [0,1,0,0,0,1,1,1,1,1,0,0,1,0,0],
    [0,1,1,0,0,1,0,0,0,1,0,0,1,0,0],
    [0,1,0,0,0,1,0,0,0,1,1,1,1,0,0],
    [0,1,0,1,1,1,1,1,1,1,0,0,1,0,0],
    [0,1,1,1,0,0,0,0,0,1,0,0,1,0,0],
    [0,1,0,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,0,0,0,0,0,1,0,0,0,0,1,0,0],
    [0,1,0,1,1,1,0,1,0,1,1,1,1,0,0],
    [0,1,1,1,0,1,1,1,1,1,0,0,1,1,"A"],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

# distance de manhattan
def heuristic(a,b):
    return (abs(a[0]-b[0]) + abs(a[1] - b[1]))



def astar(maze,start, end):
    open_set = []
    heapq.heappush(open_set,(0, start)) 
    came_from = {}
    g_score = {start :0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        current = heapq.heappop(open_set)[1]
        visited.add(current)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current] 
            path.append(start)
            return path[::-1],visited
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS:
                if maze[neighbor[0]][neighbor[1]] == 0:
                    continue               
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return [], visited


def find_pos(maze, target):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == target:
                return (r, c)
    return None

visited = set()
start = find_pos(maze, "D")
end = find_pos(maze, "A")
run = True
path, visited = astar(maze, start,end)
path_index = 0
clock = pygame.time.Clock()
show_path = False
show_visited = False
while run :

    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 0:
                pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif maze[row][col] == "A":
                pygame.draw.rect(screen, (0, 255, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif maze[row][col] == "D":
                pygame.draw.rect(screen, (255, 0, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else :
                pygame.draw.rect(screen, WHITE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))


    for btn, text in [(path_btn, path_text), (visited_btn, visited_text), (reset_btn, reset_text)]:
        pygame.draw.rect(screen, BLACK, btn, border_radius=10)
        text_rect = text.get_rect(center=btn.center)   
        screen.blit(text, text_rect)

    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if path_btn.collidepoint(event.pos):
                show_path = True
            if visited_btn.collidepoint(event.pos):
                show_visited = True
            if reset_btn.collidepoint(event.pos):
                show_path=False
                show_visited=False
                path_index = 0
                
    if visited and show_visited:
     for r, c in visited:
        if maze[r][c] not in ("D", "A"): 
            pygame.draw.rect(screen, VISITED, 
                             (c * TILE_SIZE, r * TILE_SIZE , TILE_SIZE, TILE_SIZE))
   
    if path and show_path:
        for i in range(path_index):
            r, c = path[i]
            pygame.draw.rect(screen, PATH, 
                             (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        if path_index < len(path):
            path_index += 1    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    pygame.display.flip()
    clock.tick(5)

pygame.quit()
sys.exit()