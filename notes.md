# joke crawler dev notes

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

