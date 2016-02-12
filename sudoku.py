sample_grid = [
	[1,6,2,0,0,0,0,0,0],
	[0,0,0,2,8,9,0,0,0],
	[9,0,0,0,0,1,5,0,0],
	[2,5,0,0,0,6,4,0,0],
	[4,0,0,0,1,0,0,0,7],
	[0,0,1,9,0,0,0,6,5],
	[0,0,3,6,0,0,0,0,4],
	[0,0,0,5,9,8,0,0,0],
	[0,0,0,0,0,0,2,5,6]
]

def print_grid(grid):
	separator_line = "+ - - - + - - - + - - - +"
	for i in range(9):
		if(i % 3) == 0: print separator_line
		for j, value in enumerate(grid[i]):
			if (j % 3) == 0: print "|",
			print (value if value else " "),
		print "|"
	print separator_line


def read_from_file(filename):
	with open(filename) as f:
		grid = [map(int,line.split(",")) for line in f.read().splitlines()]
	return grid

def row(grid,i):
	"""
	return a list of elements for row i
	"""
	return grid[i]

def col(grid,j):
	"""
	return a list of elements for column j
	"""
	return [row[j] for row in grid]

def box_range(k):
	return range((k/3)*3,((k+1)/3)*3)

def box(grid,i,j):
	"""
	return a list of elements for box at index i,j
	"""
	return [grid[k][l] for k in box_range(i) for l in box_range(j)]


def candidates_for(grid,i,j):
	"""
	return the basic candidates for the cell [i,j]
	"""
	if grid[i][j]: return [grid[i][j]]
	return [v for v in range(1,10) if v not in row(grid,i) and v not in col(grid,j) and v not in box(grid,i,j)]

def basic_candidates(grid):
	cdts = [candidates_for(grid,i,j)  for i in range(9) for j in range(9)]
	return cdts

def solve(grid):
	was_modified = true
	cdts = basic_candidates(grid)
	while was_modified:
		grid, cdts, was_modified = 
	return grid


test_grid = read_from_file("sample.csv")

print_grid(sample_grid)

print_grid(test_grid)

print basic_candidates(test_grid)