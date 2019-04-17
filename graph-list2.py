import sys
import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGRAY = (169, 169, 169)
YELLOW = (222, 178, 0)
PINK = (225, 96, 253)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
ORANGE = (255, 99, 71)
GRAY = (119, 136, 153)
LIGHTORANGE = (255, 176, 56)
INTERMEDIARYORANGE = (255, 154, 0)
LIGHTBLUE = (60, 170, 255)
DARKBLUE = (0, 101, 178)
BEIGE = (178, 168, 152)

BORDER_THICKNESS = 1.0

HEIGHT_TOTAL = 680
WIDTH = 600
HEIGHT = 600
SCREEN_SIZE = (WIDTH, HEIGHT_TOTAL)

FONTSIZE_START = 50
FONTSIZE_COMMANDS_INTIAL = 25
FONTSIZE_MAZE = 20

SIZE = 25


def text(background, message, color, size, coordinate_x, coordinate_y):
    font = pygame.font.SysFont(None, size)
    text = font.render(message, True, color)
    background.blit(text, [coordinate_x, coordinate_y])


class NodeBorder():
    def __init__(self, pos_x, pos_y, width, height):
        self.color = BLACK
        self.thickness = BORDER_THICKNESS
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    def render(self, background):
        pygame.draw.rect(background, self.color, [
                         self.pos_x, self.pos_y, self.width, self.height])


class Node():
    def __init__(self, pos_x, pos_y):
        self.color = DARKGRAY

        self.id = None
        self.visited = False
        self.explored = False

        self.matrix_pos_x = 0
        self.matrix_pos_y = 0

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = SIZE
        self.height = SIZE

        self.top_border = NodeBorder(
            self.pos_x, self.pos_y, SIZE, BORDER_THICKNESS)
        self.bottom_border = NodeBorder(
            self.pos_x, self.pos_y + SIZE - BORDER_THICKNESS, SIZE, BORDER_THICKNESS)
        self.right_border = NodeBorder(
            self.pos_x + SIZE - BORDER_THICKNESS, self.pos_y, BORDER_THICKNESS, SIZE)
        self.left_border = NodeBorder(
            self.pos_x, self.pos_y, BORDER_THICKNESS, SIZE)

        self.neighbors_not_visited = []
        self.neighbors_connected = []
        self.parent = None

    def render(self, background):
        pygame.draw.rect(background, self.color, [
                         self.pos_x, self.pos_y, self.width, self.height])

        self.top_border.render(background)
        self.bottom_border.render(background)
        self.right_border.render(background)
        self.left_border.render(background)


