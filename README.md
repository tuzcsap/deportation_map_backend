## To run backend:

- create .env file with MONGOPASSWORD CLUSTER_URL

### Locally:
- create venv:

    `python -m venv venv`
- activate venv:

    `.\venv\Scripts\activate.bat` (windows)

    `source venv/bin/activate` (mac or linux)

- install requirements:

  `pip install -r requirements.txt`

- run fastapi server:

    `python -m uvicorn main:app --reload`

Backend should run on http://127.0.0.1:8000/

### In docker:
- build docker image from Dockerfile:

    `docker build -t mapbackend .`

- run docker container:

    `docker run -d --name mapbackend -p 8000:80 mapbackend`

Backend should run on http://127.0.0.1:8000/
