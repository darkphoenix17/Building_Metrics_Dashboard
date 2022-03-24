Steps to expose grafana dashboard

1) Search for grafana service by ```kubectl get svc -n monitoring```.

2) We are using vagrant to virtualise our environment so we have occupied port 3000 of our local system in our vagrantfile and connected it to port 3000 of our vagrant environment. We will port forward our ```svc/prometheus-grafana``` service using the belong command after we ssh into the vagrant.
```$ vagrant ssh```
```$ kubectl port-forward -n monitoring --address 0.0.0.0 svc/prometheus-grafana 3000:80```

3) Now go to url ```"http:localhost:3000"``` in your browser. It will redirect you to grafan login page. Put the following credentials:

    **Email or username: admin** 

    **Password: prom-operator**

4) You can now see the Grafana Dashboard.