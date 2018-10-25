import numpy as np
import sys
import functools
# import pylab
# import matp
from PIL import Image
import scipy.signal as sig


class GameOfLife:

    def __init__(self, N=100, T=200, img="src.PNG"):
        self.N = N
        self.T = T  # The maximum number of generations

        self.grid = np.zeros(N * N, dtype='i').reshape(N, N)

        # A lookup table for the state a cell in the next generation givin its state and the number of neighbors
        self.rule = {(0, 0): 0, (0, 1): 0, (0, 2): 0, (0, 3): 1, (0, 4): 0, (0, 5): 0, (0, 6): 0, (0, 7): 0, (0, 8): 0, (1, 0): 0, (1, 1): 0, (1, 2): 1, (1, 3): 1, (1, 4): 0, (1, 5): 0, (1, 6): 0, (1, 7): 0, (1, 8): 0}
        self.rule2 = np.zeros((2, 9), dtype='i')
        for i in self.rule.keys():
            self.rule2[i[0], i[1]] = self.rule[i]

        # The GoL convolution kernel
        self.conv = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype='i')

        with Image.open(img).resize((self.N, self.N)) as im:
            # Start by detecting the palette
            # self.pal = im.convert('P', palette=Image.ADAPTIVE, colors=2).getpalette()[0:6]
            self.pal = im.getpalette()[0:6]
            # if im.getpixel((0, 0)) != tuple(self.pal[0:3]):
                # self.pal[0:3], self.pal[3:6] = self.pal[3:6], self.pal[0:3]
            if im.getpixel((0, 0)) != 0:
                im = im.remap_palette([1, 0])

            print(str(self.pal))

            for i in range(0, self.N):
                for j in range(0, self.N):
                    self.grid[j][i] = im.getpixel((i, j))
                    # if(im.getpixel((i, j)) == tuple(self.pal[3:6])):
                    #     self.grid[j][i] = 1
                    # else:
                    #     self.grid[j][i] = 0
            print(self.grid[50])

    @functools.lru_cache(maxsize=None)
    def snippet(self, g, n):
        return [self.rule[(g[i], n[i])] for i in range(10)]

    def play(self):
        """ Play Conway's Game of Life. """
        for t in range(self.T):  # Evolve!
            neighbors = sig.convolve2d(self.grid, self.conv, mode="same", boundary="wrap")
            self.grid[...] = self.rule2[self.grid, neighbors]
            # self.grid = it.operands[2]

            # Output the new configuration
            im = Image.fromarray((self.grid * 255).astype(np.uint8))
            # im.putpalette(pal)
            # im.save(f"{t:03}" + ".png", "PNG")
            imP = im.convert('P', palette=self.pal, colors=2)  # .remap_palette([1, 0])
            imP.putpalette(self.pal)
            imP.save(f"{t:03}" + ".Png", "PNG")


if(__name__ == "__main__"):
    game = GameOfLife(N=700, T=200, img=sys.argv[1])
    game.play()
