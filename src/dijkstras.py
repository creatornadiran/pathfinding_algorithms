import pygame
import math
from queue import Queue
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("DIJKTRA'S PATH FINDING ALGORITHM")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.cost = float("inf")
        self.color =WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.came_from= None

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE
    def make_open(self):
        self.color = GREEN
    def make_closed(self):
        self.color = RED
    def make_barrier(self):
        self.color = BLACK
    def make_start(self):
        self.color = ORANGE
    def make_end(self):
        self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows-1 and not grid[self.row +1][self.col].is_barrier(): #Checking DOWN Neighbor
            self.neighbors.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid[self.row -1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row-1][self.col])
        if self.col < self.total_rows-1 and not grid[self.row ][self.col+1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col+1])
        if self.col> 0 and not grid[self.row ][self.col-1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col-1])
    def __lt__(self,other):
        return False
def draw_path(node, draw):
    current = node
    while current.color != ORANGE:
        current.make_path()
        current = current.came_from
        draw()
def algorithm(draw, grid, start, end):
    open_set = Queue()
    start.cost = 0
    open_set.put(start)
    open_set_hash = {start} #will be evaluated
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get() #Current Node
        open_set_hash.remove(current) #To prevent duplication

        if current == end: #Draws path
            draw_path(current, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_cost = current.cost+1
            if temp_cost < neighbor.cost: #If algorithm finds a more efficient way updates g score with efficient one and opens it
                neighbor.came_from = current
                neighbor.cost = temp_cost
                if neighbor not in open_set_hash: #If not open make it
                    open_set.put(neighbor)
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
            draw() #updates grids on every iteration

            if current != start: #don't check again
                current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,gap,rows)
            grid[i].append(node)
    return grid
def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0,i*gap), (width, i*gap)) #Draws vertical lines
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))  # Draws horizontal lines


def draw(win, grid, rows, width):
     win.fill(WHITE)
     for row in grid:
        for node in row:
            node.draw(win)
     draw_grid(win, rows, width)
     pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row, col
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: #LEFT -- Start / End Node
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width )
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
            elif pygame.mouse.get_pressed()[2]: #RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end=None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c: #Resets
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(WIN, WIDTH)