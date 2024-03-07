import ndcctools.work_queue as WorkQueue; 
import os
import sys
import signal
import re
from typing import List
from typing import Dict

def getSeeds() -> Dict[str, List[str]]:
    all_files = os.listdir("{}/../data".format(os.getcwd()))

    seeds_list = [file for file in all_files if file.endswith(".config")]
    seed_groups: Dict[str, List[str]] = {}
    for seed in seeds_list:
        seed_trimmed = seed.split('.')[0]
        decision_model = re.split(r'\d+', seed_trimmed)[0]
        if (decision_model not in seed_groups):
            seed_groups[decision_model] = [seed_trimmed]
        else:
            seed_groups[decision_model].append(seed_trimmed)
    return seed_groups
    
def interruptHandler(signal, frame):
    print("Keyboard Interrupt Read! Shutting down...")
    sys.exit(0)

# Function that times runs of a decision model based on the list of seeds passed in
def timeSeeds(seeds: List[str], WorkQueue: WorkQueue):
    for file in seeds_trimmed :
        command = f"python3 sugarscape.py --conf {file}.config > {file}.json"
        task = WorkQueue.Task(command)
        task.specify_input_file("../sugarscape.py", "sugarscape.py", cache = True)
        task.specify_input_file(f"../data/{file}.config", f"{file}.config", cache = True)
        task.specify_input_file(f"../agent.py", "agent.py", cache = True)
        task.specify_input_file(f"../disease.py", "disease.py", cache = True)
        task.specify_input_file(f"../cell.py", "cell.py", cache = True)
        task.specify_input_file(f"../environment.py", "environment.py", cache = True)
        task.specify_input_file(f"../ethics.py", "ethics.py", cache = True)
        task.specify_output_file(f"{file}.json", f"{file}.json", cache = False)
        print(f"Task submitted: python3 sugarscape.py --conf {file}.config\n")
        WorkQueue.submit(task)

    while not WorkQueue.empty() :
        t = WorkQueue.wait()
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

seeds_list = getSeeds()
print(seeds_list)


# try:
#     q = wq.WorkQueue(name="sugarscape", debug_log = "my.debug.log", transactions_log="my.transaction.log", port=9125)
# except Exception :
#     print("Could not activate Work Queue: ", sys.exception())
