# RAFAEL RestAPI 
This is a simple RestAPI service for the Project Rafael. This is a work in progress version, only working with the Monica database.

## How to deploy
1. Clone the repository
2. copy the env.sample to .env.prod and fill the variables with mongodb host, port and user credentials.
3. docker compose up -d

You need to configure the web server to expose it to the internet. Otherwise you can only access it locally.

## How to use
You can look at the available endpoints in the Swagger documentation at the /docs endpoint. Once you have the service running, you can access it at http://localhost:8080/docs. You can use http methods to access the endpoints, for instance, to get all the data, you can use the following command:

```bash
curl -X GET "http://localhost:8080/api/v1/monica/all" 
```
Or, if you want data from a specific date range, you can use the following command:

```bash
curl -X GET "http://localhost:8080/api/v1/monica/all/2022-02-23&2022-02-26" 
```

## Credits
email: [marco.puccini@enea.it](marco.puccini@enea.it)

## TODO
- [ ] Add more endpoints for Monica
- [ ] Add endpoints for other sensors (e.g. ANAS)
- [ ] Add user authentication?