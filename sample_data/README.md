# Load Data Script for Crude Oil Imports

# Description
This script loads the US crude oil import dataset (data.csv), located in the same folder into the PostgreSQL database via the FastAPI server you have already setup.
The FastAPI server needs to be running for this script to work. If it is not running, please follow the `README.md` file in the root of the project to set it up and run it. 
## Assumptions
1. API Endpoint: The script assumes the API endpoint is http://0.0.0.0:5321/crude-oil-imports/bulk.  Ensure this is correct for your environment.  The script sends a POST request to this endpoint.
2. This script loads in a batch of `10000` by default, if you want to change it, you can tweak `batch_size` variable in the code.

### Setup
Use the same virtual environment for the FastAPI server or install `httpx` module separately.
    
```bash
    cd <project_directory>
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
  ```
OR

```bash    
    pip install httpx
```

# Run the code

```bash
cd sample_data/
python3 load_data.py
```