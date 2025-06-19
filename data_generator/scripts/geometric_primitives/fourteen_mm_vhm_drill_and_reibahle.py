import numpy as np
import madcad as mdc


class fourteen_mm_vhm_drill_and_reibahle:
    def __init__(self, new_cad_model):
        self.dir = np.random.choice([
            "direction_1", "direction_2", "direction_3",
            "direction_4", "direction_5", "direction_6"
        ])

        self.new_cad_model = new_cad_model

        self.pos_x = np.random.uniform(10, self.new_cad_model.length - 10)
        self.pos_y = np.random.uniform(10, self.new_cad_model.depth - 10)
        self.pos_z = np.random.uniform(10, self.new_cad_model.height - 10)

        self.depth = np.random.uniform(1, 30)
        self.reib_height = 2.57
        self.total_depth = self.depth + self.reib_height

        self.max_volume = 1731
        self.max_manufacturing_time = 1
        self.reclamp_supplement = 2

        self.vectors = self._build_vectors()

    def _build_vectors(self):
        return {
            "direction_1": {
                "vector_A": mdc.dvec3(0, 0, -0.0001),
                "vector_B": mdc.dvec3(-7.5, 0, -0.0001),
                "vector_C": mdc.dvec3(-7.5, 0, self.depth),
                "vector_D": mdc.dvec3(0, 0, self.total_depth),
            },
            "direction_2": {
                "vector_A": mdc.dvec3(0, 0, self.new_cad_model.height - self.total_depth),
                "vector_B": mdc.dvec3(-7.5, 0, self.new_cad_model.height - self.depth),
                "vector_C": mdc.dvec3(-7.5, 0, self.new_cad_model.height),
                "vector_D": mdc.dvec3(0, 0, self.new_cad_model.height),
            },
            "direction_3": {
                "vector_A": mdc.dvec3(0, -0.0001, 0),
                "vector_B": mdc.dvec3(-7.5, -0.0001, 0),
                "vector_C": mdc.dvec3(-7.5, self.depth, 0),
                "vector_D": mdc.dvec3(0, self.total_depth, 0),
            },
            "direction_4": {
                "vector_A": mdc.dvec3(0, self.new_cad_model.depth - self.total_depth, 0),
                "vector_B": mdc.dvec3(-7.5, self.new_cad_model.depth - self.depth, 0),
                "vector_C": mdc.dvec3(-7.5, self.new_cad_model.depth, 0),
                "vector_D": mdc.dvec3(0, self.new_cad_model.depth, 0),
            },
            "direction_5": {
                "vector_A": mdc.dvec3(-0.0001, 0, 0),
                "vector_B": mdc.dvec3(-0.0001, 0, -7.5),
                "vector_C": mdc.dvec3(self.depth, 0, -7.5),
                "vector_D": mdc.dvec3(self.total_depth, 0, 0),
            },
            "direction_6": {
                "vector_A": mdc.dvec3(self.new_cad_model.length - self.total_depth, 0, 0),
                "vector_B": mdc.dvec3(self.new_cad_model.length - self.depth, 0, -7.5),
                "vector_C": mdc.dvec3(self.new_cad_model.length, 0, -7.5),
                "vector_D": mdc.dvec3(self.new_cad_model.length, 0, 0),
            },
        }

    def manufacturing_time_calculation(self, _deburrer):
        _manufacturing_time = self.max_manufacturing_time * (_deburrer.volume() / self.max_volume)

        if self.dir in ["direction_1"]:
            _manufacturing_time += self.reclamp_supplement

        return _manufacturing_time

    def transformation(self):
        _vectors = [self.vectors[self.dir]["vector_A"],
                    self.vectors[self.dir]["vector_B"],
                    self.vectors[self.dir]["vector_C"],
                    self.vectors[self.dir]["vector_D"],
                    ]

        _section = mdc.Wire(_vectors).segmented().flip()

        if self.dir in ["direction_1", "direction_2"]:
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.Z), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, self.pos_y, 0))
        elif self.dir in ["direction_3", "direction_4"]:
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.Y), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, 0, self.pos_y))
        elif self.dir in ["direction_5", "direction_6"]:
            _deburrer = mdc.revolution(2 * np.pi, (mdc.O, mdc.X), _section)
            _deburrer.mergeclose()
            _deburrer = _deburrer.transform(mdc.vec3(0, self.pos_x, self.pos_y))

        _manufacturing_time = round(self.manufacturing_time_calculation(_deburrer), 4)
        return _deburrer, _manufacturing_time
