# Myscript.py - System Information Script

The requested script is implemented mostly as a wrapper around psutil, which provides
the necessary data. It is able to deal with (=ignore) some potential errors I could
think of, usually missing access rights.

As the script itself is the solution, I add here below the results it produced on my system to
prove that it works as intented.

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-2$ ./myscript.py -x
usage: myscript.py [-d] [-c] [-p] [-r] [-o] [-h]
myscript.py: error: unrecognized arguments: -x


stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-2$ ./myscript.py -h
Usage: myscript.py [options..]
Myscript - a simple system information script

Myscript options:
  -d, --disk       check disk stats
  -c, --cpu        check cpu stats
  -p, --ports      check listen ports
  -r, --ram        check ram stats
  -o, --overview   top 10 process with most CPU usage.
  -h, --help       show this help message.


stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-2$ ./myscript.py -d
=== Disk Stats ===
  Volume     : /dev/nvme1n1p3 (/)
  Filesystem : btrfs
  Total      : 464.2 GB
  Used       : 159.0 GB
  Free       : 302.7 GB
  Used %     : 34.4%

  Volume     : /dev/nvme1n1p2 (/boot)
  Filesystem : ext4
  Total      : 973.4 MB
  Used       : 481.1 MB
  Free       : 425.1 MB
  Used %     : 53.1%

  Volume     : /dev/nvme1n1p3 (/home)
  Filesystem : btrfs
  Total      : 464.2 GB
  Used       : 159.0 GB
  Free       : 302.7 GB
  Used %     : 34.4%

  Volume     : /dev/nvme1n1p1 (/boot/efi)
  Filesystem : vfat
  Total      : 598.8 MB
  Used       : 19.3 MB
  Free       : 579.5 MB
  Used %     : 3.2%

  Volume     : /dev/nvme0n1 (/mnt/113a321b-04c1-4ccf-aed8-3fd3cf3c2c80)
  Filesystem : ext4
  Total      : 3.7 TB
  Used       : 504.3 GB
  Free       : 3.0 TB
  Used %     : 14.2%


stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-2$ ./myscript.py --cpu
=== CPU Stats ===
  Cores (physical) : 8
  Cores (logical)  : 16
  Usage            : 0.4%
  Frequency (cur)  : 3506 MHz
  Frequency (min)  : 2983 MHz
  Frequency (max)  : 5053 MHz


stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-2$ ./myscript.py -p
=== Listening Ports ===
  Proto   Address               Port     PID       Process
  ---------------------------------------------------------------------
  TCP     127.0.0.54            53       -         -
  TCP     127.0.0.53            53       -         -
  TCP     ::1                   631      -         -
  TCP     127.0.0.1             631      -         -
  TCP     0.0.0.0               5355     -         -
  TCP     ::                    5355     -         -
  TCP     127.0.0.1             11434    -         -
  TCP     0.0.0.0               27036    20316     steam
  TCP     127.0.0.1             27060    20316     steam
  TCP     0.0.0.0               27500    -         -
  TCP     127.0.0.1             33007    20316     steam
  TCP     127.0.0.1             46611    20316     steam
  TCP     127.0.0.1             57343    20316     steam


stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-2$ ./myscript.py -r
=== RAM Stats ===
  Total  : 30.5 GB
  Used   : 9.5 GB
  Free   : 21.0 GB
  Used % : 31.1%


stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-2$ ./myscript.py -o
=== Top 10 Processes by CPU Usage ===
  PID      Name                       CPU %     MEM %     Status
  --------------------------------------------------------------------
  204116   python3                    1.9       0.1       running
  20316    steam                      1.0       1.3       sleeping
  69649    kworker/0:5-events         1.0       0.0       idle
  173101   kworker/u64:8-events_unbo  1.0       0.0       idle
  1        systemd                    0.0       0.1       sleeping
  2        kthreadd                   0.0       0.0       sleeping
  3        pool_workqueue_release     0.0       0.0       sleeping
  4        kworker/R-rcu_gp           0.0       0.0       idle
  5        kworker/R-sync_wq          0.0       0.0       idle
  6        kworker/R-kvfree_rcu_recl  0.0       0.0       idle
```
