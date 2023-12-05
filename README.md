# autoTrack

Set up:
- In order to install conda follow the steps in the documentation [here](https://conda.io/projects/conda/en/latest/user-guide/install/windows.html)
- Setup python 3.10 environment using conda 
    - `conda create -n darts -y python=3.10`
    - `conda activate darts`
- Clone autotracker and install dependencies
    - `git clone -b develop https://github.com/pratiksha-pai/autoTrack.git`
    - `cd autoTrack`
    - `pip install -r requirements.txt`
- Navigate to the folder that contains code
    - `cd acquire_images`
- Run the main script 
    - `python main.py`