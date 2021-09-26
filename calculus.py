import math as m

ans = []

for x0 in range(-20, 20):
    for y0 in range(-20, 20):
        x = x0 / 2
        y = y0 / 2

        u = m.e ** ((x + y) / 2)
        g = (x * x - 4 * (y * y)) ** 3

        u1 = (x + y) / 2 * (m.e ** ((x + y) / 2))
        g1 = 3 * ((x * x - 4 * y * y) ** 2)

        f1 = u * g1 + u1 * g
        f = u * g

        if not f1:
            print('YES science', f, x, y)