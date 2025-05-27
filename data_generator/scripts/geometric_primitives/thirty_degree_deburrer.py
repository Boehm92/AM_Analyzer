import numpy as np
import madcad as mdc


class thirty_degree_deburrer:
    def __init__(self, new_cad_model):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3", "direction_4", "direction_5",
                                     "direction_6"])
        self.new_cad_model = new_cad_model
        self.pos_x = np.random.uniform(-7, 17.78)
        self.pos_y = np.random.uniform(-7, 17.78)

        self.max_volume = 2381
        self.max_manufacturing_time = 1
        self.manufacturing_time_side_supplement = 0

        self.vectors = {
            "direction_1": {
                "vector_A": mdc.dvec3(0, 0, -0.002),
                "vector_B": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 0, -0.002),
                "vector_C": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 0, 1),
                "vector_D": mdc.dvec3(-10.25, 0, 6.22),
                "vector_E": mdc.dvec3(0, 0, 6.22),
            },
            "direction_2": {
                "vector_A": mdc.dvec3(0, 0, 3.78),
                "vector_B": mdc.dvec3(-10.25, 0, 3.78),
                "vector_C": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 0, 9),
                "vector_D": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 0, 10.002),
                "vector_E": mdc.dvec3(0, 0, 10.002),
            },
            "direction_3": {
                "vector_A": mdc.dvec3(0, -0.1, 0),
                "vector_B": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), -0.002, 0),
                "vector_C": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 1, 0),
                "vector_D": mdc.dvec3(-10.25, 6.22, 0),
                "vector_E": mdc.dvec3(0, 6.22, 0),
            },
            "direction_4": {
                "vector_E": mdc.dvec3(0, 10.002, 0),
                "vector_D": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 10.002, 0),
                "vector_C": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 9, 0),
                "vector_B": mdc.dvec3(-10.25, 3.78, 0),
                "vector_A": mdc.dvec3(0, 3.78, 0),
            },
            "direction_5": {
                "vector_A": mdc.dvec3(-0.002, 0, 0),
                "vector_B": mdc.dvec3(-0.002, 0, -10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12))))),
                "vector_C": mdc.dvec3(1, 0, -10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12))))),
                "vector_D": mdc.dvec3(6.22, 0, -10.25),
                "vector_E": mdc.dvec3(6.22, 0, 0),
            },
            "direction_6": {
                "vector_A": mdc.dvec3(3.78, -0.002, 0),
                "vector_B": mdc.dvec3(3.78, -0.002, -10.25),
                "vector_C": mdc.dvec3(9, -0.002, -10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12))))),
                "vector_E": mdc.dvec3(10.002, -0.002, 0),
                "vector_D": mdc.dvec3(10.002, -0.002,
                                      -10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12))))),
            },
        }

    def manufacturing_time_calculation(self, _deburrer):
        _volume = mdc.intersection(self.new_cad_model, _deburrer).volume()
        _manufacturing_time = self.max_manufacturing_time * (_volume / self.max_volume)

        if self.dir in ["direction_1", "direction_3", "direction_4", "direction_5", "direction_6"]:
            _manufacturing_time += self.manufacturing_time_side_supplement

        return _manufacturing_time

    def transformation(self):
        _vectors = [self.vectors[self.dir]["vector_A"],
                    self.vectors[self.dir]["vector_B"],
                    self.vectors[self.dir]["vector_C"],
                    self.vectors[self.dir]["vector_D"],
                    self.vectors[self.dir]["vector_E"],
                    ]

        _section = mdc.Wire(_vectors).segmented().flip()

        if self.dir == "direction_1":
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.Z), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, self.pos_y, 0))
        if self.dir == "direction_2":
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.Z), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, self.pos_y, 0))
        if self.dir == "direction_3":
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.Y), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, 0, self.pos_y))
        if self.dir == "direction_4":
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.Y), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, 0, self.pos_y))
        if self.dir == "direction_5":
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.X), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(0, self.pos_x, self.pos_y))
        if self.dir == "direction_6":
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.X), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(0, self.pos_x, self.pos_y))

        _manufacturing_time = round(self.manufacturing_time_calculation(_deburrer), 4)

        return _deburrer, _manufacturing_time
