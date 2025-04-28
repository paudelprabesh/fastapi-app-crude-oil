# FastAPI server for creating, retrieving, updating and deleting US crude oil import dataset 

This project provides a FastAPI application that allows you to manage a dataset of US crude oil imports.  
You can use it to create, retrieve, update, and delete records in the dataset.

### Features

* **Retrieve:**

    * **Get Paginated Crude Oil Imports:** Retrieves a list of crude oil import records in paginated form. This allows for efficient processing of large datasets by returning data in smaller, manageable chunks.
        * Endpoint: `GET /crude-oil-imports/`
        * Status Code: 200 OK

    * **Get Crude Oil Imports by UUID:** Retrieves a specific crude oil import record using its unique identifier (UUID).
        * Endpoint: `GET /crude-oil-imports/{uuid}`
        * Status Code: 200 OK
* **Create:**

    * **Insert Crude Oil Import:** Adds a new crude oil import record to the database.
        * Endpoint: `POST /crude-oil-imports/`
        * Status Code: 201 Created
    * **Insert Bulk Crude Oil Imports:** Adds multiple crude oil import records to the database in a single request.
        * Endpoint: `POST /crude-oil-imports/bulk`
        * Status Code: 201 Created
* **Update:**

    * **Patch Crude Oil Import by UUID:** Modifies specific fields of an existing crude oil import record identified by its UUID.  This performs a partial update.
        * Endpoint: `PATCH /crude-oil-imports/{uuid}`
        * Status Code: 200 OK
    * **Update Crude Oil Import by UUID:** Replaces the entire content of an existing crude oil import record with new data.
        * Endpoint: `PUT /crude-oil-imports/{uuid}`
        * Status Code: 200 OK
* **Delete:**
    * **Delete Crude Oil Import by UUID:** Removes a crude oil import record from the database using its UUID.
        * Endpoint: `DELETE /crude-oil-imports/{uuid}`
        * Status Code: 200 OK

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
Swagger allows you to view request types and all very easily.

### Notes:
1. `UUID`: UUIDs are used to identify each records. Instead of relying on the database's auto-generated integer IDs, we use `UUID` and hide 
database id from the client, which is very easy to mess up. 
For example: A mistaken id for a delete query, deletes a record. It also hides database primary key and how they are setup.
2. `Null values`: For simplicity, we don't allow null values to any records. A quick glance showed that there were no nulls
in the provided dataset, and hence assumed it to simplify design.