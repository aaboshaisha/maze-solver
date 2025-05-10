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
    def __init__(self, x1, y1, x2, y2, window,
                 has_left_wall=True, has_right_wall=True,
                 has_top_wall=True, has_bottom_wall=True):
        
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        
        # its top left corner
        self.x1, self.y1 = x1, y1

        # bot right
        self.x2, self.y2 = x2, y2
        
        self.window = window # access window to draw itself

    def draw(self):
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


def main():
    win = Window(800, 600)
    cell = Cell(50, 50, 100, 100, win)
    print(cell.x1, cell.y1, cell.x2, cell.y2)
    cell.draw()
    win.wait_for_close()

main()
