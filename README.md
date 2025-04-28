# FastAPI server for creating, retrieving, updating and deleting US crude oil import dataset 

This project provides a FastAPI application that allows you to manage a dataset of US crude oil imports.  
You can use it to create, retrieve, update, and delete records in the database.


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

Visit the [swagger UI](http://0.0.0.0:5321/docs#) http://0.0.0.0:5321/docs# to add, retrieve, update, delete US crude oil import records.
Swagger allows you to view request types and all very easily.

### Design Notes:
1. `UUID`: UUIDs are used to identify each records. Instead of relying on the database's auto-generated integer IDs, we use `UUID` and hide 
database id from the client, which is very easy to mess up. 
For example: A mistaken id for a delete query, deletes a record. It also hides database primary key and how they are setup.
2. `Null values`: For simplicity, we don't allow null values to any records. A quick glance showed that there were no nulls
in the provided dataset, and hence assumed it to simplify design.
3. `year and month`. In addition to being `int`, they also need to be inbetween a certain range to be valid.
Year should be between `1900` and `2100`, and month should be in range of `1` and `12`.
4. `quantity`: `quantity` must be a positive integer.

### Sample API usage:

I highly recommend using swagger UI http://0.0.0.0:5321/docs# to experiment on the endpoints.
Each endpoint is documented with sample request and response there. Here, I have listed quick urls or curl commands that can be 
used to do CRUD operations.

### Retrieve:
    
  * **Get Paginated Crude Oil Imports:** Retrieves a list of crude oil import records in paginated form. This allows for efficient processing of large datasets by returning data in smaller, manageable chunks.
      * Endpoint: `GET /crude-oil-imports/`
      * Status Code: 200 OK
      * Sample request: http://0.0.0.0:5321/crude-oil-imports/?skip=0&limit=2
      * Sample response:
      * ```json
        {
            "status": 201,
            "message": "Success",
            "data": {
              "metadata": {
                "skip": 0,
                "limit": 2,
                "total": 483056
              },
              "paginated_data": [
                {
                  "year": 2009,
                  "month": 1,
                  "originName": "Belize",
                  "originTypeName": "Country",
                  "destinationName": "EXXONMOBIL REFINING & SPLY CO / BEAUMONT / TX",
                  "destinationTypeName": "Refinery",
                  "gradeName": "Light Sour",
                  "quantity": 61,
                  "uuid": "6ca3c2e0-a6e1-4c50-a278-3ac51bc713a7"
                },
                {
                  "year": 2009,
                  "month": 1,
                  "originName": "Belize",
                  "originTypeName": "Country",
                  "destinationName": "FLINT HILLS RESOURCES LP / WEST / TX",
                  "destinationTypeName": "Refinery",
                  "gradeName": "Light Sour",
                  "quantity": 62,
                  "uuid": "3714f2a5-6d37-4459-b939-a535bf34bc4a"
                }
              ]
            }
        }
         ```

    * **Get Crude Oil Imports by UUID:** Retrieves a specific crude oil import record using its unique identifier (UUID).
        * Endpoint: `GET /crude-oil-imports/{uuid}`
        * Status Code: 200 OK
        * Sample request: http://0.0.0.0:5321/crude-oil-imports/6ca3c2e0-a6e1-4c50-a278-3ac51bc713a7
        * Sample response: 
        ```json
        {
           "status": "200",
           "message": "Success",
           "data": {
               "year": 2009,
               "month": 1,
               "originName": "Belize",
               "originTypeName": "Country",
               "destinationName": "EXXONMOBIL REFINING & SPLY CO / BEAUMONT / TX",
               "destinationTypeName": "Refinery",
               "gradeName": "Light Sour",
               "quantity": 61,
               "uuid": "6ca3c2e0-a6e1-4c50-a278-3ac51bc713a7"
          }
        }
         ```
### Create:

  * **Insert Crude Oil Import:** Adds a new crude oil import record to the database.
      * Endpoint: `POST /crude-oil-imports/`
      * Status Code: `201` Created
      * Sample request:
      ```bash 
    curl -X 'POST' \
      'http://0.0.0.0:5321/crude-oil-imports/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "year": 2000,
      "month": 1,
      "originName": "Brazil",
      "originTypeName": "Brasilia",
      "destinationName": "Argentina",
      "destinationTypeName": "Buenos",
      "gradeName": "Refinery",
      "quantity": 2
    }'
    ```
    * Sample response:
    ```json
    {
        "status": 201,
        "message": "Success",
        "data": {
          "year": 2000,
          "month": 1,
          "originName": "Brazil",
          "originTypeName": "Brasilia",
          "destinationName": "Argentina",
          "destinationTypeName": "Buenos",
          "gradeName": "Refinery",
          "quantity": 2,
          "uuid": "16838e66-cec5-4eb6-a7be-87095b8df208"
        }
    }
    ```
    * **Insert Bulk Crude Oil Imports:** Adds multiple crude oil import records to the database in a single request.
        * Endpoint: `POST /crude-oil-imports/bulk`
        * Status Code: 201 Created
        * Sample request: 
          ```bash
          curl -X 'POST' \
          'http://0.0.0.0:5321/crude-oil-imports/bulk' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '[
            {
              "year": 2011,
              "month": 1,
              "originName": "Chile",
              "originTypeName": "Botswana",
              "destinationName": "Temporary",
              "destinationTypeName": "Buenos",
              "gradeName": "Refinery",
              "quantity": 2
            },
            {
              "year": 2010,
              "month": 1,
              "originName": "Brazil",
              "originTypeName": "Brasilia",
              "destinationName": "Argentina",
              "destinationTypeName": "Buenos",
              "gradeName": "Refinery",
              "quantity": 2
            }
            ]'
          ```
        * Sample response: 
          ```json
            {
              "status": 201,
              "message": "Success",
              "data": [
                {
                  "year": 2011,
                  "month": 1,
                  "originName": "Chile",
                  "originTypeName": "Botswana",
                  "destinationName": "Temporary",
                  "destinationTypeName": "Buenos",
                  "gradeName": "Refinery",
                  "quantity": 2,
                  "uuid": "9aa50db4-6702-4bbd-a4df-3caaef4826ef"
                },
                {
                  "year": 2010,
                  "month": 1,
                  "originName": "Brazil",
                  "originTypeName": "Brasilia",
                  "destinationName": "Argentina",
                  "destinationTypeName": "Buenos",
                  "gradeName": "Refinery",
                  "quantity": 2,
                  "uuid": "20256ff9-2a93-403b-92c7-f5d5af08d340"
                }
              ]
            }
          ```
* **Update:**

    * **Patch Crude Oil Import by UUID:** Modifies specific fields of an existing crude oil import record identified by its UUID.  This performs a partial update.
        * Endpoint: `PATCH /crude-oil-imports/{uuid}`
        * Status Code: 200 OK
        * Sample request: 
           ```bash
          curl -X 'PATCH' \
          'http://0.0.0.0:5321/crude-oil-imports/947eb299-189f-47e4-a0b7-85ffb2630cbc' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
                  "year": 1999,
                  "month": 11,
                  "originName": "USA",
                  "originTypeName": "PA",
                  "destinationName": "UK",
                  "destinationTypeName": "LONDON",
                  "gradeName": "Refinery",
                  "quantity": 190
                }'
            ```
        * Sample response:
          ```json
          {
          "status": 201,
          "message": "Success",
          "data": {
                "year": 1999,
                "month": 11,
                "originName": "USA",
                "originTypeName": "PA",
                "destinationName": "UK",
                "destinationTypeName": "LONDON",
                "gradeName": "Refinery",
                "quantity": 190,
                "uuid": "947eb299-189f-47e4-a0b7-85ffb2630cbc"
              }
          }
          ```
      
    * **Update Crude Oil Import by UUID:** Replaces the entire content of an existing crude oil import record with new data.
        * Endpoint: `PUT /crude-oil-imports/{uuid}`
        * Status Code: 200 OK
        * Sample request:
          ```bash
          curl -X 'PUT' \
            'http://0.0.0.0:5321/crude-oil-imports/9aa50db4-6702-4bbd-a4df-3caaef4826ef' \
            -H 'accept: application/json' \
            -H 'Content-Type: application/json' \
            -d '{
            "year": 2000,
            "month": 1,
            "originName": "string",
            "originTypeName": "string",
            "destinationName": "string",
            "destinationTypeName": "string",
            "gradeName": "string",
            "quantity": 0
          }'
          ```
       * Sample response:
         ```json
         {
         "status": 201,
         "message": "Success",
         "data": {
           "year": 2000,
           "month": 1,
           "originName": "string",
           "originTypeName": "string",
           "destinationName": "string",
           "destinationTypeName": "string",
           "gradeName": "string",
           "quantity": 0,
           "uuid": "9aa50db4-6702-4bbd-a4df-3caaef4826ef"
          }
         }
         ```
* **Delete:**
    * **Delete Crude Oil Import by UUID:** Removes a crude oil import record from the database using its UUID.
        * Endpoint: `DELETE /crude-oil-imports/{uuid}`
        * Status Code: 200 OK
        * Sample request: 
        ```bash
        curl -X 'DELETE' 'http://0.0.0.0:5321/crude-oil-imports/9aa50db4-6702-4bbd-a4df-3caaef4826ef' \-H 'accept: application/json'
        ``` 
        * Sample response:
        ```json
      {
          "status": 201,
          "message": "Success",
          "data": {
            "year": 2000,
            "month": 1,
            "originName": "string",
            "originTypeName": "string",
            "destinationName": "string",
            "destinationTypeName": "string",
            "gradeName": "string",
            "quantity": 0,
            "uuid": "9aa50db4-6702-4bbd-a4df-3caaef4826ef"
          }
        }
        ```
      