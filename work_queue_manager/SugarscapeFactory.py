import ndcctools.work_queue as wq; 
import os
import sys
import signal

def getFiles() :
    # TODO: Change this to a function call later, for portability
    all_files = os.listdir("{}/../data".format(os.getcwd()))

    seeds_list = [file for file in all_files if file.endswith(".config")]
    return seeds_list
    
def interruptHandler(signal, frame, wq: wq):
    print("Keyboard Interrupt Read! Shutting down...")
    wq.work_queue_shut_down_workers(0)
    sys.exit(0)

try:
    q = wq.WorkQueue(name="sugarscape", debug_log = "my.debug.log", transactions_log="my.transaction.log", port=9125)
except Exception :
    print("Could not activate Work Queue: ", sys.exception())
# workers =  wq.Factory(batch_type="slurm", manager_name="sugarscape_no_batch")
# TODO: Figure out 
# Pieces of information we need to determine the correct partition:
# 1. How long does a job take on average? (Rough estimate)
# 2. How many workers do we want to run at once?

# signal.signal(signal.SIGINT, interruptHandler)
# workers.workers_per_cycle = 10
# workers.max_workers = 32
# workers.memory = 25600
# workers.cores = 3
# workers.batch_options = "--partition=short"
seeds_list = getFiles()
seeds_trimmed = []
for file in seeds_list :
        file_trimmed = file.split('.')[0]
        seeds_trimmed.append(file_trimmed)
print(seeds_trimmed)

for file in seeds_trimmed :
    command = f"python3 sugarscape.py --conf {file}.config > {file}.json"
    task = wq.Task(command)
    task.specify_input_file("../sugarscape.py", "sugarscape.py", cache = True)
    task.specify_input_file(f"../data/{file}.config", f"{file}.config", cache = True)
    task.specify_input_file(f"../agent.py", "agent.py", cache = True)
    task.specify_input_file(f"../disease.py", "disease.py", cache = True)
    task.specify_input_file(f"../cell.py", "cell.py", cache = True)
    task.specify_input_file(f"../environment.py", "environment.py", cache = True)
    task.specify_input_file(f"../ethics.py", "ethics.py", cache = True)
    task.specify_output_file(f"{file}.json", f"{file}.json", cache = False)
    # task.specify_priority(20000000)
    # task.specify_cores(1)
    # task.specify_max_retries(3)
    print(f"Task submitted: python3 sugarscape.py --conf {file}.config\n")
    q.submit(task)

while not q.empty() :
    t = q.wait()
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