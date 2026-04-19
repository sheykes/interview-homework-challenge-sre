# Create and Run a Docker Image

I created a minimal Dockerfile based on the task.

If this would be uploaded/used inside an organisation there likely would
be the need for custom labels etc that could be added to the Dockerfile.

To build and run I used these commands:

```
docker build -t my-http-server .
docker run -p 8080:8080 my-http-server
```

Verifying this resulted in:

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-3$ curl -4 http://localhost:8080
Wrong header!

stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-3$ curl -4 -H "Challenge: orcrist.org" http://localhost:8080
Everything works!
```

As you can see I had to force curl to use IPv4. As it turns out my system by default uses IPv6 even for localhost, while the used
socketserver inside server.py has set `address_family = socket.AF_INET` <https://github.com/python/cpython/blob/3.14/Lib/socketserver.py>

So when I didn't enforce IPv4 the result was this:

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-3$ curl http://localhost:8080
curl: (56) Recv failure: Die Verbindung wurde vom Kommunikationspartner zurückgesetzt
```
