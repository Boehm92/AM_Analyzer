from geometric_primitives.ten_mm_miller import ten_mm_miller
from geometric_primitives.thirty_degree_deburrer import thirty_degree_deburrer
from geometric_primitives.high_performance_drill import high_performance_drill
from geometric_primitives.fourteen_mm_vhm_drill_and_reibahle import fourteen_mm_vhm_drill_and_reibahle
from geometric_primitives.five_mm_vhm_drill import five_mm_vhm_drill
from geometric_primitives.Round import Round


class MachiningFeature:
    def __init__(self, machining_feature_id, new_cad_model):
        self.machining_feature_id = machining_feature_id
        self.new_cad_model = new_cad_model
        self.machining_feature = [ten_mm_miller, thirty_degree_deburrer, fourteen_mm_vhm_drill_and_reibahle,
                                  high_performance_drill, five_mm_vhm_drill, Round]

    def create(self):
        return self.machining_feature[self.machining_feature_id](self.new_cad_model).transformation()
