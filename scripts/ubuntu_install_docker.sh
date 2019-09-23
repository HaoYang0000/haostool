# 卸载旧版本docker
sudo apt-get remove docker docker-engine docker.io

# 更新系统软件
sudo apt-get update

# 安装依赖包
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# 添加官方密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# 添加仓库
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# 再次更新软件
sudo apt-get update

# 安装docker
sudo apt-get install docker-ce

# 查看docker版本
docker -v

# 下载docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

# 授权
sudo chmod +x /usr/local/bin/docker-compose

# 查看版本信息
docker-compose --version


# ref https://www.cnblogs.com/sweetsunnyflower/p/9862943.html