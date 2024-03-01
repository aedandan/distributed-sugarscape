import ndcctools.work_queue as wq; 
import os

def getFiles() :
    # TODO: Change this to a function call later, for portability
    all_files = os.listdir("/lustre/home/aemccall/sugarscape-ookami/data")

    seeds_list = [file for file in all_files if file.endswith(".config")]
    return seeds_list

try:
    q = wq.WorkQueue(name="sugarscape_port")
   
except:
    print("Could not do it")
workers =  wq.Factory(batch_type="slurm", 
                      manager_name="sugarscape_port")
# TODO: Figure out 
# Pieces of information we need to determine the correct partition:
# 1. How long does a job take on average? (Rough estimate)
# 2. How many workers do we want to run at once?
workers.workers_per_cycle = 20
workers.max_workers = 20
workers.min_workers = 1
workers.batch_options = "--partition=short"
seeds_list = getFiles()
seeds_trimmed = []
for file in seeds_list :
        file_trimmed = file.split('.')[0]
        seeds_trimmed.append(file_trimmed)
print(seeds_trimmed)

with workers:
    for file in seeds_list :
        file_trimmed = file.split(".")
        command = f"python3 ../sugarscape.py --conf {file}"
        task = wq.Task(command)
        task.specify_input_file("../sugarscape.py", "sugarscape.py", cache = True)
        task.specify_input_file(f"../data/{file}", file, cache = True)
        task.specify_output_file(f"../data/{file}.json", f"{file}.json", cache = True)
        q.submit(task) 

    while not q.empty() :
        t = q.wait()
        if t:
            print("Task {} has returned!".format(t.id))

            if t.return_status == 0:
                print("command exit code:\n{}".format(t.return_status))
                print("stdout:\n{}".format(t.output))
            else:
                print("There was a problem executing the task.")
        else:
            print("nada")