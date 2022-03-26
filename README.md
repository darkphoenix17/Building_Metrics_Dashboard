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

SSH insto the vagrant box and use the kubectl command to check if all the deployments, service, pods are running properly or not.

```$ vagrant ssh```  \
```$ kubectl get all --all-namespaces```

***

## Configure Vagrant Box

Here we have to ssh into the vagrant box to write kubectl command but we can abstract that on our locally installed kubectl be configuring our local kubeconfig file.

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


