from random import choice, randint
import pygame

from gameparts import (APPLE_COLOR, BAD_APPLE_COLOR, BOARD_BACKGROUND_COLOR,
                       BORDER_COLOR, DOWN, GRID_HEIGHT, GRID_SIZE, GRID_WIDTH,
                       LEFT, RIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, SNAKE_COLOR,
                       UP)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

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

    def __init__(self, bitten: bool = False) -> None:
        super().__init__()
        self.position = self.randomize_position()
        self.bitten = bitten
        self.body_color = BAD_APPLE_COLOR if bitten else APPLE_COLOR

    def randomize_position(self):
        """Метод, генерирующий позицию яблока."""
        self.positionX = (randint(0, GRID_WIDTH - 1)) * GRID_SIZE
        self.positionY = (randint(0, GRID_HEIGHT - 1)) * GRID_SIZE
        return (self.positionX, self.positionY)

    def _draw_apple(self):
        """Метод, отрисовки яблока."""
        x, y = self.position
        cx, cy = x + GRID_SIZE // 2, y + GRID_SIZE // 2
        r = GRID_SIZE // 2 - 2

        # Тело яблока — красный круг
        pygame.draw.circle(screen, self.body_color, (cx, cy + 2), r)
        pygame.draw.circle(screen, BORDER_COLOR, (cx, cy + 2), r, 1)

        # Черешок — коричневая линия
        pygame.draw.line(screen, (101, 67, 33), (cx, cy - r + 2),
                         (cx, cy - r - 3), 2)

        # Листик — зелёный эллипс (или маленький круг)
        pygame.draw.ellipse(
            screen, (0, 180, 0),
            pygame.Rect(cx + 1, cy - r - 2, 6, 4)
        )

    def draw(self):
        """Метод, отрисовки  плохого яблока."""
        self._draw_apple()
        if self.bitten:
            x, y = self.position
            cx, cy = x + GRID_SIZE // 2, y + GRID_SIZE // 2
            # r = GRID_SIZE // 2 - 2
            # bite_center = (cx + r - 2, cy + 2)
            for dx, dy, r in [(-6, 0, 4), (2, -3, 3), (3, 3, 3)]:
                c = (cx + r + dx, cy + 2 + dy)
                pygame.draw.circle(screen, BOARD_BACKGROUND_COLOR, c, 6)
                pygame.draw.circle(screen, BORDER_COLOR, c, 6, 1)


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
        self.take_bad_apple = False
        self.max_length = 1

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
        if self.take_bad_apple:
            del self.positions[-2:]
            self.last = self.positions[-1]
            self.take_bad_apple = False
        elif len(self.positions) > self.length:
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
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод отрисовки змейки и затирания последнего сегмента."""
        for position in self.positions[0:]:
            center = (position[0] + GRID_SIZE // 2,
                      position[1] + GRID_SIZE // 2)
            pygame.draw.circle(screen, self.body_color, center,
                               GRID_SIZE // 2 - 1)
            pygame.draw.circle(screen, BORDER_COLOR, center,
                               GRID_SIZE // 2 - 1, 1)

        # Отрисовка головы змейки
        x, y = self.positions[0]
        # определяем центр клетки головы
        cx, cy = x + GRID_SIZE // 2, y + GRID_SIZE // 2
        # Радиус -1 что бы не выходил за границы
        r = GRID_SIZE // 2 - 1
        pygame.draw.circle(screen, self.body_color, (cx, cy), r)
        pygame.draw.circle(screen, BORDER_COLOR, (cx, cy), r, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
