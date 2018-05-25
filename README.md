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
D:\Home Directories\Home\Documents\Repositories\python3-asyncio-example [master ≡ +1 ~2 -0 !]> python .\async.py --help
usage: async.py [-h]
                [--cluster {poc01,devops1,se3,isilon,sql,toVCenter,fromVCenter}]

optional arguments:
  -h, --help            show this help message and exit
  --cluster {poc01,devops1,se3,isilon,sql,toVCenter,fromVCenter}
                        Choose a cluster in .creds
```

### Running it
```
D:\Home Directories\Home\Documents\Repositories\python3-asyncio-example [master ≡ +1 ~2 -0 !]> python .\async.py --cluster devops1
Running initial query for IDs
Running 43 sub requests syncronously
Running 43 sub requests asyncronously
Data from : Fri May 25 00:00:00 UTC 2018 - Fri May 25 24:00:00 UTC 2018
Event series reported : 43
Sync : 26.0512638092041
Async : 5.69584321975708
Number of calls : 44
```
Note the difference!
