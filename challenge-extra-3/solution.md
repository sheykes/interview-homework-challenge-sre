# Helm Unittest

To solve this challenge I used helm-unittest. The reason for choosing this is that I
have experience with it and after a quick look at the documentation of chart-testing
like the approach of having a helm plugin instead of a fully independent binary more.

I created the test files so that they make very general basic checks (are things rendered
when they should be?) and then checked every value substitution in the templates.

The result looks like this:

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-3$ helm unittest ./server-chart/

### Chart [ server-chart ] ./server-chart/

 PASS  Deployment	server-chart/tests/deployment_test.yaml
 PASS  Service	server-chart/tests/service_test.yaml

Charts:      1 passed, 1 total
Test Suites: 2 passed, 2 total
Tests:       26 passed, 26 total
Snapshot:    0 passed, 0 total
Time:        11.656026ms
```
