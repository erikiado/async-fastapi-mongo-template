# async-fastapi-mongo: zana-cion

## project requirements
- docker
- docker-compose

docker via the [docker-compose.yml](https://github.com/erikiado/async-fastapi-mongo-template/blob/main/docker-compose.yml) will be in charge of installing poetry and with it the python dependecies necessary to run the mongo service and the app.

## how to run
once you have all dependencies installed, run this command to build and start the application:
```bash
docker-compose up
```
## running tests

```bash
docker-compose run --rm web pytest -vv
```
if/when all tests pass you should be able to see all passing test including the code coverage
![test_coverage](https://github.com/erikiado/async-fastapi-mongo-template/assets/2940899/58183ff8-0f84-4a93-b38a-952fb43a315e)
check for further testing configuration https://fastapi.tiangolo.com/tutorial/testing/

## endpoints
**once the user is created in the db you should be able to get, update and delete the user**

**all get/list fields return users id for now, if more fields are needed feel free to update the [UserResponse schema](https://github.com/erikiado/async-fastapi-mongo-template/blob/main/zana/schemas/users.py)**

#### creating a User:
- Endpoint: POST http://localhost:9008/api/v1/users
- Description: This endpoint is used to create a new user by sending a POST request with JSON data containing user information such as name, age, telephone, and created_at.
```bash
curl -X POST \
  http://localhost:9008/api/v1/users \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "erick",
    "age": 30,
    "telephone": "1234567890",
    "created_at": "2021-07-10T16:00:00"
  }'
```

#### getting a all users:
- Endpoint: GET http://localhost:9008/api/v1/users/
- Description: This endpoint retrieves information about all users
```bash
curl http://localhost:9008/api/v1/users/
```

**remember to replace the {user_id} with the created user_id**
#### getting a User by ID:
- Endpoint: GET http://localhost:9008/api/v1/users/{user_id}
- Description: This endpoint retrieves information about a user specified by their unique identifier (user_id).
```bash
curl http://localhost:9008/api/v1/users/{user_id}
```

#### updating a User:
- Endpoint: PUT http://localhost:9008/api/v1/users/{user_id}
- Description: This endpoint updates an existing user's information with the provided data. It requires sending a PUT request with JSON data containing the fields to be updated.
```bash
curl -X PUT \
  http://localhost:9008/api/v1/users/{user_id} \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "erick",
    "age": 31,
    "telephone": "1234567890"
  }'
```
you should be able to update a single field by using the following curl
```bash
curl -X PUT \
  http://localhost:9008/api/v1/users/{user_id} \
  -H 'Content-Type: application/json' \
  -d '{
    "age": 31
  }'
```

#### deleting a User:
- Endpoint: DELETE http://localhost:9008/api/v1/users/{user_id}
- Description: This endpoint deletes an existing user specified by their unique identifier (user_id).
```bash
curl -X DELETE \
  http://localhost:9008/api/v1/users/{user_id}
```

## acknowledgements
thanks [@grillazz](https://github.com/grillazz) for the starting template

https://github.com/grillazz/fastapi-mongodb
