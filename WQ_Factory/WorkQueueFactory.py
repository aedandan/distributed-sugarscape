import subprocess
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 WorkQueueFactory.py manager_name")
        sys.exit(1)
    manager_name = sys.argv[1]
    subprocess.run(["work_queue_factory", "-T", "condor", "-M", manager_name])