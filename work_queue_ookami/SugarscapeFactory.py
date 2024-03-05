import ndcctools.work_queue as wq; 
import os
import sys

def getFiles() :
    # TODO: Change this to a function call later, for portability
    all_files = os.listdir("/lustre/home/aemccall/sugarscape-ookami/data")

    seeds_list = [file for file in all_files if file.endswith(".config")]
    return seeds_list

try:
    q = wq.WorkQueue(name="sugarscape_port_v2", debug_log = "my.debug.log", transactions_log="my.transaction.log")
    #q.specify_max_resources({'cores': 8, 'memory':  16384})
except Exception :
    print("Could not activate Work Queue: ", sys.exception())
workers =  wq.Factory(batch_type="slurm", 
                      manager_name="sugarscape_port_v2")
# TODO: Figure out 
# Pieces of information we need to determine the correct partition:
# 1. How long does a job take on average? (Rough estimate)
# 2. How many workers do we want to run at once?

workers.workers_per_cycle = 20
workers.max_workers = 200
workers.min_workers = 20
workers.memory = 16384
workers.batch_options = "--partition=short"
seeds_list = getFiles()
seeds_trimmed = []
for file in seeds_list :
        file_trimmed = file.split('.')[0]
        seeds_trimmed.append(file_trimmed)
print(seeds_trimmed)

with workers:
    for file in seeds_trimmed :
        command = f"python3 sugarscape.py --conf {file}.config"
        task = wq.Task(command)
        task.specify_input_file("sugarscape.py", "sugarscape.py", cache = True)
        task.specify_input_file(f"./data/{file}.config", f"{file}.config", cache = True)
        task.specify_input_file(f"agent.py", "agent.py", cache = True)
        task.specify_input_file(f"disease.py", "disease.py", cache = True)
        task.specify_input_file(f"cell.py", "cell.py", cache = True)
        task.specify_input_file(f"environment.py", "environment.py", cache = True)
        task.specify_input_file(f"ethics.py", "ethics.py", cache = True)
        task.specify_output_file(f"{file}.json", f"{file}.json", cache = False)
        q.submit(task) 

    while not q.empty() :
        t = q.wait()
        worker_summary = q.worker_summary()
        for w in worker_summary:
            print("{} workers with: {} cores, {} MB memory, {} MB disk".format(w.workers, w.cores, w.memory, w.disk))
        if t:
            print("Task {} has returned!".format(t.id))
            print(f"Task has returned with status {t.return_status}")
            print(f"output is {t.output}")
            if t.return_status == 0:
                print("command exit code:\n{}".format(t.return_status))
                print("stdout:\n{}".format(t.output))
            else:
                print("There was a problem executing the task.")
        else:
            print("nada")