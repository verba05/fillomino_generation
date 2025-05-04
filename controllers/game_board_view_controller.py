from queue import Queue
import random
import numpy as np

import copy

from numpy.f2py.auxfuncs import throw_error
from pysat.solvers import Minisat22
import time

from cnf_generator import CNFGenerator
from views.winned_game_view import WinnedGameView


class GameBoardController:

    def __init__(self, view, i, j):
        self.view = view
        self.solution = None
        self.solver = None
        self.i, self.j = i, j
        self.cnf_generator = CNFGenerator()
        self.current_chosen_number = 0
        self.decoded_solution = None
        self.beginning_time = None


    def solve_cnf(self):
        time_start = time.time()
        self.solver = self.cnf_generator.generate_cnf(self.i, self.j)
        time_end = time.time()
        print("time to create solver: ", time_end - time_start)

        time_start = time.time()
        number_of_cells = self.i * self.j
        number_of_rand_cells = 0
        if number_of_cells == 50:
            number_of_rand_cells = 5
        elif number_of_cells == 64:
            number_of_rand_cells = 6
        elif number_of_cells == 100:
            number_of_rand_cells = 8
        else:
            number_of_rand_cells = 10

        while True:
            random_values = []
            randomised_cells = []
            for i in range(number_of_rand_cells):
                while True:
                    x = np.random.randint(0, self.i)
                    y = np.random.randint(0, self.j)
                    if x * y in randomised_cells:
                        continue
                    k = np.random.randint(4, 10)
                    random_values.append(x * self.j * 9 + y * 9 + k)
                    randomised_cells.append(x * y)
                    break

            self.solver.solve(assumptions=random_values)
            if self.solver.get_model() is not None:
                break
        time_end = time.time()
        print("time to generate solution", time_end - time_start)

        self.solution = self.solver.get_model()

    def decode(self, input):
        if isinstance(input, list):
            board = []

            for element in input:
                k = element % 9
                if k == 0:
                    k = 9
                tmp = element - k
                j = (tmp // 9) % self.j
                tmp = tmp - (j * 9)
                i = tmp // (self.j * 9)
                board.append((i, j, k))

            print("board", board)

            return board
        elif isinstance(input, int):
            k = input % 9
            if k == 0:
                k = 9
            tmp = input - k
            j = (tmp // 9) % self.j
            tmp = tmp - (j * 9)
            i = tmp // (self.j * 9)
            return (i, j, k)
        else:
            raise ValueError("Illegal input")


    def generate_board(self):

        self.solve_cnf()

        def isTrue(value):
            return value > 0

        original_solution = list(filter(isTrue, self.solution[:self.i * self.j * 9]))

        self.decoded_solution = self.decode(original_solution)
        board = [[k, False, False] for x, y, k in self.decoded_solution]
        queue = Queue()
        polyominos = []
        polyominos_counter = 0

        for i in range(self.i):
            for j in range(self.j):
                if board[i * self.j + j][1] == False:
                    queue.put((i, j))
                    polyominos.append([(i, j)])
                    board[i * self.j + j][1] = True
                    while not queue.empty():

                        x, y = queue.get()
                        current_cell_index = x * self.j + y
                        if x > 0 and board[current_cell_index][0] == board[(x - 1) * self.j + y][0] and board[(x - 1) * self.j + y][1] == False:

                            polyominos[polyominos_counter].append((x - 1, y))
                            board[(x - 1) * self.j + y][1] = True
                            queue.put((x - 1, y))

                        if x < self.i - 1 and board[current_cell_index][0] == board[(x + 1) * self.j + y][0] and board[(x + 1) * self.j + y][1] == False:
                            polyominos[polyominos_counter].append((x + 1, y))
                            board[(x + 1) * self.j + y][1] = True
                            queue.put((x + 1, y))

                        if y > 0 and board[current_cell_index][0] == board[x * self.j + y - 1][0] and board[x * self.j + y - 1][1] == False:
                            polyominos[polyominos_counter].append((x, y - 1))
                            board[x * self.j + y - 1][1] = True
                            queue.put((x, y - 1))

                        if y < self.j - 1 and board[current_cell_index][0] == board[x * self.j + y + 1][0] and board[x * self.j + y + 1][1] == False:
                            polyominos[polyominos_counter].append((x, y + 1))
                            board[x * self.j + y + 1][1] = True
                            queue.put((x, y + 1))


                    polyominos_counter += 1

                else:
                    continue


        for i in range(self.i):
            for j in range(self.j):
                print(self.decoded_solution[i * self.j + j][2], end="")
            print()

        cells_on_board = []

        for i in range(len(polyominos)):
            elements_to_print = None
            number = len(polyominos[i])
            if len(polyominos[i]) == 1:
                elements_to_print = polyominos[i]
            elif len(polyominos[i]) == 2 or len(polyominos[i]) == 3:
                elements_to_print = random.sample(polyominos[i], 1)
            elif len(polyominos[i]) == 4 or len(polyominos[i]) == 5 or len(polyominos[i]) == 6:
                elements_to_print = random.sample(polyominos[i], random.choice([1,2]))
            elif len(polyominos[i]) == 7:
                elements_to_print = random.sample(polyominos[i], random.choice([1,2,3]))
            else:
                elements_to_print = random.sample(polyominos[i], random.choice([1,2,3,4]))

            cells_on_board.extend([(x, y, number) for x, y in elements_to_print])



            for x, y in elements_to_print:
                self.view.cells[x * self.j + y].setText(str(number))
                self.view.cells[x * self.j + y].isLocked = True
                font = self.view.cells[x * self.j + y].font()
                font.setUnderline(True)
                self.view.cells[x * self.j + y].setFont(font)
                board[x * self.j + y][2] = True



        assumptions_array = [x * self.j * 9 + y * 9 + k for x, y, k in cells_on_board]
        self.solver.add_clause([-var for var in self.solution[:self.i * self.j * 9]])
        time0 = time.time()
        while True:
            self.solver.solve(assumptions=assumptions_array)
            solution = self.solver.get_model()
            if solution is None:
                print("success")
                break
            else:
                print("failure")
                current_solution = list(filter(isTrue, solution[:self.i * self.j * 9]))
                different_cells = list(set(original_solution) - set(current_solution))
                while different_cells:

                    random_cell = random.choice(different_cells)
                    decoded_cell = self.decode(random_cell)
                    if decoded_cell[2] == 2 or decoded_cell[2] == 3:
                        different_cells.remove(random_cell)
                        continue
                    polyomino_index = None
                    for i in range(len(polyominos)):
                        if decoded_cell[2] == len(polyominos[i]) and (decoded_cell[0], decoded_cell[1]) in polyominos[i]:
                            polyomino_index = i
                            break

                    visible_cells_count = 0
                    for x, y in polyominos[polyomino_index]:
                        if board[x * self.j + y][2]:
                            visible_cells_count += 1

                    x, y, number = decoded_cell

                    if visible_cells_count == number - 1:
                        different_cells.remove(random_cell)
                    else:
                        cells_on_board.append(decoded_cell)
                        board[x * self.j + y][2] = True
                        self.view.cells[x * self.j + y].setText(str(decoded_cell[2]))
                        font = self.view.cells[x * self.j + y].font()
                        font.setUnderline(True)
                        self.view.cells[x * self.j + y].setFont(font)
                        self.view.cells[x * self.j + y].isLocked = True
                        assumptions_array.append(random_cell)
                        break
        print(self.decode(assumptions_array))
        print(len(assumptions_array))
        self.setBoardCellsView()
        self.beginning_time = time.time()

    def numberSelectionChangeHandler(self, number: int):
            self.view.selection_number_buttons[self.current_chosen_number].changeState()
            self.current_chosen_number = number - 2
            self.view.selection_number_buttons[self.current_chosen_number].changeState()

    def boardCellClickedHandler(self, index_cell):
        if not self.view.cells[index_cell].isLocked:
            self.view.cells[index_cell].setText(str(self.current_chosen_number + 2))
            self.setBoardCellsView()

            for i in range (self.i * self.j):
                if self.view.cells[i].text() == "" or self.decoded_solution[i][2] != int(self.view.cells[i].text()):
                    return

            self.view.winned_game_view = WinnedGameView(time.time() - self.beginning_time)
            self.view.winned_game_view.resize(self.view.size())
            self.view.winned_game_view.move(self.view.pos())
            self.view.winned_game_view.show()
            self.view.close()

    def setBoardCellsView(self):
        numberStyleMap = {
            1: "#D3D3D3",
            2: "#FFA07A",
            3: "#90EE90",
            4: "#F08080",
            5: "#F0E68C",
            6: "#DDA0DD",
            7: "#AFEEEE",
            8: "#F4A460",
            9: "#D8BFD8",
            10: "#87CEEB"
        }

        was_visited = [False] * self.i * self.j

        for i in range(len(self.view.cells)):
            if self.view.cells[i].text() == "" or was_visited[i]:
                continue
            queue = Queue()
            polyomino = []
            polyomino.append(i)

            cells_counter = 1
            queue.put((i // self.j, i % self.j))
            was_visited[i] = True
            while not queue.empty():
                x, y = queue.get()

                if x < self.i - 1 and self.view.cells[x * self.j + y].text() == self.view.cells[
                    (x + 1) * self.j + y].text() and not was_visited[(x + 1) * self.j + y]:
                    queue.put((x + 1, y))
                    polyomino.append((x + 1) * self.j + y)
                    was_visited[(x + 1) * self.j + y] = True
                if x > 0 and self.view.cells[x * self.j + y].text() == self.view.cells[
                    (x - 1) * self.j + y].text() and not was_visited[(x - 1) * self.j + y]:
                    queue.put((x - 1, y))
                    polyomino.append((x - 1) * self.j + y)
                    was_visited[(x - 1) * self.j + y] = True
                if y < self.j - 1 and self.view.cells[x * self.j + y].text() == self.view.cells[
                    x * self.j + y + 1].text() and not was_visited[x * self.j + y + 1]:
                    queue.put((x, y + 1))
                    polyomino.append(x * self.j + y + 1)
                    was_visited[x * self.j + y + 1] = True
                if y > 0 and self.j - 1 and self.view.cells[x * self.j + y].text() == self.view.cells[
                    x * self.j + y - 1].text() and not was_visited[x * self.j + y - 1]:
                    queue.put((x, y - 1))
                    polyomino.append(x * self.j + y - 1)
                    was_visited[x * self.j + y - 1] = True

            print(polyomino)

            if len(polyomino) < int(self.view.cells[i].text()):
                for index in polyomino:
                    self.view.cells[index].setStyleSheet(
                        """
                            background-color: grey;  
                            color: white;
                            border: 1px solid black;
                            border-radius: 0px;
                        """
                    )
            elif len(polyomino) > int(self.view.cells[i].text()):
                for index in polyomino:
                    self.view.cells[index].setStyleSheet(
                        """
                            background-color: red;
                            color: white;
                            border: 1px solid black;
                            border-radius: 0px;
                        """
                    )
            elif len(polyomino) == int(self.view.cells[i].text()):
                for index in polyomino:
                    self.view.cells[index].setStyleSheet(
                        f"""
                            background-color: {numberStyleMap[int(self.view.cells[index].text())]};
                            color: black;   
                            border: 1px solid black;
                            border-radius: 0px; 
                        """
                    )

    def clear_errors_button_clicked(self):
        for i in range(self.i * self.j):
            if self.view.cells[i].text() == "" or self.view.cells[i].isLocked:
                continue
            if int(self.view.cells[i].text()) != self.decoded_solution[i][2]:
                self.view.cells[i].setText("")
                self.view.cells[i].setStyleSheet(
                    """
                        background-color: grey;  
                        color: white;
                        border: 1px solid black;
                        border-radius: 0px;
                    """
                )

        self.setBoardCellsView()