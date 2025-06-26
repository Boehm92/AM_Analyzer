import argparse
from multiprocessing import Pool
from DataGenerator import run_single_model

_parser = argparse.ArgumentParser(description='Base configuration of the synthetic data generator')
_parser.add_argument('--target_directory',
                     dest='target_directory', default='TRAINING_DATASET_SOURCE', type=str,
                     help='The variable TRAINING_DATASET_SOURCE is an environment variable used '
                          'to access the training and test CAD data in the CAFR framework.')
_parser.add_argument('--cad_data_generation_start_cycle',
                     dest='cad_data_generation_start_cycle', type=int, default=1,
                     help='Start ID of the data generation process.')
_parser.add_argument('--cad_data_generation_end_cycles',
                     dest='cad_data_generation_end_cycles', type=int, default=2000,
                     help='End ID of the data generation process (non-inclusive).')
_parser.add_argument('--machining_config',
                     dest='machining_config',
                     type=str,
                     default="""[(0, np.random.randint(0, 7)),
                                 (1, np.random.randint(0, 4)),
                                 (2, np.random.randint(0, 3)),
                                 (3, np.random.randint(0, 7)),
                                 (4, np.random.randint(0, 7)),
                                 (5, np.random.randint(0, 7))
                                 ]""",

                     help='Machining feature ID:'
                          '0: ten_mm_miller'
                          '1: thirty_degree_deburrer'
                          '2: fourteen_mm_vhm_drill_and_reibahle'
                          '3: high_performance_drill'
                          '4: five_mm_vhm_drill '
                          '5: Round)')
_parser.add_argument('--random_generation_seed',
                     dest='random_generation_seed', type=int, default=42,
                     help='Random seed for consistent generation.')

if __name__ == '__main__':
    _config = _parser.parse_args()

    model_ids = list(range(_config.cad_data_generation_start_cycle, _config.cad_data_generation_end_cycles))
    num_workers = 18

    print(f"🔧 Starte parallele Datengenerierung mit {num_workers} Prozessen ...")

    with Pool(num_workers) as pool:
        pool.map(run_single_model, [(model_id, _config) for model_id in model_ids])

    print("✅ Datengenerierung abgeschlossen.")
