# Media Service Converter

1. Create `.env` file or copy existed example `cp .env.example .env`
2. For production deploy just run `docker compose up -d --build`
3. Docs place url `http://127.0.0.1:8000/docs`

For update run `git pull`, `docker-compose up -d app`, `docker-compose run app alembic upgrade head`

# API

### Create user

`POST` `http://127.0.0.1:8000/users`  

Example request (application/json):

`{
  "username": "Tom"
}`

Server response:

`{
  "user_id": "ff90812f-6ef9-4d6e-af77-d0e0fc00a3da",
  "token": "2b22739ef48e4d04b16757e6591814a2"
}`

### Upload media

`POST` `http://127.0.0.1:8000/records`

Requared parameters (multipart/form-data): 

`user_id` - UUID number of user  
`token` - Original user token  
`file` - File in `.wav` format.

Server response:

`{
  "file": "http://127.0.0.1:8000/record?id=31d299c4-0ae2-485e-ac06-40fd92311231&user=ff90812f-6ef9-4d6e-af77-d0e0fc00a3da"
}`

### Download file

`GET` `http://127.0.0.1:8000/record?id={record_id}&user={user_id}`

`record_id` - Media file UUID  
`user_id` - User UUID
