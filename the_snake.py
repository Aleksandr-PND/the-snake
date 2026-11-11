import pygame

from gameparts import Apple, BadApple, Snake, clock, screen
from gameparts import BOARD_BACKGROUND_COLOR, DOWN, LEFT, RIGHT, UP, SPEED


# Заголовок окна игрового поля:
pygame.display.set_caption(f'Змейка | Максимальная длина змейки: {1}')


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    bad_apple = BadApple()
    snake = Snake()
    positions_coincide = True
    while positions_coincide:
        if snake.position == bad_apple.position:
            bad_apple = BadApple()
        else:
            break
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            if snake.length > snake.max_length:
                snake.max_length = snake.length
                pygame.display.set_caption('Змейка | Максимальная длина '
                                           f'змейки: {snake.max_length}')
            apple = Apple()
            bad_apple = BadApple()
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
        if snake.positions[0] == bad_apple.position and snake.length < 2:
            snake.reset()
        elif snake.positions[0] == bad_apple.position:
            snake.length -= 1
            snake.take_bad_apple = True
            bad_apple = BadApple()
        screen.fill(BOARD_BACKGROUND_COLOR)
        bad_apple.draw()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
