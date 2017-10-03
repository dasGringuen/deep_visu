# deep_visu
Deep learning and machine learning visualization and experiments framework.

Help to keep track of experiments by saving the results and the configuration on single html file.

## Features:
    -   Visualization for real time signals
    -   Python3
    -   Bokeh


## Requirements

* python3
* bokeh


## Setup and customize
1. Create a generic initialization file. This will create a configuration file called _el.conf_ in the current directory. This file will determine the ip address of the host and some other options.

```sh
    ~$ elinit
```
    
2. Customize the el.conf file created in the previous step
```sh
    user="ad"               # remote login user name
    ip="localhost"          # remote host address or domain name
    file_manager="nautilus" # File manager can specify Nautilus, Dolphin or any other
```

3.  To avoid writing the remote password everytime (Optional)
    The public key will be copied to the remote host
    
    ~$ elsetup_remote_host
    
## Use
### Ping the remote host

    ~$ elping

### Connect using ssh

    ~$ elconn
    
### To browse remote file system 
It will run the file manager configured in step 2

    ~$ elfs
    
### Todos

 - Improve performance
 - Remove the use of Bokeh client

### License

-   GPL v3

**Free Software**

