import numpy as np
import madcad as mdc


class thirty_degree_deburrer:
    def __init__(self, new_cad_model):
        self.dir = np.random.choice([
            "direction_1", "direction_2", "direction_3",
            "direction_4", "direction_5", "direction_6"
        ])

        self.new_cad_model = new_cad_model
        self.pos_x = np.random.uniform(5, self.new_cad_model.length  - 5)
        self.pos_y = np.random.uniform(5, self.new_cad_model.depth - 5)
        self.pos_z = np.random.uniform(5, self.new_cad_model.height - 5)
        self.depth = np.random.uniform(1, 16)


        self.max_manufacturing_time = 3
        self.reclamp_supplement = 2

        self.vectors = {
            "direction_1": {
                "vector_A": mdc.dvec3(0, 0, -0.0001),
                "vector_B": mdc.dvec3(-0.1, 0, -0.0001),
                "vector_C": mdc.dvec3(-0.1, 0, self.depth),
                "vector_D": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 0, self.depth),
                "vector_E": mdc.dvec3(-10.25, 0, self.depth + 5.22),
                "vector_F": mdc.dvec3(0, 0, self.depth + 5.22),
            },
            "direction_2": {
                "vector_A": mdc.dvec3(0, 0, self.new_cad_model.height - (self.depth + 5.22)),
                "vector_B": mdc.dvec3(-10.25, 0, self.new_cad_model.height - (self.depth + 5.22)),
                "vector_C": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 0,
                                      self.new_cad_model.height - self.depth),
                "vector_D": mdc.dvec3(-0.1, 0, self.new_cad_model.height - self.depth),
                "vector_E": mdc.dvec3(-0.1, 0, self.new_cad_model.height + 0.0001),
                "vector_F": mdc.dvec3(0, 0, self.new_cad_model.height + 0.0001),
            },
            "direction_3": {
                "vector_A": mdc.dvec3(0, -0.0001, 0),
                "vector_B": mdc.dvec3(-0.1, -0.0001, 0),
                "vector_C": mdc.dvec3(-0.1, self.depth, 0),
                "vector_D": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), self.depth, 0),
                "vector_E": mdc.dvec3(-10.25, (self.depth + 5.22), 0),
                "vector_F": mdc.dvec3(0, (self.depth + 5.22), 0),
            },
            "direction_4": {
                "vector_A": mdc.dvec3(0, self.new_cad_model.depth - (self.depth + 5.22), 0),
                "vector_B": mdc.dvec3(-10.25, self.new_cad_model.depth - (self.depth + 5.22), 0),
                "vector_C": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))),
                                      self.new_cad_model.depth - self.depth, 0),
                "vector_D": mdc.dvec3(-0.1, self.new_cad_model.depth - self.depth, 0),
                "vector_E": mdc.dvec3(-0.1, self.new_cad_model.depth + 0.0001, 0),
                "vector_F": mdc.dvec3(0, self.new_cad_model.depth + 0.0001, 0),
            },
            "direction_5": {
                "vector_A": mdc.dvec3(-0.0001, 0, 0),
                "vector_B": mdc.dvec3(-0.0001, 0, -0.1),
                "vector_C": mdc.dvec3(self.depth, 0, -0.1),
                "vector_D": mdc.dvec3(self.depth, 0, -10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12))))),
                "vector_E": mdc.dvec3((self.depth + 5.22), 0, -10.25),
                "vector_F": mdc.dvec3((self.depth + 5.22), 0, 0),
            },
            "direction_6": {
                "vector_A": mdc.dvec3(self.new_cad_model.length - (self.depth + 5.22), 0, 0),
                "vector_B": mdc.dvec3(self.new_cad_model.length - (self.depth + 5.22), 0, -10.25),
                "vector_C": mdc.dvec3(self.new_cad_model.length -self.depth, 0,
                                      -10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12))))),
                "vector_D": mdc.dvec3(self.new_cad_model.length - self.depth, 0, -0.1),
                "vector_E": mdc.dvec3(self.new_cad_model.length + 0.0001, 0, -0.1),
                "vector_F": mdc.dvec3(self.new_cad_model.length + 0.0001, 0, 0),
            },
        }

    def manufacturing_time_calculation(self, _deburrer):
        _manufacturing_time = self.max_manufacturing_time

        if self.dir in ["direction_1"]:
            _manufacturing_time += self.reclamp_supplement

        return _manufacturing_time

    def transformation(self):
        _vectors = [self.vectors[self.dir]["vector_A"],
                    self.vectors[self.dir]["vector_B"],
                    self.vectors[self.dir]["vector_C"],
                    self.vectors[self.dir]["vector_D"],
                    self.vectors[self.dir]["vector_E"],
                    self.vectors[self.dir]["vector_F"],
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
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, 0, self.pos_z))
        if self.dir == "direction_4":
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.Y), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, 0, self.pos_z))
        if self.dir == "direction_5":
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.X), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(0, self.pos_x, self.pos_z))
        if self.dir == "direction_6":
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.X), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(0, self.pos_x, self.pos_z))

        _manufacturing_time = round(self.manufacturing_time_calculation(_deburrer), 4)

        return _deburrer, _manufacturing_time
