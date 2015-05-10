# snippet crawler dev notes

## mongodb

download: http://www.mongodb.org/downloads

### install manually
```bash
# download on azure
screen -S down
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1410-clang-3.0.2.tgz

# upload to dev vm
scp root@aint:~/tmp/mongodb-linux-x86_64-ubuntu1410-clang-3.0.2.tgz .
scp mongodb-linux-x86_64-ubuntu1410-clang-3.0.2.tgz root@ls:~/

# install
tar -zxvf mongodb-linux-x86_64-ubuntu1410-clang-3.0.2.tgz
mkdir -p /opt/mongodb
cp -R -n mongodb-linux-x86_64-ubuntu1410-clang-3.0.2/* /opt/mongodb
echo 'export PATH=/opt/mongodb/bin:$PATH' >> ~/.bashrc
apt-get install libc++-dev
```

### run manually
```bash
screen -S mdb
mkdir -p /data/mongodb
mongod --dbpath /data/mongodb
```

### enable authentication
login via `mongo` to create the administrator and close localhost exception:
```javascript
use admin
db.createUser(
  {
    user: "root",
    pwd: "YOUR_PASSWORD",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)
```

restart the `mongod` with auth required:
```bash
mongod --dbpath /data/mongodb --bind_ip=0.0.0.0 --auth
```

login as `root` with auth:
```bash
mongo --port 27017 -u root -p YOUR_PASSWORD --authenticationDatabase admin
```

### create user

create after logged in as admin
```javascript
use snippetcrawl
db.createUser(
  {
    user: "YOUR_USERNAME",
    pwd: "YOUR_PASSWORD",
    roles: [ { role: "dbOwner", db: "snippetcrawl" } ]
  }
)
```

login as `YOUR_USERNAME` with auth:
```bash
mongo --port 27017 -u YOUR_USERNAME -p YOUR_PASSWORD --authenticationDatabase snippetcrawl
```


## python

### setup devenv for python3

```bash
sudo apt-get install python3-pip python3-dev python3-setuptools
```

### install via pip
```bash
sudo pip3 install pymongo
sudo pip3 install requests
sudo pip3 install beautifulsoup4
sudo pip3 install flask
```

### install by requirements.txt 
```bash
pip3 install -r requirements.txt
```

### fix `ImportError: cannot import name 'IncompleteRead'` 
```bash
sudo easy_install3 -U pip
```

### upload to devbox
```bash
scp -r *.* root@stcaraa:~/snipcrawl/

rsync -aP *.py root@ls:~/snipcrawl/
```


## dba

### read

```javascript
use snippetcrawl;

db.queue_crawl.find().count();
db.queue_crawl.find({ "status": "new" }).count();
db.queue_crawl.find().sort( { "date": 1 } ).pretty();

db.queue_page.find().count();
db.queue_page.find().sort( { "date": 1 } ).pretty();
db.queue_page.find({}, { "text": 0 }).sort( { "date": 1 } ).pretty();
db.queue_page.find({}, { "text": 0, "data": 0 }).sort( { "date": 1 } ).pretty();

db.snippet.find().count();
db.snippet.find().sort( { "date": -1 } ).pretty();
db.snippet.find({}, { "archive": 0 }).sort( { "date": -1 } ).pretty();
```


### create

```javascript
use snippetcrawl;

```


## dev

### assign debug

```python
from DatabaseAccessor import DatabaseAccessor
dal = DatabaseAccessor()
job = dal.queue_page_renew("http://neihanshequ.com/joke/?is_json=1&max_time=1431168324")
job = dal.queue_page_take_raw()
from json import loads
text = job.get('text', "")
page_content = loads(text)
page_content["data"]["min_time"]
page_content["data"]["max_time"]
page_content["data"]["data"][0]["group"]["content"]
```

post-
url: 1431168324
min: 1431168024
max: 1431156324

api-
url: 1431168324
min: 1431168324
max: 1431156624

http://neihanshequ.com/p3659746976


## deploy

upload to pi03:
```cmd
cd D:\UserWei\Desktop\
scp snipcrawl1.zip root@szgeek-pi03:~/
```

dist to linux vm:
```bash
scp snipcrawl1.zip root@stcaraa:/tmp/
scp snipcrawl1.zip root@stcaloc:/tmp/
scp snipcrawl1.zip root@szgeek:/tmp/
```

up and run:
```bash
cd /tmp/

unzip snipcrawl1.zip
mv snipcrawl1 ~/scrawl
unzip snipcrawl1.zip
mv snipcrawl1 ~/sassign
unzip snipcrawl1.zip
mv snipcrawl1 ~/sparse
```

limit:
```
start: http://neihanshequ.com/joke/?is_json=1&max_time=1431168324 - 2015/5/9 下午6:45:24
pause: http://neihanshequ.com/joke/?is_json=1&max_time=1428054324 - 2015/4/3 下午5:45:24
new:   http://neihanshequ.com/joke/?is_json=1&max_time=1431266365 - 2015/5/10 下午9:54:25
paus2: http://neihanshequ.com/joke/?is_json=1&max_time=1428051565 - 2015/4/3 下午4:59:25

```

