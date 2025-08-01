# Photis-API
RESTful API-server for Photis client

---

## Installation guide

There are three supported methods for building the application: utilizing Docker Compose (recommended), using standalone Docker commands, or performing a manual build from source
### Building with Docker-compose
1. Check if you have docker and docker-compose installed
2. Go to project direcory and run: ``` docker compose up ```  
That`s it!

Compose automatically creates shared directory /storage, where all your database data and logs will be stored in.

### Building with Docker

1. Check if you have docker installed.
2. To build container run ` build.sh ` script
3. To launch app run ` run.sh ` script

All shell scripts are located in app/sh_files directory.  

In this method app uses *photis* docker volume to store data.  
Backup of database, logs and other data can be created by running ` ./make_backup ` script. It will copy all files from photis docker volume and create .tar archive in current directory.

By default, server will run on port 8000. If you need other port, change -p flag in `run.sh` script like this: *docker run -p <host_port>:<container_port> ...*

### Building from source 
1. create python venv and install dependencies:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
2. Go to project dir and create .env file with SECRET_KEY (requuired by Flask):
    ```
    cd app
    SECRET_KEY=$(openssl rand -hex 32 | sha256sum | awk '{print $1}')
    echo "SECRET_KEY=$SECRET_KEY" > .env
    ```
3. To launch app, run:
    ```
    gunicorn -w 4 -b 0.0.0.0:8000 main:app
    ```

#### Default (test) data 
After installation database will not contain any data. But if you want to test API, you can generate it by running *db_defaults_gen.py* script - it will create sample data for every table.


---

## Summary Table of Endpoints

| Endpoint               | Method(s)  | JWT Required | Parameters               | Description                                                    | Success Response    | Error Response                      |
|------------------------|------------|--------------|--------------------------|----------------------------------------------------------------|---------------------|-----------------------------------|
| `/login`               | GET, POST  | No           | JSON: `username`, `password` | Authenticate user and get JWT token                              | 200 + `{access_token}` | 404 + `{error: "invalid login data"}` |
| `/`                    | GET, POST  | No           | None                     | Index route; rejects any request                               | 400                 | —                                 |
| `/add-item`            | POST       | Yes          | JSON with `image` and other data | Add new item with image, saving to storage                    | 204 (No Content)     | 404 + `{error: 'some data is missing'}` or `{error: 'item already exists or data is corrupted'}` |
| `/delete-item/<id>`    | DELETE     | Yes          | Path: item ID (int)      | Delete item by ID                                              | 204 (No Content)     | 404 + `{error: "Invalid id: <id>"}` |
| `/delete-category/<id>`| DELETE     | Yes          | Path: category ID (int)  | Delete category by ID                                          | 204 (No Content)     | 404 + `{error: "Invalid id: <id>"}` |
| `/item/<id>`           | GET        | Yes          | Path: item ID or `"all"` | Get one item by ID or list of all items                        | 200 + item(s) JSON   | 404 + `{error: "invalid id: <id>"}` or `{error: "error while loading items"}` |
| `/files/<id>`          | GET        | Yes          | Path: item ID (int)      | Download stored file image associated with item               | File download        | 404 + `{error: "invalid id"}`     |
| `/categories`          | GET        | Yes          | None                     | Get list of all categories                                     | 200 + categories JSON| 404 + `{error: "cannot load categories from database"}` |
| `/add-category`        | POST       | Yes          | JSON category data       | Add new category                                               | 204 (No Content)     | 404 + `{error: "category data is missing"}` or `{error: "category already exists"}` |
| `/report`              | GET        | Yes          | JSON with `"id_list"` (optional) | Generate PDF report for specified items                       | PDF file download    | 404 + `{error: "invalid id"}`     |

---

## Notes on Response Structures:

- All authenticated routes require JWT Bearer token passed in the `Authorization` header.
- PDF reports and objects images are served as file downloads from server storage.
- Category list is static as implemented.
---


