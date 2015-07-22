# A Simple Web Server
This is a sample code for buiding a simple web server. The tutorial is from [Ruslan's blog][1].


### The basic mode of how web server works

1. Run `webserver1.py`. The web server creates a socket to accept connections.
2. Run `client1.py`. The client sends http request to the server.(You can also just visit [http://localhost:8888/hello][2]in the browser.)
3. The client will receive http response content.

### WSGI(Python Web Server Gateway Interface)
There are various web frameworks in Python, such as Django, Flask and Pyramid etc. How could we run web server with multiple web frameworks without changing any modifying server's code? The answer is WSGI.

1. Run `wsgiserver.py`. This is a simple WSGI server impletation.
2. You can use any Python web framework to write the application and run with it.
3. There is a test for Django in `helloworld`. It's just a simple Django test project.
4. Run `djangoapp.py`. It will run Django application with your Web server. 
```python
python webserver2.py djangoapp:app
```
Try to visit [http://localhost:8888/hello][3].

You can also try other frameworks, it will also work well.

### Concurrent Server
1. Run `iterativeserver.py`. This is a basic web server to handle one request at a time.
2. Run `sleepserver.py`. This server handles one request and then blocks for 60 secondes.
3. Now run `concurrentserver.py`. This is a concurrent server by using `fork()` system call. The parent process accepts a connection and child process handles it.
4. You should not forget close duplicate file descriptors in parent and child process. Because parent and child share the same file descriptors after the call to fork. You can examine what will happen if we do not close duplicate descriptors in `concurrentserver2.py`.
    - The server no longer sleeps for 60s, but the curl doesn't terminate. It will eventually run out of available file descriptors;Run `client2.py` to test. 
    - Your server creates zombie processes. Even if you try to kill zombies with $ kill -9 , they will survive. (A zombie is a process that has terminated, but its parent has not waited for it and has not received its termination status yet. )

5. You need to modify your server code to wait for zombies to get their termination status.It was modified in `concurrentserver3.py`.
6. But if your child processes send too many SIGCHLD signals, the server process will miss serverl signals, which left several zombies still running background.It was modified in `concurrentserver_final.py`.

Now, we have built a simple web server.

---
##References:
1. [Ruslan's blog][4]
2. [python socket docs][5]
3. [socket programming][6]


  


  [1]: http://ruslanspivak.com/lsbaws-part1/
  [2]: http://localhost:8888/hello
  [3]: http://localhost:8888/hello
  [4]: http://ruslanspivak.com/lsbaws-part1/
  [5]: https://docs.python.org/2/library/socket.html#socket.error
  [6]: https://docs.python.org/2/howto/sockets.html
