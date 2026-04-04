from fastapi import FastAPI
import math
import numpy as np
import sympy as sp

app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}

#endpoints

# - generate solvable puzzle
# - solve matrix via matrix multiplication
# - solve matrix via brute force
@app.get("/solution/brute_force/{puzzle_input}")
def brute_force(puzzle_input: str):
    puzzle_input_matrix = convert_string_representation_to_matrix(puzzle_input)

    max_solution_val = 2 ** len(puzzle_input)

    for i in range(0, max_solution_val + 1):
        binary_representation = bin(i)[2:]

        guess_matrix = convert_string_representation_to_matrix(binary_representation)

        if check_solution(puzzle_input_matrix, guess_matrix):
            return binary_representation
    
    return ''


@app.get("/solution/matrix_multiplication/{puzzle_input}")
def matrix_multiplication_solution(puzzle_input: str):
    # x: solution matrix
    # p: puzzle input matrix
    # b: desired output matrix
    # A: transformation matrix

    # b = A * x + p
    # x = (b - p) * A^-1
    puzzle_input_matrix = convert_string_representation_to_matrix(puzzle_input)
    print('puzzle input matrix:')
    print(puzzle_input_matrix)
    desired_output_matrix = create_desired_output_matrix(len(puzzle_input))
    print('desired output matrix:')
    print(desired_output_matrix)
    transformation_matrix = create_transformation_matrix(len(puzzle_input_matrix))
    print('transformation matrix:')
    print(transformation_matrix)
    inverse_transformation_matrix = np.array(sp.Matrix(transformation_matrix).inv_mod(2)).astype(int)
    print('inverse transformation matrix:')
    print(inverse_transformation_matrix)

    x = (desired_output_matrix - puzzle_input_matrix) * inverse_transformation_matrix
    print(x)

    return x.tolist()

#helper methods
#get max value
def check_solution(matrix1, matrix2) -> bool:
    pass

def convert_string_representation_to_matrix(string_representation: str) -> np.array:
    n = math.sqrt(len(string_representation))
    if not n.is_integer():
        #todo: replace with proper logging
        print("Input does not represent a square matrix")
        return None

    n = int(n)
    matrix = []
    for i in string_representation:
        matrix.append(int(i))
    return np.array(matrix)

def create_desired_output_matrix(size: int) -> np.array:
    matrix = []
    for i in range(size):
        matrix.append(1)
    return np.array(matrix)

def create_transformation_matrix(size: int) -> np.array:
    matrix = np.zeros((size, size))

    for i in range(size):
        # a light will toggle itself and its neightbors
        matrix[i, i] = 1
        # an up or down neighbor might be out of bounds
        up_i = i - size
        if up_i >= 0:
            pass
            # matrix[i, up_i] = 1
            matrix[up_i, i] = 1
        down_i = i + size
        if down_i < size:
            pass
            # matrix[i, down_i] = 1
            matrix[down_i, i] = 1
        # a left or right neighbor might not actually be a neighbor
        left_i = i - 1
        if i % size != 0:
            pass
            matrix[left_i, i] = 1
        right_i = i + 1
        if i % size != size - 1:
            pass
            matrix[right_i, i] = 1
    return matrix