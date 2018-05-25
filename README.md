# python3-asyncio-example

## Simple demonstration of asyncio (Thanks Drew!)

### Setup .creds
```
{
	"cluster1": {
        	"servers":["IP","IP","IP","IP"],
        	"username": "user",
        	"password": "pw"
	}
}
```

### Help TXT
```
D:\Home Directories\Home\Documents\Repositories\python3-asyncio-example [master ≡ +0 ~1 -0 !]> python .\async.py -h
usage: async.py [-h] -c {poc01,devops1,se3,isilon,sql,toVCenter,fromVCenter}

optional arguments:
  -h, --help            show this help message and exit
  -c {poc01,devops1,se3,isilon,sql,toVCenter,fromVCenter}, --cluster {poc01,devops1,se3,isilon,sql,toVCenter,fromVCenter}
                        Choose a cluster in .creds
```

### Running it
```
D:\Home Directories\Home\Documents\Repositories\python3-asyncio-example [master ≡ +0 ~1 -0 !]> python .\async.py -c devops1
Running initial query for IDs
Running 43 sub requests syncronously
Running 43 sub requests asyncronously
Data from : Fri May 25 00:00:00 UTC 2018 - Fri May 25 24:00:00 UTC 2018
Event series reported : 43
Sync : 24.770633935928345
Async : 5.1178858280181885
```
Note the difference!
