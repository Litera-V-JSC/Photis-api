# ReceiptScanner-API
RESTful API-server for receipt scanner client

---

## Installation guide

### Build app
1. To build the app, you need to have docker installed.
2. If you already have docker, go to "app" directory (source code stores here) :
    ```
    cd app
    ```
3. Build docker container and create volume  
    Simply run ``` ./build.sh ``` script or build it manually:
    ``` 
    docker volume create receipt_scanner 
    docker build . -t receipt_scanner:latest
    ```

### Running the app 
To run container use ```./run.sh``` script or launch it manually:    
``` 
docker run -p 8000:8000 --mount type=volume,source=receipt_scanner,destination=/app/storage receipt_scanner:latest
```  
By default, server will run on port 8000. If you need other port, run it manually and change -p flag like this: -p <host_port>:<container_port>

### Creating backup 
Backup of database and stored files can be created with ``` ./make_backup ``` script. It will copy all files from receipt_scanner docker volume and create .tar archive in current directory.

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


