# EvoSim
> Agent-based simulator of Evolutionary Dynamics 

Try to stick to the guidelines mentioned in [The Hitchhiker’s Guide to Python](http://docs.python-guide.org/en/latest/)

## Installation
The usage of virtual environments is recommended in order to create isolated Python environments and 
avoid version conflicts with other projects!

0. Ensure to have virtualenv installed:
`pip install virtualenv`
1. Set-up a virtual environment (recommended interpreter: Python 3.6.4):
`virtualenv evosim`
or 
`virtualenv -p <PATH_TO_PREFERRED_INTERPRETER> evosim`
2. Activate the virtual environment: `source $PROJECT_ROOT/venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

## Documentation
Important methods are documented using reST docstrings.
We do not build separate docs yet, but in the future, we might consider to integrate Sphinx.
