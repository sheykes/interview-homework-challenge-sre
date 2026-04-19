# Challenge 5: Helm Chart

I created all the requested files according to the task.
`_helpers.tpl` contains the usual templates that I consider best practice.

As I had a minikube available on my machine to run and verify the chart I simply loaded
the image created in Challenge 3 into my minikube and set the values accordingly (which means
referencing a localhost repository and imagePullPolicy: Never to use that manually loaded image).

When using a proper image registry these values would have to be changed. In production the `latest`
tag should also usually not be used as there is no guarantee what actually is behind that, a semantic
version number or at least a commit ID is preferable as a tag.

## Verification

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-5$ helm lint ./server-chart
==> Linting ./server-chart
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-5$ helm template ./server-chart
---
# Source: server-chart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: release-name-server-chart
  labels:
    helm.sh/chart: server-chart-0.1.0
    app.kubernetes.io/name: server-chart
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: server-chart
    app.kubernetes.io/instance: release-name
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: http
---
# Source: server-chart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: release-name-server-chart
  labels:
    helm.sh/chart: server-chart-0.1.0
    app.kubernetes.io/name: server-chart
    app.kubernetes.io/instance: release-name
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: server-chart
      app.kubernetes.io/instance: release-name
  template:
    metadata:
      labels:
        app.kubernetes.io/name: server-chart
        app.kubernetes.io/instance: release-name
    spec:
      containers:
        - name: server-chart
          image: "localhost/my-http-server:latest"
          imagePullPolicy: Never
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-5$ helm install server ./server-chart
NAME: server
LAST DEPLOYED: Sat Apr 18 17:01:47 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

To test if it works as expected I set a port forward to the deployed service and repeated the tests from Challenge 3:

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-5$ kubectl port-forward svc/server-server-chart 8080:8080
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
Handling connection for 8080
Handling connection for 8080

stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-3$ curl http://localhost:8080
Wrong header!
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-3$ curl -H "Challenge: orcrist.org" http://localhost:8080
Everything works!
```
It has to be noted that this time the server has no issues with not explicitly setting IPv4 as minikube internally uses it, in contrast
to the Podman setup I used in challenge 3.
