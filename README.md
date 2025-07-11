## Transaction API

The project is based on a modular, layered architecture, with a clear separation of concerns:

 - API Layer – `FastAPI` is used for building the REST interface.
 - Service Layer – business logic is encapsulated in the `TransactionService` class, which can be tested independently from the API layer.
 - Validation Layer – dedicated validation of CSV file structure `TransactionValidator` allows flexible testing and reuse.
 - Persistence Layer – `SQLAlchemy` & `PostgreSQL` as a data storage layer.
 - unit and integration tests – based on pytest, functional tests added as an example 

This approach enables:

- easy testing of each layer in isolation,
- clean and predictable separation of responsibilities
- increased readability

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

### API docs
Automatically generated Swagger UI docs under http://localhost:8000/docs


### Example usage

#### Upload transaction
```cmd
http -f POST http://localhost:8000/transactions/upload file@{/path/to/your/file.csv}
```

#### Fetch transactions (with filter)
```cmd
http GET http://localhost:8000/transactions?page=1&product_id={uuid}
```