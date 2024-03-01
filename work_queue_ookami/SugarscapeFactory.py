import ndcctools.work_queue as wq; 
import os

def getFiles() :
    all_files = os.listdir(os.getcwd())

    # Filter files that start with "meow"
    combined_books_list = [file for file in all_files if file.startswith("combined_books")]
    return combined_books_list

try:
    q = wq.WorkQueue(name="bhau")
   
except:
    print("Could not do it")
workers =  wq.Factory(batch_type="slurm", manager_name="bhau")
workers.workers_per_cycle = 200
workers.max_workers = 2000
workers.min_workers = 200
workers.batch_options = "--partition=short"
combined_book_list = getFiles()
print(len(combined_book_list))

with workers:
    i = 0
    for file in combined_book_list :
        command = f"python3 WordCounter.py {file} {i} > word_frequency_{i}.txt"
        task = wq.Task(command)
        task.specify_input_file("WordCounter.py", "WordCounter.py", cache = True)
        task.specify_input_file(file, file, cache = True)
        task.specify_input_file("test-env.sh", "test-env.sh", cache = True)
        task.specify_output_file(f"word_frequency_{i}.txt", f"word_frequency_{i}.txt", cache = True)
        q.submit(task)
        i += 1

    while not q.empty() :
        t = q.wait(100)
        if t:
            print("Task {} has returned!".format(t.id))

            if t.return_status == 0:
                print("command exit code:\n{}".format(t.return_status))
                print("stdout:\n{}".format(t.output))
            else:
                print("There was a problem executing the task.")
        else:
            print("nada")