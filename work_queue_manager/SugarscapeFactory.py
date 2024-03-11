import ndcctools.work_queue as WorkQueue; 
import os
import sys
import signal
import re
import time
import getopt
from typing import List
from typing import Dict


all_decision_models = []
def getSeeds() -> Dict[str, List[str]]:
    all_files = os.listdir("{}/../data".format(os.getcwd()))

    seeds_list = [file for file in all_files if file.endswith(".config")]
    print("All seeds: ", seeds_list)
    seed_groups: Dict[str, List[str]] = {}
    for seed in seeds_list:
        seed_trimmed = seed.split('.')[0]
        decision_model = re.split(r'\d+', seed_trimmed)[0]
        all_decision_models.append(seed_trimmed)
        if (decision_model not in seed_groups):
            seed_groups[decision_model] = [seed_trimmed]
        else:
            seed_groups[decision_model].append(seed_trimmed)
    
    return seed_groups
    
def interruptHandler(signal, frame):
    print("Keyboard Interrupt Read! Shutting down...")
    sys.exit(0)

def run_simulations(seed_groups: Dict[str, List[str]], wq: WorkQueue) :
    time_dictionary = {}
    decision_model_names = seed_groups.keys()
    jobs_start = time.time()
    jobs_end = 0
    for file in all_decision_models:
        command = f"python3 sugarscape.py --conf {file}.config > {file}.json"
        task = WorkQueue.Task(command)
        task.specify_input_file("../sugarscape.py", "sugarscape.py", cache = False)
        task.specify_input_file(f"../data/{file}.config", f"{file}.config", cache = False)
        task.specify_input_file(f"../agent.py", "agent.py", cache = False)
        task.specify_input_file(f"../disease.py", "disease.py", cache = False)
        task.specify_input_file(f"../cell.py", "cell.py", cache = False)
        task.specify_input_file(f"../environment.py", "environment.py", cache = False)
        task.specify_input_file(f"../ethics.py", "ethics.py", cache = False)
        task.specify_output_file(f"{file}.json", f"{file}.json", cache = False)
        task.specify_tag(file)
        print(f"Task submitted: python3 sugarscape.py --conf {file}.config\n")
        wq.submit(task)

    while not wq.empty():
        t = wq.wait()
        if t:
            print("Task {} has returned!".format(t.tag))
            print(f"Task has returned with status {t.return_status}")
            print(f"output is {t.output}")
            if t.return_status == 0:
                print("command exit code:\n{}".format(t.return_status))
                print("stdout:\n{}".format(t.output))
            else:
                print("There was a problem executing the task.")
        else:
            print("No task generated.")
        jobs_end = time.time() - jobs_start
        task_tag = t.tag
        
        for decision_model in decision_model_names:
            if decision_model in task_tag :
                if decision_model in time_dictionary:
                    time_dictionary[decision_model] += jobs_end
                else:
                    time_dictionary[decision_model] = jobs_end
                
    return time_dictionary


def readCommandLineArguments() -> int:
    commandLineArgs = sys.argv[1:]
    short_options = 's:'
    long_options = "--seeds"
    try:
        arguments, values = getopt.getopt(commandLineArgs, shortopts=short_options, longopts=long_options)
    except getopt.GetoptError as error:
        print(error)
        printUsage()
    if len(arguments) != 1 or arguments[0][0] not in("-s", "--seeds"):
        printUsage()
    return arguments[0][1]

def printUsage():
    print("USAGE: python3 SugarscapeFactory.py -s [number of seeds per decision model]")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, interruptHandler)
    try:
        q = WorkQueue.WorkQueue(name="sugarscape_osg_stampede3_v2", debug_log = "debug.sugarscape.distrib.log", 
                                transactions_log="transaction.sugarscape.distrib.log", port=9125)
        q.activate_fast_abort(3)
    except Exception :
        print("Could not activate Work Queue: ", sys.exception())

    all_sugarscape_seeds = getSeeds()
    number_of_seeds = readCommandLineArguments()
    decision_model_times = {}
    decision_model_simulation_duration = run_simulations(all_sugarscape_seeds, q)
    all_simulations_time = 0
    for key in decision_model_simulation_duration.keys():
        all_simulations_time += decision_model_simulation_duration[key]
        single_model_avg_time = decision_model_simulation_duration[key] / float(number_of_seeds)
        print(f"Decision model {key} took {decision_model_simulation_duration[key]} seconds to run, with an average of {single_model_avg_time} seconds")
    average_duration_per_simulation = all_simulations_time / (float(number_of_seeds) * len(decision_model_simulation_duration.keys()))
    print("Sugarscape took {} seconds to run in total. Each task on an average took {} seconds".format(all_simulations_time, average_duration_per_simulation))
    sys.exit(0)
    