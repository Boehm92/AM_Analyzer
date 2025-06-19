import numpy as np
import madcad as mdc


class high_performance_drill:
    def __init__(self, new_cad_model):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3", "direction_4", "direction_5", "direction_6"])
        self.new_cad_model = new_cad_model

        self.pos_x = np.random.uniform(10, self.new_cad_model.length - 10)
        self.pos_y = np.random.uniform(10, self.new_cad_model.depth - 10)
        self.pos_z = np.random.uniform(10, self.new_cad_model.height - 10)

        self.depth = np.random.uniform(1.0, 30.0)
        self.tip_height = 0.69
        self.max_volume = 608
        self.max_manufacturing_time = 0.5
        self.reclamp_supplement = 2

        self.vectors = self._build_vectors()

    def _build_vectors(self):
        body_d = self.depth
        tip = self.tip_height
        total_d = body_d + tip

        return {
            "direction_1": {
                "vector_A": mdc.dvec3(0, 0, -0.002),
                "vector_B": mdc.dvec3(-4.4, 0, -0.002),
                "vector_C": mdc.dvec3(-4.4, 0, body_d),
                "vector_D": mdc.dvec3(-2.5, 0, total_d),
                "vector_E": mdc.dvec3(0, 0, total_d),
            },
            "direction_2": {
                "vector_A": mdc.dvec3(0, 0, self.new_cad_model.height - total_d),
                "vector_B": mdc.dvec3(-2.5, 0, self.new_cad_model.height - total_d),
                "vector_C": mdc.dvec3(-4.4, 0, self.new_cad_model.height - body_d),
                "vector_D": mdc.dvec3(-4.4, 0, self.new_cad_model.height + 0.0001),
                "vector_E": mdc.dvec3(0, 0, self.new_cad_model.height + 0.0001),
            },
            "direction_3": {
                "vector_A": mdc.dvec3(0, -0.002, 0),
                "vector_B": mdc.dvec3(-4.4, -0.002, 0),
                "vector_C": mdc.dvec3(-4.4, body_d, 0),
                "vector_D": mdc.dvec3(-2.5, total_d, 0),
                "vector_E": mdc.dvec3(0, total_d, 0),
            },
            "direction_4": {
                "vector_A": mdc.dvec3(0, self.new_cad_model.depth - total_d, 0),
                "vector_B": mdc.dvec3(-2.5, self.new_cad_model.depth - total_d, 0),
                "vector_C": mdc.dvec3(-4.4, self.new_cad_model.depth - body_d, 0),
                "vector_D": mdc.dvec3(-4.4, self.new_cad_model.depth + 0.0001, 0),
                "vector_E": mdc.dvec3(0, self.new_cad_model.depth + 0.0001, 0),
            },
            "direction_5": {
                "vector_A": mdc.dvec3(-0.002, 0, 0),
                "vector_B": mdc.dvec3(-0.002, 0, -4.4),
                "vector_C": mdc.dvec3(body_d, 0, -4.4),
                "vector_D": mdc.dvec3(total_d, 0, -2.5),
                "vector_E": mdc.dvec3(total_d, 0, 0),
            },
            "direction_6": {
                "vector_A": mdc.dvec3(self.new_cad_model.length - total_d, -0.001, 0),
                "vector_B": mdc.dvec3(self.new_cad_model.length - total_d, -0.001, -2.5),
                "vector_C": mdc.dvec3(self.new_cad_model.length - body_d, -0.001, -4.4),
                "vector_D": mdc.dvec3(self.new_cad_model.length + 0.0001, -0.001, -4.4),
                "vector_E": mdc.dvec3(self.new_cad_model.length + 0.0001, -0.001, 0),
            },
        }

    def manufacturing_time_calculation(self, _drill):
        _manufacturing_time = self.max_manufacturing_time * (_drill.volume() / self.max_volume)

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

        if self.dir in ["direction_1", "direction_2"]:
            _drill = mdc.revolution(2 * np.pi, (mdc.O, mdc.Z), _section)
            _drill.mergeclose()
            _drill = _drill.transform(mdc.vec3(self.pos_x, self.pos_y, 0))
        elif self.dir in ["direction_3", "direction_4"]:
            _drill = mdc.revolution(2 * np.pi, (mdc.O, mdc.Y), _section)
            _drill.mergeclose()
            _drill = _drill.transform(mdc.vec3(self.pos_x, 0, self.pos_z))
        elif self.dir in ["direction_5", "direction_6"]:
            _drill = mdc.revolution(2 * np.pi, (mdc.O, mdc.X), _section)
            _drill.mergeclose()
            _drill = _drill.transform(mdc.vec3(0, self.pos_x, self.pos_z))

        _manufacturing_time = round(self.manufacturing_time_calculation(_drill), 4)
        return _drill, _manufacturing_time
