
from PIL import Image
from math import sin, cos, pi

arena = Image.open("res/arena2.png")
exa0 = Image.open("res/0.png")
exa1 = Image.open("res/1.png")
exa2 = Image.open("res/2.png")
exa3 = Image.open("res/3.png")
boss = Image.open("res/boss.png")

def midpoint(image):
    return (image.size[0]/2, image.size[1]/2)

def add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def sub(t1, t2):
    return add(t1, mul(t2, -1))

def mul(t, s):
    return (t[0] * s, t[1] * s)

def advance(start, angle):
    amt = int(exa0.size[0]/2*5/4)
    x = amt * cos(angle)
    y = -amt * sin(angle)
    return add(start, (x, y))

def paste_mid(base, layer, coords):
    r = add(sub(midpoint(base), midpoint(layer)), coords)
    r = (int(r[0]), int(r[1]))
    base.paste(layer, r, mask=layer)
    
# get positions around boss hitbox
def boss_start(angle):
    b = midpoint(boss)
    return (b[0]*cos(angle), -b[1]*sin(angle))

# advances one line of explosions x times
def exaflare_advance(image, start, angle, x):
    if x >= 1:
        next = advance(start, angle)
        paste_mid(image, exa1, next)
        if x >= 2:
            next = advance(next, angle)
            paste_mid(image, exa2, next)
            if x >= 3:
                next = advance(next, angle)
                paste_mid(image, exa3, next)

# creates 3 lines of explosions that advance x times
def exaflare_line(image, start, angles, x):
    paste_mid(image, exa0, start)
    exaflare_advance(image, start, angles[0], x)
    exaflare_advance(image, start, angles[1], x)
    exaflare_advance(image, start, angles[2], x)
    
# creates 3 "exaflares" at points R, L, T that advance x times
def create_exaflare(R, RA, L, LA, T, TA, x):
    image = arena.copy()
    paste_mid(image, boss, (0, 0))
    exaflare_line(image, R, RA, x)
    exaflare_line(image, L, LA, x)
    exaflare_line(image, T, TA, x)
    return image

# sword start points
R = boss_start(pi/6)
L = boss_start(pi*5/6)
T = boss_start(pi*3/2)

# sword angles
RA = (0, pi*3/2, pi/2)
LA = (pi/4, pi*7/4, pi*5/4)
TA = (pi/4, pi*3/4, pi*5/4)

for i in range(4):
    create_exaflare(R, RA, L, LA, T, TA, i).save("result_%s.png" % i)