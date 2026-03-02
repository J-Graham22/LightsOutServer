from fastapi import FastAPI

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


#helper methods
#get max value
def check_solution(matrix1, matrix2) -> bool:
    pass
