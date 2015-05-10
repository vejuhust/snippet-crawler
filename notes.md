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
