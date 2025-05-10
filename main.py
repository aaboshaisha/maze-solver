import tkinter as tk
import time

class Point:
    def __init__(self, x=0, y=0):
        self.x = x # left
        self.y = y # top


class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def draw(self, canvas, fill_color):
        canvas.create_line(self.a.x, self.a.y, self.b.x, self.b.y, fill=fill_color, width=2)


class Window:
    def __init__(self, width, height):
        self.window = tk.Tk()
        self.window.title('Maze-Solver')
        self.canvas = tk.Canvas(self.window, bg='white', width=width, height=height)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.running = False
        self.window.protocol('WM_DELETE_WINDOW', self.close)

    def redraw(self):
        self.window.update_idletasks()
        self.window.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        print('Window closed..')

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color='black'):
        line.draw(self.canvas, fill_color=fill_color)


class Cell:
    def __init__(self, win, has_left_wall=True, has_right_wall=True,
                 has_top_wall=True, has_bottom_wall=True):
        
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        
        self.window = win # access window to draw itself

    def draw(self, x1, y1, x2, y2):
        # x1, y1 top left corner, x2, y2 bot right
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        
        tl = Point(self.x1, self.y1)
        tr = Point(self.x2, self.y1)
        bl = Point(self.x1, self.y2)
        br = Point(self.x2, self.y2)

        if self.has_left_wall:
            self.window.draw_line(Line(tl, bl))
        if self.has_right_wall:
            self.window.draw_line(Line(tr, br))
        if self.has_top_wall:
            self.window.draw_line(Line(tl, tr))
        if self.has_bottom_wall:
            self.window.draw_line(Line(bl, br))


    def draw_move(self, to_cell, undo=False):
        def get_center_point(cell):
            x1, y1, x2, y2 = cell.x1, cell.y1, cell.x2, cell.y2
            cx = x1 + (x2 - x1)/2
            cy = y2 + (y1 - y2)/2
            return Point(cx, cy)

        c1 = get_center_point(self)
        c2 = get_center_point(to_cell)

        fill_color = 'red'
        if undo:
            fill_color = 'gray'
        self.window.draw_line(Line(c1, c2), fill_color)

class Maze:
    def __init__(self, x1, y1, nrows, ncols, cell_size_x, cell_size_y, win):
        self.x1 = x1
        self.y1 = y1
        self.nrows = nrows
        self.ncols = ncols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._create_cells()
        
    def _create_cells(self):
        self.cells = []
        for i in range(self.ncols):
            row = [Cell(self.win) for j in range(self.nrows)]
            self.cells.append(row)

        for i in range(self.ncols):
            for j in range(self.nrows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 - self.cell_size_y
        cell = self.cells[i][j]
        cell.draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self.win is None:
            return 
        self.win.redraw()
        time.sleep(0.05)


def main():
    pass

main()
