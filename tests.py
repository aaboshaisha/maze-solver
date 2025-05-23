import unittest

from main import Window, Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        win = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(len(m1.cells),num_cols,)
        self.assertEqual(len(m1.cells[0]),num_rows,)

        nrows = 3
        ncols = 4
        m2 = Maze(200,200, nrows, ncols, 25, 25, win)
        self.assertEqual(len(m2.cells), ncols)
        self.assertEqual(len(m2.cells[0]), nrows)

    def test_break_walls(self):
        win = Window(800, 600)
        num_cols = 5
        num_rows = 5
        m1 = Maze(200, 200, num_rows, num_cols, 50, 50, win)
        self.assertEqual(m1.cells[0][0].has_top_wall,False,)
        self.assertEqual(m1.cells[num_cols - 1][num_rows - 1].has_bottom_wall,False,)


if __name__ == '__main__':
    unittest.main()
