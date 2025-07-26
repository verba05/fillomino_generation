import gc
from queue import Queue
import random
import numpy as np

from numpy.f2py.auxfuncs import throw_error
from pysat.solvers import Minisat22
import time

from cnf_generator import CNFGenerator
from views.winned_game_view import WinnedGameView


class GameBoardController:

    def __init__(self, view, i, j, k):
        self.view = view
        self.solution = None
        self.solver = None
        self.i, self.j, self.k = i, j, k
        self.cnf_generator = CNFGenerator()
        self.current_chosen_number = 0
        self.decoded_solution = None
        self.beginning_time = None


    def solve_cnf(self):

        time_begin = time.time()
        self.solver = self.cnf_generator.generate_cnf(self.i, self.j, self.k)

        number_of_cells = self.i * self.j
        number_of_rand_cells = 0
        if number_of_cells == 50:
            number_of_rand_cells = 5
        elif number_of_cells == 64:
            number_of_rand_cells = 7
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
                    if (x, y) in randomised_cells:
                        continue
                    k = np.random.randint(4, self.k + 1)
                    random_values.append(x * self.j * self.k + y * self.k + k)
                    randomised_cells.append((x, y))
                    break
            self.solver.solve(assumptions=random_values)
            if self.solver.get_model() is not None:
                break
                time_end = time.time()

        self.solution = self.solver.get_model()

    def decode(self, input):
        if isinstance(input, list):
            board = []

            for element in input:
                k = element % self.k
                if k == 0:
                    k = self.k
                tmp = element - k
                j = (tmp / self.k) % self.j
                tmp = tmp - (j * self.k)
                i = tmp / (self.j * self.k)
                board.append((i, j, k))


            return board
        elif isinstance(input, int):
            k = input % self.k
            if k == 0:
                k = self.k
            tmp = input - k
            j = (tmp // self.k) % self.j
            tmp = tmp - (j * self.k)
            i = tmp // (self.j * self.k)
            return (i, j, k)
        else:
            raise ValueError("Illegal input")


    def generate_board(self):
        self.solve_cnf()

        def isTrue(value):
            return value > 0

        original_solution = list(filter(isTrue, self.solution[:self.i * self.j * self.k]))

        self.decoded_solution = self.decode(original_solution)
        board = [[k, False] for x, y, k in self.decoded_solution]
        queue = Queue()
        polyominos = []
        polyominos_counter = 0
        cell_to_polyomino = {}
        for i in range(self.i):
            for j in range(self.j):
                if board[i * self.j + j][1] == False:
                    queue.put((i, j))
                    cell_to_polyomino[(i, j)] = polyominos_counter
                    polyominos.append([(i, j)])
                    board[i * self.j + j][1] = True
                    while not queue.empty():

                        x, y = queue.get()
                        cell_to_polyomino[(x, y)] = polyominos_counter
                        current_cell_index = x * self.j + y
                        if x > 0 and board[current_cell_index][0] == board[(x - 1) * self.j + y][0] and \
                                board[(x - 1) * self.j + y][1] == False:
                            polyominos[polyominos_counter].append((x - 1, y))
                            board[(x - 1) * self.j + y][1] = True
                            queue.put((x - 1, y))

                        if x < self.i - 1 and board[current_cell_index][0] == board[(x + 1) * self.j + y][0] and \
                                board[(x + 1) * self.j + y][1] == False:
                            polyominos[polyominos_counter].append((x + 1, y))
                            board[(x + 1) * self.j + y][1] = True
                            queue.put((x + 1, y))

                        if y > 0 and board[current_cell_index][0] == board[x * self.j + y - 1][0] and \
                                board[x * self.j + y - 1][1] == False:
                            polyominos[polyominos_counter].append((x, y - 1))
                            board[x * self.j + y - 1][1] = True
                            queue.put((x, y - 1))

                        if y < self.j - 1 and board[current_cell_index][0] == board[x * self.j + y + 1][0] and \
                                board[x * self.j + y + 1][1] == False:
                            polyominos[polyominos_counter].append((x, y + 1))
                            board[x * self.j + y + 1][1] = True
                            queue.put((x, y + 1))

                    polyominos_counter += 1

        time0 = time.time()
        while True:
            isBoardFoundable = True
            cells_on_board = []
            polyominos_cells_counters = list(0 for _ in range(len(polyominos)))
            for i in range(len(polyominos)):
                elements_to_print = None
                number = len(polyominos[i])
                if len(polyominos[i]) == 1:
                    elements_to_print = polyominos[i]
                    polyominos_cells_counters[i] = 1
                elif len(polyominos[i]) == 2 or len(polyominos[i]) == 3:
                    elements_to_print = random.sample(polyominos[i], 1)
                    polyominos_cells_counters[i] = 1
                elif len(polyominos[i]) == 4 or len(polyominos[i]) == 5 or len(polyominos[i]) == 6:
                    choice = random.choice([1, 2])
                    elements_to_print = random.sample(polyominos[i], choice)
                    polyominos_cells_counters[i] = choice
                else:
                    choice = random.choice([3, 4])
                    elements_to_print = random.sample(polyominos[i], choice)
                    polyominos_cells_counters[i] = choice

                cells_on_board.extend([(x, y, number) for x, y in elements_to_print])

            assumptions_array = [x * self.j * self.k + y * self.k + k for x, y, k in cells_on_board]
            self.solver.add_clause([-var for var in self.solution[:self.i * self.j * self.k]])
            while True:
                self.solver.solve(assumptions=assumptions_array)
                solution = self.solver.get_model()

                if solution is None:
                    break
                else:
                    current_solution = list(filter(isTrue, solution[:self.i * self.j * self.k]))
                    different_cells = list(set(original_solution) - set(current_solution))
                    while different_cells:
                        random_cell = random.choice(different_cells)
                        decoded_cell = self.decode(random_cell)
                        if decoded_cell[2] == 2:
                            different_cells.remove(random_cell)
                            continue
                        polyomino_index = cell_to_polyomino[(decoded_cell[0], decoded_cell[1])]

                        visible_cells_count = polyominos_cells_counters[polyomino_index]
                        x, y, number = decoded_cell
                        if visible_cells_count == number - 1:
                            different_cells.remove(random_cell)
                        else:
                            cells_on_board.append(decoded_cell)
                            polyominos_cells_counters[polyomino_index] += 1
                            assumptions_array.append(random_cell)
                            break
                        if different_cells == []:
                            isBoardFoundable = False
                            break

                if not isBoardFoundable:
                    break

            if isBoardFoundable:
                break


        for x, y, number in cells_on_board:
            self.view.cells[x * self.j + y].setText(str(number))
            self.view.cells[x * self.j + y].isLocked = True
            font = self.view.cells[x * self.j + y].font()
            font.setUnderline(True)
            self.view.cells[x * self.j + y].setFont(font)
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
            old_view = self.view
            self.view = WinnedGameView(time.time() - self.beginning_time)
            self.view.setFixedSize(old_view.size())
            self.view.move(old_view.pos())
            self.view.show()
            old_view.setParent(None)
            old_view.deleteLater()
            old_view.close()
            del old_view
            gc.collect()

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
