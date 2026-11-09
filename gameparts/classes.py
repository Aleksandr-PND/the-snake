from random import choice, randint
import pygame

from gameparts import (APPLE_COLOR, BOARD_BACKGROUND_COLOR, BORDER_COLOR, DOWN,
                       GRID_HEIGHT, GRID_SIZE, GRID_WIDTH, LEFT, RIGHT,
                       SCREEN_WIDTH, SCREEN_HEIGHT, SNAKE_COLOR, UP)


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Родительский класс для змейки и яблока"""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color: tuple[int, ...] = (0, 0, 0)

    def draw(self):
        """метод отрисовки"""
        pass


class Apple(GameObject):
    """Класс описывающий яблоко на поле."""

    body_color: tuple[int, int, int]

    def __init__(self) -> None:
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Метод, генерирующий позицию яблока."""
        self.positionX = (randint(0, GRID_WIDTH - 1)) * GRID_SIZE
        self.positionY = (randint(0, GRID_HEIGHT - 1)) * GRID_SIZE
        return (self.positionX, self.positionY)

    def draw(self):
        """Метод, отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения змейки."""
        self.new_head = self.get_head_position()
        self.last = self.positions[-1]
        self.positions.insert(0, self.new_head)
        if len(self.positions) > self.length:
            del self.positions[-1]

    def get_head_position(self):
        """Метод обновления позиции головы змейки."""
        head = (self.positions[0][0] // GRID_SIZE,
                self.positions[0][1] // GRID_SIZE)
        new_head = (((head[0] + self.direction[0]) * GRID_SIZE) % SCREEN_WIDTH,
                    ((head[1] + self.direction[1])
                     * GRID_SIZE) % SCREEN_HEIGHT)
        return new_head

    def reset(self):
        """Метод сброса змейки в начальное состояние."""
        screen.fill((BOARD_BACKGROUND_COLOR))
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        sequence = (RIGHT, LEFT, UP, DOWN)
        self.direction = choice(sequence)
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод отрисовки змейки и затирания последнего сегмента."""
        for position in self.positions[0:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)