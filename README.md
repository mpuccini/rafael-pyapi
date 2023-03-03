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
If you need to stop the service, you can use `docker compose down`.


## How to use
You can look at the available endpoints in the Swagger documentation at the /docs endpoint. Once you have the service running, you can access it at http://localhost:8080/docs to test all available routes. You may try the API with `curl`. First of all you need to authenticate with your credentials:
```bash
curl -X 'POST' \
  'http://localhost:8000/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=<YOUR_USERNAME>&password=<YOUR_PASSWORD>&scope=&client_id=&client_secret='
```
The response is a JSON with yout access token. You can use it to access the endpoints. For instance, to get one single document as a sample of the data, you can use the following command:

```bash
curl -X 'GET' \
  'http://localhost:8000/api/monica/one' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'
```

## Jupyter Notebook example

In the `example_notebook` folder you can find a Jupyter Notebook with some examples of how to use the API. You can run it with the following command:
```bash
jupyter notebook notebooks/RAFAEL_API_Example.ipynb
```
and play in your browser with the examples.


## TODO
- [ ] Add more endpoints for Monica
- [ ] Add endpoints for other sensors (e.g. ANAS)
- [X] Add user authentication?
- [X] Add a dev mongo instance to the docker-compose file
- [X] Add js scripts to populate the dev database with fake users and documents
- [ ] Write tests



### Credits
email: [marco.puccini@enea.it](marco.puccini@enea.it)