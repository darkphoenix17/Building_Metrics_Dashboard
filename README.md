# Steps & output to set up a metric dashboard for a flask application using Grafana, Prometheus and Jaeger Tracing.

## Setup

Run ```$ vagrant up``` in the home directory of the repo where the Vagrantfile is located.

This will create up a opensuse box with the name 'dashboard' in you VB environment. 

The Vagrantfile has some scripts pre written which will do the following:
1) Install basic some dependencies.
2) Install k3s
3) Install Helm
4) Install Grafana and Promethous using Helm
5) Install Jaeger CRD, service account, role, role binding and operator
6) Configure Jaeger operator to be cluster wide.
7) Verify if all the installations.

***

## Verify Setup

SSH into the vagrant box and use the kubectl command to check if all the deployments, service, pods are running properly or not.

```$ vagrant ssh```  \
```$ kubectl get all --all-namespaces```

***

## Configure Vagrant Box

Here we have to ssh into the vagrant box to write kubectl command but we can abstract that on our locally installed kubectl by configuring our local kubeconfig file.

```$ vagrant ssh``` \
```$ cat /etc/rancher/k3s/k3s.yaml``` \
*(copy the content show by above command and paste it in "~/.kube/config" file using below command)* \
```$ vim ~/.kube/config``` 

***

## Steps to expose grafana dashboard

1) Search for grafana service by ```kubectl get svc -n monitoring```.

2) We are using vagrant to virtualise our environment so we have occupied port 3000 of our local system in our vagrantfile and connected it to port 3000 of our vagrant environment. We will port forward our ```svc/prometheus-grafana``` service using the belong command after we ssh into the vagrant. \
```$ vagrant ssh``` \
```$ kubectl port-forward -n monitoring --address 0.0.0.0 svc/prometheus-grafana 3000:80``` 

3) Now go to url ```"http:localhost:3000"``` in your browser. It will redirect you to grafana login page. Put the following credentials: \
**Email or username: admin** <br /> **Password: prom-operator**

4) You can now see the Grafana Dashboard.

***

## Create Jaeger Instance

In order to use Jaeger we have to create a Jaeger Instance. Follow the steps below.<br />

```$ kubectl apply -f jaeger-tracing/jaeger.yaml``` <br />
*(We have to enable sidecar injector for our instance located in a particular namespace to allow jeager instance to check for traces in application in a different namespace.)*<br />
```$ kubectl apply -f jaeger-tracing/injector-enable.yaml```

***

## Steps to expose Jaeger UI

1) Check the namespace where your jaeger instance is been created. let it be ```${namespace}```

2) We are using vagrant to virtualise our environment so we have occupied port 16686 of our local system in our vagrantfile and connected it to port 16686 of our vagrant environment. We will port forward our ```svc/my-traces-query``` (jaeger instance service) using the below command after we ssh into the vagrant. \
```$ vagrant ssh``` \
```$ kubectl port-forward -n ${namespace} --address 0.0.0.0 svc/$(kubectl get svc -n ${namespace} -l app=jaeger -o jsonpath={.items[2].metadata.name}) 16686:16686``` 

3) You can now see the Jaeger UI at ```"http:localhost:16686"``` in your local browser.

*** 

## Run our flask application.

1) Go to manifest and deploy our application to kubernetes. Following is the command to do it in one go.
``` $ kubectl apply -f manifests/app/.```

***


## Expose Frontend of our boiler code.

1) Our frontend is deployed in default namespace with a service name ```svc/frontend```.
2) We are using vagrant to virtualise our environment so we have occupied port 8080 of our local system in our vagrantfile and connected it to port 8080 of our vagrant environment. We will port forward our ```svc/frontend``` (jaeger instance service) using the below command after we ssh into the vagrant. \
```$ vagrant ssh``` \
```$ kubectl port-forward --address 0.0.0.0 svc/frontend 8080:8080```
3) You can now see the out frontend UI at ```"http:localhost:8080"``` in your local browser.

***


# Below are the images showing outputs.


### Setup the Jaeger and Prometheus source
Exposing Grafana to the internet and then setting Prometheus as a data source. Screenshot of the home page after logging into Grafana.

![Grafana Homepage](/outputs/grafana_homepage.png)

<hr />

### Describe SLO/SLI for our project
What the SLIs are, based on an SLO of *monthly uptime* and *request response time*.

(SLI) ***monthly uptime*** : *monthly uptime* percentage of website/network application/physical server/etc.  is 99.8%. This is the ratio of percentage to the time during which website/network application/physical server/etc. is able to serve requests or perform programmed operations.

We can set our (SLO) goal for the future - ***monthly uptime*** percentage of website/network application/physical server/etc. to be 99.9%.


(SLI) ***request response time***- *request response time* of specified website/network application is 20 ms. This is the time during which the response is being handled by a remote website/network application.

We can set our (SLO): ***request response time*** of website to 10 ms.

<hr />

