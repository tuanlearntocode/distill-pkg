from pathlib import Path
from scipy.interpolate import make_interp_spline, CubicSpline, interp1d
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Distill():
    def __init__(self, xf, xw, xd, subtances):
        self.xf = xf
        self.yf = None
        self.yf_vapor = None
        self.xw = xw
        self.yw = xw
        self.xd = xd
        self.yd = xd
        self.R_min = None
        self.R = None
        self.subtances = subtances          # your composition e.g: 'ethanol-water'

        # liquid-vapor balance
        parent = Path(__file__).resolve().parent
        df = pd.read_excel(str(parent)+'\data.xlsx',
                           sheet_name=self.subtances)
        self.liquid = df['x'].to_numpy()
        self.vapor = df['y'].to_numpy()
        self.temp = df['t'].to_numpy()

        # stages
        self.t_stage = None

    def cubic(self, x, y):
        f = CubicSpline(x, y, bc_type='natural')
        return f

    def interpolation(self, x, y):
        f = interp1d(x, y)
        return f

    def initial_calulate(self):             # calculate needed information
        f = self.cubic(self.liquid, self.vapor)
        self.yf_vapor = np.around(f(self.xf), 3)
        self.R_min = np.around(
            (self.xd - self.yf_vapor) / (self.yf_vapor - self.xf), 3)
        self.R = np.around(1.3*self.R_min + 0.3, 3)
        self.yf = np.around(self.R/(self.R+1)*self.xf + self.xd/(self.R+1), 3)

        # line recitify and striping
        recitify = np.array([[self.xd, self.xf], [self.yd, self.yf]])
        stripping = np.array([[self.xw, self.xf], [self.yw, self.yf]])

        # stair line
        f_recitify = self.interpolation(recitify[0, :], recitify[1, :])
        f_stripping = self.interpolation(stripping[0, :], stripping[1, :])
        f1 = self.cubic(self.vapor, self.liquid)

        y1 = self.yd
        stair_x = np.array([self.xd])
        stair_y = np.array([])

        # main loop
        while True:
            stair_y = np.append(stair_y, [y1, y1])
            x1 = f1(y1)
            stair_x = np.append(stair_x, [x1, x1])
            if x1 >= self.xf:
                y1 = f_recitify(x1)
            elif x1 < self.xf and x1 > self.xw:
                y1 = f_stripping(x1)
            elif x1 < self.xw:
                stair_y = np.append(stair_y, x1)
                break

        self.t_stage = (stair_x.size - 1) / 2

    def balance_line(self):
        coor = np.array([self.liquid, self.vapor])
        return coor

    def draw_yx(self):
        # y = x line
        xo = np.array([0, 1])
        yo = np.array([0, 1])

        # balance line
        coor = self.balance_line()
        x = coor[0, :]
        y = coor[1, :]
        X_Y_Spline = make_interp_spline(x, y)
        X_ = np.linspace(x.min(), x.max(), 500)
        Y_ = X_Y_Spline(X_)

        # line recitify and striping
        recitify = np.array([[self.xd, self.xf], [self.yd, self.yf]])
        stripping = np.array([[self.xw, self.xf], [self.yw, self.yf]])

        # stair line
        f_recitify = self.interpolation(recitify[0, :], recitify[1, :])
        f_stripping = self.interpolation(stripping[0, :], stripping[1, :])
        f1 = self.cubic(self.vapor, self.liquid)

        y1 = self.yd
        stair_x = np.array([self.xd])
        stair_y = np.array([])

        # main loop
        while True:
            stair_y = np.append(stair_y, [y1, y1])
            x1 = f1(y1)
            stair_x = np.append(stair_x, [x1, x1])
            if x1 >= self.xf:
                y1 = f_recitify(x1)
            elif x1 < self.xf and x1 > self.xw:
                y1 = f_stripping(x1)
            elif x1 < self.xw:
                stair_y = np.append(stair_y, x1)
                break

        # draw
        # Must put on top to take effect to window size
        plt.figure(figsize=(5, 5))
        plt.plot(xo, yo, linewidth=1.0, color='orange')
        plt.plot(X_, Y_, linewidth=1.0, color=(0, 0, 1, 0.7))
        plt.plot(recitify[0, :], recitify[1, :],
                 linewidth=1.0, color=(1, 1, 0), zorder=0)
        plt.plot(stripping[0, :], stripping[1, :],
                 linewidth=1.0, color=(0, 1, 0), zorder=0)
        plt.plot(stair_x, stair_y, linewidth=1.0,
                 color=(0, 0, 0, 0.8), zorder=0)
        plt.xlim(0, 1)
        plt.ylim(0, 1)

        plt.show()

    def draw_tx(self):
        plt.figure(figsize=(5, 5))
        # T-x line

        x = self.liquid
        y = self.temp
        txlSpline = make_interp_spline(x, y)
        X_1 = np.linspace(x.min(), x.max(), 500)
        Y_1 = txlSpline(X_1)
        plt.plot(X_1, Y_1, linewidth=1.0, color=(0, 0, 1, 0.7))

        x = self.vapor
        y = self.temp
        tylSpline = make_interp_spline(x, y)
        X_2 = np.linspace(x.min(), x.max(), 500)
        Y_2 = tylSpline(X_2)
        plt.plot(X_2, Y_2, linewidth=1.0, color=(0, 1, 0, 0.7))

        plt.show()
