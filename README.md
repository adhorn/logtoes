



**LogToES**:

Simple demo of the asynchronous worker pattern using Flask and Celery.
This demo demonstrates the use of a python decorator to send API logs to Elasticsearch in real-time for analysis.

![Logs to ES](https://github.com/adhorn/logtoes/blob/master/pics/demo0.png)


**Why this demo?**:

While Flask + Celery code is very common on the internet, I could not find any ready-to-use example which would combine all the bells and whistles necessary to run the asynchronous pattern code in production. This demo also uses Gunicorn to serve the Flask application.
This code here gives you just that (hopefully).


**Asynchronous Pattern on AWS**:

![Architecture](https://github.com/adhorn/logtoes/blob/master/pics/demo1.png)

![How it works (part1)](https://github.com/adhorn/logtoes/blob/master/pics/demo2.png)

![How it works (part2)](https://github.com/adhorn/logtoes/blob/master/pics/demo3.png)


**What is Flask?**: 
Flask is a fun and easy to use microframework for Python based on Werkzeug.
It is easy to setup and use, and has a large community, lots of examples, etc:

```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
```

```
$ python hello.py
 * Running on http://localhost:5000/
```

**What is Gunicorn?**
Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.


**What is Celery?**
Celery is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time operation, but supports scheduling as well. 
The execution units, called tasks, are executed concurrently on a single or more worker servers using multiprocessing, Eventlet,	or gevent. Tasks can execute asynchronously (in the background) or synchronously (wait until ready).
Celery is used in production systems to process millions of tasks a day.

**Amazon Elasticsearch Service** makes it easy to deploy, operate, and scale Elasticsearch for log analytics, full text search, application monitoring, and more. Amazon Elasticsearch Service is a fully managed service that delivers Elasticsearch’s easy-to-use APIs and real-time capabilities along with the availability, scalability, and security required by production workloads. The service offers built-in integrations with Kibana, Logstash, and AWS services including Amazon Kinesis Firehose, AWS Lambda, and Amazon CloudWatch so that you can go from raw data to actionable insights quickly.


**How to run the code:**

Create a virtualenv and install the requirements.

```
$ virtualenv ~/.virtualenvs/logtoes && source ~/.virtualenvs/logtoes/bin/activate
$ pip install -r requirements.txt
```

Launch 2 terminal sessions since you need to run both Gunicorn and Celery. 

In the first terminal ( make sure to activate your Virtualenv logtoes) - launch Celery workers

```
$ celery -A start_celery worker -l debug -P gevent
```

In the second terminal (make sure to activate your Virtualenv logtoes) - launch Gunicorn server

```
$ gunicorn -w 1 -b 0.0.0.0:5555 -k gevent logtoes.logtoes:app
* Test the API on http://0.0.0.0:5555/api/echo
```

This should respond: 
```
{"Application Status": "Surprising, but I am up and running!"}
```


You can now start a third terminal to launch Flower, a tool to vizualise your tasks

```
$ celery -A start_celery flower --port=4444
* running on http://localhost:4444/tasks
```


**Note:**

This demo used Geocity to enrich the log information with the location (converting IP to Country) - if you want to update the data, do the following:

```
cd logtoes/geocity && { curl -O http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz ; cd -; } 
cd logtoes/geocity && { gunzip GeoLiteCity.dat.gz ; cd -; }
```






