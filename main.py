import tkinter as tk
import time
import random

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
    def __init__(self, win=None, has_left_wall=True, has_right_wall=True,
                 has_top_wall=True, has_bottom_wall=True):
        
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        
        self.window = win # access window to draw itself
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        # x1, y1 top left corner, x2, y2 bot right
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        
        tl = Point(self.x1, self.y1)
        tr = Point(self.x2, self.y1)
        bl = Point(self.x1, self.y2)
        br = Point(self.x2, self.y2)

        colors = ['white', 'black']
        self.window.draw_line(Line(tl, bl), colors[self.has_left_wall])
        self.window.draw_line(Line(tr, br), colors[self.has_right_wall])
        self.window.draw_line(Line(tl, tr), colors[self.has_top_wall])
        self.window.draw_line(Line(bl, br), colors[self.has_bottom_wall])



    def draw_move(self, to_cell, undo=False):
        def get_center_point(cell):
            x1, y1, x2, y2 = cell.x1, cell.y1, cell.x2, cell.y2
            cx = x1 + abs(x2 - x1)/2
            cy = y1 + abs(y2 - y1)/2
            return Point(cx, cy)

        c1 = get_center_point(self)
        c2 = get_center_point(to_cell)

        fill_color = 'red'
        if undo:
            fill_color = 'gray'
        self.window.draw_line(Line(c1, c2), fill_color)


class Maze:
    def __init__(self, x1, y1, nrows, ncols, cell_size_x, cell_size_y, win, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.nrows = nrows
        self.ncols = ncols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

        if seed is not None:
            random.seed(seed)

        
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
        y2 = y1 + self.cell_size_y
        cell = self.cells[i][j]
        cell.draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self.win is None:
            return 
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        i, j = self.ncols - 1, self.nrows - 1
        self.cells[i][j].has_bottom_wall = False
        self._draw_cell(i, j)
        

    def _get_adjacent(self, i, j, maxc, maxr, cells):
        potential_neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]    
        valid = [(ni, nj) for ni, nj in potential_neighbors 
                 if 0 <= ni < maxc and 0 <= nj < maxr and cells[ni][nj].visited == False]
        return valid
    
    def _break_inbetween(self, i1, j1, i2, j2):
        src = self.cells[i1][j1]
        dst = self.cells[i2][j2]
        
        # If src is to the left of dst
        if i1 < i2:
            src.has_right_wall = False
            dst.has_left_wall = False
        # If src is to the right of dst
        elif i1 > i2:
            src.has_left_wall = False
            dst.has_right_wall = False
        # If src is above dst
        elif j1 < j2:
            src.has_bottom_wall = False
            dst.has_top_wall = False
        # If src is below dst
        else:
            src.has_top_wall = False
            dst.has_bottom_wall = False

        # redraw after walls removed
        self._draw_cell(i1, j1)
        self._draw_cell(i2, j2)
        
    
    def _break_walls_r(self, i, j):
        self.cells[i][j].visited = True
        to_visit = self._get_adjacent(i, j, self.ncols, self.nrows, self.cells)
        while to_visit != []:
            ni, nj = random.choice(to_visit)
            self._break_inbetween(i, j, ni, nj)
            self._break_walls_r(ni, nj)
            to_visit = self._get_adjacent(i, j, self.ncols, self.nrows, self.cells)
            if len(to_visit) == 0:
                self._draw_cell(i, j)

    def _reset_cells_visited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False



def main():
    win = Window(800, 600)
    ncols = 3
    nrows = 4
    m1 = Maze(200, 200, nrows, ncols, 50, 50, win)
    win.wait_for_close()

main()
