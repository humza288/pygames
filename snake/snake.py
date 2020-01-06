import pygame
import random
import copy

s_width = 800
s_height = 800
block_size = 20
game_over = False
pivot_positions = {}


class Snake(object):
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
        self.elements = {(head[0], head[1]): "up", (tail[0], tail[1]): 'up'}


def move_snake_head(s_object, direction):

    global game_over

    if direction == 'continue':
        try:
            direction = s_object.elements[(s_object.head[0], s_object.head[1])]
        except:
            game_over = True

    s_object.elements[(s_object.head[0], s_object.head[1])] = direction
    pivot_positions[(s_object.head[0], s_object.head[1])] = direction

    if direction == 'left':
        if s_object.head[0] < 1:
            s_object.head[0] = 39
        else:
            s_object.head[0] -= 1

    elif direction == 'right':
        if s_object.head[0] > 39:
            s_object.head[0] = 0
        else:
            s_object.head[0] += 1

    elif direction == 'up':
        if s_object.head[1] < 1:
            s_object.head[1] = 39
        else:
            s_object.head[1] -= 1

    elif direction == 'down':
        if s_object.head[1] > 39:
            s_object.head[1] = 0
        else:
            s_object.head[1] += 1

    move_snake_body(s_object)


def get_food(s_object):
    elements = list(s_object.elements.keys())
    direction = list(s_object.elements.values())

    if direction[-1] == 'left':
        s_object.elements[elements[-1][0] + 1, elements[-1][1]] = 'left'
    elif direction[-1] == 'right':
        s_object.elements[elements[-1][0] - 1, elements[-1][1]] = 'right'
    elif direction[-1] == 'up':
        s_object.elements[elements[-1][0], elements[-1][1] - 1] = 'up'
    elif direction[-1] == 'down':
        s_object.elements[elements[-1][0], elements[-1][1] + 1] = 'down'


def move_snake_body(s_object):

    temp_elements = copy.deepcopy(s_object.elements)

    for elem in s_object.elements:
        if elem in pivot_positions:
            temp_elements[elem] = pivot_positions[elem]

    for elem in s_object.elements:
        if temp_elements[elem] == 'left':
            del temp_elements[elem]
            if elem[0] < 1:
                temp_elements[(39, elem[1])] = 'left'
            else:
                temp_elements[(elem[0] - 1, elem[1])] = 'left'

        elif temp_elements[elem] == 'right':
            del temp_elements[elem]
            if elem[0] > 39:
                temp_elements[(0, elem[1])] = 'right'
            else:
                temp_elements[(elem[0] + 1, elem[1])] = 'right'

        elif temp_elements[elem] == 'up':
            del temp_elements[elem]
            if elem[1] < 1:
                temp_elements[(elem[0], 39)] = 'up'
            else:
                temp_elements[(elem[0], elem[1] - 1)] = 'up'

        elif temp_elements[elem] == 'down':
            del temp_elements[elem]
            if elem[1] > 39:
                temp_elements[(elem[0], 0)] = 'down'
            else:
                temp_elements[(elem[0], elem[1] + 1)] = 'down'

    s_object.elements = temp_elements


def draw_snake(surface, s_object):

    for i, j in s_object.elements:
        pygame.draw.rect(win, (0, 255, 0),
                         (i * block_size,
                          j * block_size, block_size,
                          block_size))


def rand_coord():
    pair = (random.randint(1, 39), random.randint(1, 39))
    return pair


def draw_food(surface, x_coord, y_coord):
    pygame.draw.rect(surface, (255, 0, 0), (x_coord * block_size, y_coord * block_size, block_size, block_size))


def create_grid():
    grid = [[(0, 0, 0) for _ in range(40)] for _ in range(40)]

    return grid


def draw_grid(surface, grid, s_object, x_coord, y_coord):
    surface.fill((0, 0, 0))
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (0, i * block_size), (s_width, i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (j * block_size, 0), (j * block_size, s_height))
    draw_food(surface, x_coord, y_coord)
    draw_snake(surface, s_object)


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (s_width/2 - label.get_width() / 2, s_height / 2 -label.get_height() / 2))


def lost(surface):
    surface.fill((0, 0, 0))
    draw_text_middle('You Lost!', 75, (255, 0, 0), surface)


def update_score(score, surface):
    font = pygame.font.SysFont('comicsans', 22, bold=True)
    score = font.render(score, 1, (225, 225, 225))
    surface.blit(score, (600, 20))


def main(surface):
    run = True

    grid = create_grid()
    snake = Snake([29, 22], [29, 23])
    x_coord, y_coord = rand_coord()
    clock = pygame.time.Clock()
    move_time = 0
    move_speed = 0.14
    score = 0

    while run:
        move_time += clock.get_rawtime()
        clock.tick()

        if move_time/1000 > move_speed:
            move_time = 0
            move_snake_head(snake, 'continue')

        for event in pygame.event.get():
            if event.type == pygame.QUIT or game_over:
                if game_over:
                    lost(surface)
                pygame.display.update()
                pygame.time.delay(1000)
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_snake_head(snake, 'left')
                elif event.key == pygame.K_RIGHT:
                    move_snake_head(snake, 'right')
                elif event.key == pygame.K_UP:
                    move_snake_head(snake, 'up')
                elif event.key == pygame.K_DOWN:
                    move_snake_head(snake, 'down')

        if x_coord == snake.head[0] and y_coord == snake.head[1]:
            get_food(snake)
            x_coord, y_coord = rand_coord()
            score += 1

        if run:
            draw_grid(surface, grid, snake, x_coord, y_coord)
            update_score('Snake Len: ' + str(score + 2), win)
            pygame.display.update()


pygame.init()
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Snake')
main(win)