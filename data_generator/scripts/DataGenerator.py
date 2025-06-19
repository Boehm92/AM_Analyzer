import os
import time
import numpy as np
import madcad as mdc
from geometric_primitives.base_primitive import Manifold
from utils.MachiningFeature import MachiningFeature
from utils.MachiningFeatureLabels import MachiningFeatureLabels

def run_single_model(args):
    model_id, config = args
    start_time = time.time()

    base_path = os.getenv(config.target_directory)
    np.random.seed(config.random_generation_seed + model_id)

    _machining_feature_id_list = []
    _machining_feature_list = []
    _manufacturing_time = 0

    # try:
    _manifold = Manifold()
    _new_cad_model = _manifold.transform()

    # _machining_config = [(0, np.random.randint(0, 2)),
    #                      (1, np.random.randint(0, 2)),
    #                      (2, np.random.randint(0, 2)),
    #                      (4, np.random.randint(0, 2)),
    #                      (5, np.random.randint(0, 2)),]
    _machining_config = [(8, 7)]

    generated_features = []
    generated_ids = []

    for feature_id, count in _machining_config:
        for _ in range(count):
            try:
                feature, m_time = MachiningFeature(feature_id, _manifold).create()
                # mdc.show([feature, _new_cad_model])
                if m_time <= 0:
                    raise ValueError("Manufacturing time is zero or negative.")
                _manufacturing_time += m_time
                generated_features.append(feature)
                generated_ids.append(feature_id)
            except Exception as e:
                print(f"[⚠] Fehler beim Erzeugen von Feature {feature_id} für Modell {model_id}: {e}")


    valid_features = []
    valid_ids = []
    for i, feature in enumerate(generated_features):
        try:
            # mdc.show([_new_cad_model, feature, feature])
            _new_cad_model = mdc.difference(_new_cad_model, feature)
            valid_features.append(feature)
            valid_ids.append(generated_ids[i])
        except Exception as e:
            print(f"[⚠] CSG-Differenz fehlgeschlagen (Modell {model_id}, Feature-ID {generated_ids[i]}): {e}")


    _new_cad_model.mergeclose()
    _new_cad_model = mdc.segmentation(_new_cad_model)

    mdc.show([_new_cad_model])

    model_path = os.path.join(base_path, f"{model_id}.stl")
    mdc.write(_new_cad_model, model_path)

    labels = MachiningFeatureLabels(valid_features, model_id, config.target_directory, valid_ids)
    labels.write_vertices_file()
    labels.write_bounding_box_file()
    labels.write_manufacturing_time_file(_manufacturing_time)

    elapsed = round(time.time() - start_time, 2)  # ⏱️ Zeit stoppen
    print(f"✔ Modell {model_id} erstellt mit {len(valid_features)} Features: {valid_ids} ({elapsed} Sek.)")

    # except Exception as e:
    #     elapsed = round(time.time() - start_time, 2)
    #     print(f"[⛔] Schwerwiegender Fehler bei Modell {model_id} ({elapsed} Sek.): {e}")
