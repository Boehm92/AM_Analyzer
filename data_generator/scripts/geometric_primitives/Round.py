import math
import numpy as np
import madcad as mdc


class Round:
    def __init__(self, new_cad_model):
        self.new_cad_model = new_cad_model
        self.dir = np.random.choice([
            "direction_1", "direction_2", "direction_3", "direction_4",
            "direction_5", "direction_6", "direction_7", "direction_8",
            "direction_9", "direction_10", "direction_11", "direction_12"
        ])

        self.radius = 2
        self.length = self.radius * (1 - math.sin(math.radians(45)))
        self.width = self.length  # same value
        self.depth_value = 10.3
        self.offset = 0.0001

        self.max_volume = 62
        self.max_manufacturing_time = 0.16
        self.manufacturing_time_side_supplement = 0

        self.len_x = self.new_cad_model.length
        self.len_y = self.new_cad_model.depth
        self.len_z = self.new_cad_model.height

        self.positive = {
            "x": self.len_x + self.offset,
            "y": self.len_y + self.offset,
            "z": self.len_z + self.offset
        }
        self.negative = -self.offset

        self.round_vectors = self._build_vectors()
        self.depth = self._build_depth_vectors()

    def _build_vectors(self):
        n = self.negative
        p = self.positive
        r = self.radius
        l = self.length
        w = self.width

        return {
            "direction_1": {  # front-top
                "vector_A": mdc.vec3(n, n, p["z"] - r),
                "vector_B": mdc.vec3(n, n, p["z"]),
                "vector_C": mdc.vec3(n, n + r, p["z"]),
                "vector_D": mdc.vec3(n, n + l, p["z"] - w),
            },
            "direction_2": {  # front-bottom
                "vector_A": mdc.vec3(n, n + r, n),
                "vector_B": mdc.vec3(n, n, n),
                "vector_C": mdc.vec3(n, n, n + r),
                "vector_D": mdc.vec3(n, n + l, n + w),
            },
            "direction_3": {  # back-top
                "vector_A": mdc.vec3(n, p["y"] - r, p["z"]),
                "vector_B": mdc.vec3(n, p["y"], p["z"]),
                "vector_C": mdc.vec3(n, p["y"], p["z"] - r),
                "vector_D": mdc.vec3(n, p["y"] - l, p["z"] - w),
            },
            "direction_4": {  # back-bottom
                "vector_A": mdc.vec3(n, p["y"], n + r),
                "vector_B": mdc.vec3(n, p["y"], n),
                "vector_C": mdc.vec3(n, p["y"] - r, n),
                "vector_D": mdc.vec3(n, p["y"] - l, n + w),
            },
            "direction_5": {  # left-top
                "vector_A": mdc.vec3(n + r, n, p["z"]),
                "vector_B": mdc.vec3(n, n, p["z"]),
                "vector_C": mdc.vec3(n, n, p["z"] - r),
                "vector_D": mdc.vec3(n + l, n, p["z"] - w),
            },
            "direction_6": {  # left-bottom
                "vector_A": mdc.vec3(n, n, n + r),
                "vector_B": mdc.vec3(n, n, n),
                "vector_C": mdc.vec3(n + r, n, n),
                "vector_D": mdc.vec3(n + l, n, n + w),
            },
            "direction_7": {  # left-front
                "vector_A": mdc.vec3(n + r, n, n),
                "vector_B": mdc.vec3(n, n, n),
                "vector_C": mdc.vec3(n, n + r, n),
                "vector_D": mdc.vec3(n + l, n + w, n),
            },
            "direction_8": {  # left-back
                "vector_A": mdc.vec3(n, p["y"] - r, n),
                "vector_B": mdc.vec3(n, p["y"], n),
                "vector_C": mdc.vec3(n + r, p["y"], n),
                "vector_D": mdc.vec3(n + l, p["y"] - w, n),
            },
            "direction_9": {  # right-top
                "vector_A": mdc.vec3(p["x"], n, p["z"] - r),
                "vector_B": mdc.vec3(p["x"], n, p["z"]),
                "vector_C": mdc.vec3(p["x"] - r, n, p["z"]),
                "vector_D": mdc.vec3(p["x"] - l, n, p["z"] - w),
            },
            "direction_10": {  # right-bottom
                "vector_A": mdc.vec3(p["x"] - r, n, n),
                "vector_B": mdc.vec3(p["x"], n, n),
                "vector_C": mdc.vec3(p["x"], n, n + r),
                "vector_D": mdc.vec3(p["x"] - l, n, n + w),
            },
            "direction_11": {  # right-front
                "vector_A": mdc.vec3(p["x"], n + r, n),
                "vector_B": mdc.vec3(p["x"], n, n),
                "vector_C": mdc.vec3(p["x"] - r, n, n),
                "vector_D": mdc.vec3(p["x"] - l, n + w, n),
            },
            "direction_12": {  # right-back
                "vector_A": mdc.vec3(p["x"] - r, p["y"], n),
                "vector_B": mdc.vec3(p["x"], p["y"], n),
                "vector_C": mdc.vec3(p["x"], p["y"] - r, n),
                "vector_D": mdc.vec3(p["x"] - l, p["y"] - w, n),
            },
        }

    def _build_depth_vectors(self):
        return {
            dir: (getattr(self.new_cad_model, dim) + 0.001) * axis
            for dir, (dim, axis) in {
                "direction_1": ("length", mdc.X),
                "direction_2": ("length", mdc.X),
                "direction_3": ("length", mdc.X),
                "direction_4": ("length", mdc.X),
                "direction_5": ("depth",  mdc.Y),
                "direction_6": ("depth",  mdc.Y),
                "direction_7": ("height", mdc.Z),
                "direction_8": ("height", mdc.Z),
                "direction_9": ("depth",  mdc.Y),
                "direction_10": ("depth",  mdc.Y),
                "direction_11": ("height", mdc.Z),
                "direction_12": ("height", mdc.Z),
            }.items()
        }

    def manufacturing_time_calculation(self, round):
        time = self.max_manufacturing_time * (round.volume() / self.max_volume)
        if self.dir in {"direction_2", "direction_4", "direction_6", "direction_10"}:
            time += self.manufacturing_time_side_supplement
        return time

    def transformation(self):
        v = self.round_vectors[self.dir]
        profile = [
            mdc.Segment(v["vector_A"], v["vector_B"]),
            mdc.Segment(v["vector_B"], v["vector_C"]),
            mdc.ArcThrough(v["vector_C"], v["vector_D"], v["vector_A"])
        ]
        face = mdc.flatsurface(profile)
        body = mdc.extrusion(self.depth[self.dir], face)
        time = round(self.manufacturing_time_calculation(body), 4)
        return body, time
