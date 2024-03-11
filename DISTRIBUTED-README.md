DISTRIBUTED SUGARSCAPE

A distributed version of Sugarscape introduced in Growing Artificial Societies (1996) by Epstein and Axtell as written by Dr. Nate Kremer-Herman and their collaborators:

Copyright:
Nate Kremer-Herman, Seattle University

Contributors:
Ankur Gupta
Colin Hanrahan
Willem Hueffed
Nate Kremer-Herman
Maria Milkowski
Joshua Palicka
Mariana Shuman
Lucas Vorkoper

Attribution:
Herve Lange (https://github.com/langerv/sugarscape)
Joshua Palicka (https://github.com/joshuapalicka/sugarscape)

This program is a Python implementation of a Work Queue manager-worker application using Work Queue's API bindings. 

Requirements:
Bash
Python3
Miniconda
CCTools Work Queue (Python API)
CCTools Poncho 

Installation:

If you do not already have Miniconda installed on your machine, please run the following commands to install it (or run the assocated Make command):

mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

And then:
~/miniconda3/bin/conda init bash

Note that the previous line requires closing and re-opening a terminal for
correct behavior.

If you do not already have CCTools installed on your machine, please run the following commands to install it (assumes Miniconda installation):

conda create -n cctools-env -y -c conda-forge --strict-channel-priority python ndcctools

conda activate cctools-env 

Alternatively, run the assocated Make command specified later in this document. If that command fails, these commands are confirmed to work when run individually.

Note: the last line above is required once every session to establish the cctools environment and guarantee correct behavior.

Finally, if you do not have a copy of Sugarscape,
please run the following commands to clone it:

git clone git@github.com:nkremerh/sugarscape.git

Or similar git clone command for HTTPS.

When all of the above are installed, move the folders "work_queue_manager"
and "WQ_Factory" into the top level directory of Sugarscape.

Deployment:

The manager program cannot spin up Work Queue workers on its own. It requires a login on a separate endpoint where HTCondor or SLURM are installed. Once logged into an endpoint of this nature, run the associated Make command for activating workers. 

Once workers are active, use the following instructions to determine how best to run the program.

To run the Python script that activates the Work Queue manager process and submit tasks to live work queue workers (assuming they are already active):

python3 SugarscapeFactory.py -s [the number of seeds per decision model] > [name of your output file]

Where the number of seeds per decision model is number specified in the Sugarscape config.json file. These must match in order to produce accurate timing data for the program.

If there are issues with Work Queue commands not getting recognized, please confirm that cctools was installed correctly and that the env is set to "cctools-env".

Alternatively, confirm that the number of seeds specified in the Sugarscape config.json file is 50 and simply run the "make distributed_data" command specified above.

Makefile Options:

make clean
    Clean up working files and logs created by the software.
    Note: will remove any JSON files created by the other make options.

make slurm_factory
    Run the Python script that spins up Work Queue workers on a compute node that has an installation of the SLURM batch job execution engine. This will run on a terminal until a keyboard interrupt (Control-C) is received.

make condor_factory 
    Run the Python script that spins up Work Queue workers on a compute node that has an installation of the HTCondor batch job execution engine. This will run on a terminal until a keyboard interrupt (Control-C) is received.

make install_conda
    Run the conda installation commands as specified above. 

make install_cctools
    Run the CCTools installation commands as specified above.

make distributed_data
    Run the Python script that submits tasks to live Work Queue workers. Note that this command redirects all output to the associated output file provided in the makefile. If seeing output to the console is desired, run the Makefile option labeled "distributed_data_console".

make distributed_data_console
    Run the Python script that submits tasks to live Work Queue workers. Note that this command prints all output to the console. If saving output to a file is desired, run the Makefile option labeled "distributed_data".

make distributed_data_group
    Run the Python script that submits tasks to live Work Queue workers. Note that this command redirects all output to the associated output file provided in the makefile. If seeing output to the console is desired, run the Makefile option labeled "distributed_data_console".

make distributed_data_console_group
    Run the Python script that submits tasks to live Work Queue workers. Note that this command redirects all output to the associated output file provided in the makefile. If seeing output to the console is desired, run the Makefile option labeled "distributed_data_console". Groups jobs by decision model type.