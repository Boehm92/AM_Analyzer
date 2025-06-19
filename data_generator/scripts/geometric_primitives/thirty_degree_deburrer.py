import numpy as np
import madcad as mdc


class thirty_degree_deburrer:
    def __init__(self, new_cad_model):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3", "direction_4", "direction_5",
                                     "direction_6"])
        self.new_cad_model = new_cad_model
        self.pos_x = np.random.uniform(20, self.new_cad_model.length  - 20)
        self.pos_y = np.random.uniform(20, self.new_cad_model.depth - 20)
        self.pos_z = np.random.uniform(20, self.new_cad_model.height - 20)

        self.max_volume = 2381
        self.max_manufacturing_time = 3
        self.reclamp_supplement = 2

        self.vectors = {
            "direction_1": {
                "vector_A": mdc.dvec3(0, 0, -0.0001),
                "vector_B": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 0, -0.0001),
                "vector_C": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 0, 1),
                "vector_D": mdc.dvec3(-10.25, 0, 6.22),
                "vector_E": mdc.dvec3(0, 0, 6.22),
            },
            "direction_2": {
                "vector_A": mdc.dvec3(0, 0, self.new_cad_model.height - 6.22),
                "vector_B": mdc.dvec3(-10.25, 0, self.new_cad_model.height - 6.22),
                "vector_C": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 0,
                                      self.new_cad_model.height - 1),
                "vector_D": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 0,
                                      self.new_cad_model.height + 0.0001),
                "vector_E": mdc.dvec3(0, 0, self.new_cad_model.height + 0.0001),
            },
            "direction_3": {
                "vector_A": mdc.dvec3(0, -0.0001, 0),
                "vector_B": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), -0.0001, 0),
                "vector_C": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))), 1, 0),
                "vector_D": mdc.dvec3(-10.25, 6.22, 0),
                "vector_E": mdc.dvec3(0, 6.22, 0),
            },
            "direction_4": {
                "vector_E": mdc.dvec3(0, self.new_cad_model.depth + 0.0001, 0),
                "vector_D": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))),
                                      self.new_cad_model.depth + 0.0001, 0),
                "vector_C": mdc.dvec3(-10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12)))),
                                      self.new_cad_model.depth - 1, 0),
                "vector_B": mdc.dvec3(-10.25,  self.new_cad_model.depth - 6.22, 0),
                "vector_A": mdc.dvec3(0, self.new_cad_model.depth - 6.22, 0),
            },
            "direction_5": {
                "vector_A": mdc.dvec3(-0.0001, 0, 0),
                "vector_B": mdc.dvec3(-0.0001, 0, -10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12))))),
                "vector_C": mdc.dvec3(1, 0, -10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12))))),
                "vector_D": mdc.dvec3(6.22, 0, -10.25),
                "vector_E": mdc.dvec3(6.22, 0, 0),
            },
            "direction_6": {
                "vector_A": mdc.dvec3(self.new_cad_model.length - 6.22, -0.0001, 0),
                "vector_B": mdc.dvec3(self.new_cad_model.length - 6.22, -0.0001, -10.25),
                "vector_C": mdc.dvec3(self.new_cad_model.length -1, -0.0001,
                                      -10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12))))),
                "vector_E": mdc.dvec3(self.new_cad_model.length + 0.0001, -0.0001, 0),
                "vector_D": mdc.dvec3(self.new_cad_model.length + 0.0001, 0.0001,
                                      -10.25 - (5.22 * (np.sin(np.pi / 12) / np.cos(np.sin(np.pi / 12))))),
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
