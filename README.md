# ReceiptScanner-API
RESTful API-server for receipt scanner client

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

In this method app uses *receipt_scanner* docker volume to store data.  
Backup of database, logs and other data can be created by running ` ./make_backup ` script. It will copy all files from receipt_scanner docker volume and create .tar archive in current directory.

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

---

## Summary Table of Endpoints

| Endpoint       | Method(s)         | Auth Required | Description                                                   | Request Data / Params                 | Response                           |
|----------------|-------------------|---------------|---------------------------------------------------------------|-------------------------------------|-----------------------------------|
| `/login`       | GET, POST         | No            | Authenticate user and get JWT token                            | JSON: `{ "username": str, "password": str }`  | JSON: `{ "access_token": str }` or error |
| `/`            | GET, POST         | No            | Index page — rejects all requests                              | None                                | 400 Bad Request                   |
| `/add`         | POST              | Yes           | Add an item, save image                                        | JSON with item data including `"image"` | 204 No Content or error           |
| `/delete/<id>` | DELETE            | Yes           | Delete existing item by id                                     | URL param: item id (int)             | 204 No Content or error           |
| `/item/<id>`   | GET               | Yes           | Get item by id or list all items (`id=all`)                   | URL param: item id or `all`           | JSON item(s) or error             |
| `/files/<id>`  | GET               | Yes           | Download item image by item id                                 | URL param: item id (int)              | File or error                    |
| `/categories`  | GET               | Yes           | Get list of item categories                                   | None                                | JSON categories or error          |
| `/report`      | GET               | Yes           | Generate PDF report for specified item IDs                    | JSON with `"id_list": [ids]` | PDF file or error                |

---

## Notes on Response Structures:

- All authenticated routes require JWT Bearer token passed in the `Authorization` header.
- PDF reports and receipt images are served as file downloads from server storage.
- Receipt data structure depends on database schema (see `db` module).
- Category list is static as implemented.
---


