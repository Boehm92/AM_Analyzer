import numpy as np
import madcad as mdc


class ninety_degree_deburrer:
    def __init__(self, new_cad_model):
        self.dir = np.random.choice([
            "direction_1", "direction_2", "direction_3",
            "direction_4", "direction_5", "direction_6"
        ])

        self.new_cad_model = new_cad_model

        # Safe positions within the base part
        self.pos_x = np.random.uniform(10, self.new_cad_model.length - 10)
        self.pos_y = np.random.uniform(10, self.new_cad_model.depth - 10)
        self.pos_z = np.random.uniform(10, self.new_cad_model.height - 10)

        self.max_volume = 10.9
        self.max_manufacturing_time = 0.33
        self.reclamp_supplement = 2

        self.vectors = self._build_vectors()

    def _build_vectors(self):
        """Build the 2D section for each direction with appropriate offset."""
        return {
            "direction_1": {
                "vector_A": mdc.dvec3(0, 0, -0.0001),
                "vector_B": mdc.dvec3(-3.15, 0, -0.0001),
                "vector_C": mdc.dvec3(-2.75, 0, 0.4),
                "vector_D": mdc.dvec3(0, 0, 0.4),
            },
            "direction_2": {
                "vector_A": mdc.dvec3(0, 0, self.new_cad_model.height - 0.4),
                "vector_B": mdc.dvec3(-2.75, 0, self.new_cad_model.height - 0.4),
                "vector_C": mdc.dvec3(-3.15, 0, self.new_cad_model.height + 0.0001),
                "vector_D": mdc.dvec3(0, 0, self.new_cad_model.height + 0.0001),
            },
            "direction_3": {
                "vector_A": mdc.dvec3(0, -0.0001, 0),
                "vector_B": mdc.dvec3(-3.15, -0.0001, 0),
                "vector_C": mdc.dvec3(-2.75, 0.4, 0),
                "vector_D": mdc.dvec3(0, 0.4, 0),
            },
            "direction_4": {
                "vector_A": mdc.dvec3(0, self.new_cad_model.depth - 0.4, 0),
                "vector_B": mdc.dvec3(-2.75, self.new_cad_model.depth - 0.4, 0),
                "vector_C": mdc.dvec3(-3.15, self.new_cad_model.depth + 0.0001, 0),
                "vector_D": mdc.dvec3(0, self.new_cad_model.depth + 0.0001, 0),
            },
            "direction_5": {
                "vector_A": mdc.dvec3(-0.0001, 0, 0),
                "vector_B": mdc.dvec3(-0.0001, 0, -3.15),
                "vector_C": mdc.dvec3(0.4, 0, -2.75),
                "vector_D": mdc.dvec3(0.4, 0, 0),
            },
            "direction_6": {
                "vector_A": mdc.dvec3(self.new_cad_model.length - 0.4, 0, 0),
                "vector_B": mdc.dvec3(self.new_cad_model.length - 0.4, 0, -2.75),
                "vector_C": mdc.dvec3(self.new_cad_model.length + 0.0001, 0, -3.15),
                "vector_D": mdc.dvec3(self.new_cad_model.length + 0.0001, 0, 0),
            },
        }

    def manufacturing_time_calculation(self, _deburrer):
        time = self.max_manufacturing_time * (_deburrer.volume() / self.max_volume)

        # Supplement only for direction_1 (starts at Z = -0.0001)
        if self.dir == "direction_1":
            time += self.reclamp_supplement

        return time

    def transformation(self):
        # Build and revolve profile
        vectors = [self.vectors[self.dir][k] for k in ["vector_A", "vector_B", "vector_C", "vector_D"]]
        section = mdc.Wire(vectors).segmented().flip()

        axis = {
            "direction_1": (mdc.O, mdc.Z),
            "direction_2": (mdc.O, mdc.Z),
            "direction_3": (mdc.O, mdc.Y),
            "direction_4": (mdc.O, mdc.Y),
            "direction_5": (mdc.O, mdc.X),
            "direction_6": (mdc.O, mdc.X),
        }[self.dir]

        _deburrer = mdc.revolution(2 * np.pi, axis, section)
        _deburrer.mergeclose()

        # Translate to position
        if self.dir in ["direction_1", "direction_2"]:
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, self.pos_y, 0))
        elif self.dir in ["direction_3", "direction_4"]:
            _deburrer = _deburrer.transform(mdc.vec3(self.pos_x, 0, self.pos_y))
        elif self.dir in ["direction_5", "direction_6"]:
            _deburrer = _deburrer.transform(mdc.vec3(0, self.pos_x, self.pos_y))

        # Calculate time
        m_time = round(self.manufacturing_time_calculation(_deburrer), 4)
        return _deburrer, m_time
