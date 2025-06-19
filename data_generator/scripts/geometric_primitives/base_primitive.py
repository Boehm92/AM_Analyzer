import madcad as mdc
import numpy as np

class Manifold:
    def __init__(self):
        self.length = 70
        self.height = 70
        self.depth = 60
        self.manifold_dimensions = mdc.vec3(self.length, self.depth, self.height)

    def transform(self):
        return mdc.brick(mdc.vec3(0, 0, 0), self.manifold_dimensions)
