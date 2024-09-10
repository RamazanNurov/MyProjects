import pygame as pg
from math import *
width, height = 800, 600
half_width, half_height = width//2, height//2
player_pos = (half_width // 4, half_height // 2 - 25)
player_angle = 0
player_speed = 2
fps = 60
clock = pg.time.Clock()
tile = 50

fov = pi/3
half_fov = fov/2
num_rays = 200
max_depth = 100
delta_angle = fov / num_rays
dist = num_rays / (2*tan(half_fov))
proj_coeff = 3 * dist * tile
scale = width // num_rays

texture_width = 1200
texture_height = 1200
texture_scale = texture_width // tile
pg.init()


text_map = [
    '111111111111',
    '1.....2....1',
    '1.22.....2.1',
    '1..........1',
    '1.22.......1',
    '1.2......2.1',
    '1.....2....1',
    '111111111111'
]

world_map = {}
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == '1':
            world_map[(i * tile, j * tile)] = '1'
        if char == '2':
            world_map[(i * tile, j * tile)] = '2'


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle

    @property
    def pos(self):
        return self.x, self.y

    def movement(self):
        sin_a = sin(self.angle)
        cos_a = cos(self.angle)

        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.x += player_speed * cos_a
            self.y += player_speed * sin_a
        if keys[pg.K_s]:
            self.x += -player_speed * cos_a
            self.y += -player_speed * sin_a
        if keys[pg.K_a]:
            self.x += player_speed * sin_a
            self.y += -player_speed * cos_a
        if keys[pg.K_d]:
            self.x += -player_speed * sin_a
            self.y += player_speed * cos_a
        if keys[pg.K_LEFT]:
            self.angle -= 0.05
        if keys[pg.K_RIGHT]:
            self.angle += 0.05


def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile


def ray_casting(sc, player_pos, player_angle, textures):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - half_fov
    for ray in range(num_rays):
        sin_a = sin(cur_angle)
        cos_a = cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # verticals
        x, dx = (xm + tile, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, width, tile):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * tile

        # horizontals
        y, dy = (ym + tile, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, height, tile):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * tile

        # projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % tile
        depth *= cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = min(int(proj_coeff / depth), 2 * height)

        wall_column = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
        wall_column = pg.transform.scale(wall_column, (scale, proj_height))
        sc.blit(wall_column, (ray * scale, half_height - proj_height // 2))

        cur_angle += delta_angle
class Drawing:

    def __init__(self, win):
        self.sc = win
        self.font = pg.font.SysFont('Arial', 25, bold=True)
        self.textures = {'1': pg.image.load('images/wall1.png').convert(),
                         '2': pg.image.load('images/wall2.png').convert(),
                         'S': pg.image.load('images/sky3.png').convert()
                         }

    def background(self, angle):
        sky_offset = -10 * degrees(angle) % width
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset - width, 0))
        self.sc.blit(self.textures['S'], (sky_offset + width, 0))
        pg.draw.rect(self.sc, 'darkgreen', (0, half_height, width, half_width))

    def world(self, play_pos, play_angle):
        ray_casting(self.sc, play_pos, play_angle, self.textures)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, 'green')
        self.sc.blit(render, (5, 5))


sc = pg.display.set_mode((width, height))
player = Player()
drawing = Drawing(sc)
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    sc.fill('black')
    player.movement()
    drawing.background(player.angle)
    drawing.world(player.pos, player.angle)
    drawing.fps(clock)
    pg.display.flip()
    clock.tick(fps)

pg.quit()
