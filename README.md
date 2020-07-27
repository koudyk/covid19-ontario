# covid19-ontario
Tracking COVID-19 cases in Ontario

## Running the notebook
### Run it virtually on Binder (recommended)
1. Open the notebook here: [https://hub.gke.mybinder.org/user/koudyk-covid19-ontario-1uhteuab/notebooks/covid-ontario.ipynb](https://hub.gke.mybinder.org/user/koudyk-covid19-ontario-1uhteuab/notebooks/covid-ontario.ipynb)
2. Wait for it to build (it needs to install the package requirements)
3. Run the notebook by selecting Cell > Run All


### Run it locally
1. Get to project directory: `cd /path/to/repo`
2. Create a virtual python environment: `python3 -m venv venv`
3. Activate the environment: `source venv/bin/activate`
4. Install the requirements: `xargs -L 1 pip install < requirements.txt`
5. Run the notebook: `jupyter notebook covid-ontario.ipynb`
