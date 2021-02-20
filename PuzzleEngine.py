"""
This class is responsible for storing all the information about the current state of the puzzle. It will also be
responsible for determining the next moves using one of the algorithms. It will also keep a moves log.
"""
import random


class PuzzleState:
    def __init__(self, puzzle_variables):
        # Board containing the initial positions of the queens.
        # Each column would contain only one queen.
        # The row positions will be generated randomly.
        self.dimensions = puzzle_variables['dimensions']
        self.puzzle_variables = puzzle_variables
        self.board = []
        self.log = []
        self.population = []
        self.fitted_population = []
        self.generation_count = 0
        self.g_n = 0
        self.initialize_generation()
        self.determine_fitness()
        self.fitted_population.sort()
        for i in range(self.dimensions):
            self.board.append(random.randint(0, self.dimensions - 1))

    """
    Responsible for checking if a queen is safe or not.
    """

    def q_is_safe(self, row, col):
        # Check the lower right diagonal for possible attacks
        i = 1
        while row + i < self.dimensions and col + i < self.dimensions:
            if self.board[col + i] == row + i:
                return False
            i += 1

        # Check the upper left diagonal for possible attacks
        i = 1
        while row - i > -1 and col - i > -1:
            if self.board[col - i] == row - i:
                return False
            i += 1

        # Check the upper right diagonal for possible attacks
        i = 1
        while row - i > -1 and col + i < self.dimensions:
            if self.board[col + i] == row - i:
                return False
            i += 1

        # Check the lower left diagonal for possible attacks
        i = 1
        while row + i < self.dimensions and col - i > -1:
            if self.board[col - i] == row + i:
                return False
            i += 1

        # Check the right row for possible attacks
        i = 1
        while col + i < self.dimensions:
            if self.board[col + i] == row:
                return False
            i += 1

        # Check the left row for possible attacks
        i = 1
        while col - i > -1:
            if self.board[col - i] == row:
                return False
            i += 1

        return True

    """
      Responsible for calculating the number of attacks on a queen.
    """

    def number_of_attacks(self, row, col, board):
        n = 0
        # Check the lower right diagonal for possible attacks
        i = 1
        while row + i < self.dimensions and col + i < self.dimensions:
            if board[col + i] == row + i:
                n += 1
            i += 1

        # Check the upper left diagonal for possible attacks
        i = 1
        while row - i > -1 and col - i > -1:
            if board[col - i] == row - i:
                n += 1
            i += 1

        # Check the upper right diagonal for possible attacks
        i = 1
        while row - i > -1 and col + i < self.dimensions:
            if board[col + i] == row - i:
                n += 1
            i += 1

        # Check the lower left diagonal for possible attacks
        i = 1
        while row + i < self.dimensions and col - i > 0:
            if board[col - i] == row + i:
                n += 1
            i += 1

        # Check the right row for possible attacks
        i = 1
        while col + i < self.dimensions:
            if board[col + i] == row:
                n += 1
            i += 1

        # Check the left row for possible attacks
        i = 1
        while col - i > -1:
            if board[col - i] == row:
                n += 1
            i += 1

        return n

    """
      Responsible for calculating the total number of attack on the board.
    """

    def calc_total_attacks(self, col):
        up_board = []
        down_board = []
        for idx, row in enumerate(self.board):
            if idx == col:
                up_board.append(row - 1)
                down_board.append(row + 1)
            else:
                up_board.append(row)
                down_board.append(row)

        up_attacks = self.number_of_attacks(up_board[col], col, up_board)
        down_attacks = self.number_of_attacks(down_board[col], col, up_board)
        i = 1
        while col + i < self.dimensions:
            up_attacks += self.number_of_attacks(up_board[col + i], col + i, up_board)
            down_attacks += self.number_of_attacks(down_board[col + i], col + i, down_board)
            i += 1

        i = 1
        while col - i > -1:
            up_attacks += self.number_of_attacks(up_board[col - i], col - i, up_board)
            down_attacks += self.number_of_attacks(down_board[col - i], col - i, down_board)
            i += 1

        if up_board[col] == -1:
            return down_attacks, 'down'

        elif down_board[col] == self.dimensions:
            return up_attacks, 'up'

        else:
            return min((up_attacks, 'up'), (down_attacks, 'down'))

    """
      Responsible for applying A* Algorithm.
    """

    def astar_algorithm(self):
        solved = False
        queue = []
        for col in range(self.dimensions):
            n_attacks, direction = self.calc_total_attacks(col)
            h_n = n_attacks
            f_n = self.g_n + h_n
            move = (f_n, str(col), direction)
            for q in queue:
                if q[1] == str(col) and q[0] <= move[0]:
                    move = q
                    queue.remove(q)
            queue.append(move)
        self.g_n += 1

        i = 0
        queue.sort()
        q_col = int(int(queue[i][1]))
        while i < self.dimensions:
            if (self.board[q_col] + 1 == self.dimensions and queue[i][2] == 'down') or (
                    self.board[q_col] - 1 < 0 and queue[i][2] == 'up'):
                i += 1
                if i < self.dimensions:
                    q_col = int(int(queue[i][1]))
            elif len(self.log) > 0:
                temp_board = []
                for col, row in enumerate(self.board):
                    if str(col) == queue[i][1]:
                        if queue[i][2] == 'up':
                            temp_board.append(row - 1)
                        else:
                            temp_board.append(row + 1)
                    else:
                        temp_board.append(row)

                if temp_board in self.log:
                    i += 1
                else:
                    break
            else:
                break
        n_q_save = 0
        for col, row in enumerate(self.board):
            if self.q_is_safe(row, col):
                n_q_save += 1

        if n_q_save == self.dimensions:
            solved = True
        elif i < self.dimensions:
            selected_q = queue[i]
            prev_board = []
            for row in self.board:
                prev_board.append(row)
            self.log.append(prev_board)
            if selected_q[2] == 'up' and self.board[int(selected_q[1])] - 1 > -1:
                self.board[int(selected_q[1])] -= 1
            elif selected_q[2] == 'down' and self.board[int(selected_q[1])] + 1 < self.dimensions:
                self.board[int(selected_q[1])] += 1

        return solved

    """
      Responsible creating the initial generation for the Genetic algorithm.
    """

    def initialize_generation(self):
        i = 0
        while i < self.puzzle_variables['population_size']:
            board = []
            for _ in range(self.dimensions):
                board.append(random.randint(0, self.dimensions - 1))

            if board not in self.population:
                self.population.append(board)
                i += 1

    """
      Responsible for calculating the fitness of each parent in the generation for the Genetic algorithm.
    """

    def determine_fitness(self):
        for board in self.population:
            fit = 0
            for col, row in enumerate(board):
                fit += self.number_of_attacks(row, col, board)
            self.fitted_population.append((fit, board))

    """
      Responsible applying crossover between selected parents.
    """

    def crossover(self, p1, p2, new_population):
        child1 = []
        child2 = []
        if self.puzzle_variables['crossover'] == 'Single point':
            crossover_point = random.randint(1, self.dimensions - 1)
            for i in range(crossover_point):
                child1.append(p1[i])
                child2.append(p2[i])

            for i in range(crossover_point, self.dimensions):
                child1.append(p2[i])
                child2.append(p1[i])

        else:
            crossover_point_1 = random.randint(0, self.dimensions / 2)
            crossover_point_2 = random.randint(crossover_point_1 + 1, self.dimensions - 1)
            for i in range(0, crossover_point_1):
                child1.append(p1[i])
                child2.append(p2[i])

            for i in range(crossover_point_1, crossover_point_2):
                child1.append(p2[i])
                child2.append(p1[i])

            for i in range(crossover_point_2, self.dimensions):
                child1.append(p1[i])
                child2.append(p2[i])

        t_fit = []
        for child in [child1, child2]:
            fit = 0
            for col, row in enumerate(child):
                fit += self.number_of_attacks(row, col, child)
            t_fit.append(fit)

        if t_fit[0] < t_fit[1]:
            new_population.append(child1)
        else:
            new_population.append(child2)

    def mutation(self, new_population, n_recomb):
        n_mutation = int(self.puzzle_variables['mutation_rate'] * self.puzzle_variables['population_size'])
        for _ in range(n_mutation):
            n_bits = random.randint(1, self.dimensions / 2)
            for _ in range(n_bits):
                rand_child = random.randint(n_recomb + 1, self.puzzle_variables['population_size'] - 1)
                rand_gene = random.randint(0, self.puzzle_variables['dimensions'] - 1)
                rand_row = random.randint(0, self.puzzle_variables['dimensions'] - 1)
                while rand_row == new_population[rand_child][rand_gene]:
                    rand_row = random.randint(0, self.puzzle_variables['dimensions'] - 1)
                new_population[rand_child][rand_gene] = rand_row

    def genetic_algorithm(self):
        solved = False
        new_population = []
        if self.generation_count == self.puzzle_variables['n_generations']:
            return True, self.generation_count

        if self.fitted_population[0][0] != 0:
            recombination_rate = 1 - self.puzzle_variables['crossover_rate']
            n_recomb = int(round(recombination_rate, 1) * self.puzzle_variables['population_size'])
            if self.puzzle_variables['recombination'] == 'With elitism':
                for elite in self.population[:n_recomb]:
                    new_population.append(elite)
            else:
                picked = []
                i = 0
                while i < n_recomb:
                    num = random.randint(0, self.puzzle_variables['population_size'] - 1)
                    if num not in picked:
                        picked.append(num)
                        new_population.append(self.population[num])
                        i += 1

            total_population_attacks = 0
            for member in self.fitted_population:
                total_population_attacks += member[0]

            probabilites = []
            for member in self.fitted_population:
                probabilites.append(1 - (member[0] / total_population_attacks))

            n_crossover = int(self.puzzle_variables['crossover_rate'] * self.puzzle_variables['population_size'])
            for _ in range(n_crossover):
                selected = random.choices(population=self.population, k=2, weights=probabilites)
                first_parent = selected[0]
                second_parent = selected[1]

                p1 = []
                p2 = []

                for i in range(self.dimensions):
                    p1.append(first_parent[i])

                for i in range(self.dimensions):
                    p2.append(second_parent[i])

                self.crossover(p1, p2, new_population)

            self.mutation(new_population, n_recomb)

            self.population = new_population
            self.fitted_population = []
            self.determine_fitness()
            self.fitted_population.sort()

            self.board = self.fitted_population[0][1]
            self.generation_count += 1
            if self.fitted_population[0][0] == 0:
                solved = True

        else:
            solved = True
            self.board = self.fitted_population[0][1]

        return solved, self.generation_count
