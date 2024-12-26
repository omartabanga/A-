import pygame
import heapq
import random
import time

# the initializing 
pygame.init()

# Screen and grid dimensions
screen_width, screen_height = 800, 800
tile_size = 40
grid_width = screen_width // tile_size
grid_height = screen_height // tile_size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
VISITED_COLOR = (173, 216, 230)

# setup for the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("A* Pathfinding Game")

# Directions 
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, goal):
    open_list = PriorityQueue()
    open_list.put(start, 0)
    came_from = {}
    cost_so_far = {}

    came_from[start] = None
    cost_so_far[start] = 0

    while not open_list.empty():
        current = open_list.get()

        if current == goal:
            break

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < grid_width and 0 <= neighbor[1] < grid_height:
                # makes the damage tile traversable
                if grid[neighbor[1]][neighbor[0]] == 10:
                    tile_cost = 1  # the cost to pass through it
                else:
                    tile_cost = 1 if grid[neighbor[1]][neighbor[0]] in [1, 5] else grid[neighbor[1]][neighbor[0]]

                if tile_cost == -1:  # Obstacle
                    continue

                new_cost = cost_so_far[current] + tile_cost

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    open_list.put(neighbor, priority)
                    came_from[neighbor] = current

    return came_from

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()
    return path

def generate_random_grid():
    grid = [[1 for _ in range(grid_width)] for _ in range(grid_height)]

    # putting obstacled randomly
    for _ in range(40):
        x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
        grid[y][x] = -1

    # putting gold randomly 
    for _ in range(10):
        x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
        if grid[y][x] == 1:
            grid[y][x] = 5

    # putting damage randomly
    for _ in range(10):
        x, y = random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)
        if grid[y][x] == 1:
            grid[y][x] = 10

    return grid

def main():
    
    clock = pygame.time.Clock()
    grid = generate_random_grid()

    # Start and goal positions
    start = (0, 0)
    goal = (grid_width - 1, grid_height - 1)

    # Ensure start and goal positions are walkable
    grid[start[1]][start[0]] = 1
    grid[goal[1]][goal[0]] = 1

    # Player stats
    player_health = 100  # Start with 100 health
    player_gold = 0

    # Pathfinding
    came_from = a_star_search(grid, start, goal)
    path = reconstruct_path(came_from, start, goal)

    running = True
    for node in path:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        # Check if the current node is a gold or damage cell
        x, y = node
        if grid[y][x] == 5:  # Gold cell
            player_gold += 1
            grid[y][x] = 1  # Collect the gold and turn it into a normal cell
            print(f"Gold collected! Total gold: {player_gold}")

        elif grid[y][x] == 10:  # Damage cell
            player_health -= 10  # Lose 10 health when stepping on damage cell
            grid[y][x] = 1  # Turn the damage cell into a normal cell
            print(f"Ouch! Lost 10 health. Current health: {player_health}")

        # Mark the current tile as visited
        grid[y][x] = 2  # Mark as visited

        # Draw the grid
        for y in range(grid_height):
            for x in range(grid_width):
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)

                if grid[y][x] == -1:  # Obstacle
                    pygame.draw.rect(screen, BLACK, rect)
                elif grid[y][x] == 10:  # Damage tile
                    pygame.draw.rect(screen, RED, rect)
                elif grid[y][x] == 5:  # Gold tile
                    pygame.draw.rect(screen, GOLD, rect)
                elif grid[y][x] == 2:  # Visited tile
                    pygame.draw.rect(screen, VISITED_COLOR, rect)
                else:  # Normal tile
                    pygame.draw.rect(screen, GREEN, rect, 1)

        # Draw the current path node
        rect = pygame.Rect(node[0] * tile_size, node[1] * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, BLUE, rect)

        # Draw start and goal
        start_rect = pygame.Rect(start[0] * tile_size, start[1] * tile_size, tile_size, tile_size)
        goal_rect = pygame.Rect(goal[0] * tile_size, goal[1] * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, GREEN, start_rect)
        pygame.draw.rect(screen, GREEN, goal_rect)

        pygame.display.flip()

        # Slow down the visualization
        time.sleep(0.2)  # Pause for 0.2 seconds for each step

        # Check for game over condition
        if player_health <= 0:
            print(f"Game Over! You lost all your health. Total gold collected: {player_gold}")
            break

    if player_health > 0:
        print(f"Game Over! Total gold collected: {player_gold}")
    pygame.quit()


if __name__ == "__main__":
    main()


