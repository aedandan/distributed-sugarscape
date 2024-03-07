import subprocess

subprocess.run(["work_queue_factory", "-T", "condor", "-M", "osgtest", "--poncho-env=package.tar.gz"])