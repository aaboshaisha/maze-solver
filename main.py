import tkinter as tk

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


def main():
    win = Window(800, 600)

    c1 = Cell(win)
    c1.has_right_wall = False
    c1.draw(50, 50, 100, 100)

    c2 = Cell(win)
    c2.has_left_wall = False
    c2.has_bottom_wall = False
    c2.draw(100, 50, 150, 100)

    c1.draw_move(c2)

    c3 = Cell(win)
    c3.has_top_wall = False
    c3.has_right_wall = False
    c3.draw(100, 100, 150, 150)

    c2.draw_move(c3)

    c4 = Cell(win)
    c4.has_left_wall = False
    c4.draw(150, 100, 200, 150)

    c3.draw_move(c4, True)

    win.wait_for_close()

main()
