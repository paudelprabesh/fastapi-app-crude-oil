# FastAPI server for creating, retrieving, updating and deleting US crude oil import dataset 

This project provides a FastAPI application that allows you to manage a dataset of US crude oil imports.  
You can use it to create, retrieve, update, and delete records in the dataset.

### Features

* **Create:** Add new crude oil import records to the database.

* **Retrieve:**

    * List all crude oil import records, in paginated form, allowing you to process large datasets efficiently

    * Retrieve a specific record by its UUID.

* **Update:** Modify an existing crude oil import record.

* **Delete:** Remove a crude oil import record from the database.

* **Filter:** Retrieve records based on specific criteria (e.g., year, originName).

### Prerequisites
1. **Python**: Please visit https://wiki.python.org/moin/BeginnersGuide/Download to get python installed.
2. **PostgresSQL**: Please use the `docker-compose.yml` to run the postgres container (instructions below). 
   See [Install Docker engine](https://docs.docker.com/engine/install/) or 
    [Install Docker Desktop](https://docs.docker.com/desktop/) guide for installing docker.
    **OR**
 [Visit postgres install guide](https://www.postgresql.org/download/) to download and run a postgres server locally on 
port 5342.

### Setup
1. **Clone the repository:**

    ```bash
    git clone https://github.com/paudelprabesh/fastapi-app-crude-oil.git
    cd fastapi-app-crude-oil
    ```
2. **Create a virtual environment (Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Setup postgres:** 
    The docker compose file is already setup to run the postgres container on port 5432.
    username and password can be found in the `docker-compose.yml` file. 
    ```bash
    docker compose up -d
    ```

5. **Run the application:**

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 5321
    ``` 

### Load dataset

`sample_data/` has the crude oil data and the script `load_data.py` which can be used to load the data.csv into the
postgres db. Instructions on how to use it are in the `Readme.md` within the same directory.

### Experiment

Visit the [swagger UI](http://0.0.0.0:5321/docs#) to add, retrieve, update, delete US crude oil import records.
