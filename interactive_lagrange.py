import numpy as np
import matplotlib, sys, itertools
from matplotlib import pyplot as plt


class Lagrange:
    """
    A class for the Langrange interpolation functions -- essentially code from class hehe
    """
    def w_factory(self, xs, i):
        denominator = np.prod([xs[i] - a for j, a in enumerate(xs) if i != j])
        def w(x):
            numerator = np.prod([x - a for j, a in enumerate(xs) if i != j])
            return numerator / denominator
        return w

    def generate_polynomial(self, xs, ys): 
        def lagrange(x):
            ws = [self.w_factory(xs, i) for i, _ in enumerate(xs)]
            return sum(y * ws[i](x) for i, y in enumerate(ys))
     
        return lagrange

class Plotter:
    """
    Where all the plotting/configuration happens
    """
    
    def __init__(self):
        self.fig = plt.figure()
        self.axis_points = 100
        self.set_view_lim(100, 100)

        self.xs = np.array([])
        self.ys = np.array([])

        self.lagrange = Lagrange()

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_press)

        self.colors = itertools.cycle(['r', 'g', 'b', 'c', 'm', 'y'])

        plt.show()

    def set_view_lim(self, xlim, ylim):
        """
        Changes the view limit of the plot and redraws
        """
        self.xlim = xlim
        self.ylim = ylim
        self.revert_view_lim()
        self.x_axis = np.linspace(0, self.xlim, self.axis_points)
        self.fig.canvas.draw()

    def revert_view_lim(self):
        """
        Reverts view limit after plotting changes it
        """
        plt.xlim(0, self.xlim, self.axis_points)
        plt.ylim(0, self.ylim, self.axis_points)

    def zoom_in(self):
        """
        Decreases the x/y view limit -- zooming out
        """
        self.set_view_lim(self.xlim - 50, self.ylim - 50)
        self.redraw()

    def zoom_out(self):
        """
        Increases the x/y view limit -- zooming in
        """
        self.set_view_lim(self.xlim + 50, self.ylim + 50)
        self.redraw()

    def clear_plot(self):
        """
        Erases everything on the plot
        """
        self.xs = np.array([])
        self.ys = np.array([])
        plt.clf()
        self.revert_view_lim()
        plt.plot(0, 0, 'o')
        self.redraw()

    def plot_points(self):
        """
        Plots the data points
        """
        plt.plot(self.xs, self.ys, 'o', color=next(self.colors))

    def plot_lagrange(self):
        """
        Plots the interpolation polynomial
        """
        lg = self.lagrange.generate_polynomial(self.xs, self.ys)
        plt.plot(self.x_axis, [lg(x) for x in self.x_axis])

    def redraw(self):
        """
        Redraws the canvas for when changes occur
        """
        self.fig.canvas.draw()

    def on_press(self, event):
        """
        On key press event
        """
        sys.stdout.flush()

        if event.key == 'c':
            self.clear_plot()
        elif event.key == '-':
            self.zoom_out()
        elif event.key == '=':
            self.zoom_in()

        self.redraw()

    def on_click(self, event):
        """
        On mouse click event
        """
        if event.xdata in self.xs and event.ydata in self.ys or event.inaxes == None:
            return

        plt.clf()
        self.revert_view_lim()
        self.xs = np.append(self.xs, event.xdata)
        self.ys = np.append(self.ys, event.ydata)
        self.plot_lagrange()
        self.plot_points()
        self.redraw()

def main():
    plot = Plotter()

if __name__ == "__main__":
    main()
