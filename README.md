# zana-cion

## how to run

## running tests

docker-compose run --rm web pytest -vv


## endpoints



curl -X POST \
  http://localhost:9008/api/v1/users \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "erick",
    "age": 30,
    "telephone": "1234567890",
    "created_at": "2021-07-10T16:00:00"
  }'


curl http://localhost:9008/api/v1/users/{user_id}


curl -X PUT \
  http://localhost:9008/api/v1/users/65f22938d8b252af2ae9773d \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "erick",
    "age": 31,
    "telephone": "1234567890"
  }'

curl -X PUT \
  http://localhost:9008/api/v1/users/65f22938d8b252af2ae9773d \
  -H 'Content-Type: application/json' \
  -d '{
    "age": 31
  }'
