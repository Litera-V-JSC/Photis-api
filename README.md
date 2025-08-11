# Photis-API
RESTful API-server for Photis client

---

## Installation guide

There are three supported methods for building the application: utilizing Docker Compose (recommended), using standalone Docker commands, or performing a manual build from source
### Building with Docker-compose (recommended)
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
2. Go to project dir and create .env file with SECRET_KEY (required by Flask):
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
After installation database will not contain any data. But if you want to test API, you can generate it by running `db_defaults_gen.py` - it will create sample data for every table.  
For example, it will create such users:

| Username | Password | Admin
|-------------|-------------|-------------|
| adm_usr   | adm_pasw | True
| usr1   | pasw1 | False


---

## Summary Table of Endpoints

| Method   | URL                   | Description                                 | JWT Required | Request (body/parameters)                              | Responses (status, body)                                                                                     |
|----------|-----------------------|---------------------------------------------|--------------|--------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| GET,POST | /login                | Authentication to get JWT token              | No           | JSON { "username": string, "password": string }        | 200 { "access_token": string, "user_data": object } or 404 { "error": "invalid login data" }                  |
| GET,POST | /                     | Index page, always returns an error          | No           | None                                                   | 400 (Bad Request)                                                                                             |
| POST     | /add-item             | Add item and save image                        | Yes          | JSON with data including "image" field                  | 204 No Content or 404 { "error": "some data is missing" / "item already exists or data is corrupted" }       |
| DELETE   | /delete-item/<id>     | Delete item by ID                              | Yes          | Path parameter: id (int)                                | 204 No Content or 404 { "error": "Invalid id: <id>" }                                                       |
| GET      | /item/<id>            | Get item by ID or all items                    | Yes          | Path parameter: id = int or "all"                       | 200 JSON object or list of objects, 404 { "error": "invalid id: <id>" / "error while loading items" }         |
| GET      | /files/<id>           | Download item image by ID                       | Yes          | Path parameter: id (int)                                | Image file or 404 { "error": "invalid id" }                                                                 |
| GET      | /categories           | Get list of categories                          | Yes          | None                                                   | 200 JSON list of categories or 404 { "error": "cannot load categories from database" }                       |
| DELETE   | /delete-category/<id> | Delete category by ID                           | Yes          | Path parameter: id (int)                                | 204 No Content or 404 { "error": "Invalid id: <id>" }                                                       |
| POST     | /add-category         | Add new category                                | Yes          | JSON category data                                     | 204 No Content or 404 { "error": "category data is missing" / "category already exists" / "internal errors" } |
| GET      | /users                | Get list of users (public data)                 | Yes          | None                                                   | 200 JSON list of users or 404 { "error": "cannot load usernames from database" }                             |
| DELETE   | /delete-user/<username> | Delete user by username                         | Yes          | Path parameter: username (string)                       | 204 No Content or 404 { "error": "user does not exist: <username>" }                                        |
| POST     | /add-user             | Add new user                                    | Yes          | JSON user data                                        | 204 No Content or 404 { "error": "user data is missing" / "user already exists" / "internal errors" }         |
| GET      | /report               | Generate and get PDF report                      | Yes          | JSON { "id_list": [int] } (optional)                   | PDF report file or 404 { "error": "invalid id" }                                                            |

---

## Notes on Response Structures:

- Success response is always 200 or 204
- All authenticated routes require JWT Bearer token passed in the `Authorization` header.
- PDF reports and objects images are served as file downloads from server storage.
---


