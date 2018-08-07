# launchpad-query
This is a small script to query Launchpad for Contrail bugs and print out related info into csv format. One of its uses is to collect some statistics for bugs contains certain tags.

# Installation
1. Get the script  
```wget https://raw.githubusercontent.com/vcheny/launchpad-query/master/lpq.py```  
or  
```git clone git@github.com:vcheny/launchpad-query.git```  
2. Install launchpadlib if missing  
```sudo apt-get install python-launchpadlib```  
or  
```pip install launchpadlib```  

# Usage
```
[cheny-mbp:~/Work/github/launchpad-query]$ ./lpq.py -h
usage: lpq [-h] [-a AFTER] [-b BEFORE] [--open_only] [--closed_only] tag

Script to query Contrail related bugs in launchpad

positional arguments:
  tag                   List launchpad matching given tags

optional arguments:
  -h, --help            show this help message and exit
  -a AFTER, --after AFTER
                        List launchpad created since given time e.g.
                        2018-03-19
  -b BEFORE, --before BEFORE
                        List launchpad created before given time e.g.
                        2018-03-19
  --open_only           Only list LPs in open state
  --closed_only         Only list LPs not in open state
```

The script requires an authorization to access Launchpad on your behalf when it is first run.

```lab@ubuntu1604:~$ ./lpq.py jtac
The authorization page:
 (https://launchpad.net/+authorize-token?oauth_token=fm3Wg1lhT1RSRd26pkcp&allow_permission=DESKTOP_INTEGRATION)
should be opening in your browser. Use your browser to authorize
this program to access Launchpad on your behalf.
Waiting to hear from Launchpad about your decision...

Error: Your passwords didn't match
Please set a password for your new keyring: 
Please confirm the password: 
```

If browser doesn't pop up automatically, copy the url into browser. You would need to authorize the access after login.
Once authorization is done, set a local password lock it.


