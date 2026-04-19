# Challenge 5: Helm Chart

## Objective

Create a Helm chart to deploy the Python HTTP server from Challenge 3 to Kubernetes.

## Background

The Challenge 3 server is a Python HTTP application that:
- Listens on **port 8080**
- Returns `200 OK` with "Everything works!" when the request includes header `Challenge: orcrist.org`
- Returns `404 Not Found` with "Wrong header!" otherwise

Assume the Docker image has been built from your Challenge 3 Dockerfile.

## Requirements

Complete the Helm chart in `server-chart/` with the following:

### 1. values.yaml
Define configurable values for:
- Container image (repository, tag, pull policy)
- Number of replicas
- Service configuration (type, port)
- Resource limits/requests (optional)

### 2. templates/deployment.yaml
Create a Kubernetes Deployment that:
- Deploys the container image
- Exposes container port 8080
- Uses values from values.yaml

### 3. templates/service.yaml
Create a Kubernetes Service that:
- Exposes the deployment
- Routes traffic to port 8080

### 4. (Optional) templates/_helpers.tpl
Add template helpers for consistent naming and labels.

## Deliverables

A working Helm chart that can be:
1. Validated with: `helm lint ./server-chart`
2. Rendered with: `helm template ./server-chart`
3. Installed with: `helm install server ./server-chart`

## Acceptance Criteria

- [ ] `helm lint` passes without errors
- [ ] `helm template` renders valid Kubernetes manifests
- [ ] Deployment targets container port 8080
- [ ] Service correctly routes to the deployment
- [ ] All hardcoded values are parameterized in values.yaml

---

# Solution

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
