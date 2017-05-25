


Demo Flask app for running logtoes - logs are now sent in real-time to an Elasticsearch cluster using asynchronous tasks powered by Celery.



**LogToES**:

Simple demo of the asynchronous worker pattern using Flask and Celery.
This demo demonstrates the use of a python decorator to send API logs to Elasticsearch in real-time for analysis.

![Architecture](https://github.com/adhorn/logtoes/blob/master/pics/demo1.png)

![How it works (part1)](https://github.com/adhorn/logtoes/blob/master/pics/demo2.png)

![How it works (part2)](https://github.com/adhorn/logtoes/blob/master/pics/demo3.png)


**Why this demo?**:

While Flask + Celery code is very common on the internet, I could not find any ready-to-use example which would combine all the bells and whistles necessary to run code in production.
This code here gives you just that (hopefully).


**What is Flask?**: 
Flask is a fun and easy to use microframework for Python based on Werkzeug.
It is easy to setup and use:

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
$ pip install Flask
$ python hello.py
 * Running on http://localhost:5000/
```

**What is Celery?**
Celery is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time operation, but supports scheduling as well. 
The execution units, called tasks, are executed concurrently on a single or more worker servers using multiprocessing, Eventlet,	or gevent. Tasks can execute asynchronously (in the background) or synchronously (wait until ready).
Celery is used in production systems to process millions of tasks a day.

**Amazon Elasticsearch Service** makes it easy to deploy, operate, and scale Elasticsearch for log analytics, full text search, application monitoring, and more. Amazon Elasticsearch Service is a fully managed service that delivers Elasticsearch’s easy-to-use APIs and real-time capabilities along with the availability, scalability, and security required by production workloads. The service offers built-in integrations with Kibana, Logstash, and AWS services including Amazon Kinesis Firehose, AWS Lambda, and Amazon CloudWatch so that you can go from raw data to actionable insights quickly.


**Prerequisites:**


* This demo used Geocity to enrich the log information with the location (converting IP to Country)
	```
	cd logtoes/geocity && { curl -O http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz ; cd -; } 
	cd logtoes/geocity && { gunzip GeoLiteCity.dat.gz ; cd -; }
	```


* Create Amazon Elasticsearch Cluster (I used version 2.3)
 * create security policy to allow access from your IP address only, your CLI arn, or any other access policy.





