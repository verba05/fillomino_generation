import ast

from pysat.solvers import Minisat22

class CNFGenerator:

    def normalize_polyomino(self, polyomino):
        min_x = min(cell[0] for cell in polyomino)
        min_y = min(cell[1] for cell in polyomino)
        return tuple(sorted([(cell[0] - min_x, cell[1] - min_y) for cell in polyomino]))

    def generate_polyominoes(self, n):
        polyominoes = set()
        def generate_next_cell(polyomino, n, k):
            if k == n:
                polyomino = self.normalize_polyomino(polyomino)
                polyominoes.add(polyomino)

            else:
                neighbours = [(-1, 0),(1, 0),(0, -1), (0, 1)]
                for cell in polyomino:
                    for dx, dy in neighbours:
                        x = cell[0] + dx
                        y = cell[1] + dy
                        if (x, y) not in polyomino:
                            generate_next_cell(polyomino + [(x, y)], n, k + 1)

        generate_next_cell([(0,0)],n,1)
        return polyominoes

    def can_shape_be_placed(self, shape, center_i, center_j, max_i, max_j):
        for (i, j) in shape:
            new_i = center_i + i
            new_j = center_j + j
            if not (0 <= new_i and 0 <= new_j and new_j < max_j and new_i < max_i):
                return False
        return True

    def generate_cnf(self, max_i, max_j, max_k):
        solver = Minisat22()
        for i in range(max_i):
            for j in range(max_j):
                clause = []
                for k in range(1, max_k+1):
                    clause.append(i * max_j * max_k + j * max_k + k)
                solver.add_clause(clause)
                for k in range(1, max_k+1):
                    for l in range(k+1, max_k+1):
                        solver.add_clause([-(i * max_j * max_k + j * max_k + k), -(i * max_j * max_k + j * max_k + l)])
                clause.clear()

        for i in range(max_i):
            for j in range(max_j):
                if i > 0:
                    solver.add_clause([-(i * max_j * max_k + j * max_k + 1), -((i - 1) * max_j * max_k + j * max_k + 1)])
                if i < max_i-1:
                    solver.add_clause([-(i * max_j * max_k + j * max_k + 1),  -((i + 1) * max_j * max_k + j * max_k + 1)])
                if j > 0:
                    solver.add_clause([-(i * max_j * max_k + j * max_k + 1), -(i * max_j * max_k + (j - 1) * max_k + 1)])
                if j < max_j-1:
                    solver.add_clause([-(i * max_j * max_k + j * max_k + 1), -(i * max_j * max_k + (j + 1) * max_k + 1)])


        support_variable = max_i * max_j * max_k + 1
        for k in range(2, 6):
            shapes = self.generate_polyominoes(k)
            cell_in_groups = {}
            for i in range(max_i):
                for j in range(max_j):
                    for shape in shapes:
                        if self.can_shape_be_placed(shape, i, j, max_i, max_j):
                            coordinates_of_shape = [(x + i, y + j) for x, y in shape]
                            for x, y in coordinates_of_shape:
                                solver.add_clause([-(support_variable), (x * max_j * max_k + y * max_k + k)])

                                if (x, y) not in cell_in_groups:
                                    cell_in_groups[(x, y)] = []

                                cell_in_groups[(x, y)].append(support_variable)

                                neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                                for dx, dy in neighbors:
                                    if 0 <= dx < max_i and 0 <= dy < max_j and (dx, dy) not in coordinates_of_shape:
                                        solver.add_clause([-(support_variable), -(dx * max_j * max_k + dy * max_k + k)])

                            support_variable += 1

            for (i, j), groups in cell_in_groups.items():
                clause = []
                clause.append(-(i * max_j * max_k + j * max_k + k))
                for group in groups:
                    clause.append(group)
                solver.add_clause(clause)
                clause.clear()

        polyominos_file = open("polyominos.txt", "r")
        for k in range(6, max_k + 1):
            number_of_polyominoes = int(polyominos_file.readline())
            shapes = []
            for i in range(number_of_polyominoes):
                shapes.append(ast.literal_eval(polyominos_file.readline()))
            cell_in_groups = {}

            for i in range(max_i):
                for j in range(max_j):
                    for shape in shapes:
                        if self.can_shape_be_placed(shape, i, j, max_i, max_j):
                            for coordinates in shape:
                                solver.add_clause([-support_variable,
                                                   ((i + coordinates[0]) * max_j * max_k + (j + coordinates[1]) * max_k + k)])

                            coordinates_of_shape = [(x + i, y + j) for x, y in shape]

                            for x, y in coordinates_of_shape:

                                if (x, y) not in cell_in_groups:
                                    cell_in_groups[(x, y)] = []

                                cell_in_groups[(x, y)].append(support_variable)

                                neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                                for nx, ny in neighbors:
                                    if 0 <= nx < max_i and 0 <= ny < max_j and (nx, ny) not in coordinates_of_shape:
                                        solver.add_clause([-support_variable, -(nx * max_j * max_k + ny * max_k + k)])

                            support_variable += 1

            for (i, j), groups in cell_in_groups.items():
                clause = []
                clause.append(-(i * max_j * max_k + j * max_k + k))
                for group in groups:
                    clause.append(group)
                solver.add_clause(clause)
                clause.clear()
        polyominos_file.close()

        return solver

