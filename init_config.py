import configparser

config = configparser.ConfigParser()



config['PATH LIST'] = {
        'cifdir':'cifdir/pcod_1000',
        'database-path':'database'
}

config['CALCULATION'] = {
        'adjacent_num':2,
        'adjacency_algorithm':'neib',
        'max_neib':'{"Si":4,"O":2}',
        'n_jobs':-1,
        'method':'mean',
        'target_atoms':'["Si1","O1"]',
        'reference':1e-8,
        'sep_value':0.5,
        'offset':5,
        'use_mesh_flag':'True'
}   

with open('config', 'w') as file:
    config.write(file)