class Maze():
    def __init__(self, background, initial_x, initial_y):
        self.maze = []
        self.total_nodes = 0
        self.maze_created = False
        self.initial_coordinate_x = initial_x
        self.initial_coordinate_y = initial_y
        self.final_coordinate_x = 0
        self.final_coordinate_y = 0
        self.minpoints = 0

        x = 0
        y = 0
        for i in range(0, WIDTH, SIZE):
            self.maze.append([])
            for j in range(0, HEIGHT, SIZE):
                self.maze[x].append(Node(i, j))
                self.total_nodes += 1
                y += 1
            x += 1

        self.define_initial_neighbors_not_visited()

    def add_edge(self, node, neighbor):
        edge_weight = random.randint(1, 20)
        neighbor.neighbors_connected.append((node, edge_weight))
        node.neighbors_connected.append((neighbor, edge_weight))

    def remove_neighbors_visited(self):
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].neighbors_not_visited = [
                    x for x in self.maze[i][j].neighbors_not_visited if not x.visited]

    def define_initial_neighbors_not_visited(self):
        id = 0
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].matrix_pos_x = i
                self.maze[i][j].matrix_pos_y = j
                id += 1
                self.maze[i][j].id = id
                if i > 0 and j > 0 and i < int(HEIGHT / SIZE) - 1 and j < int(HEIGHT / SIZE) - 1:
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i + 1][j])  # bot
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j - 1])  # left
                elif i == 0 and j == 0:
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i + 1][j])  # bot
                elif i == int(HEIGHT / SIZE) - 1 and j == 0:
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j + 1])  # right
                elif i == 0 and j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j - 1])  # left
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i + 1][j])  # bot
                elif i == int(HEIGHT / SIZE) - 1 and j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j - 1])  # left
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i - 1][j])  # top
                elif j == 0:
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i + 1][j])  # bot
                elif i == 0:
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i + 1][j])  # bot
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j - 1])  # left
                elif i == int(HEIGHT / SIZE) - 1:
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j - 1])  # left
                elif j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i + 1][j])  # bot
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors_not_visited.append(
                        self.maze[i][j - 1])  # left

    def dijkstra_to_define_final(self, background):
        initial_node = self.maze[self.initial_coordinate_x][self.initial_coordinate_y]
        max_distance = 100000
        distances = {}
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                if self.maze[i][j] == self.maze[self.initial_coordinate_x][self.initial_coordinate_y]:
                    distances[self.maze[i][j]] = 0
                else:
                    distances[self.maze[i][j]] = max_distance
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].explored = False
        number_explored = 0
        while number_explored < self.total_nodes:
            # Pega o elemento com a menor distancia entre os nao explorados
            shorter_distance = max_distance
            for key, value in distances.items():
                if value < shorter_distance and not key.explored:
                    shorter_distance_node = key
                    shorter_distance = value
            # Marco como explorado
            shorter_distance_node.explored = True
            number_explored += 1

            for neighbor in shorter_distance_node.neighbors_connected:
                total_distance = shorter_distance + neighbor[1]
                if total_distance < distances[neighbor[0]]:
                    neighbor[0].parent = shorter_distance_node
                    distances[neighbor[0]] = total_distance

        # Pega o elemento com o maior distancia pro inicio
        bigger_distance = -1
        for key, value in distances.items():
            if value > bigger_distance:
                bigger_distance = value
                bigger_distance_node = key
        self.minpoints = bigger_distance
        self.final_coordinate_x = bigger_distance_node.matrix_pos_x
        self.final_coordinate_y = bigger_distance_node.matrix_pos_y

    def break_border(self, node, neightbor, color):
        # right
        if (neightbor.matrix_pos_x == node.matrix_pos_x + 1) and (neightbor.matrix_pos_y == node.matrix_pos_y):
            node.right_border.color = color
            neightbor.left_border.color = color
        # left
        elif (neightbor.matrix_pos_x == node.matrix_pos_x - 1) and (neightbor.matrix_pos_y == node.matrix_pos_y):
            node.left_border.color = color
            neightbor.right_border.color = color
        # bot
        elif (neightbor.matrix_pos_x == node.matrix_pos_x) and (neightbor.matrix_pos_y == node.matrix_pos_y + 1):
            node.bottom_border.color = color
            neightbor.top_border.color = color
        # top
        elif (neightbor.matrix_pos_x == node.matrix_pos_x) and (neightbor.matrix_pos_y == node.matrix_pos_y - 1):
            node.top_border.color = color
            neightbor.bottom_border.color = color

    def dfs(self, background):
        current_cell = random.choice(random.choice(self.maze))
        current_cell.visited = True
        current_cell.color = GREEN
        stack = [current_cell]
        visited_cells = 1

        while visited_cells != self.total_nodes or len(stack) != 0:
            self.remove_neighbors_visited()
            if len(current_cell.neighbors_not_visited) > 0:
                random_neighbor = random.choice(
                    current_cell.neighbors_not_visited)

                self.break_border(current_cell, random_neighbor, GREEN)

                self.add_edge(current_cell, random_neighbor)
                current_cell = random_neighbor
                stack.append(current_cell)
                current_cell.visited = True
                current_cell.color = GREEN
                visited_cells += 1
            else:
                current_cell.color = YELLOW

                if current_cell.top_border.color == GREEN:
                    current_cell.top_border.color = YELLOW
                if current_cell.bottom_border.color == GREEN:
                    current_cell.bottom_border.color = YELLOW
                if current_cell.right_border.color == GREEN:
                    current_cell.right_border.color = YELLOW
                if current_cell.left_border.color == GREEN:
                    current_cell.left_border.color = YELLOW

                if len(stack) == 1:
                    stack.pop()
                else:
                    stack.pop()
                    current_cell = stack[-1]
            self.render(background)
            text(background, "GENERATING MAZE", WHITE,
                 FONTSIZE_COMMANDS_INTIAL, 215, 620)
            pygame.display.update()
        self.maze_created = True

    def prim(self, background):
        initial_cell = random.choice(random.choice(self.maze))
        initial_cell.visited = True
        initial_cell.color = YELLOW

        without_neighbors_visited = [initial_cell]
        visited_cells_number = 1

        while visited_cells_number != self.total_nodes:
            self.remove_neighbors_visited()
            # filtra a lista de celulas com vizinhos não visitados
            without_neighbors_visited = [
                x for x in without_neighbors_visited if len(x.neighbors_not_visited) > 0]
            current_cell = random.choice(without_neighbors_visited)

            if len(current_cell.neighbors_not_visited) > 0:
                for cell_visited in without_neighbors_visited:
                    for cell in cell_visited.neighbors_not_visited:
                        cell.color = GREEN

                random_neighbor = random.choice(
                    current_cell.neighbors_not_visited)

                self.break_border(current_cell, random_neighbor, YELLOW)

                self.add_edge(current_cell, random_neighbor)

                random_neighbor.visited = True
                random_neighbor.color = YELLOW

                if len(random_neighbor.neighbors_not_visited) > 0:
                    without_neighbors_visited.append(random_neighbor)

                visited_cells_number += 1

            self.render(background)
            text(background, "GENERATING MAZE", WHITE,
                 FONTSIZE_COMMANDS_INTIAL, 215, 620)
            pygame.display.update()
        self.maze_created = True

    def kruskal(self, background):
        equals_id = False
        while not equals_id:
            # verifica se todas as celulas pertencem ao mesmo conjunto
            ids = set()
            for i in range(0, int(HEIGHT / SIZE)):
                for j in range(0, int(WIDTH / SIZE)):
                    ids.add(self.maze[i][j].id)
            if (len(ids) == 1):
                equals_id = True

            current_cell = random.choice(random.choice(self.maze))
            random_neighbor = random.choice(current_cell.neighbors_not_visited)

            if random_neighbor.id != current_cell.id:
                current_cell.color = YELLOW
                self.break_border(current_cell, random_neighbor, YELLOW)
                self.add_edge(current_cell, random_neighbor)
                random_neighbor.color = YELLOW
                id_neighbor = random_neighbor.id
                for i in range(0, int(HEIGHT / SIZE)):
                    for j in range(0, int(WIDTH / SIZE)):
                        if self.maze[i][j].id == id_neighbor:
                            self.maze[i][j].id = current_cell.id

            self.render(background)
            text(background, "GENERATING MAZE", WHITE,
                 FONTSIZE_COMMANDS_INTIAL, 215, 620)
            pygame.display.update()
        self.maze_created = True

    def dijkstra(self, background, player):
        initial_node = self.maze[player.matrix_pos_x][player.matrix_pos_y]

        max_distance = 100000
        distances = {}
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                if self.maze[i][j] == self.maze[player.matrix_pos_x][player.matrix_pos_y]:
                    distances[self.maze[i][j]] = 0
                else:
                    distances[self.maze[i][j]] = max_distance
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].explored = False
        number_explored = 0
        while number_explored < self.total_nodes:
            # Pega o elemento com a menor distancia entre os nao explorados
            shorter_distance = max_distance
            for key, value in distances.items():
                if value < shorter_distance and not key.explored:
                    shorter_distance_node = key
                    shorter_distance = value
            # Marco como explorado
            shorter_distance_node.explored = True
            number_explored += 1

            shorter_distance_node.color = PINK

            if shorter_distance_node.top_border.color == YELLOW:
                shorter_distance_node.top_border.color = PINK
            if shorter_distance_node.bottom_border.color == YELLOW:
                shorter_distance_node.bottom_border.color = PINK
            if shorter_distance_node.right_border.color == YELLOW:
                shorter_distance_node.right_border.color = PINK
            if shorter_distance_node.left_border.color == YELLOW:
                shorter_distance_node.left_border.color = PINK
            
            for neighbor in shorter_distance_node.neighbors_connected:
                total_distance = shorter_distance + neighbor[1]
                if total_distance < distances[neighbor[0]]:
                    neighbor[0].parent = shorter_distance_node
                    distances[neighbor[0]] = total_distance

            self.render(background)
            text(background, "SOLVING MAZE", WHITE,
                 FONTSIZE_COMMANDS_INTIAL, 218, 620)
            player.render(background)
            pygame.display.update()

        current = self.maze[self.final_coordinate_x][self.final_coordinate_y]
        while current.parent != initial_node:
            current = current.parent
            current.color = ORANGE

            if current.top_border.color == PINK:
                current.top_border.color = ORANGE
            if current.bottom_border.color == PINK:
                current.bottom_border.color = ORANGE
            if current.right_border.color == PINK:
                current.right_border.color = ORANGE
            if current.left_border.color == PINK:
                current.left_border.color = ORANGE

            self.render(background)
            player.render(background)
            pygame.display.update()

    def render(self, background):
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].render(background)
        if self.maze_created:
            self.maze[self.initial_coordinate_x][self.initial_coordinate_y].color = BEIGE
            self.maze[self.final_coordinate_x][self.final_coordinate_y].color = LIGHTBLUE


