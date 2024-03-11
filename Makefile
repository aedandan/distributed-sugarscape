CONFIG = config.json
DATACHECK = data/data.complete
PLOTCHECK = plots/plots.complete
DISTRIBUTED_OUTPUT = sugarscape_distributed_timing.txt
CONDA_ACTIVATE = source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

DATASET = $(DATACHECK) \
		data/*[[:digit:]]*.config \
		data/*.json \
		data/*.sh

PLOTS = $(PLOTCHECK) \
		plots/*.dat \
		plots/*.pdf \
		plots/*.plg

CLEAN = log.json \
		$(DATASET) \
		$(PLOTS) \
		$(DISTRIBUTED_OUTPUT)


# Change to python3 (or other alias) if needed
PYTHON = python
PYTHON3 = python3
SUGARSCAPE = sugarscape.py
FACTORY = WorkQueueFactory.py
FACTORY_FOLDER = WQ_Factory
MANAGER_NAME = sugarscape_osg_stampede3_v2
CONDOR = condor
SLURM = slurm

# Check for local Bash and Python aliases
BASHCHECK = $(shell which bash > /dev/null; echo $$?)
PYCHECK = $(shell which python > /dev/null; echo $$?)
PY3CHECK = $(shell which python3 > /dev/null; echo $$?)

$(DATACHECK):
	cd data && $(PYTHON) run.py --conf ../$(CONFIG)
	touch $(DATACHECK)

$(PLOTCHECK): $(DATACHECK)
	cd plots && $(PYTHON) plot.py --path ../data/ --conf ../$(CONFIG) --outf data.dat
	touch $(PLOTCHECK)

all: $(DATACHECK) $(PLOTCHECK)

data: $(DATACHECK)

plots: $(PLOTCHECK)

seeds:
	cd data && $(PYTHON) run.py --conf ../$(CONFIG) --seeds

condor_factory:
	cd $(FACTORY_FOLDER) && $(PYTHON3) $(FACTORY) $(MANAGER_NAME) $(CONDOR)

slurm_factory:
	cd $(FACTORY_FOLDER) && $(PYTHON3) $(FACTORY) $(MANAGER_NAME) $(SLURM)

install_conda:
	mkdir -p ~/miniconda3 &&
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh &&
	bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 &&
	rm -rf ~/miniconda3/miniconda.sh &&
	~/miniconda3/bin/conda init bash

install_cctools:
	conda create -n cctools-env -y -c conda-forge --strict-channel-priority python ndcctools

cctools_env: install_cctools
	$(CONDA_ACTIVATE) cctools-env

distributed_data_group: seeds cctools_env
	python3 SugarscapeFactory.py -s 50 > $(DISTRIBUTED_OUTPUT)

distributed_data_console: seeds cctools_env
	python3 SugarscapeFactory.py -s 50

distributed_data_group: seeds cctools_env
	python3 SugarscapeFactoryDecisionModelRuntime.py -s 50 > $(DISTRIBUTED_OUTPUT)

distributed_data_console_group: seeds cctools_env
	python3 SugarscapeFactoryDecisionModelRuntime.py -s 50


setup:
	@echo "Checking for local Bash and Python installations."
ifneq ($(BASHCHECK), 0)
	@echo "Could not find a local Bash installation."
	@echo "Please update the Makefile and configuration file manually."
else
	@echo "Found alias for Bash."
endif
ifeq ($(PY3CHECK), 0)
	@echo "Found alias for Python."
	sed -i 's/PYTHON = python$$/PYTHON = python3/g' Makefile
	sed -i 's/"python"/"python3"/g' $(CONFIG)
else ifneq ($(PYCHECK), 0)
	@echo "Could not find a local Python installation."
	@echo "Please update the Makefile and configuration file manually."
else
	@echo "This message should never be reached."
endif

test:
	$(PYTHON) $(SUGARSCAPE) --conf $(CONFIG)

clean:
	rm -rf $(CLEAN) || true

lean:
	rm -rf $(PLOTS) || true

.PHONY: all clean data lean plots setup

# vim: set noexpandtab tabstop=4:
