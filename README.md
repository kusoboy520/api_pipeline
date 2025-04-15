## Sample FastAPI Application with batch-update user data

![image](./flowchart.PNG)

## How to start

pip install
`python -m pip install -r requirements.txt`

start service

`python main:app --reload`


### 1. FastAPI: Recommendation service

Method: GET

[DOCS: localhost:8000/swagger](http://localhost:8000/swagger)

Parameters:

* userid: string
* itemid: the item that user click(int)

### 2. RabbitMQ: save message from api

Message format(string)

ex. '{"userid": userid, "itemid":itemid}'

### 3. Redis DB: in-memory database(low latency)

Only storage data for one day.

### 4 Prefect: DAG Workflow

Modern workflow orchestration for data and ML engineers

Host: localhost:4200
