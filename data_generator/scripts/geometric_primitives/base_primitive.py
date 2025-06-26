import madcad as mdc
import numpy as np

class Manifold:
    def __init__(self):
        self.length = np.random.uniform(55, 75)
        self.height = np.random.uniform(55, 75)
        self.depth = np.random.uniform(55, 75)
        self.manifold_dimensions = mdc.vec3(self.length, self.depth, self.height)

    def transform(self):
        return mdc.brick(mdc.vec3(0, 0, 0), self.manifold_dimensions)
