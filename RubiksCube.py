#ChatGPT was used to solve this problem
import random
import copy

# rubiks_cube.py
# A flexible Rubik's Cube data structure and operations for NxN cubes,
# plus text-based display of cube state.

# Create a solved cube
def create_solved_cube(n):
    """
    Generate a solved Rubik's Cube of size n.
    Returns a dict mapping each face ('U','D','F','B','L','R') to an n×n grid of color chars.
    Face-to-color mapping:
      U='W' (white), D='Y' (yellow), F='G' (green), B='B' (blue), L='O' (orange), R='R' (red)
    """
    colors = {'U': 'W', 'D': 'Y', 'F': 'G', 'B': 'B', 'L': 'O', 'R': 'R'}
    cube = {face: [[color]*n for _ in range(n)] for face, color in colors.items()}
    return cube

# Rotate a single face (2D list) 90°
def rotate_face(face, cw=True):
    if cw:
        return [list(row)[::-1] for row in zip(*face)]
    else:
        return [list(row) for row in zip(*face[::-1])]

# Helpers to extract and apply strips (rows/cols)
def get_strip(cube, face, kind, idx):
    return cube[face][idx][:] if kind == 'row' else [cube[face][r][idx] for r in range(len(cube[face]))]

def set_strip(cube, face, kind, idx, strip):
    if kind == 'row':
        cube[face][idx] = strip[:]
    else:
        for r, v in enumerate(strip): cube[face][r][idx] = v

# Map neighbors for layer rotation
neighbor_map = {
    'F': [('U','row',lambda n,l: n-1-l,False),('R','col',lambda n,l: l,False),
          ('D','row',lambda n,l: l,True),('L','col',lambda n,l: n-1-l,True)],
    'B': [('U','row',lambda n,l: l,True),('L','col',lambda n,l: l,False),
          ('D','row',lambda n,l: n-1-l,False),('R','col',lambda n,l: n-1-l,True)],
    'U': [('F','row',lambda n,l: l,False),('R','row',lambda n,l: l,False),
          ('B','row',lambda n,l: l,False),('L','row',lambda n,l: l,False)],
    'D': [('F','row',lambda n,l: n-1-l,False),('L','row',lambda n,l: n-1-l,False),
          ('B','row',lambda n,l: n-1-l,False),('R','row',lambda n,l: n-1-l,False)],
    'L': [('U','col',lambda n,l: l,False),('F','col',lambda n,l: l,False),
          ('D','col',lambda n,l: l,False),('B','col',lambda n,l: n-1-l,True)],
    'R': [('U','col',lambda n,l: n-1-l,False),('B','col',lambda n,l: l,False),
          ('D','col',lambda n,l: n-1-l,False),('F','col',lambda n,l: n-1-l,True)],
}

# Rotate one layer on a face
# face in 'U','D','F','B','L','R', layer 0..n-1, direction 'CW' or 'CCW'
def rotate_layer(cube, face, layer, direction='CW'):
    n = len(cube['U'])
    for _ in range(1 if direction=='CW' else 3):
        old = []
        for f2,kind,idxf,rev in neighbor_map[face]:
            idx = idxf(n, layer)
            s = get_strip(cube, f2, kind, idx)
            old.append(s[::-1] if rev else s)
        for i,(f2,kind,idxf,rev) in enumerate(neighbor_map[face]):
            idx = idxf(n, layer)
            s = old[(i-1)%4]
            set_strip(cube, f2, kind, idx, s[::-1] if rev else s)
        if layer==0: cube[face] = rotate_face(cube[face],True)
        elif layer==n-1: cube[face] = rotate_face(cube[face],False)

# Display cube in net layout
def display_cube(cube):
    n=len(cube['U'])
    print("    U")
    for r in cube['U']: print("      "+" ".join(r))
    print("L   F   R   B")
    for i in range(n):
        print(" ".join(cube['L'][i])+"   "+" ".join(cube['F'][i])+"   "+
              " ".join(cube['R'][i])+"   "+" ".join(cube['B'][i]))
    print("    D")
    for r in cube['D']: print("      "+" ".join(r))

# Scramble function
def shuffler(cube, moves=20):
    faces=list(neighbor_map)
    n=len(cube['U'])
    for _ in range(moves): rotate_layer(cube, random.choice(faces), random.randrange(n), random.choice(['CW','CCW']))

# Example usage: show original vs scrambled for either a solved or user-defined cube
if __name__=='__main__':
    # Option A: start with a solved cube
    # original = create_solved_cube(3)

    # Option B: define your own cube state manually:
    original = {
    'U': [
            ['W','W','W'], 
            ['W','G','W'], 
            ['R','W','W']
            ],
    'D': [
            ['Y','Y','Y'], 
            ['Y','B','Y'], 
            ['Y','Y','Y']
            ],
    'F': [
            ['G','G','G'], 
            ['G','G','G'], 
            ['G','G','G']
            ],
    'B': [
            ['B','B','B'], 
            ['B','B','B'], 
            ['B','B','B']
            ],
    'L': [
            ['O','O','O'], 
            ['O','O','O'], 
            ['O','O','O']
            ],
    'R': [
            ['R','R','R'], 
            ['R','R','R'], 
            ['R','R','R']
            ],
}

    # Display the original (unscrambled) cube
    print("Original cube:")
    display_cube(original)

    # Make a copy and scramble it
    scrambled = copy.deepcopy(original)
    shuffler(scrambled, moves=12)

    # Display the scrambled cube
    print("\nScrambled cube:")
    display_cube(scrambled)

    # Display the solved cube
    print("\nSolved cube:")
    original = create_solved_cube(3)
    display_cube(original)
    