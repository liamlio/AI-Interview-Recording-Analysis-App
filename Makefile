# Set up development environment
env:
	conda create -n hack python==3.9
	conda activate hack

.PHONY: install
# Install in your current Python environment
install:
	pip install -r requirements.txt
	pip install st-annotated-text-custom/
	pip install vindent_utils/
