import pygame
import math
from queue import PriorityQueue
#display or windows for the visualization of the A* path finding algorithm [which is a square]
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")
#setting up the colors for the visuals
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

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		#setting the co-ordinates of the cubes in the display:
		self.x = row * width
		self.y = col * width
		self.color = WHITE#the color of the start cubes will be white
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):#getting the position of the node
		return self.row, self.col

	def is_closed(self):#have we already looked at this node
		return self.color == RED

	def is_open(self):#is this node open to visit
		return self.color == GREEN

	def is_barrier(self):# is this path blocked? If so the algorithm will not consider this path as a node
		return self.color == BLACK

	def is_start(self):#the start node
		return self.color == ORANGE

	def is_end(self): #the end node
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE
	#making way for algorithm
	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):# win=windows where are we going to draw these cubes
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))#drawing the cubes (start_node,end_node etc.)

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #checking DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # checking UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # checking RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # checking LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):#lt=less than , while comparing spots the one spot is less than its other spots
		return False


def h(p1, p2):#defining the heuristic function for the algorithm where p1 and p2 are two points
	#using the Manhattan distance formulae which is basically measuring the distance between the two vertices??? x positional values and between their y positional values and returning the sum of their distances
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)#where abs=absolute value


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}# starting the g score at infinity
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}# starting the f score at infinity
	f_score[start] = h(start.get_pos(), end.get_pos()) #taking heuristic value to calculate the guess value from the start node to the end node

	open_set_hash = {start}#checking what the priority queue has inside

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current) 

		if current == end:# found the path
			reconstruct_path(came_from, end, draw)
			end.make_end()#make path
			return True

		for neighbor in current.neighbors:#otherwise calculate the other neighbors and calculate their neighbor scores
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:#if the new neighbor score is less than what it was previously in the table
				#update the values:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows #the width of each cube
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):#finding the mouse cursor/position on the grid
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)#calling to draw the grid
		for event in pygame.event.get():
			if event.type == pygame.QUIT:#if 'x' at the top right hand corner is clicked end the event
				run = False

			if pygame.mouse.get_pressed()[0]: #left mouse button
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:# so that start and end point does not become the sam
					start = spot
					start.make_start()

				elif not end and spot != start:# so that start and end point does not become the sam
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: #right mouse button
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:#if we press key down
				if event.key == pygame.K_SPACE and start and end: #if the key is the space bar and not yet started the algorithm
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)

