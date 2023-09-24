class Polynomial:
    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        self.a: float = a
        self.b: float = b
        self.c: float = c
        self.d: float = d

    def surface_points(self) -> list:
        xs = []
        ys = []
        xp = []
        yp = []
        xs[0] = x8
        ys[0] = y8
        xp[0] = x8
        yp[0] = y8
        dxp = (x4-x9)/9
        dxs = (x3-x8)/9
        for i in range(1, 10):
            xp[i] = xp[i-1] + dxp
            yp[i] = y9 - np.sqrt(self.Rle**2 - (xp[i] - x9)**2)
            xs[i] = xs[i-1] + dxs
            ys[i] = y9 + np.sqrt(self.Rle**2 - (xs[i] - x9)**2)
        for i in range(10, 30):
            xp[i] = xp[i-1] + dxp
            #tu trzeba dalej dopisać
        return xs, ys, xp, yp