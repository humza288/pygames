import pygame
import random
import copy

s_width = 800
s_height = 800
block_size = 20
movements = {}


class Snake(object):
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail
        self.elements = {(head[0], head[1]): "up", (tail[0], tail[1]): 'up', (tail[0], tail[1] + 1): 'up'}


def move_snake_head(s_object, direction):

    s_object.elements[(s_object.head[0], s_object.head[1])] = direction
    movements[(s_object.head[0], s_object.head[1])] = direction

    if direction == 'left':
        s_object.head[0] -= 1

    elif direction == 'right':
        s_object.head[0] += 1

    elif direction == 'up':
        s_object.head[1] -= 1

    elif direction == 'down':
        s_object.head[1] += 1

    move_snake_body(s_object)


def move_snake_body(s_object):

    temp_elements = copy.deepcopy(s_object.elements)

    for elem in s_object.elements:
        if elem in movements:
            temp_elements[elem] = movements[elem]

        elif s_object.elements[elem] == 'left':
            del temp_elements[elem]
            temp_elements[(elem[0] - 1, elem[1])] = 'left'

        elif s_object.elements[elem] == 'right':
            del temp_elements[elem]
            temp_elements[(elem[0] + 1, elem[1])] = 'right'

        elif s_object.elements[elem] == 'up':
            del temp_elements[elem]
            temp_elements[(elem[0], elem[1] - 1)] = 'up'

        elif s_object.elements[elem] == 'down':
            del temp_elements[elem]
            temp_elements[(elem[0], elem[1] + 1)] = 'down'

    s_object.elements = temp_elements


def draw_snake(surface, s_object):

    for i, j in s_object.elements:
        pygame.draw.rect(win, (0, 255, 0),
                         (i * block_size,
                          j * block_size, block_size,
                          block_size))


def rand_coord():
    pair = (random.randint(0, 40), random.randint(0, 40))
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


def main(surface):
    run = True

    grid = create_grid()
    snake = Snake([29, 22], [29, 23])
    x_coord, y_coord = rand_coord()

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_snake_head(snake, 'left')
                elif event.key == pygame.K_RIGHT:
                    move_snake_head(snake, 'right')
                elif event.key == pygame.K_UP:
                    move_snake_head(snake, 'up')
                elif event.key == pygame.K_DOWN:
                    move_snake_head(snake, 'down')
                elif event.key == pygame.K_s:
                    move_snake_body(snake)

        draw_grid(surface, grid, snake, x_coord, y_coord)
        pygame.display.update()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Snake')
main(win)