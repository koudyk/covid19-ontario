# covid19-ontario
Tracking COVID-19 cases in Ontario, in each regional Public Health Unit. 

## Running the notebook
### Run it virtually on Binder (recommended for non-programmers)
1. Open the notebook here: [https://mybinder.org/v2/gh/koudyk/covid19-ontario/master?filepath=covid-ontario.ipynb](https://mybinder.org/v2/gh/koudyk/covid19-ontario/master?filepath=covid-ontario.ipynb)
2. Wait for it to build (it needs to install the package requirements)
3. Run the notebook by selecting Cell > Run All


### Run it locally
Run the following commands in your terminal (i.e., copy and paste the `shaded words` into your terminal). Note that this only works in a unix-based system (should work on Mac or Linux with Python3)
1. Get to project directory: `cd /path/to/repo`
2. Create a virtual python environment: `python3 -m venv venv`
3. Activate the environment: `source venv/bin/activate`
4. Install the requirements: `xargs -L 1 pip install < requirements.txt`
5. Run the notebook: `jupyter notebook covid-ontario.ipynb`
