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

| Method  | Endpoint          | Description                    | Auth Required | Request Body                       | Response                                                                                  |
|---------|-------------------|-------------------------------|---------------|----------------------------------|------------------------------------------------------------------------------------------|
| POST    | `/login`          | Login and get JWT token        | No            | `{ "username": "string", "password": "string" }`     | `200 OK` with `{ "access_token": "jwt_token_string" }` or `404 Not Found` with `{"error": "invalid password"}` |
| GET/POST| `/`               | Invalid; returns 400           | No            | N/A                              | `400 Bad Request`                                                                         |
| POST    | `/add`            | Add new receipt                | Yes           | JSON with at least keys: `category` (string), `sum` (number), `receipt_date` (string, e.g. "YYYY-MM-DD"), `image` (base64-encoded PNG string) | `204 No Content` on success; `404 Not Found` with JSON error `{ "error": "data is missing" }` or `{ "error": "receipt already exists" }` |
| DELETE  | `/delete/<id>`    | Delete receipt by ID           | Yes           | N/A                              | `204 No Content` on success; `404 Not Found` with JSON error `{ "error": "Invalid id: <id>" }`                           |
| GET     | `/receipt/all`    | List all receipts              | Yes           | N/A                              | `200 OK` with JSON array `[ {...receipt fields...}, ... ]` or `404 Not Found` with `{ "error": "error while loading list of all receipts from database" }` |
| GET     | `/receipt/<id>`   | Get receipt by ID              | Yes           | N/A                              | `200 OK` with JSON object `{ ...receipt fields... }` or `404 Not Found` with `{ "error": "invalid id: <id>" }`           |
| GET     | `/files/<id>`     | Download receipt image         | Yes           | N/A                              | `200 OK` serves image file; `404 Not Found` with `{ "error": "invalid receipt id" }`                                              |
| GET     | `/categories`     | List predefined receipt categories | Yes       | N/A                              | `200 OK` with JSON array `["ГСМ топливо", "Товары", "Услуги"]`                                                             |
| GET     | `/report`         | Generate PDF report            | Yes           | Optional JSON `{ "id_list": [<int>, ...] }`                                                                | `200 OK` serves generated PDF file; `404 Not Found` with `{ "error": "invalid receipt id" }`                                   |

---

## Notes on Response Structures:

- All authenticated routes require JWT Bearer token passed in the `Authorization` header.
- PDF reports and receipt images are served as file downloads from server storage.
- Receipt data structure depends on database schema (see `db` module).
- Category list is static as implemented.
---