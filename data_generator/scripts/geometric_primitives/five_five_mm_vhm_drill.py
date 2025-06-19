import numpy as np
import madcad as mdc


class five_five_mm_vhm_drill:
    def __init__(self, new_cad_model):
        self.dir = np.random.choice(["direction_1", "direction_2", "direction_3"])

        self.new_cad_model = new_cad_model
        self.radius = 2.75
        self.pos_x = np.random.uniform(0.5 + self.radius, self.new_cad_model.length - 0.5 - self.radius)
        self.pos_y = np.random.uniform(0.5 + self.radius, self.new_cad_model.depth - 0.5 - self.radius)
        self.pos_z = np.random.uniform(0.5 + self.radius, self.new_cad_model.height - 0.5 - self.radius)

        self.start = -0.0001
        self.depth_x = self.new_cad_model.length + 0.0001
        self.depth_y = self.new_cad_model.depth + 0.0001
        self.depth_z = self.new_cad_model.height + 0.0001

        self.max_volume = 7699
        self.max_manufacturing_time = 3.33
        self.reclamp_supplement = 2

        self.transform = {
            "direction_1": [mdc.vec3(self.pos_x, self.pos_y, self.start),
                            mdc.vec3(self.pos_x, self.pos_y, self.depth_z)],
            "direction_2": [mdc.vec3(self.pos_x, self.start, self.pos_z),
                            mdc.vec3(self.pos_x, self.depth_y, self.pos_z)],
            "direction_3": [mdc.vec3(self.start, self.pos_y, self.pos_z),
                            mdc.vec3(self.depth_x, self.pos_y, self.pos_z)],
        }

    def manufacturing_time_calculation(self, _through_hole):
        _manufacturing_time = self.max_manufacturing_time * (_through_hole.volume() / self.max_volume)

        if self.dir in ["direction_1"]:
            _manufacturing_time += self.reclamp_supplement

        return _manufacturing_time

    def transformation(self):
        _through_hole = mdc.cylinder(self.transform[self.dir][0], self.transform[self.dir][1], self.radius)
        _manufacturing_time = round(self.manufacturing_time_calculation(_through_hole), 4)

        return _through_hole, _manufacturing_time
