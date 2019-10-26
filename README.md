## photo-processor exercise

### Installation

Prerequisites:  
- Docker  
- Ability to run `make`

Start the app:  
- `make start`

Create the db schema after booting the app:  
- `make create-db`

### Usage

Verify that you have pending photos:  
`http://localhost:3000/photos/pending`

To start processing photos send some json as a `PUT` request to:  
`http://localhost:3000/photos/process`

Sample JSON request:

```
[
    "4a37b140-022d-4fba-aa25-a0527d15ecf2",
    "240f5321-35d2-495d-8324-58112d80528b"
]
```

There is a sample rudimentary script called submit_pending.py in the scripts directory that will submit all pending photos for processing.

To examine created thumbnails copy them from the app container to your host (this will create tpp-app-thumbs directory in your current directory):  
`docker cp tpp-app:/tpp-app-thumbs/ .`

### Useful tools

Postgres PSQL can be accessed via:  
- `make psql`

Shell on the app container can be accessed via:  
- `make shell`

New database migrations can be created using:  
- `make revise-db`

Upgrade database to the latest version via:  
- `make upgrade-db`

Downgrade database to the previous version via:  
- `make downgrade-db`

RabbitMQ management console can be accessed at:  
`http://localhost:15672/`

### Production considerations

- Currently database migrations run on the app container and require volume mapping of app to host to preserve created migrations. It may be better to run migrations in a dedicated container.
- Currently both web server and processor run on the same container. This is an antipattern for docker / microservices so it may be desireble to separate those into two services.
- Currently we are using internal flask webserver which is not suitable for production for security and reliability reasons. A combination of gunicorn and nginx with proper configuration would work well in production.
- Currently each call to /photos/process creates a new rabbitmq connection and closes it. Depending on how often that endpoint is called a more sophisticated approach for connection management may be chosen.

### Testing

- Testing ommited due to time constraints
- It would be desirable to add end to end testing from sending a request to /photos/process to verfiying creation of an appropriate thumbnail file in the target directory.
- More sophisticated testing may verify dimensions of the generated thumbnail and test it against known target using image similarity.

### Architecture Q & A

- Why use ORM and migrations?  
  For such a simple app there was no benefit in using ORM and migrations, however because it is an interview exercise, I thought it would be appropriate to do so.

- Why not to use `flask-sqlalchemy` and `flask-migrate`?  
  `flask-sqlalchemy` and `flask-migrate` definitely make life easier however it seems like the model definition in `flask-sqlalchemy` is not compatible with pure `sqlalchemy`. Therefore to use model definitions from `flask-sqlalchemy` in photo processor we would have to bind the processor to `flask` even though it is not a web application. I believe it is important to keep photo processor decoupled from the web app and at the same time to share model definitions instead of duplicating them. Therefore using `sqlalchemy` and alembic directly seemed like a good option.
