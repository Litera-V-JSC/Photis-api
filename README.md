# ReceiptScanner-API
RESTful API-server for receipt scanner client

## Installation
1. To install the app, check if you have docker installed on your machine.
2. If you have docker installed, go to "app" directory:
```
cd app
```
3. Build docker container and volume  

    build manually:
    ``` 
    docker volume create receipt_scanner 
    docker build . -t receipt_scanner:latest
    ```
    or just use ``` build.sh ``` script:
    it will do everthing automatically

## Run the app
To run the app you must just run built docker container.  
You can launch it manually:
``` 
docker run -p 8000:8000 --mount type=volume,source=receipt_scanner,destination=/app/storage receipt_scanner:latest
```

or use ```./run.sh``` script  

By default, server will run on port=8000. If you need another port, run app manually and change -p flag like this: -p <host_port>:<container_port>

### Creating backup 
Backup of database and stored files can be created with ``` ./make_backup ``` script. It copies all files from receipt_scanner volume and creates .tar archive with copied data in current directory.