### Creating SLI metrics.

The 4 Golden Signals we already know and the 5th one is also popular metric - Uptime:

1. **Latency** - response time during which the requests are served, usually measured in milliseconds;
2. **Traffic** - the value of load on the target, usually measured in requests per second, or megabits/kilobits per second;
3. **Errors** - the amount of failed requests, usually measured in number of requests with return HTTP-code 500 in a second; 
4. **Saturation/Utilization** - indicates the percentage of system resources used (CPU usage %, Memory usage %/GB/MB);
5. **Uptime** -  the overall availability metric, could be shown as time from the last reboot/fail or more often as a percentage, indicating the ratio of time the monitored target was available for service to the time it wasn't (eg. 99.9% of uptime, so in contrast - 0.1% of overall time it was in downtime or in maintenance, it didn't serve its designated work).

<hr />

### Create a Dashboard to measure our SLIs
Creating a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. 

![Create Dashboard_2](/outputs/final_dashboard_2.png)

<hr />

### Tracing our Flask App
We will create a Jaeger span to measure the processes on the backend.

![Jaeger Tracing Flask Code](/outputs/tracing_flask_code.png)

<hr />

### Jaeger in Dashboards
Now that the trace is running, let's add the metric to our current Grafana dashboard.

![Jaeger Grafana Trace](/outputs/jaeger_grafana_explore.png) 

![Jaeger Row Dashboard](/outputs/jaeger_dashboard.png)

<hr />

### Creating SLIs and SLOs
We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name four SLIs that you would use to measure the success of this SLO.

As our application I would consider 'backend' application:

1. **Uptime**. <u>SLI</u>: Uptime of the application availability per month. <u>SLO</u>: Uptime of the application - 99.95%.
2. **Latency**:
   - <u>SLI</u>: Average response time per 30 seconds periods per month. <u>SLO</u>: Average response time per 30 sec periods per month less than 100ms. 
   - <u>SLI</u>: Percentage of request count which complete in less than 100ms. <u>SLO</u>: 99% of request count will complete in less than 100ms.
3. **Errors**. <u>SLI:</u> HTTP 500 errors % rate per 1 minute ranges. <u>SLO</u>:  HTTP 500 errors % rate per 1 minute is less than 1%.
4. **Traffic**. <u>SLI</u>: Total requests per minute. <u>SLO</u>: Total requests per minute is less than 1800.

<hr />

### Final Dashboard
Creating a Final Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Screenshot of the dashboard is below, a description of what graphs are represented in the dashboard.

Dashboard: General Dashboards Project:

Row 'Prometheus':

- <u>CPU Usage</u>: CPU Usage fractions of 2 application deployments - backend-app and frontend-app;
- <u>Memory Usage</u>: Memory usage in MiB of 2 application deployments - backend-app and frontend-app;
- <u>Uptime ('frontend')</u>: frontend application uptime graph;
- <u>Uptime ('backend')</u>: backend application uptime graph;
- <u>HTTP 4xx Errors</u>: the number of HTTP requests with response code 4xx, over 30 sec intervals, shown per application and path;
- <u>HTTP 5xx Errors</u>: the number of HTTP requests with response code 5xx, over 30 sec intervals, shown per application and path;
- <u>HTTP requests per second</u>: the number of HTTP requests per second;
- <u>Total requests per minute</u>: the amount of all HTTP requests measured over one minute intervals;
- <u>Average response time [30s]</u>: the average response time for HTTP requests over 30 sec intervals, shown per application and path;
- <u>Requests under 100ms</u>: the percentage of requests which were finished within 100ms, shown per application and path;
- <u>HTTP 5xx Errors % rate per minute</u>: the percentage rate of HTTP 5xx errors per 1 minute intervals;
- <u>HTTP 4xx Errors % rate per minute</u>: the percentage rate of HTTP 4xx errors per 1 minute intervals;

Row 'Jaeger':

- <u>Min latency ( backend '/api' )</u>: minimal latency in milliseconds of the requests which were served by the '/api' endpoint of backend app, within the specified time range;
- <u>Avg latency ( backend '/api' )</u>: average latency in milliseconds of the requests which were served by the '/api' endpoint of backend app, within the specified time range;
- <u>Max latency ( backend '/api' )</u>: maximum latency in milliseconds of the requests which were served by the '/api' endpoint of backend app, within the specified time range;
- <u>Requests Count by Latency ( backend '/api' )</u>: the amount of total requests served by the backend 'api'-endpoint distributed by the serving duration, within the specified time range;
- <u>Backend HTTP 500 Errors Count Indicator</u>: the amount of requests with response code HTTP 500, served by the backend 'api'-endpoint distributed by the serving duration, within the specified time range.

![Create Dashboard_1](/outputs/final_dashboard_1.png)

![Final Dashboard_2](/outputs/final_dashboard_2.png)

![Final Dashboard_3](/outputs/final_dashboard_3.png)
