from fastapi import FastAPI
import math
import numpy as np
import sympy as sp
import logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Color Puzzle API")

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
    logging.info(f"Solving puzzle for puzzle input {puzzle_input}")

    puzzle_input_matrix = convert_string_representation_to_matrix(puzzle_input)
    if puzzle_input_matrix is None:
        return "" #todo: change this to something proper
    logging.info(f"Converted puzzle input to matrix")

    desired_output_matrix = create_desired_output_matrix(len(puzzle_input))

    transformation_matrix = create_transformation_matrix(len(puzzle_input_matrix))
    if transformation_matrix is None:
        return "" #todo: change this to something proper
    logging.info(f"Created transformation matrix of dimensions {len(puzzle_input)}x{len(puzzle_input)}")

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
        logger.info(f"Input does not represent a square matrix. Length provided: {len(string_representation)}")
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

    side_length = math.sqrt(size)
    if not side_length.is_integer():
        logger.info(f"Size is not representative of a square matrix. Size provided: {size}")
        return None 

    for i in range(size):
        # a light will toggle itself and its neightbors
        matrix[i, i] = int(1)
        # an up or down neighbor might be out of bounds
        up_i = int(i - side_length)
        if up_i >= 0:
            matrix[i, up_i] = int(1)
            # matrix[up_i, i] = int(1)
        down_i = int(i + side_length)
        if down_i < size:
            matrix[i, down_i] = int(1)
        # a left or right neighbor might not actually be a neighbor
        left_i = int(i - 1)
        if i % side_length != 0 and left_i >= 0:
            matrix[i, left_i] = int(1)
        right_i = int(i + 1)
        if i % side_length != side_length - 1 and right_i < size:
            matrix[i, right_i] = int(1)
    return matrix