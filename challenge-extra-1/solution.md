# Kubernetes Extra Challenge

As this task is a simple "just execute commands" below the output of the commands:

## Apply manifests

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-1$ kubectl apply -f manifests/
namespace/collector created
namespace/integration created
namespace/orcrist created
namespace/monitoring created
namespace/tools created
deployment.apps/nginx-deployment created
service/nginx-service created
pod/pod-example-orcrist created
pod/pod-nginx-tools created
pod/pod-example-integration created
pod/pod-example-monitoring created
```

## Get Namespaces

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-1$ kubectl get namespaces
NAME              STATUS   AGE
collector         Active   60s
default           Active   35m
integration       Active   60s
kube-node-lease   Active   35m
kube-public       Active   35m
kube-system       Active   35m
monitoring        Active   60s
orcrist           Active   60s
tools             Active   60s
```

## Get all resources

This is the simple way to do it. It is limited to the resources covered by "get all", which are all
that create pods. For services etc this doesn't work.

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-1$ kubectl get all --all-namespaces
NAMESPACE     NAME                                    READY   STATUS    RESTARTS   AGE
integration   pod/pod-example-integration             1/1     Running   0          2m50s
kube-system   pod/coredns-7d764666f9-mbj9c            1/1     Running   0          37m
kube-system   pod/etcd-minikube                       1/1     Running   0          37m
kube-system   pod/kube-apiserver-minikube             1/1     Running   0          37m
kube-system   pod/kube-controller-manager-minikube    1/1     Running   0          37m
kube-system   pod/kube-proxy-rzn28                    1/1     Running   0          37m
kube-system   pod/kube-scheduler-minikube             1/1     Running   0          37m
kube-system   pod/storage-provisioner                 1/1     Running   0          37m
monitoring    pod/pod-example-monitoring              1/1     Running   0          2m50s
orcrist       pod/nginx-deployment-59f86b59ff-465xw   1/1     Running   0          2m50s
orcrist       pod/nginx-deployment-59f86b59ff-fx4vq   1/1     Running   0          2m50s
orcrist       pod/nginx-deployment-59f86b59ff-xmsgx   1/1     Running   0          2m50s
orcrist       pod/pod-example-orcrist                 1/1     Running   0          2m50s
tools         pod/pod-nginx-tools                     1/1     Running   0          2m50s

NAMESPACE     NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE
default       service/kubernetes      ClusterIP   10.96.0.1       <none>        443/TCP                  37m
kube-system   service/kube-dns        ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   37m
orcrist       service/nginx-service   ClusterIP   10.110.29.232   <none>        80/TCP                   2m50s

NAMESPACE     NAME                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kube-system   daemonset.apps/kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   37m

NAMESPACE     NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
kube-system   deployment.apps/coredns            1/1     1            1           37m
orcrist       deployment.apps/nginx-deployment   3/3     3            3           2m50s

NAMESPACE     NAME                                          DESIRED   CURRENT   READY   AGE
kube-system   replicaset.apps/coredns-7d764666f9            1         1         1       37m
orcrist       replicaset.apps/nginx-deployment-59f86b59ff   3         3         3       2m50s
```

This is the more complicated way to get all existing resources (output shortened as it is huge - 576 lines on my system):

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-1$ kubectl get $(kubectl api-resources --verbs=list -o name | paste -sd,) --all-namespaces --ignore-not-found
Warning: v1 ComponentStatus is deprecated in v1.19+
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME                                 STATUS    MESSAGE   ERROR
componentstatus/controller-manager   Healthy   ok        
componentstatus/scheduler            Healthy   ok        
componentstatus/etcd-0               Healthy   ok        

NAMESPACE         NAME                                                             DATA   AGE
collector         configmap/kube-root-ca.crt                                       1      8m7s
default           configmap/kube-root-ca.crt                                       1      42m
integration       configmap/kube-root-ca.crt                                       1      8m7s
kube-node-lease   configmap/kube-root-ca.crt                                       1      42m
kube-public       configmap/cluster-info                                           2      42m
kube-public       configmap/kube-root-ca.crt                                       1      42m
kube-system       configmap/coredns                                                1      42m
kube-system       configmap/extension-apiserver-authentication                     6      42m
kube-system       configmap/kube-apiserver-legacy-service-account-token-tracking   1      42m
kube-system       configmap/kube-proxy                                             2      42m
kube-system       configmap/kube-root-ca.crt                                       1      42m
kube-system       configmap/kubeadm-config                                         1      42m
kube-system       configmap/kubelet-config                                         1      42m
monitoring        configmap/kube-root-ca.crt                                       1      8m7s
orcrist           configmap/kube-root-ca.crt                                       1      8m7s
tools             configmap/kube-root-ca.crt                                       1      8m7s

NAMESPACE     NAME                                 ENDPOINTS                                     AGE
default       endpoints/kubernetes                 10.0.2.15:8443                                42m
[...]
```

## Services in Namespace

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-1$ kubectl get svc -n orcrist
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
nginx-service   ClusterIP   10.110.29.232   <none>        80/TCP    9m57s
```

## Deployments in Namespace

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-1$ kubectl get deployments -n tools
No resources found in tools namespace.
```

## Get Image from Deployment

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-1$ kubectl get deployment nginx-deployment -n orcrist -o jsonpath='{.spec.template.spec.containers[*].image}'
nginx:latest
```

## Port Forward

First identify which port is exposed by the service, then forward that to 8080 on my computer and test it:

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-1$ kubectl get svc -n orcrist
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
nginx-service   ClusterIP   10.110.29.232   <none>        80/TCP    13m
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-1$ kubectl port-forward svc/nginx-service 80:8080 -n orcrist
error: Service nginx-service does not have a service port 8080
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-1$ kubectl port-forward svc/nginx-service 8080:80 -n orcrist
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
Handling connection for 8080

stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-3$ curl http://localhost:8080
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, nginx is successfully installed and working.
Further configuration is required for the web server, reverse proxy, 
API gateway, load balancer, content cache, or other features.</p>

<p>For online documentation and support please refer to
<a href="https://nginx.org/">nginx.org</a>.<br/>
To engage with the community please visit
<a href="https://community.nginx.org/">community.nginx.org</a>.<br/>
For enterprise grade support, professional services, additional 
security features and capabilities please refer to
<a href="https://f5.com/nginx">f5.com/nginx</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

As expected nginx can be reached and delivers a welcome page.

