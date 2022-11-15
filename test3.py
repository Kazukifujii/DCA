from subprocess import run

run('python3 make_dataset_randzeo.py',shell=True)
run('python3 test.py',shell=True)