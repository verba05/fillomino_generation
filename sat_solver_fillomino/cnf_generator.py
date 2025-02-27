import ast

from pysat.solvers import Minisat22


class CNFGenerator:

    def normalize(self, polyomino):
        min_x = min(square[0] for square in polyomino)
        min_y = min(square[1] for square in polyomino)
        return sorted([(square[0] - min_x, square[1] - min_y) for square in polyomino])

    def generate_polyominoes(self, n):

        def generate(polyomino, remaining):
            if remaining == 0:
                normalized = tuple(self.normalize(polyomino))
                if normalized not in unique_polyominoes:
                    unique_polyominoes.add(normalized)
                    polyominoes.append(polyomino)
                return

            for cell in polyomino:
                for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_cell = (cell[0] + x, cell[1] + y)
                    if new_cell not in polyomino:
                        generate(polyomino + [new_cell], remaining - 1)

        polyominoes = []
        unique_polyominoes = set()
        generate([(0, 0)], n - 1)
        return polyominoes

    def can_shape_be_placed(self, shape, center_i, center_j, max_i, max_j):
        for (i, j) in shape:
            new_i = center_i + i
            new_j = center_j + j
            if not (0 <= new_i and 0 <= new_j and new_j < max_j and new_i < max_i):
                return False
        return True





    def generate_cnf(self, max_i, max_j):
        solver = Minisat22()



        for i in range(max_i):
            for j in range(max_j):
                clause = []
                for k in range(1, 10):
                    clause.append(i * max_j * 9 + j * 9 + k)
                solver.add_clause(clause)
                for k in range(1, 10):
                    for l in range(1, 10):
                        if k != l:
                            solver.add_clause([-(i * max_j * 9 + j * 9 + k), -(i * max_j * 9 + j * 9 + l)])
                clause.clear()


        for i in range(max_i):
            for j in range(max_j):
                if i > 0:
                    solver.add_clause([-(i * max_j * 9 + j * 9 + 1), -((i - 1) * max_j * 9 + j * 9 + 1)])
                if i < max_i-1:
                    solver.add_clause([-(i * max_j * 9 + j * 9 + 1),  -((i + 1) * max_j * 9 + j * 9 + 1)])
                if j > 0:
                    solver.add_clause([-(i * max_j * 9 + j * 9 + 1), -(i * max_j * 9 + (j - 1) * 9 + 1)])
                if j < max_j-1:
                    solver.add_clause([-(i * max_j * 9 + j * 9 + 1), -(i * max_j * 9 + (j + 1) * 9 + 1)])


        for i in range(max_i):
            for j in range(max_j):
                clause = []
                clause.append(-(i * max_j * 9 + j * 9 + 2))
                if i > 0:
                    clause.append((i - 1) * max_j * 9 + j * 9 + 2)
                if i < max_i-1:
                    clause.append((i + 1) * max_j * 9 + j * 9 + 2)
                if j > 0:
                    clause.append(i * max_j * 9 + (j - 1) * 9 + 2)
                if j < max_j-1:
                    clause.append(i * max_j * 9 + (j + 1) * 9 + 2)
                solver.add_clause(clause)
                for m in range(len(clause[1:])):
                    for n in range(m + 1, len(clause[1:])):
                        solver.add_clause([-(clause[n]), -(clause[m])])
                        solver.add_clause([-(clause[m]) , -(clause[n])])
                clause.clear()





        shapes = self.generate_polyominoes(3)
        groups_index_max = max_i * max_j * 9 + max_j * 9 + 9 + 1
        cell_in_groups = {}
        for i in range(max_i):
            for j in range(max_j):
                for shape in shapes:
                    if self.can_shape_be_placed(shape, i, j, max_i, max_j):
                        for coordinates in shape:
                            solver.add_clause([-(groups_index_max), ((i + coordinates[0]) * max_j * 9 + (j + coordinates[1]) * 9 + 3)])

                        coordinates_of_shape = [(x + i, y + j) for x, y in shape]

                        for x, y in coordinates_of_shape:

                            if (x, y) not in cell_in_groups:
                                cell_in_groups[(x, y)] = []

                            cell_in_groups[(x, y)].append(groups_index_max)

                            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                            for dx, dy in neighbors:
                                if 0 <= dx < max_i and 0 <= dy < max_j and (dx, dy) not in coordinates_of_shape:
                                    solver.add_clause([-(groups_index_max) , -(dx * max_j * 9 + dy * 9 + 3)])

                        groups_index_max += 1

        for (i, j), groups in cell_in_groups.items():
            clause = []
            clause.append(-(i * max_j * 9 + j * 9 + 3))
            for group in groups:
                clause.append(group)
            solver.add_clause(clause)
            clause.clear()


        shapes = self.generate_polyominoes(4)
        cell_in_groups = {}

        for i in range(max_i):
            for j in range(max_j):
                for shape in shapes:
                    if self.can_shape_be_placed(shape, i, j, max_i, max_j):
                        for coordinates in shape:
                            solver.add_clause([-groups_index_max, ((i + coordinates[0]) * max_j * 9 + (j + coordinates[1]) * 9 + 4)])


                        coordinates_of_shape = [(x + i, y + j) for x, y in shape]

                        for x, y in coordinates_of_shape:

                            if (x, y) not in cell_in_groups:
                                cell_in_groups[(x, y)] = []

                            cell_in_groups[(x, y)].append(groups_index_max)

                            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                            for dx, dy in neighbors:
                                if 0 <= dx < max_i and 0 <= dy < max_j and (dx, dy) not in coordinates_of_shape:
                                    solver.add_clause([-groups_index_max, -(dx * max_j * 9 + dy * 9 + 4)])

                        groups_index_max += 1

        for (i, j), groups in cell_in_groups.items():
            clause = []
            clause.append(-(i * max_j * 9 + j * 9 + 4))
            for group in groups:
                clause.append(group)
            solver.add_clause(clause)
            clause.clear()


        shapes = self.generate_polyominoes(5)
        groups_index_min = groups_index_max
        cell_in_groups = {}

        for i in range(max_i):
            for j in range(max_j):
                for shape in shapes:
                    if self.can_shape_be_placed(shape, i, j, max_i, max_j):
                        for coordinates in shape:
                            solver.add_clause([-groups_index_max,  (i + coordinates[0]) * max_j * 9 + (j + coordinates[1]) * 9 + 5])

                        coordinates_of_shape = [(x + i, y + j) for x, y in shape]

                        for x, y in coordinates_of_shape:

                            if (x, y) not in cell_in_groups:
                                cell_in_groups[(x, y)] = []

                            cell_in_groups[(x, y)].append(groups_index_max)

                            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                            for nx, ny in neighbors:
                                if 0 <= nx < max_i and 0 <= ny < max_j and (nx, ny) not in coordinates_of_shape:
                                    solver.add_clause([-groups_index_max, -(nx * max_j * 9 + ny * 9 + 5)])

                        groups_index_max += 1

        for (i, j), groups in cell_in_groups.items():
            clause = []
            clause.append(-(i * max_j * 9 + j * 9 + 5))
            for group in groups:
                clause.append(group)
            solver.add_clause(clause)
            clause.clear()

        polyominos_file = open("polyominos.txt", "r")
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
                            solver.add_clause([-groups_index_max,((i + coordinates[0]) * max_j * 9 + (j + coordinates[1]) * 9 + 6)])

                        coordinates_of_shape = [(x + i, y + j) for x, y in shape]

                        for x, y in coordinates_of_shape:

                            if (x, y) not in cell_in_groups:
                                cell_in_groups[(x, y)] = []

                            cell_in_groups[(x, y)].append(groups_index_max)

                            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                            for nx, ny in neighbors:
                                if 0 <= nx < max_i and 0 <= ny < max_j and (nx, ny) not in coordinates_of_shape:
                                    solver.add_clause([-groups_index_max, -(nx * max_j * 9 + ny * 9 + 6)])

                        groups_index_max += 1

        for (i, j), groups in cell_in_groups.items():
            clause = []
            clause.append(-(i * max_j * 9 + j * 9 + 6))
            for group in groups:
                clause.append(group)
            solver.add_clause(clause)
            clause.clear()

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
                            solver.add_clause([-groups_index_max, ((i + coordinates[0]) * max_j * 9 + (j + coordinates[1]) * 9 + 7)])

                        coordinates_of_shape = [(x + i, y + j) for x, y in shape]

                        for x, y in coordinates_of_shape:

                            if (x, y) not in cell_in_groups:
                                cell_in_groups[(x, y)] = []

                            cell_in_groups[(x, y)].append(groups_index_max)

                            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                            for nx, ny in neighbors:
                                if 0 <= nx < max_i and 0 <= ny < max_j and (nx, ny) not in coordinates_of_shape:
                                    solver.add_clause([-groups_index_max, -(nx * max_j * 9 + ny * 9 + 7)])

                        groups_index_max += 1

        for (i, j), groups in cell_in_groups.items():
            clause = []
            clause.append(-(i * max_j * 9 + j * 9 + 7))
            for group in groups:
                clause.append(group)
            solver.add_clause(clause)
            clause.clear()

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
                            solver.add_clause([-groups_index_max, ((i + coordinates[0]) * max_j * 9 + (j + coordinates[1]) * 9 + 8)])
                        coordinates_of_shape = [(x + i, y + j) for x, y in shape]

                        for x, y in coordinates_of_shape:

                            if (x, y) not in cell_in_groups:
                                cell_in_groups[(x, y)] = []

                            cell_in_groups[(x, y)].append(groups_index_max)

                            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                            for nx, ny in neighbors:
                                if 0 <= nx < max_i and 0 <= ny < max_j and (nx, ny) not in coordinates_of_shape:
                                    solver.add_clause([-groups_index_max, -(nx * max_j * 9 + ny * 9 + 8)])

                        groups_index_max += 1

        for (i, j), groups in cell_in_groups.items():
            clause = []
            clause.append(-(i * max_j * 9 + j * 9 + 8))
            for group in groups:
                clause.append(group)
            solver.add_clause(clause)
            clause.clear()

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
                            solver.add_clause([-(groups_index_max), ((i + coordinates[0]) * max_j * 9 + (j + coordinates[1]) * 9 + 9)])
                        coordinates_of_shape = [(x + i, y + j) for x, y in shape]

                        for x, y in coordinates_of_shape:

                            if (x, y) not in cell_in_groups:
                                cell_in_groups[(x, y)] = []

                            cell_in_groups[(x, y)].append(groups_index_max)

                            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                            for nx, ny in neighbors:
                                if 0 <= nx < max_i and 0 <= ny < max_j and (nx, ny) not in coordinates_of_shape:
                                    solver.add_clause([-(groups_index_max), -(nx * max_j * 9 + ny * 9 + 9)])

                        groups_index_max += 1

        for (i, j), groups in cell_in_groups.items():
            clause = []
            clause.append(-(i * max_j * 9 + j * 9 + 9))
            for group in groups:
                clause.append(group)
            solver.add_clause(clause)

        polyominos_file.close()
        return solver

