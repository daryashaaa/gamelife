import unittest
from GameLife import  GameLife

class TestGame(unittest.TestCase):

    def test_clear(self):
        game = GameLife()
        nolife = game.grids
        for r in range(game.num_rows):
            for c in range(game.num_cols):
                nolife[1][r][c] = 0
        game.set_grid(0, game.active_grid)
        self.assertEqual(nolife, game.grids)

    def test_set(self):
        game = GameLife()
        game.set_grid(0, game.active_grid)
        game.grids[game.active_grid][0][0]=1
        self.assertEqual(1, game.grids[game.active_grid][0][0])

    def test_generation(self):
        game = GameLife()
        game.set_grid(0, game.active_grid)
        game.grids[game.active_grid][0][0] = 1
        game.update_generation()
        self.assertEqual(0, game.grids[game.active_grid][0][0])

    def test_generation_three_cell(self):
        game = GameLife()
        game.set_grid(0, game.active_grid)
        game.grids[game.active_grid][0][0] = 1
        game.grids[game.active_grid][1][0] = 1
        game.grids[game.active_grid][2][0] = 1
        game.update_generation()
        self.assertEqual(0, game.grids[game.active_grid][0][0])
        self.assertEqual(1, game.grids[game.active_grid][1][0])
        self.assertEqual(1, game.grids[game.active_grid][1][1])

if __name__ == '__main__':
    unittest.main()