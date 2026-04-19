# Challenge 4: What's wrong?

To see what a binary does we can use strace to see which syscalls it does.
In this case it looks like this:

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-4$ strace ./blackbox 
execve("./blackbox", ["./blackbox"], 0x7fffd8b35790 /* 67 vars */) = 0
brk(NULL)                               = 0x55cab505a000
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f3a42d58000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (Datei oder Verzeichnis nicht gefunden)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=125219, ...}) = 0
mmap(NULL, 125219, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f3a42d39000
close(3)                                = 0
openat(AT_FDCWD, "/lib64/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0p7\0\0\0\0\0\0"..., 832) = 832
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
fstat(3, {st_mode=S_IFREG|0755, st_size=2455432, ...}) = 0
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
mmap(NULL, 2042928, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f3a42b46000
mmap(0x7f3a42cb5000, 483328, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x16f000) = 0x7f3a42cb5000
mmap(0x7f3a42d2b000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1e4000) = 0x7f3a42d2b000
mmap(0x7f3a42d31000, 31792, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f3a42d31000
close(3)                                = 0
mmap(NULL, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f3a42b43000
arch_prctl(ARCH_SET_FS, 0x7f3a42b43740) = 0
set_tid_address(0x7f3a42b43a10)         = 230228
set_robust_list(0x7f3a42b43a20, 24)     = 0
rseq(0x7f3a42b43680, 0x20, 0, 0x53053053) = 0
mprotect(0x7f3a42d2b000, 16384, PROT_READ) = 0
mprotect(0x55cab4667000, 4096, PROT_READ) = 0
mprotect(0x7f3a42d98000, 8192, PROT_READ) = 0
prlimit64(0, RLIMIT_STACK, NULL, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0
getrandom("\x87\x3d\x96\x85\xd7\xa8\x9a\x4f", 8, GRND_NONBLOCK) = 8
munmap(0x7f3a42d39000, 125219)          = 0
access("the_magic_filez.txt", F_OK)     = -1 ENOENT (Datei oder Verzeichnis nicht gefunden)
fstat(1, {st_mode=S_IFCHR|0600, st_rdev=makedev(0x88, 0x1), ...}) = 0
brk(NULL)                               = 0x55cab505a000
brk(0x55cab507b000)                     = 0x55cab507b000
write(1, "Ooooh, what's wrong? :(", 23Ooooh, what's wrong? :() = 23
exit_group(-1)                          = ?
+++ exited with 255 +++
```

As we can see in this output the binary tried to access a file `the_magic_filez.txt`

So I tried if just creating that file was enough and as it turns out it is:

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-4$ touch the_magic_filez.txt
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-4$ ./blackbox 
Congrats! :)
```


