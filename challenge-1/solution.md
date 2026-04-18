# Challenge 1

## Log Format

The log file utilizes a space-separated format which I interpret as this based on the values actually in the logfile:

```
Timestamp Username <Unknown> Protocol ResponseCode "Method Path"
```

If there are no values the logger replaces them with "-" which is the case for the third field for all log entries.

While there are easily understandable entries already on the first page of log lines I verified that this value is never
set by using:

```
awk '{if ($3 != "-") {print}}' sample.log
```

That returned not a single line. Usually however this third field could be an (forwarded for) IP address or something like that.

As I understand this task as a basic ad-hoc task and not with the intention to write scripts that will be used again and again
I will use the fastest CLI approach for this task (simple one liners and pipes instead of sophisticated patterns).

## HTTP Code 500

Count all lines with 500 HTTP code.

The above used awk command which matches fields to patterns and returns the whole line is used as the baseline for all following
questions. To find all requests which returned HTTP Code 500 I used these commands to return and to count them:

```
awk '{if ($5 == "500") {print}}' sample.log
awk '{if ($5 == "500") {print}}' sample.log | wc -l
```

This amounts to 714 lines requests.

## Specific requests

Count all GET requests from yoko to /rrhh location and if it was successful (200).

Following the same approach I use this commands to see and count the requests:

```
awk '{if ($2 == "yoko" && $7 == "/rrhh\"" && $5 == "200") {print}}' sample.log
awk '{if ($2 == "yoko" && $7 == "/rrhh\"" && $5 == "200") {print}}' sample.log | wc -l
```

This returns 11 requests

## Requests to /

How many requests go to /?

Following the same approach I use this commands to see and count the requests:

```
awk '{if ($7 == "/\"") {print}}' sample.log
awk '{if ($7 == "/\"") {print}}' sample.log | wc -l
```

The result is 717 requests.

## Counting status codes

Count all lines without 5XX HTTP code.

To do this task I used a regex pattern instead of a direct match:

```
awk '{if ($5 !~ /^5[0-9][0-9]$/) {print}}' sample.log | wc -l
```

This results in 2191 requests.

For a deeper look into the counts I checked at first which different status codes exist in the log file
and then counted each of them:

```
HTTP_CODES=$(awk '{print $5}' sample.log | sort | uniq)
for i in $HTTP_CODES;do echo -n "$i: ";awk '{if ($5 == "'$i'") {print}}' sample.log | wc -l;done
```

This results in the following list:

```
200: 724
201: 740
404: 727
500: 714
503: 755
```

## Replacing status codes

Replace all 503 HTTP codes by 500, how many requests have a 500 HTTP code?

To replace this specific field value I again use awk for the replacement and just combine with the first used command:

```
awk '{if ($5 == "503") {$5=500; print} else {print}}' sample.log | awk '{if ($5 == "500") {print}}' | wc -l
```

The first awk command modifies the line if the status code is 503, if not it keeps the line as is.
After that I just add the match/count combination from the first task.

The result is 1469. I kept the modified logfile in-memory, but this could easily be written to a new file:

```
awk '{if ($5 == "503") {$5=500; print} else {print}}' sample.log > sample-modified.log
```
