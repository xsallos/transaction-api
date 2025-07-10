### Tests

```cmd
poetry install
sudo docker-compose -f docker-compose.tests.yml up -d
make tests
```

### Run server locally

```cmd
sudo docker-compose up
```

### Usage

#### Upload transaction
```cmd
http -f POST http://localhost:8000/transactions/upload file@/path/to/your/file.csv
```

#### Fetch transactions
```cmd
http GET http://localhost:8000/transactions?page=1
```