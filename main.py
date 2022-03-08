import pygame
import random
import colors

pygame.init()
pygame.mixer.init()

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Snakes Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    snake_size = 11
    food_size = 8.5
    fps = 60
    while not exit_game:
        if game_over:
            gameWindow.fill(colors.white)
            with open('./data/lastscore', 'w') as lsw:
                lsw.write(f'{score}')
            with open('./data/highscore', 'r') as hsr:
                if score>int(hsr.read()):
                    with open('./data/highscore', 'w') as hsw:
                        hsw.write(f'{score}')
            text_screen("Game Over! Press Enter To Continue", colors.red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = 3.6
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -3.6
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -3.6
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = 3.6
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if  (snake_x - food_x)<8 and abs(snake_y - food_y)<8:
                score +=1
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length +=5
                pygame.mixer.music.load('./sound/eaten.wav')
                pygame.mixer.music.play()


            gameWindow.fill(colors.black)
            text_screen(f'Score: {score}', colors.blue, 5, 5)
            with open('./data/lastscore', 'r') as lsr:
                text_screen(f'Last game score: {lsr.read()}', colors.blue, 200, 5)
            with open('./data/highscore', 'r') as hsr:
                text_screen(f'Highscore: {hsr.read()}', colors.blue, 600, 5)

            
            pygame.draw.rect(gameWindow, colors.red, [food_x, food_y, food_size, food_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
            plot_snake(gameWindow, colors.green, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
gameloop()

