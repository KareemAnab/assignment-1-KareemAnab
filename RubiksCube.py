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
    Returns a dictionary mapping each face ('U','D','F','B','L','R') to an n x n grid
    filled with a single color character.
    """
    # Standard color scheme: U=White, D=Yellow, F=Green, B=Blue, L=Orange, R=Red
    colors = {'U': 'W', 'D': 'Y', 'F': 'G', 'B': 'B', 'L': 'O', 'R': 'R'}
    cube = {}
    for face, color in colors.items():
        cube[face] = [[color for _ in range(n)] for _ in range(n)]
    return cube

# Utility to rotate a single face (2D list) 90°
def rotate_face(face, cw=True):
    """
    Rotate a square 2D list (face) 90° clockwise or counter-clockwise.
    Uses Pythonic transpose + reverse.
    """
    if cw:
        return [list(row)[::-1] for row in zip(*face)]
    else:
        return [list(row) for row in zip(*face[::-1])]

# Helpers to get/set strips (rows or columns) on a face
def get_strip(cube, face, kind, idx):
    if kind == 'row':
        return cube[face][idx].copy()
    else:
        return [cube[face][r][idx] for r in range(len(cube[face]))]

def set_strip(cube, face, kind, idx, strip):
    if kind == 'row':
        cube[face][idx] = strip.copy()
    else:
        for r, val in enumerate(strip):
            cube[face][r][idx] = val

# Adjacency map for each face: defines which strips move during a rotation.
neighbor_map = {
    'F': [
        ('U', 'row', lambda n, l: n-1-l, False),
        ('R', 'col', lambda n, l: l, False),
        ('D', 'row', lambda n, l: l, True),
        ('L', 'col', lambda n, l: n-1-l, True),
    ],
    'B': [
        ('U', 'row', lambda n, l: l, True),
        ('L', 'col', lambda n, l: l, False),
        ('D', 'row', lambda n, l: n-1-l, False),
        ('R', 'col', lambda n, l: n-1-l, True),
    ],
    'U': [
        ('F', 'row', lambda n, l: l, False),
        ('R', 'row', lambda n, l: l, False),
        ('B', 'row', lambda n, l: l, False),
        ('L', 'row', lambda n, l: l, False),
    ],
    'D': [
        ('F', 'row', lambda n, l: n-1-l, False),
        ('L', 'row', lambda n, l: n-1-l, False),
        ('B', 'row', lambda n, l: n-1-l, False),
        ('R', 'row', lambda n, l: n-1-l, False),
    ],
    'L': [
        ('U', 'col', lambda n, l: l, False),
        ('F', 'col', lambda n, l: l, False),
        ('D', 'col', lambda n, l: l, False),
        ('B', 'col', lambda n, l: n-1-l, True),
    ],
    'R': [
        ('U', 'col', lambda n, l: n-1-l, False),
        ('B', 'col', lambda n, l: l, False),
        ('D', 'col', lambda n, l: n-1-l, False),
        ('F', 'col', lambda n, l: n-1-l, True),
    ],
}

# Core utility: perform a layer rotation
def rotate_layer(cube, face, layer, direction='CW'):
    n = len(cube['U'])
    times = 1 if direction == 'CW' else 3
    for _ in range(times):
        neigh = neighbor_map[face]
        old = []
        for (f2, kind, idx_func, rev) in neigh:
            idx = idx_func(n, layer)
            strip = get_strip(cube, f2, kind, idx)
            old.append(strip[::-1] if rev else strip)
        for i, (f2, kind, idx_func, rev) in enumerate(neigh):
            idx = idx_func(n, layer)
            src = old[(i - 1) % 4]
            set_strip(cube, f2, kind, idx, src[::-1] if rev else src)
        if layer == 0:
            cube[face] = rotate_face(cube[face], cw=True)
        elif layer == n - 1:
            cube[face] = rotate_face(cube[face], cw=False)

# Print the cube state in a simple net layout
def display_cube(cube):
    """
    Print the cube faces in a cross (net) layout:
           U
      L    F    R    B
           D
    """
    n = len(cube['U'])
    print("    U")
    for row in cube['U']:
        print("      " + " ".join(row))

    print("L   F   R   B")
    for i in range(n):
        print(
            " ".join(cube['L'][i]) + "   " +
            " ".join(cube['F'][i]) + "   " +
            " ".join(cube['R'][i]) + "   " +
            " ".join(cube['B'][i])
        )

    print("    D")
    for row in cube['D']:
        print("      " + " ".join(row))

# Bonus: scrambler function
def shuffler(cube, moves=20):
    faces = list(neighbor_map.keys())
    n = len(cube['U'])
    for _ in range(moves):
        f = random.choice(faces)
        l = random.randint(0, n - 1)
        d = random.choice(['CW', 'CCW'])
        rotate_layer(cube, f, l, d)

# Example usage
if __name__ == '__main__':
    # Create a solved cube and a scrambled copy
    solved_cube = create_solved_cube(3)
    scrambled_cube = copy.deepcopy(solved_cube)

    # Scramble one copy
    shuffler(scrambled_cube, moves=10)

    # Display unsolved (scrambled) first
    print("Unsolved (scrambled) cube:")
    display_cube(scrambled_cube)

    # Then display the original solved cube
    print("\nSolved cube:")
    display_cube(solved_cube)