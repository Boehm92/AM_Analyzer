import numpy as np
import madcad as mdc


class thirty_degree_deburrer:
    def __init__(self, new_cad_model, angle_deg=30, flank_length=5.22, radius=10.25, max_depth=16):
        self.angle_deg = angle_deg
        self.flank_length = flank_length
        self.radius = radius
        self.max_dept = max_depth

        self.tan_angle = np.tan(np.radians(self.angle_deg))
        self.delta_x = self.flank_length * self.tan_angle

        self.dir = np.random.choice([
            "direction_1", "direction_2", "direction_3",
            "direction_4", "direction_5", "direction_6"
        ])

        self.new_cad_model = new_cad_model
        self.pos_x = np.random.uniform(self.radius, self.new_cad_model.length - self.radius)
        self.pos_y = np.random.uniform(self.radius, self.new_cad_model.depth - self.radius)
        self.pos_z = np.random.uniform(self.radius, self.new_cad_model.height - self.radius)
        self.depth = np.random.uniform(1, self.max_dept)

        self.max_manufacturing_time = 3
        self.reclamp_supplement = 2

        self.vectors = {
            "direction_1": {
                "vector_A": mdc.dvec3(0, 0, -0.0001),
                "vector_B": mdc.dvec3(-0.1, 0, -0.0001),
                "vector_C": mdc.dvec3(-0.1, 0, self.depth),
                "vector_D": mdc.dvec3(-self.radius - self.delta_x, 0, self.depth),
                "vector_E": mdc.dvec3(-self.radius, 0, self.depth + self.flank_length),
                "vector_F": mdc.dvec3(0, 0, self.depth + self.flank_length),
            },
            "direction_2": {
                "vector_A": mdc.dvec3(0, 0, self.new_cad_model.height - (self.depth + self.flank_length)),
                "vector_B": mdc.dvec3(-self.radius, 0, self.new_cad_model.height - (self.depth + self.flank_length)),
                "vector_C": mdc.dvec3(-self.radius - self.delta_x, 0, self.new_cad_model.height - self.depth),
                "vector_D": mdc.dvec3(-0.1, 0, self.new_cad_model.height - self.depth),
                "vector_E": mdc.dvec3(-0.1, 0, self.new_cad_model.height + 0.0001),
                "vector_F": mdc.dvec3(0, 0, self.new_cad_model.height + 0.0001),
            },
            "direction_3": {
                "vector_A": mdc.dvec3(0, -0.0001, 0),
                "vector_B": mdc.dvec3(-0.1, -0.0001, 0),
                "vector_C": mdc.dvec3(-0.1, self.depth, 0),
                "vector_D": mdc.dvec3(-self.radius - self.delta_x, self.depth, 0),
                "vector_E": mdc.dvec3(-self.radius, self.depth + self.flank_length, 0),
                "vector_F": mdc.dvec3(0, self.depth + self.flank_length, 0),
            },
            "direction_4": {
                "vector_A": mdc.dvec3(0, self.new_cad_model.depth - (self.depth + self.flank_length), 0),
                "vector_B": mdc.dvec3(-self.radius, self.new_cad_model.depth - (self.depth + self.flank_length), 0),
                "vector_C": mdc.dvec3(-self.radius - self.delta_x, self.new_cad_model.depth - self.depth, 0),
                "vector_D": mdc.dvec3(-0.1, self.new_cad_model.depth - self.depth, 0),
                "vector_E": mdc.dvec3(-0.1, self.new_cad_model.depth + 0.0001, 0),
                "vector_F": mdc.dvec3(0, self.new_cad_model.depth + 0.0001, 0),
            },
            "direction_5": {
                "vector_A": mdc.dvec3(-0.0001, 0, 0),
                "vector_B": mdc.dvec3(-0.0001, 0, -0.1),
                "vector_C": mdc.dvec3(self.depth, 0, -0.1),
                "vector_D": mdc.dvec3(self.depth, 0, -self.radius - self.delta_x),
                "vector_E": mdc.dvec3(self.depth + self.flank_length, 0, -self.radius),
                "vector_F": mdc.dvec3(self.depth + self.flank_length, 0, 0),
            },
            "direction_6": {
                "vector_A": mdc.dvec3(self.new_cad_model.length - (self.depth + self.flank_length), 0, 0),
                "vector_B": mdc.dvec3(self.new_cad_model.length - (self.depth + self.flank_length), 0, -self.radius),
                "vector_C": mdc.dvec3(self.new_cad_model.length - self.depth, 0, -self.radius - self.delta_x),
                "vector_D": mdc.dvec3(self.new_cad_model.length - self.depth, 0, -0.1),
                "vector_E": mdc.dvec3(self.new_cad_model.length + 0.0001, 0, -0.1),
                "vector_F": mdc.dvec3(self.new_cad_model.length + 0.0001, 0, 0),
            },
        }

    def manufacturing_time_calculation(self, _deburrer):
        _manufacturing_time = self.max_manufacturing_time

        if self.dir == "direction_1":
            _manufacturing_time += self.reclamp_supplement

        return _manufacturing_time

    def transformation(self):
        _vectors = [self.vectors[self.dir][f"vector_{ch}"] for ch in "ABCDEF"]
        _section = mdc.Wire(_vectors).segmented().flip()

        axis_map = {
            "direction_1": (mdc.Z, mdc.vec3(self.pos_x, self.pos_y, 0)),
            "direction_2": (mdc.Z, mdc.vec3(self.pos_x, self.pos_y, 0)),
            "direction_3": (mdc.Y, mdc.vec3(self.pos_x, 0, self.pos_z)),
            "direction_4": (mdc.Y, mdc.vec3(self.pos_x, 0, self.pos_z)),
            "direction_5": (mdc.X, mdc.vec3(0, self.pos_x, self.pos_z)),
            "direction_6": (mdc.X, mdc.vec3(0, self.pos_x, self.pos_z)),
        }

        axis, translation = axis_map[self.dir]
        _deburrer = mdc.revolution(2 * np.pi, (mdc.O, axis), _section)
        _deburrer.mergeclose()
        _deburrer = _deburrer.transform(translation)

        _manufacturing_time = round(self.manufacturing_time_calculation(_deburrer), 4)

        return _deburrer, _manufacturing_time