class Player():
    def __init__(self, initial_x, initial_y):
        self.pos_x = initial_x * SIZE + BORDER_THICKNESS
        self.pos_y = initial_y * SIZE + BORDER_THICKNESS
        self.matrix_pos_x = initial_x
        self.matrix_pos_y = initial_y
        self.width = SIZE - 2 * BORDER_THICKNESS
        self.height = SIZE - 2 * BORDER_THICKNESS
        self.color = RED
        self.points = 0

    def update(self, maze, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.pos_x > BORDER_THICKNESS and (maze[self.matrix_pos_x][self.matrix_pos_y].left_border.color != BLACK):
                    
                    for cell in maze[self.matrix_pos_x][self.matrix_pos_y].neighbors_connected:
                        if cell[0] == maze[self.matrix_pos_x - 1][self.matrix_pos_y]:
                            self.points += cell[1]

                    self.pos_x -= SIZE
                    self.matrix_pos_x -= 1
                if event.key == pygame.K_RIGHT and self.pos_x + BORDER_THICKNESS < WIDTH - SIZE and (maze[self.matrix_pos_x][self.matrix_pos_y].right_border.color != BLACK):
                    
                    for cell in maze[self.matrix_pos_x][self.matrix_pos_y].neighbors_connected:
                        if cell[0] == maze[self.matrix_pos_x + 1][self.matrix_pos_y]:
                            self.points += cell[1]
                    
                    self.pos_x += SIZE
                    self.matrix_pos_x += 1
                if event.key == pygame.K_UP and self.pos_y > BORDER_THICKNESS and (maze[self.matrix_pos_x][self.matrix_pos_y].top_border.color != BLACK):
                    
                    for cell in maze[self.matrix_pos_x][self.matrix_pos_y].neighbors_connected:
                        if cell[0] == maze[self.matrix_pos_x][self.matrix_pos_y - 1]:
                            self.points += cell[1]
                    
                    self.pos_y -= SIZE
                    self.matrix_pos_y -= 1
                if event.key == pygame.K_DOWN and self.pos_y + BORDER_THICKNESS < HEIGHT - SIZE and (maze[self.matrix_pos_x][self.matrix_pos_y].bottom_border.color != BLACK):
                    
                    for cell in maze[self.matrix_pos_x][self.matrix_pos_y].neighbors_connected:
                        if cell[0] == maze[self.matrix_pos_x][self.matrix_pos_y + 1]:
                            self.points += cell[1]
                    
                    self.pos_y += SIZE
                    self.matrix_pos_y += 1

    def render(self, background):
        pygame.draw.rect(background, self.color, [
                         self.pos_x, self.pos_y, self.width, self.height])


class Game():
    def __init__(self):
        try:
            pygame.init()
        except:
            print('The pygame module did not start successfully')

        self.initial_coordinate_x = 0
        self.initial_coordinate_y = 0
        self.start = False
        self.solved = False
        self.winner = False
        self.exit = False

    def load(self):
        self.background = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Maze Game')
        self.initial_coordinate_x = random.randint(0, int(HEIGHT / SIZE) - 1)
        self.initial_coordinate_y = random.randint(0, int(WIDTH / SIZE) - 1)
        self.maze = Maze(self.background, self.initial_coordinate_x,
                         self.initial_coordinate_y)
        self.player = Player(self.initial_coordinate_x,
                             self.initial_coordinate_y)

    def update(self, event):
        if not self.solved and not self.winner:
            self.player.update(self.maze.maze, event)
        if self.player.matrix_pos_x == self.maze.final_coordinate_x and self.player.matrix_pos_y == self.maze.final_coordinate_y:
            self.winner = True

    def initial_game(self):
        self.background.fill(DARKBLUE)
        pygame.draw.rect(self.background, BEIGE, [40, 40, 530, 580])
        pygame.draw.rect(self.background, LIGHTBLUE, [40, 100, 530, 450])
        pygame.draw.rect(self.background, BLACK, [110, 150, 380, 380])
        pygame.draw.rect(self.background, DARKBLUE, [110, 150, 380, 100])
        text(self.background, "MAZE ADVENTURES 2.0",
             LIGHTORANGE, FONTSIZE_START - 5, 125, 185)
        text(self.background, "PRESS (ESC) TO CLOSE GAME",
             INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL + 2, 165, 425)
        pygame.display.update()
        pygame.time.wait(180)
        text(self.background, "PRESS (D) TO START GAME (DFS)",
             INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL + 2, 125, 350)
        text(self.background, "PRESS (P) TO START GAME (PRIM'S)",
             INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL + 2, 125, 375)
        text(self.background, "PRESS (K) TO START GAME (KRUSKAL)",
             INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL + 2, 125, 400)
        pygame.display.update()
        pygame.time.wait(180)

    def end_of_game(self):
        self.maze.dijkstra(self.background, self.player)

    def render(self):
        self.background.fill(BLACK)

        self.maze.render(self.background)

        self.player.render(self.background)

        # render numbers
        for cell in self.maze.maze[self.player.matrix_pos_x][self.player.matrix_pos_y].neighbors_connected:
            text(self.background, str(cell[1]),
                 WHITE, 15, cell[0].pos_x + 5, cell[0].pos_y + 5)

        if not self.solved and not self.winner:
            pygame.draw.rect(self.background, RED, [0, 601, SIZE, SIZE])
            text(self.background, "- PLAYER", WHITE,
                 FONTSIZE_MAZE, 0 + SIZE + 3, 601 + 6)
            pygame.draw.rect(self.background, BEIGE, [
                             0, 601 + SIZE + 1, SIZE, SIZE])
            text(self.background, "- STARTING POINT", WHITE,
                 FONTSIZE_MAZE, 0 + SIZE + 3, 601 + SIZE + 1 + 6)
            pygame.draw.rect(self.background, LIGHTBLUE, [
                             0, 601 + 2 * SIZE + 2, SIZE, SIZE])
            text(self.background, "- GOAL", WHITE, FONTSIZE_MAZE,
                 0 + SIZE + 3, 601 + 2 * SIZE + 1 + 6)

            text(self.background, "PRESS (R) TO RETRY GAME",
                 WHITE, FONTSIZE_MAZE, 220, 610)
            text(self.background, "PRESS (Q) TO GIVE UP",
                 WHITE, FONTSIZE_MAZE, 230, 630)
            text(self.background, "PRESS (ESC) TO CLOSE GAME",
                 WHITE, FONTSIZE_MAZE, 212, 650)

            text(self.background, "MINIMUM " + str(self.maze.minpoints), WHITE,
                 FONTSIZE_MAZE + 5, 450, 610)

            text(self.background, "POINTS +" + str(self.player.points), WHITE,
                 FONTSIZE_MAZE + 5, 450, 630)

        elif self.winner:
            text(self.background, "YOU WIN", BLUE, FONTSIZE_MAZE + 3, 264, 610)
            text(self.background, "PRESS (R) TO RETRY GAME",
                 WHITE, FONTSIZE_MAZE, 220, 630)
            text(self.background, "PRESS (ESC) TO CLOSE GAME",
                 WHITE, FONTSIZE_MAZE, 212, 650)
        else:
            text(self.background, "YOU LOSE", RED, FONTSIZE_MAZE + 3, 262, 610)
            text(self.background, "PRESS (R) TO RETRY GAME",
                 WHITE, FONTSIZE_MAZE, 220, 630)
            text(self.background, "PRESS (ESC) TO CLOSE GAME",
                 WHITE, FONTSIZE_MAZE, 212, 650)

        pygame.display.update()

    def run(self):
        self.load()
        while not self.start:
            self.initial_game()
            pygame.display.update()
            if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit(0)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.start = True
                    self.background.fill(BLACK)
                    self.maze.dfs(self.background)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.start = True
                    self.background.fill(BLACK)
                    self.maze.prim(self.background)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    self.start = True
                    self.background.fill(BLACK)
                    self.maze.kruskal(self.background)
        pygame.display.update()
        self.maze.dijkstra_to_define_final(self.background)
        pygame.display.update()
        while not self.exit:
            if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.exit = True
            e = pygame.event.get()
            if self.winner:
                self.background.fill(BLACK)
            for event in e:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.solved = False
                        self.winner = False
                        self.start = False
                        self.run()
                    if not self.solved and event.key == pygame.K_q and not self.winner:
                        self.background.fill(BLACK)
                        self.end_of_game()
                        self.solved = True
            self.update(e)
            self.render()

        pygame.quit()
        sys.exit(0)


def main():
    mygame = Game()
    mygame.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interruption')
