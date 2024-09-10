import pygame


def check(sp, sign):
    zeroes = 0
    for row in sp:
        zeroes += row.count(0)
        if row.count(sign) == 3:
            return sign

    for col in range(3):
        if sp[0][col] == sign and sp[1][col] == sign and sp[2][col] == sign:
            return sign
    if sp[0][0] == sign and sp[1][1] == sign and sp[2][2] == sign:
        return sign
    if sp[0][2] == sign and sp[1][1] == sign and sp[2][0] == sign:
        return sign

    if zeroes == 0:
        return 'Draw'

    return False


pygame.init()

size_block = 100
margin = 15
width = height = size_block * 3 + margin * 4

sc = pygame.display.set_mode((width, height))

sp = [[0] * 3 for i in range(3)]

query = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_m, y_m = pygame.mouse.get_pos()
            col = x_m // (size_block + margin)
            row = y_m // (size_block + margin)
            if sp[row][col] == 0:
                if query % 2 == 0:
                    sp[row][col] = 'x'
                else:
                    sp[row][col] = 'o'
                query += 1
    for row in range(3):
        for col in range(3):
            if sp[row][col] == 'x':
                color = (100, 0, 0)
            elif sp[row][col] == 'o':
                color = (0, 100, 0)
            else:
                color = (100, 100, 100)
            x = col * size_block + (col + 1) * margin  # нахождение координаты x
            y = row * size_block + (row + 1) * margin  # нахождение координаты y
            pygame.draw.rect(sc, 'white', (x, y, size_block, size_block))  # отрисовка блоков
            if color == (100, 0, 0):
                pygame.draw.line(sc, (100, 0, 10), (x + 10, y + 10), (x + size_block - 10, y + size_block - 10), 3)
                pygame.draw.line(sc, (100, 0, 0), (x + size_block - 10, y + 10), (x + 10, y + size_block - 10), 3)
            elif color == (0, 100, 0):
                pygame.draw.circle(sc, (0, 100, 0), (x + size_block // 2, y + size_block // 2), size_block // 2 - 3, 3)

    if (query-1) % 2 == 0:
        game_over = check(sp, 'x')
    else:
        game_over = check(sp, 'o')

    if game_over:
        sc.fill('black')
        font = pygame.font.SysFont('Arial', 70)
        text = font.render(game_over, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_x = sc.get_width() / 2 - text_rect.width / 2
        text_y = sc.get_height() / 2 - text_rect.height / 2
        sc.blit(text, [text_x, text_y])

    pygame.display.update()
