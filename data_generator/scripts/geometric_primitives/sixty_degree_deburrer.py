import numpy as np
import madcad as mdc


class sixty_degree_deburrer:
    def __init__(self, new_cad_model):
        # self.dir = np.random.choice(["direction_1", "direction_2", "direction_3", "direction_4", "direction_5", "direction_6"])
        self.dir = "direction_6"
        self.new_cad_model = new_cad_model

        self.pos_x = np.random.uniform(20, self.new_cad_model.length - 20)
        self.pos_y = np.random.uniform(20, self.new_cad_model.depth - 20)
        self.pos_z = np.random.uniform(20, self.new_cad_model.height - 20)

        self.max_volume = 2252
        self.max_manufacturing_time = 2
        self.reclamp_supplement = 2

        self.length_main = 7.5
        self.radius = 3
        self.angle = np.pi / 6  # 30°
        self.offset = self.length_main + (self.radius * (np.sin(self.angle) / np.cos(np.sin(self.angle))))
        self.height = 3.03  # Höhe des Kegels

        self.vectors = {
            "direction_1": {
                "vector_A": mdc.dvec3(0, 0, -0.0001),
                "vector_B": mdc.dvec3(-self.offset, 0, -0.0001),
                "vector_C": mdc.dvec3(-self.offset, 0, 1),
                "vector_D": mdc.dvec3(-self.length_main, 0, self.height),
                "vector_E": mdc.dvec3(0, 0, self.height),
            },
            "direction_2": {
                "vector_A": mdc.dvec3(0, 0, self.new_cad_model.height - self.height),
                "vector_B": mdc.dvec3(-self.length_main, 0, self.new_cad_model.height - self.height),
                "vector_C": mdc.dvec3(-self.offset, 0, self.new_cad_model.height - 1),
                "vector_D": mdc.dvec3(-self.offset, 0, self.new_cad_model.height + 0.0001),
                "vector_E": mdc.dvec3(0, 0, self.new_cad_model.height + 0.0001),
            },
            "direction_3": {
                "vector_A": mdc.dvec3(0, -0.0001, 0),
                "vector_B": mdc.dvec3(-self.offset, -0.0001, 0),
                "vector_C": mdc.dvec3(-self.offset, 0, 1),
                "vector_D": mdc.dvec3(-self.length_main, self.height, 0),
                "vector_E": mdc.dvec3(0, self.height, 0),
            },
            "direction_4": {
                "vector_E": mdc.dvec3(0, self.new_cad_model.depth + 0.0001, 0),
                "vector_D": mdc.dvec3(-self.offset, self.new_cad_model.depth + 0.0001, 0),
                "vector_C": mdc.dvec3(-self.offset, self.new_cad_model.depth - 1, 0),
                "vector_B": mdc.dvec3(-self.length_main, self.new_cad_model.depth - self.height, 0),
                "vector_A": mdc.dvec3(0, self.new_cad_model.depth - self.height, 0),
            },
            "direction_5": {
                "vector_A": mdc.dvec3(-0.0001, 0, 0),
                "vector_B": mdc.dvec3(-0.0001, 0, -self.offset),
                "vector_C": mdc.dvec3(1, 0, -self.offset),
                "vector_D": mdc.dvec3(self.height, 0, -self.length_main),
                "vector_E": mdc.dvec3(self.height, 0, 0),
            },
            "direction_6": {
                "vector_A": mdc.dvec3(self.new_cad_model.length - self.height, -0.0001, 0),
                "vector_B": mdc.dvec3(self.new_cad_model.length - self.height, -0.0001, -self.length_main),
                "vector_C": mdc.dvec3(self.new_cad_model.length - 1, -0.0001, -self.offset),
                "vector_D": mdc.dvec3(self.new_cad_model.length + 0.0001, -0.0001, -self.offset),
                "vector_E": mdc.dvec3(self.new_cad_model.length + 0.0001, -0.0001, 0),
            },
        }

    def manufacturing_time_calculation(self, _deburrer):
        _manufacturing_time = self.max_manufacturing_time
        if self.dir == "direction_1":
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

        if self.dir in ["direction_1", "direction_2"]:
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.Z), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, self.pos_y, 0))
        elif self.dir in ["direction_3", "direction_4"]:
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.Y), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, 0, self.pos_z))
        elif self.dir in ["direction_5", "direction_6"]:
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.X), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(0, self.pos_x, self.pos_z))

        _manufacturing_time = round(self.manufacturing_time_calculation(_deburrer), 4)
        return _deburrer, _manufacturing_time
