# GitHubNavigator

###### Installation Instructons: In order to run the uWSGI GitHub Navigator, you need to install the following on Ubuntu or other Linux system.

### System Requirements:
	1: Pip (python-pip)
	2: CherryPy Framework (WSGI complaint)
	3: Requests (python-requests)


#### 1: Pip Installation: 

###### To install Pip, you need to execute the following commands on your ubuntu terminal with sudo permissions. 

```
sudoUser@sudoUser:~$ sudo apt-get update && sudo apt-get -y upgrade
sudoUser@sudoUser:~$ sudo apt-get install python-pip
sudoUser@sudoUser:~$ pip -V
```

#### 2: CherryPy Framework: 

###### Once you have installed Pip in the first command, it is easy to install CherryPy framework. you can also check the [link](https://docs.cherrypy.org/en/latest/install.html) if you want. In the first command CherryPy Framework is installed using Pip. In the second command one need to verfy the successful installation of CherryPy Framework. If CherryPy frame is not installed successfully then application.py will NOT run.
```
sudoUser@sudoUser:~$ pip install cherrypy
sudoUser@sudoUser:~$ python -m cherrypy.tutorial.tut01_helloworld
```
```
[15/Feb/2014:21:51:22] ENGINE Listening for SIGHUP.
[15/Feb/2014:21:51:22] ENGINE Listening for SIGTERM.
[15/Feb/2014:21:51:22] ENGINE Listening for SIGUSR1.
[15/Feb/2014:21:51:22] ENGINE Bus STARTING
[15/Feb/2014:21:51:22] ENGINE Started monitor thread 'Autoreloader'.
[15/Feb/2014:21:51:22] ENGINE Serving on http://127.0.0.1:8080
[15/Feb/2014:21:51:23] ENGINE Bus STARTED
```

#### 3: Requests

###### The default installation of Python don't have the library for making Http requests, therefore it need to be installed additionally using Pip.
```
sudoUser@sudoUser:~$ pip install requests
```

