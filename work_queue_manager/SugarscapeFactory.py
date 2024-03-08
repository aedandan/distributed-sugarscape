import ndcctools.work_queue as WorkQueue; 
import os
import sys
import signal
import re
import time
import getopt
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
def timeSeeds(seeds: List[str], WorkQueue: WorkQueue) -> float:
    jobs_start = time.time()
    for file in seeds:
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

    while not WorkQueue.empty():
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
            print("No task generated.")
    jobs_end = time.time() - jobs_start
    return jobs_end

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
    print(arguments)
    return arguments[0][1]

def printUsage():
    print("USAGE: python3 SugarscapeFactory.py -s [number of seeds per decision model]")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, interruptHandler)
    try:
        q = WorkQueue.WorkQueue(name="sugarscape", debug_log = "debug.sugarscape.distrib.log", 
                                transactions_log="transaction.sugarscape.distrib.log", port=9125)
        q.activate_fast_abort(2)
    except Exception :
        print("Could not activate Work Queue: ", sys.exception())

    all_sugarscape_seeds = getSeeds()
    number_of_seeds = readCommandLineArguments()
    print(number_of_seeds)
    decision_model_times = {}
    total_decision_model_time = 0
    # for decision_model in all_sugarscape_seeds:
    #     decision_model_simulation_duration = timeSeeds(all_sugarscape_seeds[decision_model], q)
    #     decision_model_times[decision_model] = decision_model_simulation_duration
    #     total_decision_model_time += decision_model_simulation_duration
    #     average_duration_per_simulation = decision_model_simulation_duration / number_of_seeds
    #     print("{} took {} seconds to run all simulations, with an average of {} per simulation"
    #           .format(decision_model, decision_model_simulation_duration, average_duration_per_simulation))
    sys.exit(0)
    