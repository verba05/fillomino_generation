import numpy as np

from pysat.solvers import Minisat22
import time

from cnf_generator import CNFGenerator


class GameBoardController:

    def __init__(self, view, i, j):
        self.view = view
        self.solution = None

        self.i, self.j = i, j
        self.cnf_generator = CNFGenerator()


    def solve_cnf_from_file(self):
        time_start = time.time()
        solver = self.cnf_generator.generate_cnf(self.i, self.j)
        time_end = time.time()
        print("time to create solver: ", time_end - time_start)

        time_start = time.time()
        while True:
            random_values = []
            for i in range(6):
                x = np.random.randint(0,self.i)
                y = np.random.randint(0,self.j)
                k = np.random.randint(1,10)
                random_values.append(x * self.j * 9 + y * 9 + k)

            solver.solve(assumptions=random_values)
            if solver.get_model() is not None:
                break


        time_end = time.time()
        print("time to generate solution", time_end - time_start)
        self.solution = solver.get_model()

    def generate_board(self):

        self.solve_cnf_from_file()

        def isTrue(value):
            return value > 0


        solution_filtered = filter(isTrue, self.solution[:self.i * self.j * 9])

        for value in solution_filtered:
            i = value // self.j * 9
            j = (value - (i * self.j * 9)) // 9
            k = (value - (i * self.j * 9) - (j * 9))
            if k == 0:
                k = 9
                if j == 0:
                    j = self.j - 1
                    if i == 0:
                        i = self.i - 1
                    else:
                        i = i - 1
                else:
                    j = j - 1
            self.view.cells[i * self.j + j].setText(str(k))

