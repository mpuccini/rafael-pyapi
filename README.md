# RAFAEL RestAPI 
This is a simple RestAPI service for the Project Rafael. This is a work in progress version, only working with the Monica database.

## How to develop
1. Clone the repository
2. create virtualenv with, at least, python 3.10: `python3.10 -m venv .venv`
3. activate virtualenv: `source .venv/bin/activate`
4. install requirements: `pip install -r requirements.txt`
5. setup configurations: `cp env.sample .env.dev` and fill the variables with mongodb host, port and user credentials.
6. export the environment variables: `export $(xargs < .env.dev)`
7. go to the `api` folder
8. write down your code!
9. run the service: `uvicorn main:app --reload`
   
You can now access the service at http://localhost:8080/docs. 
> You can make changes to the code and the service will reload automatically.

## How to deploy
1. Clone the repository
2. copy the env.sample to .env.prod and fill the variables with mongodb host, port and user credentials.
3. docker compose up -d

You need to configure the web server to expose it to the internet. Otherwise you can only access it locally.

## How to use
You can look at the available endpoints in the Swagger documentation at the /docs endpoint. Once you have the service running, you can access it at http://localhost:8080/docs. You can use http methods to access the endpoints, for instance, to get one single document as a sample of the data, you can use the following command:

```bash
curl -X GET "http://localhost:8000/api/v1/monica/one" 
```
Or, if you want data from a specific date range, you can use the following command:

```bash
curl -X GET "http://localhost:8000/api/v1/monica/dateRange/?start=2022-02-23&end=2022-02-24" 
```

## Credits
email: [marco.puccini@enea.it](marco.puccini@enea.it)

## TODO
- [ ] Add more endpoints for Monica
- [ ] Add endpoints for other sensors (e.g. ANAS)
- [ ] Add user authentication?