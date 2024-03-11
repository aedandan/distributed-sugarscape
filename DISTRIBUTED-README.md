DISTRIBUTED SUGARSCAPE

Python implementation of a Work Queue manager-worker application using Work Queue's API. 

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

Alternatively, or run the assocated Make command specified later in this document

Note: the last line above is required once every session to establish the cctools environment and guarantee correct behavior.

Finally, if you do not have a copy of Sugarscape,
please run the following commands to clone it:

git clone git@github.com:nkremerh/sugarscape.git

Or similar git clone command for HTTPS.

When all of the above are installed, move the folders "work_queue_manager"
and "WQ_Factory" into the top level directory of Sugarscape.

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

To run the Python script that activates the Work Queue manager process and submit tasks to live work queue workers (assuming they are already active) run:

python3 SugarscapeFactory.py -s [the number of seeds per decision model]

Where the number of seeds per decision model is number specified in the Sugarscape config.json file. These must match in order to produce accurate timing data for the program.
