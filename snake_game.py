import pygame as pg
import time
import random

pg.init()
width, height = 600, 400
sc = pg.display.set_mode((width,height))
pg.display.set_caption('Snake Game')

size = 20
fps = 10

clock = pg.time.Clock()

font_style = pg.font.SysFont(None, 40)

def message(msg,color):
    mesg = font_style.render(msg, True, color)
    sc.blit(mesg, [width / 6, height / 2])

def snake(snake_block, snake_list):
    for x in snake_list:
        pg.draw.rect(sc,'yellow',(x[0],x[1],snake_block, snake_block))

def gameLoop():

    x1,y1 = width / 2, height / 2
    x_move, y_move = 0,0

    game_close = False
    game_over = False

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(0,width - size) / size) * size
    foody = round(random.randrange(0,height - size) / size) * size
    while not game_over:

        while game_close == True:
            sc.fill('black')
            message('You lost, press q-quit or c-reset', 'red')
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pg.K_c:
                        gameLoop()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
                game_close = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    gameLoop()
                if event.key == pg.K_q:
                    game_over = True
                    game_close = False
                elif event.key == pg.K_LEFT:
                    x_move = -size
                    y_move = 0
                elif event.key == pg.K_RIGHT:
                    x_move = size
                    y_move = 0
                elif event.key == pg.K_UP:
                    x_move = 0
                    y_move = -size
                elif event.key == pg.K_DOWN:
                    x_move = 0
                    y_move = size

        if x1 >= width or x1 <= -10 or y1 >= height or y1 <= -10:
            game_close = True

        sc.fill('green')
        x1 += x_move
        y1 += y_move
        pg.draw.rect(sc, 'red', (foodx, foody, size, size))
        [pg.draw.rect(sc,(100, 100, 100),(i,j,size,size),1) for i in range(0,width,size) for j in range(0,height,size)]
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for i in snake_list[:-1]:
            if i == snake_head:
                game_close = True

        snake(size,snake_list)

        pg.display.update()
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - size) / 20) * 20
            foody = round(random.randrange(0, height - size) / 20) * 20
            snake_length += 1

        clock.tick(fps)
    pg.quit()
    quit()

gameLoop()