from itertools import product

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
	"""
	Utility function: print grid to the program output
	"""
	separator_line = "+ - - - + - - - + - - - +"
	for i in range(9):
		if(i % 3) == 0: print separator_line
		for j, value in enumerate(grid[i]):
			if (j % 3) == 0: print "|",
			print (value if value else " "),
		print "|"
	print separator_line

def print_candidates(cdts):
	"""
	Utility function: print candidates for a grid to the program output
	"""
	separator_line = "+ ---   ---   --- + ---   ---   --- + ---   ---   --- +"
	for i in range(9):
		print separator_line
		for line in range(3):
			line_list = [[str(v) if v in cdts[i][j] else " " for v in range(3*line+1,3*line+4)] for j in range(9)]
			print "|"," | ".join(["".join(three_digits) for three_digits in line_list]), "|"
	print separator_line

def read_from_file(filename):
	"""
	Read a grid from a file, in csv format. See 'sample.csv' for expected formatting
	"""
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
	return range((k/3)*3,(k/3+1)*3)

def box(grid,i,j):
	"""
	return a list of elements for box of cell i,j
	"""
	return [grid[k][l] for k in box_range(i) for l in box_range(j)]

def box_index(grid,k):
	"""
	return a list of elements for box at index k
	"""
	return [grid[i][j] for i in box_range(k/3*3) for j in box_range(k%3*3)]

ROW = 0
COL = 1
BOX = 2

def coordinates(type,x,y):
	"""
	return the i,j coordinates of the y-th element at index x
	"""
	if type is ROW: return x,y
	if type is COL: return y,x
	if type is BOX: return (x/3*3+y/3),(x%3*3+y%3)

def elements(grid,type,x):
	"""
	return a list of elements of desired type (row,col,box) at index x
	"""
	if type is ROW: return row(grid,x)
	if type is COL: return col(grid,x)
	if type is BOX: return box_index(grid,x)

def candidates_for(grid,i,j):
	"""
	return the basic candidates for the cell [i,j]
	"""
	if grid[i][j]: return [grid[i][j]]
	return [v for v in range(1,10) if v not in row(grid,i) and v not in col(grid,j) and v not in box(grid,i,j)]

def basic_candidates(grid):
	cdts = [[candidates_for(grid,i,j) for j in range(9)] for i in range(9)]
	return cdts

def filter_candidates(grid,cdts):
	new_grid = [[cdts[i][j][0] if len(cdts[i][j]) is 1 else 0 for j in range(9)] for i in range(9)]
	new_cdts = [[[v for v in range(1,10) if v in cdts[i][j] and v in candidates_for(new_grid,i,j)] for j in range(9)] for i in range(9)]
	return new_grid, new_cdts, (new_grid != grid or new_cdts != cdts)

def pyramid_generator(how_many, start, end):
	for v1 in range(start + how_many - 1,end):
		if(1 is how_many):
			yield v1
		else: 
			for v2 in range(start + how_many - 2,v1):
				if(2 is how_many):
					yield v1,v2
				else: 
					for v3 in range(start + how_many - 3,v2):
						if(3 is how_many):
							yield v1,v2,v3
						else: 
							for v4 in range(start + how_many - 4,v3):
								if(4 is how_many):
									yield v1,v2,v3,v4
								else: 
									for v5 in range(start + how_many - 5,v4):
										if(5 is how_many):
											yield v1,v2,v3,v4,v5
										else:
											for v6 in range(start + how_many - 6,v5):	
												if(6 is how_many):
													yield v1,v2,v3,v4,v5,v6

def values(how_many):
	return pyramid_generator(how_many,1,10)

def cells(how_many):
	return pyramid_generator(how_many,0,9)

def remove_from(cdts,type,x,vals,except_in):
	was_modified = False
	candidates = elements(cdts,type,x)
	for y in range(9):
		if y not in except_in and any(v in candidates[y] for v in vals):
			i,j = coordinates(type,x,y)
			cdts[i][j] = [v for v in candidates[y] if v not in vals]
			was_modified = True
	return cdts,was_modified

def filter_pairs_triplets_quadruplets(grid,cdts):
	was_modified = False
	was_modified_now = False
	for count in range(2,9):
		if(was_modified): break
		for vals in values(count):
			for type in range(3):
				for x in range(9):
					candidates = elements(cdts,type,x)
					for ys in cells(count):
						if all(len(candidates[y]) > 1 and len(candidates[y]) <= count and all(v in vals for v in candidates[y]) for y in ys):
							cdts,was_modified_now = remove_from(cdts,type,x,vals,ys) 
							was_modified = was_modified_now or was_modified
	return cdts,was_modified

def is_solved(grid):
	return not any(grid[i][j] is 0 for i in range(9) for j in range(9))

def solve(grid):
	was_modified = True
	cdts = basic_candidates(grid)
	while was_modified:
		grid,cdts,was_modified = filter_candidates(grid,cdts)
		if(not was_modified):
			cdts,was_modified = filter_pairs_triplets_quadruplets(grid,cdts) 
	if(not is_solved(grid)):
		print_candidates(cdts)
	return grid


test_grid = read_from_file("sample.csv")

print_grid(test_grid)

print_grid(solve(test_grid))
