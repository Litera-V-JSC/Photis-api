# ReceiptScanner-API
API for receipt scanner

## Installation
1. To install the app, check if you have docker installed on your machine.
2. If you have docker installed, go to "app" directory:
```
cd app
```
3. Create .env file and set SECRET_KEY variable
example of .env:
```
SECRET_KEY="your_secret_key"
```
4. Build docker container: 
``` 
docker build -t receipt_scanner:latest . 
```

## Run the app:
To run the app just launch docker container:
```
docker run -p 8000:8000 receipt_scanner:latest
```
You can choose any port by changing -p flag
